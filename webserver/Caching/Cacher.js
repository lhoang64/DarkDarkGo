

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
}

Cacher.addToCache = (queryString, snippet) => {
    if (!Cacher.cacheInitialized) Cacher.initializeCache();
    Cacher.cache.set(queryString, snippet)
}

Cacher.dumpCacheToPersistence = () => {
    const dump = JSON.stringify(Cacher.cache.dump())
    console.log("Type is ", typeof(dump))
    console.log(dump)
    fs.writeFileSync("cachedata.txt", dump)
    console.log("\nCache successfully dumped to persistence.")
}