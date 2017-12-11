let settle = require('promise-settle')

const Cacher = require('../Caching/Cacher')
const Manager = require('../Management/Manager')

let fetch = require("isomorphic-fetch")
let utils = require("./utils/Utils.js")

module.exports = Aggregator = 
{
    getResultsFromIndexServer : (query, offset, callback) => {
        query = query.replace(/[|&;$@"<>()+,]/g, " ").replace(/%20/g,' ')
        Aggregator.queryIndexServerForDocIds(query, callback)
    },

    queryIndexServerForDocIds : (query, offset, callback) => {
        // Check if the query is in the cache, if yes, we can directly call queryIndexServerForSnippets
        if (Cacher.cache.has(query)) {
            snippetwithids = Cacher.cache.get(query)
            console.log(String(Date.now()),"Query",query,"served from cache")
            Aggregator.queryIndexServerForSnippets(query, Cacher.cacher.get(query), callback)
            return
        }

        const listOfIndexServers = utils.getIndexServersInRandomRow(Manager.indexServers.map)
        
        let docIdArray = []
        let fetchPromises = listOfIndexServers.map((indexServer, i) => {
            let url = indexServer + '/getdocids?q=' + query
            return (
                fetch(url)
                .then((response) => response.json())
                .catch(() => {console.log("Couldn't fetch from index server " + indexServer)})
                .then((docidarr) => {docIdArray.concat(docidarr)})
            )
            //return fetch(indexServer, { mode: 'no-cors' }).then((result) => { ret.push("hi") })
        })

        settle(fetchPromises).then((results) => {
            if (results.length > 0 && docIdArray.length > 0) {
                queryIndexServerForSnippets(query, docIdArray, callback)
            }
        })
    },

    queryIndexServerForSnippets: (query, docids, callback) => {
        if (!Cacher.cache.has(query)){
            let snippetwithids = {
                'query': query,
                'docids': docids
            }
            Cacher.addToCache(query, snippetwithids)
        }
        const totalResult = docids.length
        // Get only [offset -> offset + 10)
        const docIdSearchSpace = utils.getDocIdInRange(docids, offset)
        const chunkIdsForDocIds = utils.getChunkIdsForDocIds(docIdSearchSpace)
        let indexServers = []
        let returnSnippets = {totalResult: totalResult, content: []}
        let fetchPromises = []
        for (let i = 0; i < chunkIdsForDocIds.length; i++) {
            const chunkId = chunkIdsForDocIds[i]
            const docId = docIdSearchSpace[i]
            Manager.indexServers.inversemap[chunkId].forEach(indexServer => {
                // Query the snippet endpoint with the docId, and add it to returnSnippets
                fetchPromises.push(
                    fetch(indexServer + "/get_snippet?id="+docId.id)
                    .then((response) => response.json())
                    .then((snippet) => {snippet.rank = docId.rank; returnSnippets.content.push(snippet)})
                    .catch((err) => {console.log(Date.now(),":",indexServer,"snippet endpoint refused connection")})
                )
            })
            settle(fetchPromises).then((responses) => {
                if (returnSnippets.content.length > 0){
                    callback(returnSnippets, undefined)
                }
                callback(undefined, "No results found for the query.")
            })
        }
    }
}


/*
{
    success: true,
    body: [snippets]
}

- Ask how many first bytesof docid is chunkid

*/