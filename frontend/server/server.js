const express = require('express');
const axios = require('axios');
const fs = require('fs');
const https = require('https');
const app = express();

app.get('/noho', async function (req, res) {
  console.log(req.query);
  const result = await axios.get(`http://localhost:5000/noho?q=${req.query.q}`);
  console.log(result);
  res.send(result.data);
});

https.createServer({
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert')
}, app)
  .listen(80, function () {
    console.log('Node dispatcher listening on port 80! Go to https://localhost:80/')
  });