# MGMT

## Flow

### Crawler

When Crawler startup, it `POST` to `/set_component_state` to notify
```
{
    "state": "online"
}
```

State can be:
- `online`: startup
- `error`: actively send its error, otherwise it would be check frequently by our Watchdog
- `waiting`: receive empty queue and waiting for chunk to crawl 
- `paused`: is online but do nothing


MGMT saves the state in its database.

Crawler send `/get_links`. MGMT returns **5** links with corresponding chunk_id
```
{
    "chunk_id": 101,
    "links": ["stuff_1.com", "stuff_2.com", "stuff_3.com", "stuff_4.com", "stuff_5.com"]
}
``` 

If there's no link or less than 5 links, send back an empty JSON `{}`.

MGMT maps chunk_id to host, set task to `crawling`. Task can be:
- `crawling`
- `crawled`
- `propagated`: replicated across Index Servers

When Crawler finishes crawling, it `POST` to `/set_content_chunk_metadata` with its state.
```
{
    "chunk_id": 101,
    "state": "crawled"
}
```

Other than `/get_links` and `/set_content_chunk_metadata`. Crawler can also `/add_links` to the queue. 
It can add as many as it want, as long as links are in this format:
```
{
    "links": ["google.com", "bing.com", "stuff.com"]
}
```

If a link or some links in a chunk fail, Crawler can request additional link without the need to
register a new chunk_id by using `/get_links/<int:number>`

### Index Builder
When startup, `/set_component_state` to notify
```
{
    "state": "online"
}
```

Index Builder `/get_content_chunk_metadata`. We return **5** content chunk metadata, 
with chunk_id and Crawler's host.
```
[
    {
        "chunk_id": 101,
        "host": "10.10.127.101"
    }
]
```

Index Builder `/get_chunks` from *Crawler* and build index. 

After finish building index, Index Builder `/set_index_chunk_metadata` to us.
```
{
    "chunk_id": 101,
    "state": "built"
}
```

State can be 
- `building` 
- `built` 
- `error`: cannot build index chunk
- `propagated`: replicated across Index Servers

If a chunk is successfully built, then we distribute it to Index Server:
**1 copy of content chunk metadata and index chunk metadata in every row.**

Q: How do we actually do it here?
- Get chunk_id which content is crawled and index is built.
- For each row of Index Server, choose a server to assign that chunk.

Say we have 5 rows, 5 servers each row, and 100 chunk_ids.

Need to come up with an algorithm to distribute them nicely so that 
each row will have a copy of a chunk_id and each server have an
equal amount of chunk_id.

### Index Server
When startup, `/set_component_state` to notify
```
{
    "state": "online"
}
```

Index Server `/get_chunks`. We return **5** chunks each time:
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

`index_server_host` are list of servers that MGMT assigns for Index Server to store these copies metadata.

*Note: SQL Database makes sense here because it's very easy to map and lookup for 
Crawler's host, Index Builder's host, and Index Server's host, given chunk_id.
More in [SQL Schema Doc](../src/database/README.md).*

Index Server might also want to send MGMT query stats at `/send_query_stats`. 
Maybe something like:
```
{
    "term": "Is mongodb webscale",
    "timestamp": 1512142011.098839,
    "query_time": "1s"
}
```
(This may not be very important at the moment. Might come back later)

### Front-End
When startup, `/set_component_state` to notify
```
{
    "state": "online"
}
```

Frond-End `/get_servers_map` periodically

```
[
    {
        "row": 1,
        "servers": ["10.10.127.101:5000", "10.10.127.101:5001", "10.10.127.101:5002"]
    },
    {
        "row": 2,
        "servers": ["10.10.127.101:5000", "10.10.127.101:5001", "10.10.127.101:5002"]
    },
    {
        "row": 3,
        "servers": ["10.10.127.101:5000", "10.10.127.101:5001", "10.10.127.101:5002"]
    }
]
```

### Other

Our Watchdogs ping each server periodically for health status at `/get_health_status`.
Other component should return:
```
{
    'status': 'healthy'
}
```
where health status can be:
- `healthy`: is functioning okay
- `failure`: let's just record it for now, recovery action can be added later
- `probation`(optional): after recovery, if remains errors free for a period of time, move to `healthy` state. 
