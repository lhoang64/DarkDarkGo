const Aggregator = require('../Aggregation/Aggregator')
const Cacher = require('../Caching/Cacher')
let Manager = require('../Management/Manager')

exports.handleQuery = (req, res) => {
    res.json({head: 'success',
    message: 
        [
            {
                title: "How To Tie A Windsor Knot | Ties.com",
                href: "https://www.ties.com/how-to-tie-a-tie/windsor",
                desc: "The Windsor Knot Tying Instructions. Start with the wide end of the tie on the right and the small end on the left. Wide end over the small end to the left. Up into the neck loop from underneath. Down to the left. Around the back of the small end to the right. Up to the center, towards neck loop."
            },
            { 
                title: "4 Ways to Tie a Tie - wikiHow",
                href: "https://www.wikihow.com/Tie-a-Tie",
                desc: "How to Tie a Tie. Have you graduated beyond the clip-on tie? Beginning with these helpful instructions, a sharp-looking tie, a mirror, and some patience, you can become an expert in tying your own fashionable knot. You have several options..."
            },
            {
                title: "Brooks Brothers | How To Tie A Tie | Tie Knots",
                href: "https://www.brooksbrothers.com/how-to-tie-a-tie/how-to-tie-a-tie,default,pg.html",
                desc: "Watch our how to tie a tie videos on five classic knots including the Bow Tie knot, Windsor knot, Half Windsor knot, Pratt knot, and Four in Hand knot. The five tie knots every man should know."
            }
        ]
    }
    )
    const query = req.query.q    
    if (!Cacher.cache.has(query)){
        let snippetwithids = {
            'query': query,
            'docids': {'1':'232'}
        }
        Cacher.addToCache(query, snippetwithids)
    }
    return

    const queryString = req.query.q
    const offset = req.query.offset
    console.log("New query:", queryString)

    if (Manager.indexServers.empty || Manager.indexServers.map.length == 0 || Manager.indexServers.inversemap.length == 0) {
        returnError(res, "No index servers online")
    } else {
        Aggregator.getResultsFromIndexServer(queryString, offset, (success, error) => {
            if (error) {
                returnError(res, error)
            }
            else {
                res.json(success)                
            }
        })}
}

exports.handleCacheSearch = (req, res) => {
    const query = req.query.q
    let ret = []
    let candidates = []
    const allKeys = Cacher.cache.keys()

    if (allKeys.constructor === Array){
        let count = 0
        let candidateCount = 0
        for (let key of allKeys) {
            if (key.startsWith(query)){
                ret.push(key)
                count++
            } else if (key.includes(query) || (query.length > 3 && query.includes(key))) {
                candidates.push(key)
                candidateCount++
            }
            if (count == 5 || candidateCount == 5)
                break
        }

        if (count < 6) {
            ret = ret.concat(candidates)
        }

        res.send(ret)
        // let ret = allKeys.filter((cachekey, index) => cachekey.startsWith(query))
        return
    }
    res.send([])
}

exports.handleHealth = (req, res) => {
    res.json(
        {
            'status': 'healthy'
        }
    )
}

/*
/searchid/:query

/searchsnippets/:id
*/
exports.fofhandler = (req, res) => {
    res.send('Invalid request')
}

returnError = (res, errormessage) => {
    res.json({
        head: 'error',
        message: errormessage
    })
}


// res.json({head: 'success',
// message: 
//     [
//         {
//             title: "How To Tie A Windsor Knot | Ties.com",
//             href: "https://www.ties.com/how-to-tie-a-tie/windsor",
//             desc: "The Windsor Knot Tying Instructions. Start with the wide end of the tie on the right and the small end on the left. Wide end over the small end to the left. Up into the neck loop from underneath. Down to the left. Around the back of the small end to the right. Up to the center, towards neck loop."
//         },
//         { 
//             title: "4 Ways to Tie a Tie - wikiHow",
//             href: "https://www.wikihow.com/Tie-a-Tie",
//             desc: "How to Tie a Tie. Have you graduated beyond the clip-on tie? Beginning with these helpful instructions, a sharp-looking tie, a mirror, and some patience, you can become an expert in tying your own fashionable knot. You have several options..."
//         },
//         {
//             title: "Brooks Brothers | How To Tie A Tie | Tie Knots",
//             href: "https://www.brooksbrothers.com/how-to-tie-a-tie/how-to-tie-a-tie,default,pg.html",
//             desc: "Watch our how to tie a tie videos on five classic knots including the Bow Tie knot, Windsor knot, Half Windsor knot, Pratt knot, and Four in Hand knot. The five tie knots every man should know."
//         }
//     ]
// }
// )
// const query = req.query.q    
// if (!Cacher.cache.has(query)){
//     let snippetwithids = {
//         'query': query,
//         'docids': {'1':'232'}
//     }
//     Cacher.addToCache(query, snippetwithids)
// }
// return