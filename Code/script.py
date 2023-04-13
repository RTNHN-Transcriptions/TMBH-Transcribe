import whisper
from bs4 import BeautifulSoup as Soup
import requests

RSS_FILE = "rss.txt"

with open(RSS_FILE, "r") as f:
    rss = f.read()

soup = Soup(rss, features="xml")

episodes = soup.find_all("item")

model = whisper.load_model("small")

for episode in reversed(episodes):
    title = episode.title.text
    episode_number = title[:title.find("-")-1]
    title_text = title[title.find("-")+1:].strip()
    pub_date = episode.pubDate.text
    description = episode.description.text
    url = episode.enclosure["url"]
    # Sometimes there is extra stuff at the end of the URL
    if url[-3:] != "mp3":
        url = url[:url.find(".mp3?")+4]
    duration = episode.find("itunes:duration").text
    subtitle = episode.find("itunes:subtitle").text
    print("Fetching audio")
    audio = requests.get(url)
    print("Writing audio to file")
    with open("tmp.mp3", "wb") as f:
        f.write(audio.content)
    print("Transcribing Audio")
    result = model.transcribe("tmp.mp3")
    print("Writing Transcript")
    with open(f"Transcripts/{title}.md", "w") as f:
        f.write("---")
        f.write(f"title: {title_text}")
        f.write(f"episode_num: {episode_number}")
        f.write(f"pub_date: {pub_date}")
        f.write(f"duration: {duration}")
        f.write(f"subtitle: {subtitle}")
        f.write("---")
        f.write(result["text"])
    
    
    

        






result = model.transcribe("audio.mp3")
print(result["text"])