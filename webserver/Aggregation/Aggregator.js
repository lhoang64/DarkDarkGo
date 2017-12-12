let settle = require('promise-settle')

const Cacher = require('../Caching/Cacher')
const Manager = require('../Management/Manager')

let fetch = require("isomorphic-fetch")
let utils = require("./utils/Utils.js")

module.exports = Aggregator = 
{
    getResultsFromIndexServer : (query, offset, indexServers, callback) => {
        Aggregator.indexServers = indexServers
        query = query.replace(/[|&;$@"<>()+,]/g, " ").replace(/%20/g,' ')
        Aggregator.queryIndexServerForDocIds(query, offset, callback)
    },

    queryIndexServerForDocIds : (query, offset, callback) => {
        // Check if the query is in the cache, if yes, we can directly call queryIndexServerForSnippets
        if (Cacher.cache.has(query)) {
            snippetwithids = Cacher.cache.get(query)["docids"]
            console.log(String(Date.now()),"Query",query,"served from cache")
            Aggregator.queryIndexServerForSnippets(query, snippetwithids, offset, callback)
            return
        }

        const listOfIndexServers = utils.getIndexServersInRandomRow(Aggregator.indexServers.map)
        
        let docIdObject = {}
        let fetchPromises = listOfIndexServers.map((indexServer, i) => {
            let url = indexServer + '/getdocids?q=' + query
            return (
                fetch(url)
                .catch(() => {console.log("Couldn't fetch from index server " + indexServer)})                
                .then((response) => response.json())
                .catch((err) => {console.log(err); console.log("Couldn't get valid docid json from index server")})
                .then((docIdObject_) => {Object.assign(docIdObject, docIdObject_)})
            )
            //return fetch(indexServer, { mode: 'no-cors' }).then((result) => { ret.push("hi") })
        })

        settle(fetchPromises).then((results) => {
            if (Object.keys(docIdObject).length > 0) {
                Aggregator.queryIndexServerForSnippets(query, docIdObject, offset, callback)
            }
        })
    },

    queryIndexServerForSnippets: (query, docids, offset, callback) => {
        if (!Cacher.cache.has(query)){
            let snippetwithids = {'query': query, 'docids': docids}
            Cacher.addToCache(query, snippetwithids)
        }
        const totalResult = Object.keys(docids).length
        // Get only [offset -> offset + 10)
        const docIdSearchSpace = utils.getDocIdInRange(docids, offset)
        const chunkIdsForDocIds = utils.getChunkIdsForDocIds(docIdSearchSpace)
        let indexServers = []
        let returnSnippets = {'totalResult': totalResult, 'content': []}
        let fetchPromises = []
        for (let i = 0; i < chunkIdsForDocIds.length; i++) {
            const chunkId = chunkIdsForDocIds[i]
            const docId = {rank: offset + i, id: docIdSearchSpace[offset + i]}
            if (!Aggregator.indexServers.inversemap[chunkId]){
                callback(undefined, "I'm alright, but the doc IDs sent by index server and chunk IDs given by management do not quite agree. :'(")
                return
            }
            Aggregator.indexServers.inversemap[chunkId].forEach(indexServer => {
                // Query the snippet endpoint with the docId, and add it to returnSnippets
                let error = undefined
                fetchPromises.push(
                    fetch(indexServer + "/get_snippet?id="+docId.id)
                    .catch(() => {error = true; console.log(Date.now() +" : " + indexServer + "snippet endpoint refused connection")})                    
                    .then((response) => {if (!error) return response.json()})
                    .catch(() => {if (!error) console.log(Date.now() +" : " + indexServer + "sent invalid JSON for docid " + docId)})                    
                    .then((snippet) => {if (!error) snippet.rank = docId.rank; returnSnippets.content.push(snippet)})
                    .catch((err) => {console.log(Date.now() +" : " + err)})
                )
            })
        }
        settle(fetchPromises).then((responses) => {
            if (returnSnippets.content.length > 0){
                callback(returnSnippets, undefined)
            } else {
                callback(undefined, "No results found for the query.")                
            }
        })
    }
}


/*
{
    success: true,
    body: [snippets]
}

- Ask how many first bytesof docid is chunkid

*/