const express = require('express');

let api_app = express();

const port = 8010;

api_app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

var routes = require('./routes');
routes(api_app);

api_app.listen(port);

console.log('API server started on port ' + port)
