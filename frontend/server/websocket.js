const WebSocketServer = require("ws").Server;
const axios = require('axios');

const wss = new WebSocketServer({ port: 4000 });

wss.on("connection", function (ws) {

    ws.on('message', async function(msg){
        console.log('received', msg);
        try {
          const result = await axios.get(`http://localhost:5000/noho?${msg}`);
          // const result = await axios.get(`https://short-sloth-87.localtunnel.me/noho?${msg}`);
          ws.send(JSON.stringify(result.data));
        } catch (e) {
          ws.send(JSON.stringify(['Sorry, something went wrong with the server', 'So here are some hardcoded strings']));
        }
    });

    ws.on('close', function() {
        console.log('closing connection');
    });
});