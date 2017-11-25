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
**Pull content chunk metadata.**
- URL: `/get_content_chunk`
- Method: `GET`
- Sample data:
    ```
    [
       {
          "ID":"bd6146c0-315f-4f67-89ad-1576dc13b701",
          "IP":"63.161.242.61",
          "port":9000
       },
       {
          "ID":"a043738c-3458-416d-99ad-99ea1b318468",
          "IP":"99.128.93.49",
          "port":9001
       },
       {
          "ID":"a7e738b4-a134-4144-9cf9-0b02400d5bd4",
          "IP":"138.76.103.233",
          "port":9002
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
          "word":"global",
          "chunk_ID":"40ddb9f5-f387-4aed-a37b-b53c2f109040",
          "entry_ID":[
             "2d9b4f7d-d7f8-4fef-ae47-2d9dc56b5bd4",
             "03ad7b8b-1a88-42f1-b42e-90e1c0321773",
             "ee91d4dc-d294-4191-8fbf-c8a2c2d18dbd"
          ]
       },
       {
          "word":"Polarised",
          "chunk_ID":"c40acae9-ac18-43da-8e5e-60e50e7b507c",
          "entry_ID":[
             "207e7883-c842-43fe-8675-0f6e11608572",
             "ca43a5fa-e697-43bd-b84f-63aa4cd9292a",
             "d71d76fb-e6ec-46f5-a53b-d51f8500f02b"
          ]
       },
       {
          "word":"explicit",
          "chunk_ID":"d2e5bb51-6bf8-4f7b-b341-8dc90e85d43e",
          "entry_ID":[
             "7d0c7a96-19d2-46c2-8b61-1cf23c5dbb8d",
             "341028f2-d09b-434e-9625-6fd0ce930930",
             "ac3e9c36-ffab-4e25-b0f5-49377badd4d2"
          ]
       }
    ]
    ```

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
