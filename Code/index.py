import json
from lunr import lunr
from tqdm import tqdm
import os

def main():
  documents = []
  for filename in tqdm(os.listdir("Data")):
    doc = {}
    with open(f"Data/{filename}", "r") as f:
      data = json.loads(f.read())
    doc["id"] = os.path.splitext(filename)[0]
    doc["episode_num"] = os.path.splitext(filename)[0]
    doc["title"] = data["meta_data"]["title"]
    doc["subtitle"] = data["meta_data"]["subtitle"]
    doc["sequences"] = [segment["text"] for segment in data["transcription_data"]["segments"]]
    documents.append(doc)
  idx = lunr(ref="id", fields=("episode_num", "title", "subtitle", "sequences"), documents=documents )
  return idx
    

if __name__ == "__main__":
  idx = main()
  with open("index.json", "w") as f:
    json.dump(idx.serialize(), f)


