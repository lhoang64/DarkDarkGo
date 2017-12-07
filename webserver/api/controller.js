const Aggregator = require('../Aggregation/Aggregator');
const Cacher = require('../Caching/Cacher');
let Manager = require('../Management/Manager');
exports.handleQuery = (req, res) => {
    /*
        1. Send query 
        2. Have static aggregation class, and caching class...perhaps they could live on different servers, or not

    */
    const queryString = req.query.q
    console.log("New query:", req.query.q)

    if (Manager.indexServers.empty) {
        res.json({
            head: 'error',
            message: 'No index servers online'
        });
    } else {
        // Make a request to the index servers, aggregate and prepare snippets
        Cacher.addToCache(queryString, "");
        res.json({
            head: 'success',
            body: []
        });
    }
}

exports.fofhandler = (req, res) => {
    res.send('Invalid request');
}