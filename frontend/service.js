export async function getReplaceText (query) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(['Here is a sentence', 'here is another']);
    }, 200);
  });
  // const q = `q=${encodeURIComponent(query)}`;
  // return await fetch(`http://172.25.0.2:5000/noho?${q}`)
}
