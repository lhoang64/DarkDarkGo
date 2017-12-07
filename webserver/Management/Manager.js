/*
This module maintains a list of index servers by querying the management, and 

*/


let fetch = require("isomorphic-fetch");

const Cacher = require('../Caching/Cacher');
const Aggregator = require('../Aggregation/Aggregator');

let exampleReply = {
    row1: ['127.0.0.1', '127.0.0.1', '127.0.0.1', '127.0.0.1', '127.0.0.1'],
    row2: ['127.0.0.1','127.0.0.1','127.0.0.1'],
    row3: ['127.0.0.1','127.0.0.1','127.0.0.1','127.0.0.1']
}

// Manager is a singleton object, accessed from both server.js and controller.js in API
module.exports = Manager = new Object();

Manager.indexServers = {
    empty: true,
    row1: [],
    row2: [],
    row3: []
}

Manager.populateIndexServers = () => {
    fetch('http://mgmtserverip')
    .catch((e)=>{
        console.log("Couldn't fetch.");
        throw e
    })
    .then((response) => response.json())
    .catch((e)=>{
        throw e
    })
    .then((responsejson) => {
        Manager.indexServers = responsejson
        Manager.indexServers.empty = false
    })
    .catch((error) => {
        console.log(error.message)
    })
}


Manager.start = () => {
    Cacher.initializeCache()

    // Repopulate it every 3 minutes
    //Manager.populateIndexServers();
}

Manager.stop = () => {
    Cacher.dumpCacheToPersistence()
}