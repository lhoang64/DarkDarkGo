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

**Set link's state**
- URL: `/set_state/link`
- Method: `POST`
- State can be:
    - `error`
    - `crawled`
- If it's successfully crawled, request message should look like this:
    ```
    {
        "link": "https://www.google.com",
        "state": "crawled"
    }
    ```
- Otherwise, if it's error, then we will send back a new link:
    ```
    {
        "link": "https://www.bing.com",
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

**Send content chunk metadata (basically state since we've already know the host)**
- URL: `/set_state/content_chunk`
- Method: `POST`
- State can be:
    - `crawled`
    - `propagated`
- Sample data:
    ```
    {
        "chunk_id": "1c",
        "state": "crawled"
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
    - `propagated`
- Sample data:
    ```
    {
        "chunk_id": 101,
        "state": "built"
    }
    ```
    
### Index Server

**Get content chunk metadata, index chunk metadata for that given Index Server**
- URL: `/get_chunks`
- Method: `GET`
- Return:  All chunks metadata each request
- Sample data:
```
[
    {
        "chunk_id": "101c",
        "hosts": {
                    "c_host": "http://101.101:101:101:5000",
                    "ib_host": "http://101.101:101:102:5000"
                  }
    }
]
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
- URL: `/get_map`
- Method: `GET`
- Sample data:

```
[
    [
        { 
            "host": "3.0.0.1",
            "chunk_ids": ["1c", "2c", "3c"]
        },
        { 
            "host": "3.0.0.2",
            "chunk_ids": ["4c", "5c", "6c"]
        }    
    ],
    [
        { 
            "host": "3.0.0.3",
            "chunk_ids": ["1c", "2c", "3c"]
        },
        { 
            "host": "3.0.0.4",
            "chunk_ids": ["4c", "5c", "6c"]
        }  
    ]
]
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

