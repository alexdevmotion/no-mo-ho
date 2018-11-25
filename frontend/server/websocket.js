const WebSocketServer = require("ws").Server;
const axios = require('axios');

const wss = new WebSocketServer({ port: 4000 });

wss.on("connection", function (ws) {

    ws.on('message', async function(msg){
        console.log('received', msg);
        // const result = await axios.get(`https://short-sloth-87.localtunnel.me/noho?${msg}`);
        const result = await axios.get(`http://localhost:5000/noho?${msg}`);
        ws.send(JSON.stringify(result.data));
    });

    ws.on('close', function() {
        console.log('closing connection');
    });
});