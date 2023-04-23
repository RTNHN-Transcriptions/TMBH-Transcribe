from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader('.'))

template = env.get_template('Code/template.html')

json_file = "Data/BIBLE33.json"

with open(json_file, "r") as f:
    data = json.loads(f.read())

audio_file = data["meta_data"]["url"]
title = data["meta_data"]["title"]

transcript_sections = [{"start":segment["start"], "end":segment["end"], "text":segment["text"]} for segment in data["transcription_data"]["segments"] ]

# Render the template with the given data
rendered_html = template.render(audio_file=audio_file, transcript_sections=transcript_sections, title=title)

# Save the rendered HTML to a file
with open('Code/output.html', 'w') as output_file:
    output_file.write(rendered_html)