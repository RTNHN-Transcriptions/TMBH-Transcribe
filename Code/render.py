from jinja2 import Environment, FileSystemLoader
import json
import os
from tqdm import tqdm

def main():
    env = Environment(loader=FileSystemLoader('.'))

    template = env.get_template('Code/template.html')

    for filename in tqdm(os.listdir("Data")):
        
        with open(f"Data/{filename}", "r") as f:
            data = json.loads(f.read())

        audio_file = data["meta_data"]["url"]
        title = data["meta_data"]["title"]

        transcript_sections = [{"start":segment["start"], "end":segment["end"], "text":segment["text"]} for segment in data["transcription_data"]["segments"] ]

        # Render the template with the given data
        rendered_html = template.render(audio_file=audio_file, transcript_sections=transcript_sections, title=title)
        filename_no_ext = os.path.splitext(filename)[0]
        # Save the rendered HTML to a file
        with open(f'SmartTranscripts/{filename_no_ext}.html', 'w') as output_file:
            output_file.write(rendered_html)

if __name__ == "__main__":
    main()