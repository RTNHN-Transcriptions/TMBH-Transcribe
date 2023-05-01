async function makeTranscript() {

    const styleElement = document.createElement('style');
    const cssContent = `
    .transcript-section {
        color: #999999;
    }
    .highlight {
        color: rgb(0, 0, 0);
    }
    `;
    styleElement.textContent = cssContent;
    document.head.appendChild(styleElement);

    const targetDiv = document.getElementById("transcript")
    const episodeNum=targetDiv.dataset.episode_num
    const linkBase = "http://tmbh-transcribe.github.io/TMBH-Transcribe/"
    const dataLink = linkBase +"Data/"+ episodeNum + ".json"
    const response = await fetch(dataLink);
    const json = await response.json();
    const segments = json.transcription_data.segments

    tempHolder = document.createDocumentFragment()

    const audioElement = document.createElement('audio');
    audioElement.id = 'audio';
    audioElement.controls = true;

    const sourceElement = document.createElement('source');
    sourceElement.src = json.meta_data.url;
    sourceElement.type = 'audio/mp3';

    audioElement.appendChild(sourceElement);

    tempHolder.appendChild(audioElement)
    
    const segmentElements = segments.map(makeTranscriptionLine)

    segmentElements.forEach((segmentElement => tempHolder.appendChild(segmentElement)))
    
    targetDiv.appendChild(tempHolder)

    function seekToTime(event) {
        const audio = document.getElementById("audio");
        audio.currentTime = +event.target.getAttribute('data-start')+.1;
        audio.play()
        }

    for (var item of document.querySelectorAll("#transcript p")) {
        item.addEventListener("click", seekToTime  , false);
       }
    
    const audio = document.getElementById('audio'); 
    const transcriptSections = document.querySelectorAll('.transcript-section');

    function updateTranscriptHighlight() {
        const currentTime = audio.currentTime; 

        transcriptSections.forEach((section) => {
            const startTime = parseFloat(section.getAttribute('data-start'));
            const endTime = parseFloat(section.getAttribute('data-end'));

            if (currentTime >= startTime && currentTime <= endTime) {
                section.classList.add('highlight');
            } else {
                section.classList.remove('highlight');
            }
        });
    }
    audio.addEventListener('timeupdate', updateTranscriptHighlight); 
    }

    function makeTranscriptionLine(segment) {
        const segmentP = document.createElement("p")
        segmentP.classList.add("transcript-section")
        segmentP.dataset.start = segment.start
        segmentP.dataset.end = segment.end
        segmentP.textContent = segment.text
        return segmentP
    }

makeTranscript().then(() => console.log("list updated")).catch((e)=>console.log(e))
