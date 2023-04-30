async function fetchIndex() {
  const response = await fetch('https://tmbh-transcribe.github.io/TMBH-Transcribe/index.json');
  const indexJson = await response.json();
  return lunr.Index.load(indexJson);
}

async function search(query) {
  const idx = await fetchIndex();

  const results = idx.search(query);
  const searchResults = results.map(result => {
    const doc = documents.find(document => document.id === parseInt(result.ref));
    return {
      ...doc,
      score: result.score
    };
  });

  return searchResults;
}