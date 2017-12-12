/**
 * This module contains utility functions for aggregation class
 */

Object.filter = (obj, predicate) => 
    Object.keys(obj)
        .filter( key => predicate(obj[key]) )
        .reduce( (res, key) => (res[key] = obj[key], res), {} );

module.exports = {
    getChunkIdsForDocIds: (docIdObject) => {
        docidArr = Object.values(docIdObject)
        let chunkIdArr = []
        for (let docid of docidArr) {
            chunkIdArr.push(docid.split('-')[1])
        }
        return chunkIdArr
    },

    getDocIdInRange: (docIdObject, offset) => {
        const lowerBound = offset * 10
        const upperBound = lowerBound + 10
        if (docIdObject[lowerBound])
            return Object.filter(docIdObject, rank > lowerBound && rank < upperBound)
        return docIdObject
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