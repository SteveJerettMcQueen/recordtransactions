import transactions as tr

from jinja2 import Template, Environment, FileSystemLoader

################################################################################

FOLDER = 'bootstrap-pages/'
TEMPLATE = 'template.html'
PATH = FOLDER + TEMPLATE
env = Environment(loader=FileSystemLoader('.'))

template = env.get_template(PATH)
template_vars = {
    'title'         : "Transactions",
    'trans'         : tr.trans.head(7),
    'curr_bal'      : tr.curr_bal,
    'size_trans'    : len(tr.trans),
    'size_credits'  : tr.credits.size,
    'sum_credits'   : tr.credits.sum(),
    'size_debits'   : tr.debits.size,
    'sum_debits'    : tr.debits.sum(),
    'size_cat'      : tr.by_category.size
}

html_out = template.render(template_vars)

# f = open(FOLDER + 'report.html','w')
# f.write(html_out.encode('utf-8'))
# f.close()