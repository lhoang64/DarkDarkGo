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
    
**Adds a link to the queue.**
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
          "port":58800
       },
       {
          "ID":"a043738c-3458-416d-99ad-99ea1b318468",
          "IP":"99.128.93.49",
          "port":41159
       },
       {
          "ID":"a7e738b4-a134-4144-9cf9-0b02400d5bd4",
          "IP":"138.76.103.233",
          "port":54670
       }
    ]
    ```

**Add index chunk metadata.**
- URL: `/add_index_chunk`
- Method: `POST`
- Sample data:

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
- URL: `/get_server_map`
- Method: `GET`
- Sample data:

## Other components' APIs
What wee need from other components are:

**Health status: healthy, failure, recovery, probation.**
- URL: `/health_status`
- Sample data:
    ```
    {"status":"healthy"}
    ```
