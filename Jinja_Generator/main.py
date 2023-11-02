from jinja2 import Template

with open('templates\\template.jinja') as f:
    tmpl = Template(f.read())

output = tmpl.render(variable = 'Welt', text_liste = ['Der', 'heilige', 'Gral'])

with open('outputs\\template.py', 'w') as f:
    f.write(output)