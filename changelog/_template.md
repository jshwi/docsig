{% for section in sections.values() %}
{% if not section %}
{{ None['nothing to build'][0] }}
{% else %}
## [{{versiondata.version}}](https://github.com/jshwi/docsig/tree/v{{versiondata.version}}) - {{versiondata.date}}

{% for category, val in definitions.items() if category in section %}
### {{ definitions[category]['name'] }}

{% for text, values in section[category].items() %}
- {{ text }}
{%- if values %}
{% if text %} ({% endif %}
{%- for issue in values %}
{{ issue.split(": ", 1)[0] }}{% if not loop.last %}, {% endif %}
{%- endfor %}
{% if text %}){% endif %}
{% endif %}

{% endfor %}

{% endfor %}
{% endif %}
{% endfor +%}
