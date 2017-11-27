# MGMT

## Our APIs

### Crawlers

**Pull a link from the top of the queue.**
- URL: `/get_link`
- Method: `GET`
- Sample data
    ```
    {"link":"http://goo.ne.jp/massa.xml"}
    ```

**Pull n links from the queue.**
- URL: `/get_links?n`
- Method: `GET`
- Sample data:
    ```
    [  
       {  
          "link":"https://vinaora.com/at/vulputate/vitae/nisl/aenean/lectus/pellentesque.js"
       },
       {  
          "link":"https://google.fr/massa.js"
       },
       {  
          "link":"http://bing.com/nec/sem.js"
       }
    ]
    ```
    
**Add a link to the queue.**
- URL: `/add_link`
- Method: `POST`
- Sample data
    ```
    {"link":"http://goo.ne.jp/massa.xml"}
    ```
    
**Add some number of links to the queue.**
- URL: `add_links`
- Method: `POST`
- Sample data:
    ```
    [  
       {  
          "link":"https://vinaora.com/at/vulputate/vitae/nisl/aenean/lectus/pellentesque.js"
       },
       {  
          "link":"https://google.fr/massa.js"
       },
       {  
          "link":"http://bing.com/nec/sem.js"
       }
    ]
    ```

**Mark a link as already scraped.**
- URL: `/add_crawled_link`
- Method: `POST`
- Sample data:
    ```
    {"link":"http://goo.ne.jp/massa.xml"}
    ```

**Add content chunk metadata.**
- URL: `/add_chunk_metadata`
- Method: `POST`
- Sample data:
    ```
    [
       {
          "title":"Nightmare City (a.k.a. City of the Walking Dead) (a.k.a. Invasión de los zombies atómicos, La) (Incubo sulla città contaminata)",
          "link":"https://msu.edu/ut/at/dolor/quis/odio.png",
          "description":"Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo."
       },
       {
          "title":"Kidnapped",
          "link":"http://redcross.org/congue/vivamus/metus/arcu.json",
          "description":"Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat. Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus."
       },
       {
          "title":"When in Rome",
          "link":"https://joomla.org/luctus/et/ultrices.html",
          "description":"Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum."
       }
    ]
    ```

### Indexers
**Add content chunk stats.**
- URL: `/add_content_chunk_stats`
- Method: `POST`
- Sample data:
    ```
    [
       {
          "chunk_ID":"bd6146c0-315f-4f67-89ad-1576dc13b701",
          "IP":"63.161.242.61",
          "port":9000,
          "state":"building"
       },
       {
          "chunk_ID":"a043738c-3458-416d-99ad-99ea1b318468",
          "IP":"99.128.93.49",
          "state":"building"
       },
       {
          "chunk_ID":"a7e738b4-a134-4144-9cf9-0b02400d5bd4",
          "IP":"138.76.103.233",
          "state":"building"
       }
    ]
    ```

**Add index chunk metadata.**
- URL: `/add_index_chunk`
- Method: `POST`
- Sample data:
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
n
**Send stats related to query. Used by index query servers.**
- URL: `/add_query_stats`
- Method: `POST`
- Sample data:
    ```
    [
       {
          "timestamp":"12:56 AM",
          "date":"2/6/2017",
          "time":35,
          "counter":48,
          "index":86
       },
       {
          "timestamp":"3:21 PM",
          "date":"11/14/2017",
          "time":18,
          "counter":23,
          "index":37
       },
       {
          "timestamp":"2:27 AM",
          "date":"6/23/2017",
          "time":93,
          "counter":21,
          "index":1
       }
    ]
    ```

### UI
**Pull map of index servers.**
- URL: `/get_servers_map`
- Method: `GET`
- Sample data:
    ```
    [
       {
          "row_number":1,
          "hosts":{
             "IP":[
                "79.54.92.235",
                "51.1.38.174",
                "13.134.94.217"
             ],
             "port":[
                1248,
                3842,
                302
             ]
          }
       },
       {
          "row_number":2,
          "hosts":{
             "IP":[
                "253.94.42.30",
                "194.21.48.83",
                "165.69.123.81"
             ],
             "port":[
                241,
                4800,
                3078
             ]
          }
       },
       {
          "row_number":3,
          "hosts":{
             "IP":[
                "185.166.126.242",
                "102.199.242.146",
                "245.86.27.171"
             ],
             "port":[
                2636,
                3051,
                919
             ]
          }
       }
    ]
    ```

## Other components' APIs
What we need from other components are:

**Health status: healthy, failure, recovery, probation.**
- URL: `/health_status`
- Sample data:
    ```
    {"status":"healthy"}
    ```
