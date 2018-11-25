const express = require('express');
const axios = require('axios');
const fs = require('fs');
const https = require('https');
const app = express();

app.get('/noho', async function (req, res) {
  console.log(req.query);
  const result = await axios.get('http://localhost/noho');
  console.log(result);
});

https.createServer({
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert')
}, app)
  .listen(3000, function () {
    console.log('Example app listening on port 3000! Go to https://localhost:3000/')
  });