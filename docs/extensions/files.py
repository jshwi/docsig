"""Generate static files."""

import shutil

from sphinx.application import Sphinx


def copy_schema(app: Sphinx) -> None:
    """Copy schema to build.

    :param app: The Sphinx application object.
    """
    infile = app.srcdir / "_generated" / "schema.json"
    outfile = app.outdir / "usage" / "configuration" / "schema.json"
    outfile.parent.mkdir(exist_ok=True, parents=True)
    shutil.copyfile(infile, outfile)


def setup(app: Sphinx) -> None:
    """Set up the Sphinx extension.

    :param app: The Sphinx application to register the extension with.
    """
    app.connect("builder-inited", copy_schema)
