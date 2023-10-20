from jinja2 import Environment, FileSystemLoader, select_autoescape
import csv

# The environment module is the core of the templating system.
# We use the filesystem loader because we wish to access local files.
# With the following code, jinja looks for all templates in 
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

# Notes on Autoescaping
# In future versions of Jinja we might enable autoescaping by default for security reasons.
# As such you are encouraged to explicitly configure autoescaping now instead of relying on the default.

# Here we print all templates found by the loader
print(env.list_templates())

# The context dictionary contains all context variables available for use in the template.
# Notice the use of {{pages}} as a list (iterable) in the base template
context = dict()
context["pages"] = [
    ("Home", "home"),
    # ("Talks", "talks"),
    ("Links", "links"),
    # ("Projects", "projects"),
    ("About Me", "about")
    ]


# The links table is loaded from a csv file.
# It can be edited with ease from excel or any spreadsheet software
with open("tables/links.csv", "rt", newline = "") as csvfile:
    reader = csv.DictReader(csvfile, dialect = "unix")
    context["links"] = []
    for row in reader:
        context["links"].append(row)
    csvfile.close()


with open("tables/slides.csv", "rt", newline = "") as f:
    reader = csv.DictReader(f, dialect = "unix")
    context["slides"] = []
    for row in reader:
        context["slides"].append(row)
    f.close()


# Opens each template and renders it into the corresponding 
# for (page_name, page) in context["pages"]:
for (page_name, page) in [context["pages"][0]]:
    template = env.get_template(page+".html")
    print("rendering " + page_name)
    f = open(page+".html", "wt")
    f.write(template.render(title = page_name, page_name = page, **context))
    f.close()