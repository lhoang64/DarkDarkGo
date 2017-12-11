module.exports = {
    getChunkIdsForDocIds: (docIdArr) => {
        let chunkIdArr = []
        for (let docid of docidArr) {
            chunkIdArr.push(docid.split('-')[0])
        }
        return chunkIdArr
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