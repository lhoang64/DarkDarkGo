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

## **`api` server**
The api server is made up of `routes` and `controller`. There are only **two** routes, as described below.

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
- **Sample Call**:
```Javascript
fetch('http://0.0.0.0:8010/search?q=sample%20call')
.then((response) => response.json())
.then((responsejson) => this.parseResult(responsejson))
.catch((error) => console.error(error));
```


### **Health reporting**
The management uses this endpoint to check on the webserver's health.
- **URL**: `/get_health?q=`
- **Method**: `GET`
- **URL Params**: None
- **Success Response**: 
```
Code: 200
{
    status: 'healthy',
}
````

- **Sample Call**:
```Javascript
fetch('http://0.0.0.0:8010/get_health')
.then((response) => response.json())
.then((responsejson) => console.log(responsejson.status))
.catch((error) => console.error(error));
```
## **Caching service** ##
A LRU cache is used to serve the most frequently queried contents on this server without overloading the index server. Cache items are stored as key-value pairs and the lookup time is `O(1)`, which is far more superior than if the query were to make double trips to the index server.

**Cache configuration**
- `maxage`: 10 days
- `maxlength`: 10000 items

**Sample cache item**

*Index:* 

>k : Query

>v : Docids for the query 
```JSON
{
    "k": "a righteous man",
    "v": ['123-abc', '801-pqb', 234-cde', '389-zxi'] 
}
```
<!-- 
## Manager ##
- Instantiates 
- Health reporting to 
- /get_health

## Aggregating service ##


## Dependencies ## -->