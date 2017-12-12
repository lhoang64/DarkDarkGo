let fetch = require("isomorphic-fetch")
const Cacher = require('../Caching/Cacher')
const Aggregator = require('../Aggregation/Aggregator')

const MGMT_ENDPOINT = "http://54.159.82.218/get_map"

// Manager is a singleton object, accessed from both server.js and controller.js in API
module.exports = Manager = {
    start: () => {
        Cacher.initializeCache()
        Manager.populateIndexServers()
        // Repopulate it every 1 minute
        Manager.intervalid = setInterval(Manager.populateIndexServers, 1000 * 30)
    },

    indexServers: {
        empty: true,
        map: [],
        inversemap: []
    },

    populateIndexServers: () => {
        console.log("Populating index servers")
        fetch(MGMT_ENDPOINT)
            .catch((e) => {
                console.log(Date.now() + ": Management server is offline.");
                throw e
            })
            .then((response) => response.json())
            .catch((e) => {
                throw e
            })
            .then((responsejson) => {
                Manager.indexServers.map = responsejson
                Manager.indexServers.empty = false
                Manager.buildInverseMap()
                console.log(Date.now() + ": Index servers retrieved")
            })
            .catch((error) => {
                console.log(Date.now(), error.message)
            })
    },

    buildInverseMap: () => {
        let temp = {}
        Manager.indexServers.map.forEach((row) => {
            row.forEach((indexServer) => {
                indexServer["chunk_ids"].forEach((chunkId) => {
                    if (temp[chunkId]) {
                        temp[chunkId].add(indexServer["host"])
                    } else {
                        temp[chunkId] = new Set()
                        temp[chunkId].add(indexServer["host"])
                    }
                })
            })
        })
        Manager.indexServers.inversemap = temp
        console.log("Inverse map constructed.")
    },

    stop: () => {
        if (Cacher.intervalid)
            clearInterval(Cacher.intervalid)
        Cacher.dumpCacheToPersistenceSync()
    }
}