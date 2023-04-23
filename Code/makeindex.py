from jinja2 import Environment, FileSystemLoader
import os

# Set up the Jinja environment
env = Environment(loader=FileSystemLoader('./'))

# Get the template file
template = env.get_template('Code/indexTemplate.html')

# Get a list of the HTML files in the folder
html_files = [f for f in os.listdir('SmartTranscripts')]

html_files.sort()

# Render the template with the list of HTML files
rendered_template = template.render(files=html_files)

# Write the rendered template to an output file
with open('index.html', 'w') as output_file:
    output_file.write(rendered_template)

