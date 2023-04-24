import whisper #pip install openai-whisper
from bs4 import BeautifulSoup as Soup #pip install bs4 lxml
import requests #pip install requests - Not actually sure if you need to install this manually
from os.path import exists
from tqdm import tqdm #pip install tqdm
import json
import torch


RSS_LINK = "https://thetenminutebiblehourpodcast.libsyn.com/rss"
CHECK_LIMIT = 20 
#There are a lot of problematic episodes, so it will only
#Check the latest 20 episodes in case I get behind 

RSS_doc = requests.get(RSS_LINK)
soup = Soup(RSS_doc.content, features="xml")
episodes = soup.find_all("item") #item is the xml tag for a podcast episode

if torch.cuda.is_available():
    model = whisper.load_model("base.en", "cuda")
else:
    model = whisper.load_model("base.en")
#pbar is a reference to the progress bar object so that the description of
#the current task within the look can be updated. 
pbar = tqdm(episodes)
for index, episode in enumerate(pbar):
    if index > 20:
        continue
    try:
        title = episode.title.text
        episode_number = title[:title.find("-")-1]
        pbar.set_description(f"Working on {episode_number}")
        if exists(f"Data/{episode_number}.json"):
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
        # pbar.set_description(f"Working on {episode_number} - Writing Transcript")
        # with open(f"Transcripts/{episode_number}.md", "w+", encoding="utf8") as f:
        #     f.write("---\n")
        #     f.write(f"title: {title_text}\n")
        #     f.write(f"episode_num: {episode_number}\n")
        #     f.write(f"pub_date: {pub_date}\n")
        #     f.write(f"duration: {duration}\n")
        #     f.write(f"subtitle: {subtitle}\n")
        #     f.write(f"url: {url}\n")
        #     f.write("---\n\n")
        #     f.write(result["text"])
        meta_data = {"title":title_text,
                    "episode_num":episode_number,
                    "pub_date":pub_date,
                    "duration": duration,
                    "subtitle": subtitle,
                    "url": url}
        all_data = {"meta_data": meta_data, "transcription_data": result, "rss_data":str(episode)}
        with open(f"Data/{episode_number}.json", "w+", encoding="utf8") as f:
            f.write(json.dumps(all_data))
    except KeyboardInterrupt:
        raise
    except Exception as e:
        title = episode.title.text
        print(f'There was a problem with the episode {title}')
        print(e)
    
