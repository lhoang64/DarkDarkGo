## SQL Schema

```
Components table: map host to type
    ------------------------------------------------------------
   | index | host          | type           | status  | health  |
    ------------------------------------------------------------
   | 0     | 10.10.127.100 | Crawler        | waiting | healthy |
   | 1     | 10.10.127.101 | Index Builider | offline | failure |
   | 2     | 10.10.127.102 | Index Server   | online  | healthy |
    ------------------------------------------------------------

Chunk table: map chunk_id to Crawler's host
    ----------------------------------------------------------------------------
   | index | chunk_id | C's host      | C's task   | IB's host     | IB's task  | 
    ----------------------------------------------------------------------------
   | 0     | 100      | 10.10.127.100 | crawling   | 10.10.127.101 | building   |
   | 1     | 101      | 10.10.127.100 | crawled    | 10.10.127.101 | built      |
   | 2     | 102      | 10.10.127.100 | propagated | 10.10.127.101 | propagated |
    ----------------------------------------------------------------------------

Links table: map link to chunk_id
    ---------------------------------------------------------
   | index | link           | chunk_id | status | task       |
    ---------------------------------------------------------
   | 0     | yahoo.com      | 100      | OK     | pending    |   
   | 1     | google.com     | 100      | Error  | crawling   |
   | 2     | bing.com       | 100      | OK     | crawled    |
   | 3     | duckduckgo.com | 100      | OK     | propagated |      
    ---------------------------------------------------------

Index table: map word to link
    ---------------------------------------
   | index | word      | link      | count |
    ---------------------------------------
   | 0     | mongodb   | yahoo.com | 10    |
   | 1     | web-scale | yahoo.com | 60    |
   | 2     | system    | yahoo.com | 30    |
    ---------------------------------------
```

Q: How can UI update stats in real time? Query every x second?

