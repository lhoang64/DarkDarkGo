# MGMT

## Flow

### Crawler

When Crawler startup, it `/send_machine_status` to notify
```
{
    'name': 'Crawler',
    'status': 'online'
}
```

State can be `online, error, waiting, or paused`
- `online`: startup
- `error`: ?
- `waiting`: receive empty queue
- `paused`: ?

Q: Do they need to send us their host or we can figure it ourselves?

MGMT saves the state in its database.

Crawler send `/get_links`. MGMT returns
```
{
    'chunk_id': 101,
    'links': ['google.com', 'bing.com']
}
``` 

Q: How many links do they want each requests?
Q: Do they want us to send them empty link if there is no links or just a status code 404?

MGMT assigns that chunk_id to that host, set task to `crawling`. Task can be:
- `crawling`
- `crawled`
- `propagated`: ?

When Crawler finishes crawling, it `send_chunk_metadata`

Q: What is chunk metadata? Why do we store it? 

Q: Is it just chunk_id and host? 
We already know that. Do you mean chunk status instead? `/send_chunk_status`
```
{
    'chunk_id: 101
    'status': 'crawled'
}
```

Crawler can `add_links` to the queue.
```
{
    'links': ['google.com', 'bing.com']
}
```

Q: How many links to add? Does it matter?

### Index Builder
When startup, `/send_machine_status` to notify
```
{
    'name': 'Index Builder',
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
After finish building index, Index Builder `/send_index_metadata`
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

Q: Step 5, replica? 

Q: Why need row_id? status? Does it have to be that way?


### Index Server
When startup, `/send_machine_status` to notify
```
{
    'name': 'Index Server',
    'status': 'online'
}
```

Index Server 

### Front-End
When startup, `/send_machine_status` to notify
```
{
    'name': 'Front-End',
    'status': 'online'
}
```

Frond-End `/get_server_map` periodically

Q: Define server map? What does it do with it?

```
{
    like what?
}
```


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
