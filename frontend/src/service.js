export async function getReplaceText (query) {
  const q = `q=${encodeURIComponent(query)}`;
  try {
    const response = await fetch(`https://noho.facebook.com:443/noho?${q}`);
    return response.data;
  } catch (err) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(['Here is a sentence', 'here is another']);
      }, 200);
    });
  }
}
