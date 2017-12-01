const Aggregator = require('../Aggregation/Aggregator');
const Cacher = require('../Caching/Cacher');
let Manager = require('../Management/Manager');

exports.handleQuery = (req, res) => {
    /*
        1. Send query 
        2. Have static aggregation class, and caching class...perhaps they could live on different servers, or not

    */
    
    console.log("Manger's IS list is " + Manager.indexServers.empty)
    if (Manager.indexServers.empty == false) {
        res.json({
            head: 'success'
        });
    } else {
        res.json({
            head: 'error'
        });
    }
}