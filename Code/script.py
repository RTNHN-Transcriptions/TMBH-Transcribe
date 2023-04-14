import whisper
from bs4 import BeautifulSoup as Soup
import requests
from os.path import exists
from tqdm import tqdm

RSS_FILE = "rss.txt"

with open(RSS_FILE, "r", encoding="utf8") as f:
    rss = f.read()

soup = Soup(rss, features="xml")

episodes = soup.find_all("item")

model = whisper.load_model("base.en", "cuda")

for episode in (pbar := tqdm(reversed(episodes))):
    try:
        title = episode.title.text
        episode_number = title[:title.find("-")-1]
        pbar.set_description(f"Working on {episode_number}")
        if exists(f"Transcripts/{episode_number}.md"):
            print(f"Already Transcribed {episode_number}")
            continue
        title_text = title[title.find("-")+1:].strip()
        pub_date = episode.pubDate.text
        description = episode.description.text
        url = episode.enclosure["url"]
        # Sometimes there is extra stuff at the end of the URL
        if url[-3:] != "mp3":
            url = url[:url.find(".mp3?")+4]
        duration = episode.find("itunes:duration").text
        subtitle = episode.find("itunes:subtitle").text
        pbar.set_description(f"Working on {episode_number} - Fetching audio")
        audio = requests.get(url)
        pbar.set_description(f"Working on {episode_number} - Writing audio to file")
        with open("tmp.mp3", "wb") as f:
            f.write(audio.content)
        pbar.set_description(f"Working on {episode_number} - Transcribing Audio")
        result = model.transcribe("tmp.mp3", verbose=False)
        pbar.set_description(f"Working on {episode_number} - Writing Transcript")
        with open(f"Transcripts/{episode_number}.md", "w+", encoding="utf8") as f:
            f.write("---\n")
            f.write(f"title: {title_text}\n")
            f.write(f"episode_num: {episode_number}\n")
            f.write(f"pub_date: {pub_date}\n")
            f.write(f"duration: {duration}\n")
            f.write(f"subtitle: {subtitle}\n")
            f.write(f"url: {url}\n")
            f.write("---\n\n")
            f.write(result["text"])
    except:
        title = episode.title.text
        print(f'There was a problem with the episode {title}')
    