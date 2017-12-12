const express = require('express');
const routes = require('./api/routes');
let Manager = require('./Management/Manager.js');

let app = express();

const port = process.env.NODE_PORT || 5000;

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

routes(app);

app.listen(port, ()=>{
    Manager.start();
    console.log('Backend server active on port ' + port);
});

// Gracefully shut down if the server unexpectedly dies
process.on('SIGINT', () => {
    Manager.stop()
    process.exit()
})

process.on('SIGTERM', () => {
    Manager.stop()
    process.exit()
})