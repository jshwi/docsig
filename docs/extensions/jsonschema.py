"""Render JSON Schema documentation tables."""

import json
import typing as t
from copy import deepcopy
from pathlib import Path

from docutils import statemachine
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx

_KV_SIMPLE = (
    "multipleOf",
    "maximum",
    "exclusiveMaximum",
    "minimum",
    "exclusiveMinimum",
    "maxLength",
    "minLength",
    "pattern",
    "default",
    "format",
    "const",
)
_KV_ARRAY = ("maxItems", "minItems", "uniqueItems")
_KV_OBJECT = ("maxProperties", "minProperties")
_COMBINATORS = ("allOf", "anyOf", "oneOf")
_SINGLEOBJECTS = ("not",)
_CONDITIONAL = ("if", "then", "else")


class JsonSchemaDirective(Directive):
    """Render a JSON Schema file as a documentation table."""

    has_content = False
    required_arguments = 1

    def run(self) -> list[t.Any]:
        document_source = Path(self.state.document.current_source or "").parent
        path = (document_source / self.arguments[0]).resolve()
        schema = json.loads(path.read_text(encoding="utf-8"))
        formatter = _SchemaFormatter(self.state, self.lineno)
        return formatter.render(schema)


class _SchemaFormatter:  # pylint: disable=too-few-public-methods
    """Build docutils tables from JSON Schema objects."""

    def __init__(self, state: t.Any, lineno: int) -> None:
        self.state = state
        self.lineno = lineno
        self.nesting = 0

    def render(self, schema: dict[str, t.Any]) -> list[t.Any]:
        """Render the schema into a docutils table.

        :param schema: The JSON Schema object to render.
        :return: A list of docutils table nodes.
        """
        body, _ = self._dispatch(deepcopy(schema))
        if not body:
            return []

        cols, _, body = self._cover(schema, body)
        return [self.state.build_table((cols, [], body), self.lineno)]

    def _cover(
        self,
        schema: dict[str, t.Any],
        body: list[list[t.Any]],
    ) -> tuple[list[int], list[t.Any], list[list[t.Any]]]:
        if "$id" in schema:
            body.insert(0, self._line(self._cell(schema["$id"])))
        elif "id" in schema:
            body.insert(0, self._line(self._cell(schema["id"])))

        nrcols = self._square(body)
        nrcols = self._square([], nrcols)
        self._calc_spans([], nrcols)
        self._calc_spans(body, nrcols)
        return [1] * nrcols, [], body

    def _dispatch(
        self,
        schema: dict[str, t.Any],
        label: list[t.Any] | None = None,
    ) -> tuple[list[list[t.Any]], list[t.Any]]:
        _: list[list[t.Any]] = []
        self.nesting += 1

        if "type" in schema:
            schema_type = schema["type"]
            if schema_type == "object" or (
                isinstance(schema_type, list) and "object" in schema_type
            ):
                rows = self._objecttype(schema)
            elif schema_type == "array" or (
                isinstance(schema_type, list) and "array" in schema_type
            ):
                rows = self._arraytype(schema)
            else:
                rows = self._objecttype(schema)
                self._check_description(schema, rows)
                rows.extend(self._simpletype(schema))
        else:
            rows = self._objecttype(schema)
            self._check_description(schema, rows)
            rows.extend(self._simpletype(schema))

        rows.extend(self._complexstructures(schema))

        if label is not None:
            rows = self._prepend(label, rows)

        self.nesting -= 1
        return rows, []

    def _objecttype(self, schema: dict[str, t.Any]) -> list[list[t.Any]]:
        rows = self._simpletype(schema)
        rows.extend(self._objectproperties(schema, "properties"))
        rows.extend(self._objectproperties(schema, "patternProperties"))
        rows.extend(self._bool_or_object(schema, "additionalProperties"))
        rows.extend(self._dependencies(schema, "dependencies"))
        rows.extend(self._pairs(schema, _KV_OBJECT))
        return rows

    def _arraytype(self, schema: dict[str, t.Any]) -> list[list[t.Any]]:
        rows = self._simpletype(schema)

        if "items" in schema:
            items = schema.pop("items")
            if isinstance(items, list):
                rows.append(self._line(self._cell("items")))
                for item in items:
                    rows.extend(self._dispatch(item, self._cell("-"))[0])
            else:
                rows.extend(self._dispatch(items, self._cell("items"))[0])

        rows.extend(self._bool_or_object(schema, "additionalItems"))
        rows.extend(self._pairs(schema, _KV_ARRAY))
        return rows

    def _simpletype(self, schema: dict[str, t.Any]) -> list[list[t.Any]]:
        rows: list[list[t.Any]] = []

        if "title" in schema:
            rows.append(self._line(self._cell(f"*{schema.pop('title')}*")))

        self._check_description(schema, rows)

        if "type" in schema:
            rows.append(
                self._line(
                    self._cell("type"),
                    self._decodetype(schema.pop("type")),
                ),
            )

        if "enum" in schema:
            enum = schema.pop("enum")
            rows.append(
                self._line(
                    self._cell("enum"),
                    self._cell(", ".join(str(value) for value in enum)),
                ),
            )

        if "examples" in schema:
            rows.extend(
                self._prepend(
                    self._cell("examples"),
                    self._render_value(schema.pop("examples")),
                ),
            )

        rows.extend(self._pairs(schema, _KV_SIMPLE))
        return rows

    def _objectproperties(
        self,
        schema: dict[str, t.Any],
        key: str,
    ) -> list[list[t.Any]]:
        rows: list[list[t.Any]] = []
        if key not in schema:
            return rows

        rows.append(self._line(self._cell(key)))
        properties = schema.pop(key)
        for prop, value in properties.items():
            label = self._cell(f"- {prop}")
            if isinstance(value, dict):
                rows.extend(self._dispatch(value, label)[0])
            else:
                rows.append(self._line(label, self._cell(value)))
        return rows

    def _complexstructures(  # pylint: disable=too-many-branches
        self,
        schema: dict[str, t.Any],
    ) -> list[list[t.Any]]:
        rows: list[list[t.Any]] = []

        for key in _COMBINATORS:
            if key not in schema:
                continue

            items: list[list[t.Any]] = []
            for item in schema.pop(key):
                content = self._dispatch(item)[0]
                if content:
                    items.extend(content)

            if items:
                rows.extend(self._prepend(self._cell(key), items))

        for key in _SINGLEOBJECTS:
            if key not in schema:
                continue

            rows.extend(self._dispatch(schema.pop(key), self._cell(key))[0])

        if _CONDITIONAL[0] in schema:
            items = []
            for key in _CONDITIONAL:
                if key not in schema:
                    continue

                content = self._dispatch(schema.pop(key))[0]
                if content:
                    items.append(self._prepend(self._cell(key), content))

            if len(items) >= 2:
                for item in items:
                    rows.extend(item)

        return rows

    def _dependencies(
        self,
        schema: dict[str, t.Any],
        key: str,
    ) -> list[list[t.Any]]:
        rows: list[list[t.Any]] = []
        if key not in schema:
            return rows

        rows.append(self._line(self._cell(key)))
        dependencies = schema.pop(key)
        for prop, value in dependencies.items():
            label = self._cell(f"- {prop}")
            if isinstance(value, list):
                rows.append(
                    self._line(
                        label,
                        self._cell(", ".join(str(item) for item in value)),
                    ),
                )
            else:
                rows.extend(self._dispatch(value, label)[0])
        return rows

    def _bool_or_object(
        self,
        schema: dict[str, t.Any],
        key: str,
    ) -> list[list[t.Any]]:
        if key not in schema:
            return []

        value = schema.pop(key)
        if isinstance(value, bool):
            return [self._line(self._cell(key), self._cell(value))]

        return self._dispatch(value, self._cell(key))[0]

    def _pairs(
        self,
        schema: dict[str, t.Any],
        keys: tuple[str, ...],
    ) -> list[list[t.Any]]:
        rows: list[list[t.Any]] = []
        for key in keys:
            if key not in schema:
                continue

            value = schema.pop(key)
            if key == "default":
                rows.extend(
                    self._prepend(self._cell(key), self._render_value(value)),
                )
            else:
                rows.append(self._line(self._cell(key), self._cell(value)))
        return rows

    def _prepend(
        self,
        prepend: list[t.Any],
        rows: list[list[t.Any]],
    ) -> list[list[t.Any]]:
        if not rows:
            return [self._line(prepend)]

        prepend[0] = len(rows) - 1
        rows[0].insert(0, prepend)
        for index in range(1, len(rows)):
            rows[index].insert(0, None)
        return rows

    def _decodetype(self, schema_type: t.Any) -> list[t.Any]:
        if isinstance(schema_type, list):
            return self._cell(" / ".join(f"*{item}*" for item in schema_type))
        return self._cell(f"*{schema_type}*")

    def _check_description(
        self,
        schema: dict[str, t.Any],
        rows: list[list[t.Any]],
    ) -> None:
        if "description" in schema:
            rows.append(self._line(self._cell(schema.pop("description"))))

    def _render_value(self, value: t.Any) -> list[list[t.Any]]:
        rows: list[list[t.Any]] = []
        if isinstance(value, list):
            if not value:
                rows.append(self._line(self._cell("")))
            else:
                for item in value:
                    rows.extend(self._render_value(item))
        elif isinstance(value, dict):
            if not value:
                rows.append(self._line(self._cell("")))
            else:
                for key, item in value.items():
                    rows.extend(
                        self._prepend(
                            self._cell(key),
                            self._render_value(item),
                        ),
                    )
        else:
            rows.append(self._line(self._cell(self._format_value(value))))
        return rows

    @staticmethod
    def _format_value(value: t.Any) -> str:
        if value is None:
            return "null"
        return str(value)

    @staticmethod
    def _square(
        rows: list[list[t.Any]],
        nrcols: int = 0,
    ) -> int:
        for row in rows:
            nrcols = max(nrcols, len(row))

        for row in rows:
            if len(row) < nrcols:
                row.extend([None] * (nrcols - len(row)))

        return nrcols

    @staticmethod
    def _calc_spans(rows: list[list[t.Any]], nrcols: int) -> None:
        for row in rows:
            target = []
            for column in range(nrcols):
                if row[column] is not None:
                    target = row[column]
                elif target:
                    target[1] += 1

            for column in range(nrcols):
                if row[column] is not None:
                    row[column] = tuple(row[column])

    @staticmethod
    def _line(*cells: list[t.Any]) -> list[t.Any]:
        return list(cells)

    def _cell(self, text: t.Any) -> list[t.Any]:
        content = self._convert_content(text)
        return [0, 0, self.lineno, content]

    def _convert_content(self, text: t.Any) -> statemachine.StringList:
        lines = statemachine.string2lines(str(text))
        items = [(self.state.document.current_source, self.lineno)] * len(
            lines,
        )
        return statemachine.StringList(lines, items=items)


def setup(app: Sphinx) -> dict[str, t.Any]:
    """Register the jsonschema directive.

    :param app: The Sphinx application object.
    :return: A dictionary of extension metadata.
    """
    app.add_directive("jsonschema", JsonSchemaDirective)
    return {"parallel_read_safe": True, "version": "1.0.0"}
