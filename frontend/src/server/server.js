const express = require('express');
const routes = require('./api/routes');

let app = express();

const port = 8010;

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

routes(app);

app.listen(port, ()=>{Manager(app)});

console.log('Backend server active on port ' + port)
