# MGMT Database

## SQL Schema Example

```

chunk
    ---------------------------
   | index  | id       | state |
   | SERIAL | INT      |       |
   |        | PRIMARY  |       |
    ---------------------------
   | 1      | 1        | OK    |
   | 2      | 2        | OK    | 
   | 3      | 3        | OK    | 
   | 4      | 4        | OK    | 
   | 5      | 5        | Error | 
    ---------------------------

link
    --------------------------------------------------
   | index  | link        | chunk_id    | state       |
   | SERIAL | VARCHAR(22) | VARCHAR(22) | VARCHAR(22) |
   |        | PRIMARY     | REF         |
    --------------------------------------------------
   | 1      | stuff1.com  | 1           | OK          |
   | 2      | stuff2.com  | 1           | OK          | 
   | 3      | stuff3.com  | 1           | OK          | 
   | 4      | stuff4.com  | 1           | OK          |
   | 5      | stuff5.com  | 1           | OK          |  
   | 6      | stuff6.com  | 2           | Error       | 
    --------------------------------------------------

   
host
    -------------------------------------------------------------------------
   | index  | host               | type           | state      | health      |
   | SERIAL | VARCHAR(22)        | VARCHAR(22)    | VARCHAR(22)| VARCHAR(22) |   
   |        | PRIMARY            |                |            |             |   
    -------------------------------------------------------------------------
   | 1      | 10.10.127.100:5000 | Crawler        | waiting   | healthy      |
   | 2      | 10.10.127.101:5000 | Index Builider | offline   | failure      |
   | 3      | 10.10.127.102:5000 | Index Server   | online    | healthy      |
    -------------------------------------------------------------------------

crawler
    ------------------------------------------------------
   | index  | chunk_id | C_host             | C_task      |
   | SERIAL | INT      | VARCHAR(22)        | VARCHAR(22) |
   |        | REF      | REF                |             | 
    ------------------------------------------------------
   | 1      | 100      | 10.10.127.100:5000 | crawling    |
   | 2      | 101      | 10.10.127.100:5000 | crawled     | 
   | 3      | 102      | 10.10.127.100:5000 | propagated  | 
    ------------------------------------------------------

index_builder
    ------------------------------------------------------
   | index  | chunk_id | IB_host            | IB_task     | 
   | SERIAL | INT      | VARCHAR(22)        | VARCHAR(22) | 
   |        | REF      | REF                |             |
    ------------------------------------------------------
   | 1      | 100      | 10.10.127.101:5000 | building    |
   | 2      | 101      | 10.10.127.101:5000 | built       |
   | 3      | 102      | 10.10.127.101:5000 | propagated  |
    ------------------------------------------------------

index_server
    ------------------------------------------------
   | Index  | row   | chunk_id | IS_host            | 
   | SERIAL | INT   | INT      | VARCHAR(22)        | 
   |        |       | REF      | REF                |
    ------------------------------------------------
   | 1      | 1     | 100      | 10.10.127.102:5000 |
   | 2      | 2     | 101      | 10.10.127.102:5000 |
   | 3      | 3     | 102      | 10.10.127.102:5000 |
    ------------------------------------------------
```

### How to install on Mac:
- Install [Posgres.app](https://postgresapp.com)
- `sudo -u <username> createdb -O <username> mgmt_db`
- `./import.sh`