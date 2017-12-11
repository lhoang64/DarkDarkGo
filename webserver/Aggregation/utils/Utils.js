module.exports = {
    getChunkIdsForDocIds: (docIdArr) => {

    },

    getDocIdInRange: (docIdArr, offset) => {

    },
    getIndexServersInRandomRow: (indexServersMap) => {
        let ret = []        
        const numRows = indexServersMap.length
        const randInt = parseInt(Math.random() * numRows, 10)
        const indexServerCompleteCopy = indexServersMap[randInt]
        indexServerCompleteCopy.forEach(hostInfo => {
            ret.push(hostInfo["host"])
        });
        return ret
    }
}