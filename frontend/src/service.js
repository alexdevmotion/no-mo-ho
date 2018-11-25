export function getReplaceText (query) {
  const q = `q=${encodeURIComponent(query)}`;
  return new Promise((resolve, reject) => {
    const ws = new WebSocket('ws://localhost:4000');

    ws.onopen = function () {
      ws.send(q);
    };

    ws.onmessage = function (response) {
      resolve(JSON.parse(response.data));
    };

    ws.onerror = function (err) {
      reject(['Something unexpected happened']);
    };
  });
}
