# Documentation for the web server #

## Introduction
The webserver runs on port 8010 and act as a middleware between the React frontend and the index server. 

## Features:
- Nginx reverse proxies all requests on port 8010 to multiple node instances load balanced by pm2
- Easy to scale vertically, the number of node instances dynamically changes with CPU capacity
- Zero downtime server restart
- Remote health monitoring on global dashboard via [keymetrics.io]() 
- LRU caching to make sure index server is not flooded with requests
---
The API server is comprised of **four** different components.

## `api` server
The api server is made up of `routes` and `controller`. There are **three** routes, as described below.

### **Search**
The frontend uses this endpoint to make any queries.
- **URL**: `/search?q=`
- **Method**: `GET`
- **Query Params**: `q=[string]` *(optional)*
- **Success Response**: 
```
Code: 200
{
    head: 'success',
    message: []
}
````
- **Error Response**:
```
Code: 200
{
    head: 'error',
    message: []
}
```

The frontend uses this route to get search results for any query. 
- **Sample Call**:
```Javascript
fetch('http://0.0.0.0:8010/search?q=sample%20call')
.then((response) => response.json())
.then((responsejson) => this.parseResult(responsejson))
.catch((error) => console.error(error));
```

## Caching service ##


## Manager ##
- Instantiates 
- Health reporting to 
- /get_health

## Aggregating service ##