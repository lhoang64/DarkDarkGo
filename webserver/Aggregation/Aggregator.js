const Cacher = require('../Caching/Cacher')
const Manager = require('../Management/Manager')

let fetch = require("isomorphic-fetch")

const INDEX_SERVER_DOCID_ENDPOINT = ""
const INDEX_SERVER_SNIPPET_ENDPOINT = ""

module.exports = Aggregator = 
{
    getResultsFromIndexServer : (query, callback) => {
        query = query.replace(/[|&;$@"<>()+,]/g, " ").replace(/%20/g,' ')
        Aggregator.queryIndexServerForDocIds(query, callback)
    },

    queryIndexServerForDocIds : (query, callback) => {
        // Check if the query is in the cache, if yes, we can directly call queryIndexServerForSnippets
        if (Cacher.cache.has(query)) {
            snippetwithids = Cacher.cache.get(query)
            console.log(String(Date.now()),"Query",query,"served from cache")
            Aggregator.queryIndexServerForSnippets(query, Cacher.cacher.get(query), callback)
        }
        responded = false
        fetch(INDEX_SERVER_DOCID_ENDPOINT + query)
        .catch((e) => {callback(undefined, "Index server docid endpoint doesn't work"); responded = true})
        .then((response) => {if (!responded) return response.json()})
        .then((responsejson) => {if (!responded) Aggregator.queryIndexServerForSnippets(query, responsejson, callback)})
    },

    queryIndexServerForSnippets: (query, docids, callback) => {
        if (!Cacher.cache.has(query)){
            let snippetwithids = {
                'query': query,
                'docids': docids
            }
            Cacher.addToCache(query, snippetwithids)
        }

        //Only query offset - offset + 10 queries

        let error = false
        let errormsg = ""
        let returnvalue = 
        fetch(INDEX_SERVER_SNIPPET_ENDPOINT, {
            method: 'POST',
            body: docids
        })
        .catch(() => {
            error = true,
            console.log("Index server's snippet endpoint is offline.")
            errormsg = "Index server's snippet endpoint is offline."
        })
        .then((response) => response.json())
        .catch(() => {
            if (!error){
                error = true,
                console.log("Index server did not return a valid JSON.")
                errormsg = "Index server did not return a valid JSON."
                throw err
            }
        })
        .then((responsejson) => responsejson)
    }
}


/*
{
    success: true,
    body: [snippets]
}

*/