async function populateList() {
  const response = await fetch("https://tmbh-transcribe.github.io/TMBH-Transcribe/files.json");
  const json = await response.json();
  const files = json.files;
  files.forEach(makeEpisode);
}

function makeEpisode(fileName) {
  const transcriptsUl = document.getElementById("transcripts")
  const episode = document.createElement("li")
  const link = document.createElement("a")
  link.href = "SmartTranscripts/" + fileName  + ".html"
  link.textContent = fileName
  episode.appendChild(link)
  transcriptsUl.appendChild(episode)
}

async function fetchIndex() {
  const response = await fetch('https://tmbh-transcribe.github.io/TMBH-Transcribe/index.json');
  const indexJson = await response.json();
  return lunr.Index.load(indexJson);
}

async function search(query) {
  const idx = await fetchIndex();
  const results = idx.search(query);
  const ids = results.map(result => result.ref)
  ids.forEach(makeEpisode)
}

populateList().then(() => console.log("list updated")).catch((e)=>console.log("Something went wrong"))
