const Cacher = require('../Caching/Cacher');
const Manager = require('../Management/Manager')

module.exports = Aggregator = 
{
    queryIndexServerForDocIds : (query) => {
        // Check if the query is in the cache, if yes, we can directly call queryIndexServerForSnippets
        if (Cacher.cache.has(query)) {
            snippetwithids = cacher.cache.get(query)
            console.log(String(Date.now()),"Query",query,"served from cache")
            return queryIndexServerForSnippets(Cacher.cacher.get(query))
        }
        const numRows = Manager.indexServers.map.length
        const randRowIndex = Math.floor((Math.random() * numRows))
        for (let k in Manager.indexServers.map[randRow].servers) {
                console.log("hi")
        }
    },

    queryIndexServerForSnippets: (query, docids) => {
        if (!Cacher.cache.has(query)){
            let snippetwithids = {
                'query': query,
                'docids': docids
            }
            Cacher.addToCache(query, snippetwithids)
        }

        let error = false
        let errormsg = ""
        let returnvalue = 
        fetch('INDEXSERVERSNIPPETENDPOINT')
        .catch((err) => {
            error = true,
            console.log("Index server's snippet endpoint is offline.")
            errormsg = "Index server's snippet endpoint is offline."
        })
        .then((response) => response.json())
        .catch((err) => {
            if (!error){
                error = true,
                console.log("Index server did not return a valid JSON.")
                errormsg = "Index server did not return a valid JSON."
                throw err
            }
        })
        .then((responsejson) => responsejson
        )
    },

    reportunsuccessfuloperation: (errormsg) => {
        return {
            success: false,
            body: errormsg
        }
    }
}


/*
{
    success: true,
    body: [snippets]
}

*/