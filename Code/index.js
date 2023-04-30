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
  link.href = "SmartTranscripts/" + fileName
  link.textContent = fileName
  episode.appendChild(link)
  transcriptsUl.appendChild(episode)
}


populateList().then(() => console.log("list updated")).catch((e)=>console.log("Something went wrong"))
