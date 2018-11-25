const express = require('express');
const axios = require('axios');
const fs = require('fs');
const https = require('https');
const app = express();

const PORT = 80;
const HOSTNAME = '0.0.0.0';

app.get('/noho', async function (req, res) {
  console.log(req.query);
  const result = await axios.get(`http://localhost:5000/noho?q=${req.query.q}`);
  console.log(result.data);
  res.send(result.data);
});

https.createServer({
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert')
}, app)
  .listen(PORT, HOSTNAME, function () {
    console.log(`Example app listening on port ${PORT}! Go to https://${HOSTNAME}:${PORT}/`)
  });