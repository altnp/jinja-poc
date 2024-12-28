from jinja2 import Template, Environment, StrictUndefined

def recursive_resolve_context(context):
    def resolve(value, context):
        if isinstance(value, str):
            prev_value = None
            while value != prev_value:
                prev_value = value
                value = Environment(
                    variable_start_string='#{',
                    variable_end_string='}',
                    # undefined=StrictUndefined
                ).from_string(value).render(context)
            return value
        elif isinstance(value, dict):
            return {k: resolve(v, context) for k, v in value.items()}
        elif isinstance(value, list):
            return [resolve(v, context) for v in value]
        return value

    return {key: resolve(value, context) for key, value in context.items()}

context = {
    "servername": "https://api.foo.com",
    "apis": ["https://#{projectname | lower()}.#{baseurl}", "https://api2.foo.com", "https://api3.foo.com"],
    "baseurl": "foo.com",
    "projectname": "API1"
}

json_template_string = '''
{
  "servername": "#{ servername }",
  "apis": [ "#{apis | join(", ")}" ],
  "options": {
    "a": "{b}"
  }
}
'''

env = Environment(
    block_start_string='{%',
    block_end_string='%}',
    variable_start_string='#{',
    variable_end_string='}',
    undefined=StrictUndefined
)

template = env.from_string(json_template_string)

json_output = template.render(recursive_resolve_context(context))

print("Rendered JSON:")
print(json_output)

with open('output.json', 'w') as json_file:
    json_file.write(json_output)
