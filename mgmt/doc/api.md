## APIs

### All Components

**Send state when wakes up.**
- URL: `/set_state/component`
- Method: `POST`
- State can be:
    - `online`: startup
    - `error`: actively send its error, otherwise it would be check frequently by our Watchdog
    - `waiting`: receive empty queue and waiting for chunk to crawl 
    - `paused`: is online but do nothing
- Sample data:
    ```
    {
        "state": "online"
    }
    ```
        
### Crawler   

**Get link to crawl**
- URL: `/get_links`
- Method: `GET`
- Return: 5 links each request
- Sample data:
    ```
    {
        "chunk_id": 101,
        "links": ["stuff_1.com", "stuff_2.com", "stuff_3.com", "stuff_4.com", "stuff_5.com"]
    }
    ```
- If there's no link or less than 5 links, send back an empty JSON

**Get a number of links to crawl**
- URL: `/get_links/<int:number>`
- Method: `GET`
- Only use when a link/some links in chunk fail to get additional links without creating a new chunk_id
- Return: a number of links
- Sample data:
    ```
    {
        "links": ["stuff_1.com", "stuff_2.com", "stuff_3.com", "stuff_4.com", "stuff_5.com"]
    }
    ```
**Set link's state**
- URL: `/set_state/link`
- Method: `POST`
- State can be:
    - `error`
    - `crawled`
- Sample data:
    ```
    {
        "link": "https://www.google.com",
        "state": "crawled"
    }
    ```


**Send content chunk metadata (basically state since we've already know the host)**
- URL: `/set_state/content_chunk`
- Method: `POST`
- State can be:
    - `crawled`
- Sample data:
    ```
    {
        "chunk_id": 101,
        "state": "crawled"
    }
    ```
    
**Add links to MGMT database**
- URL: `/add_links`
- Method: `POST`
- Sample data:
    ```
    {
        "links": ["google.com", "bing.com", "stuff.com"]
    }
    ```

**Get unpropagated chunks**
- URL: `/get_chunks/unpropagated`
- Method: `GET`
- Return: 5 chunks each request
- Sample data:
```
    {
        "chunks": [100, 101, 102]
    }
```

### Index Builder

**Get content chunk metadata**
- URL: `/get_metadata/content_chunk`
- Method: `GET`
- Return: 5 content chunks metadata each request
- Sample data:
    ```
    [
        {
            "chunk_id": 101,
            "host": "10.10.127.101"
        }
    ]
    ```

**Send index chunk metadata/state (same reason above)**
- URL: `/set_state/index_chunk`
- Method: `POST`
- State can be: 
    - `built` 
    - `error`: cannot build index chunk
- Sample data:
    ```
    {
        "chunk_id": 101,
        "state": "built"
    }
    ```
    
### Index Server

**Get content chunk metadata, index chunk metadata, index server host for distribution**
- URL: `/get_chunks`
- Method: `GET`
- Return:  5 chunks metadata each request
- Sample data:
    ```
    [
        {
            "chunk_id": 101,
            "crawler_host": "10.10.127.100:5000",
            "index_builder_host": "10.10.127.101:5000",
            "index_server_host": [
                                    {
                                        "row": 1,
                                        "host": "10.10.127.102:5000"
                                    },
                                    {
                                        "row": 2,
                                        "host": "10.10.127.102:5001"
                                    }
                                 ]
        }
    ]
    ```

**Send chunk propagated state**
- URL: `/set_chunk/propagated`
- Method: `POST`
- Sample data:
```
{
    'chunk_id': 101,
    'state': 'propagated'
}
```

**Send query stats**
- URL: `/send_stats/query`
- Method: `POST`
- Sample data:
    ```
    {
        "term": "Is mongodb webscale",
        "timestamp": 1512142011.098839,
        "query_time": "1s"
    }
    ```
    
### Front-End

**Get server map periodically**
- URL: `/get_map/index_servers`
- Method: `GET`
- Sample data:
    ```
    {
       "map":[
          {
             "servers":[
                {
                   "host":"10.10.127.101:5000",
                   "chunk_ids":[
                      1,
                      2,
                      3
                   ]
                },
                {
                   "host":"10.10.127.101:5000",
                   "chunk_ids":[
                      1,
                      2,
                      3
                   ]
                }
             ]
          },
          {
             "servers":[
                {
                   "host":"10.10.127.101:5000",
                   "chunk_ids":[
                      1,
                      2,
                      3
                   ]
                }
             ]
          },
          {
             "servers":[
                {
                   "host":"10.10.127.101:5000",
                   "chunk_ids":[
                      1,
                      2,
                      3
                   ]
                }
             ]
          }
       ],
       "inverted_map":[
          {
             "101":"10.10.10",
             "102":"10.10.11",
             "101":"10.10.12"
          },
          {
             "101":"10.10.10",
             "102":"10.10.11",
             "101":"10.10.12"
          }
       ]
    }
    ```
    
### Other

**Our Watchdogs ping all servers periodically for health status.**
- URL: `/get_health`
- Method: `GET`
- Health status can be:
    - `healthy`: is functioning okay
    - `failure`: let's just record it for now, recovery action can be added later
    - `probation`(optional): after recovery, if remains errors free for a period of time, move to `healthy` state. 
- Sample data:
    ```
    {
        "status": "healthy"
    }
    ```

