# MGMT

## Flow

### Crawler

When Crawler startup, it `/send_machine_status` to notify
```
{
    'type': 'Crawler',
    'status': 'online'
}
```

State can be `online, error, waiting, or paused`
- `online`: startup
- `error`: ?
- `waiting`: receive empty queue or status code?
- `paused`: ?

Q: Do they need to send us their host or we can figure it ourselves?

MGMT saves the state in its database.

Crawler send `/get_links`. MGMT returns
```
{
    'chunk_id': 101,
    'links': ['google.com', 'bing.com', 'stuff.com']
}
``` 

Q: How many links do they want each requests? Does it matter?

Q: Do they want us to send them empty link if there is no links or just a status code 404?

MGMT assigns that chunk_id to that host, set task to `crawling`. Task can be:
- `crawling`
- `crawled`
- `propagated`: ?

When Crawler finishes crawling, it `send_chunk_metadata`

Q: What is chunk metadata? Why do we store it? 

Q: Is it just chunk_id and host? 

A: If it is chunk_id and host. We already know that. Right?

Or do you mean chunk status instead? `/send_chunk_status`
```
{
    'chunk_id: 101
    'status': 'crawled'
}
```

Crawler can `add_links` to the queue.
```
{
    'links': ['google.com', 'bing.com', 'stuff.com']
}
```

Q: How many links to add? Does it matter?

Q: Error Handling?

Q: What if a link in a chunk fails? Does it mean a chunk fail? What to do with that?

### Index Builder
When startup, `/send_machine_status` to notify
```
{
    'type': 'Index Builder',
    'status': 'online'
}
```

Index Builder `/get_chunk_metadata`. Assume it has only chunk_id and Crawler's host
```
{
    'chunk_id': 101,
    'host': '10.10.127.101'
}
```

Q: How many chunk_metadata do they want each request?

Index Builder `/get_chunk` from *Crawler* and build index. 
After finish building index, Index Builder `/send_index_metadata` to us.
```
{
    'chunk_id': 101,
    'status': built
    'indexes': [
                  {
                    'word': 'web-scale',
                    'count': 60,
                    'links': ['google.com', 'mongodb.com']
                  },
                  {
                    'word': 'system',
                    'count': 10,
                    'links': ['google.com', 'mongodb.com']
                  }
               ] 
}
```

Q: Error Handling?

Q: Is there any chance that Index Builder fail to build from chunk_id? Why can it happen?

Q: Step 5, how does replication work? 

Q: Why need row_id? status? Does it have to be that way?

### Index Server
When startup, `/send_machine_status` to notify
```
{
    'type': 'Index Server',
    'status': 'online'
}
```

Q: What does Index Server want?

Q: What do we want from Index Server?

A: Query stats, mostly.

Q: Define query stats

A: 
- what term does user search for
- what time does they ask
- if UI can find it in the cache, can we know?
- if not, FE will ask for IS, then how much time does it take you to search for it?
- how many result found
- how is the result? can we validate this? how relevant is that?
- what is the most query keyword?

Index Server can `/send_query_stats`
```
{
    'term': 'Is mongodb webscale'
    'timestamp': 1512142011.098839,
    'query_time': '10s'
    'keyword': [
                    {
                        'word': 'web-scale',
                        'count': 10
                    }
               ]
}
```

Q: What does Index Server do?

A:
- Crawler maintains content chunk after crawled?\
- Index Builder maintains index chunk after built
- MGMT maintains chunk_metadata and index_metadata
- Index Server 

### Front-End
When startup, `/send_machine_status` to notify
```
{
    'type': 'Front-End',
    'status': 'online'
}
```

Frond-End `/get_server_map` periodically

Q: Define server map? What does it do with it?
```
[
    {
        'row_id': 1,
        'chunk_id': 101
    }
]
```
Q: Does FE need to know about Crawler's host and Index Builder's host?

### Other

Our Watchdogs ping each machine periodically for health status at `/get_health_status`.
Other component should return:
```
    'status': 'healthy'
```

Health status can be `healthy`, `failure`, `probation`
- `healthy`: fully functioning
- `failure`: let's just record it for now, recovery action can be added later
- `probation`(optional): after recovery, if remains errors free for a period of time, move to `healthy` state. 
