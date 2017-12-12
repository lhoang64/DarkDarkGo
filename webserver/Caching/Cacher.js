

// Cacher is a singleton for each server instance
const fs = require('fs');

module.exports = Cacher = new Object();

Cacher.initializeCache = () => {
    if (!Cacher.cacheInitialized) {
        const LRU = require("lru-cache")
        const options = { max: 10000 ,maxAge: 1000 * 60 * 60 * 24 * 5 } //10 days
        Cacher.cache = LRU(options)

        console.log("Initializing cache...")
        if (fs.existsSync('cachedata.txt')){        
            const data = fs.readFileSync('cachedata.txt')
            if (String(data).length > 0) {
                Cacher.cache.load(JSON.parse(data))
                console.log("Cache length is", Cacher.cache.length)
                console.log("Cache initialized from persistence")
            }
        }   
        Cacher.cacheInitialized = true
        console.log("Cacher successfully initialized")
    }

    Cacher.intervalid = setInterval(Cacher.dumpCacheToPersistenceAsync, 1000*30)
}

Cacher.addToCache = (queryString, snippet) => {
    if (!Cacher.cacheInitialized) Cacher.initializeCache();
    Cacher.cache.set(queryString, snippet)
}

Cacher.dumpCacheToPersistenceSync = () => {
    /*
    To do: Only dump if any changes have been made, and instead of rewriting, only write the change stream
    */
    const dump = JSON.stringify(Cacher.cache.dump())
    fs.writeFileSync("cachedata.txt", dump)
    console.log("\nCache successfully dumped to persistence because of SIGINT or SIGTERM.\n\n")
}

Cacher.dumpCacheToPersistenceAsync = () => {
    /*
        To do: Only dump if any changes have been made, and instead of rewriting, only write the change stream
    */
    const dump = JSON.stringify(Cacher.cache.dump())
    fs.writeFile("cachedata.txt", dump, 'utf-8', (err)=>{
        if (err) console.log("Async cache save failed.")
        else console.log(Date.now() + " : Cache successfully dumped to persistence aysnc-ally.\n\n")
    })
}