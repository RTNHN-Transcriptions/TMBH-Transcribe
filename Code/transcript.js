
document.addEventListener('DOMContentLoaded', function () {
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
});

function seekToTime(event) {
  const audio = document.getElementById("audio");
  audio.currentTime = +event.target.getAttribute('data-start')+.1;
  audio.play()
}