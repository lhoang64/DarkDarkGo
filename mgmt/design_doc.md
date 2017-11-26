# MGMT Design Doc

## Interaction with other components

### Crawer

#### Seeds 
- Crawler asks MGMT for seed or lists of seeds with
    `/get_seed`
    ```
    {   
        "link":"http://goo.ne.jp/massa.xml",
        "state":"pending"
    }
    ```
    `/get_seeds?n`
    ```
    [  
       {  
          "link":"https://vinaora.com/at/vulputate/vitae/nisl/aenean/lectus/pellentesque.js",
          "state":"pending"
       },
       {  
          "link":"https://google.fr/massa.js",
          "state":"pending"          
       },
       {  
          "link":"http://bing.com/nec/sem.js",
          "state":"pending"
       }
    ]
    ```
- When Crawler receives these, it sends back seeds' stats where it updates states
of seeds. It can also update seed stats frequently for MGMT.
    `/update_seed_stats`
    ```
    [  
       {  
          "link":"https://vinaora.com/at/vulputate/vitae/nisl/aenean/lectus/pellentesque.js",
          "state":"crawling"
       },
       {  
          "link":"https://google.fr/massa.js",
          "state":"crawling"          
       },
       {  
          "link":"http://bing.com/nec/sem.js",
          "state":"crawling"
       }
    ]
    ```
- The seed can be in 4 states. It depends on how Crawler handles it and update to MGMT.
  - pending
  - crawling
  - crawled
  - propagated
- One way MGMT can do is to have a database of all seeds with their state. MGMT updates the database
according to the changes that Crawler sends. Or MGMT can have different data structure for different states:
a queue for pending seeds, sets for crawling, crawled, propagated. The goal is to make sure that all seeds go
through all states. 

#### Content chunk
- Crawler can also send MGMT content chunk metadata with stats: IP, Port of the machine and state.
    `/add_chunk_metadata`
    ```
    [
       {
          "chunk_ID":"bd6146c0-315f-4f67-89ad-1576dc13b701",
          "IP":"63.161.242.61",
          "port":9000,
          "state":"crawling"
       },
       {
          "chunk_ID":"a043738c-3458-416d-99ad-99ea1b318468",
          "IP":"63.161.242.61",
          "port":9000,
          "state":"crawling"
       },
       {
          "chunk_ID":"a7e738b4-a134-4144-9cf9-0b02400d5bd4",
          "IP":"63.161.242.61",
          "port":9000,
          "state":"crawling"
       }
    ]
    ```
- Same as seed, content chunk also have state: crawling, crawled and propagated.

### Index Builder
- Index Builder gets chunk metadata from MGMT and uses that to look for Crawler's content database.
    `/get_chunk_metadata`
    ```
    [
       {
          "chunk_ID":"bd6146c0-315f-4f67-89ad-1576dc13b701",
          "IP":"63.161.242.61",
          "port":9000,
          "state":"propagted"
       },
       {
          "chunk_ID":"a043738c-3458-416d-99ad-99ea1b318468",
          "IP":"63.161.242.61",
          "port":9000,
          "state":"propagted"
       },
       {
          "chunk_ID":"a7e738b4-a134-4144-9cf9-0b02400d5bd4",
          "IP":"63.161.242.61",
          "port":9000,
          "state":"propagted"
       }
    ]
    ```
- Index Builder builds to index chunk and sends back to MGMT.
    `/add_index_chunk`
    ```
    [
       {
          "word":"open system",
          "chunk_ID":"b356063a-3234-4b60-a19c-3d50c160dfd6",
          "word_count":60,
          "entry_ID":[
             "f4aa090b-b200-4956-9350-bcbad04b969d",
             "9d380e2c-3394-438d-a8d0-d46d652ac732",
             "7b2d3819-d0c8-4e7c-83f0-e434b3199af2"
          ]
       },
       {
          "word":"local",
          "chunk_ID":"a6335332-a679-44fc-ae47-c9eff963905e",
          "word_count":43,
          "entry_ID":[
             "627bf7cf-4b99-4c6f-8887-63e1257bf55e",
             "89d0d0a6-03d2-4c34-adc8-e2dccf574359",
             "ebbdf83f-3a3c-41e6-b063-dfb11e343e53"
          ]
       },
       {
          "word":"Synchronised",
          "chunk_ID":"1ee756c1-274b-4d90-a8b2-84aa5a584c9e",
          "word_count":65,
          "entry_ID":[
             "b6c68d31-8ce1-4ea7-8b8a-c84188084d07",
             "f80eb544-6548-42d4-a814-2f80eeb0088b",
             "0a79a97d-d5c7-4956-9aae-fae04b9a45ba"
          ]
       }
    ]
    ```

### Index Server
- Index Server sends querying stats to MGMT.
    `/add_query_stats`
    ```
    [
       {
          "timestamp":"12:56 AM",
          "date":"2/6/2017",
          "counter":35,
          "word":"Synchronised",
          "chunk_ID":"1ee756c1-274b-4d90-a8b2-84aa5a584c9e",
          "entry_ID":"1ee756c1-274b-4d90-a8b2-84aa5a584c9e"
       },
       {
          "timestamp":"3:21 PM",
          "date":"11/14/2017",
          "counter":18,
          "word":"Synchronised",
          "chunk_ID":"1ee756c1-274b-4d90-a8b2-84aa5a584c9e",
          "entry_ID":"1ee756c1-274b-4d90-a8b2-84aa5a584c9e"
       },
       {
          "timestamp":"2:27 AM",
          "date":"6/23/2017",
          "counter":21,
          "word":"Synchronised",
          "chunk_ID":"1ee756c1-274b-4d90-a8b2-84aa5a584c9e",
          "entry_ID":"1ee756c1-274b-4d90-a8b2-84aa5a584c9e"
       }
    ]
    ```

### UI
- UI Team asks MGMT for servers map periodically. 
