import transactions as tr

from jinja2 import Template, Environment, FileSystemLoader

################################################################################

FOLDER = 'startbootstrap-bare-gh-pages/'
TEMPLATE = 'template.html'
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(FOLDER + TEMPLATE)

cols = ['Date','Entry','Form','Category','Description','Amount', 'Balance']

template_vars = {
    'title': "Transactions",
    'trans_table': tr.trans.head(15).to_html(buf=None,columns=cols)
}

f = open(FOLDER + 'report.html','w')
html_out = template.render(template_vars)
f.write(html_out.encode('utf-8'))
f.close()