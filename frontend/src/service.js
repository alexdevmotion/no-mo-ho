export async function getReplaceText (query) {
  const q = `q=${encodeURIComponent(query)}`;
  try {
    return await fetch(`https://noho.facebook.com/noho?${q}`);
  } catch (err) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(['Here is a sentence', 'here is another']);
      }, 200);
    });
  }
}
