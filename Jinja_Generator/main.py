from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./templates'))

# Render Page 1 template
template = env.get_template('base_template.jinja')
output = template.render(data={'a': 1, 'b': [2.1, 2.2, 2.3, 2.4, 2.5], 'c': 3})

# Print or do something with the rendered templates
with open('outputs/schema.py', 'w') as out_file:
    out_file.write(output)