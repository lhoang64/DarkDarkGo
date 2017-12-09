/*
This module maintains a list of index servers by querying the management, and 

*/


let fetch = require("isomorphic-fetch")

const Cacher = require('../Caching/Cacher')
const Aggregator = require('../Aggregation/Aggregator')

const MGMT_IP = ""

// Manager is a singleton object, accessed from both server.js and controller.js in API
module.exports = Manager = 
{
    indexServers : {
        empty: true,
        map: [],
        inversemap: []
    },

    populateIndexServers : () => {
        fetch(MGMT_IP + "/get_map/index_servers")
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
    },

    start : () => {
        Cacher.initializeCache()

        // Repopulate it every 3 minutes
        //Manager.populateIndexServers();
    },

    stop : () => {
        if (Cacher.intervalid)
            clearInterval(Cacher.intervalid)
        Cacher.dumpCacheToPersistenceSync()
    }
}