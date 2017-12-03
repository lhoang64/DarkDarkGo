# MGMT Database

## SQL Schema

```
link
    ---------------------------
   | link        | state       |
   | VARCHAR(22) | VARCHAR(22) |
   | PRIMARY     |             |
    ---------------------------
   | stuff1.com  | OK          |
   | stuff2.com  | OK          | 
   | stuff3.com  | OK          | 
   | stuff4.com  | OK          |
   | stuff5.com  | OK          |  
   | stuff6.com  | Error       | 
    ---------------------------

chunk
    ------------------
   | id       | state |
   | INT      |       |
   | PRIMARY  |       |
    -------------------
   | 1        | OK    |
   | 2        | OK    | 
   | 3        | OK    | 
   | 4        | OK    | 
   | 5        | Error | 
    ------------------
   
host
    ----------------------------------------------------------------
   | host               | type           | state      | health      |
   | VARCHAR(22)        | VARCHAR(22)    | VARCHAR(22)| VARCHAR(22) |   
   | PRIMARY            |                |            |             |   
    ----------------------------------------------------------------
   | 10.10.127.100:5000 | Crawler        | waiting   | healthy      |
   | 10.10.127.101:5000 | Index Builider | offline   | failure      |
   | 10.10.127.102:5000 | Index Server   | online    | healthy      |
    ----------------------------------------------------------------

crawler
    ---------------------------------------------
   | chunk_id | C_host             | C_task      |
   | INT      | VARCHAR(22)        | VARCHAR(22) |
   | REF      | REF                |             | 
    ---------------------------------------------
   | 100      | 10.10.127.100:5000 | crawling    |
   | 101      | 10.10.127.100:5000 | crawled     | 
   | 102      | 10.10.127.100:5000 | propagated  | 
    ---------------------------------------------

index_builder
    ---------------------------------------------
   | chunk_id | IB_host            | IB_task     | 
   | INT      | VARCHAR(22)        | VARCHAR(22) | 
   | REF      | REF                |             |
    ---------------------------------------------
   | 100      | 10.10.127.101:5000 | building    |
   | 101      | 10.10.127.101:5000 | built       |
   | 102      | 10.10.127.101:5000 | propagated  |
    ---------------------------------------------

index_server
    ---------------------------------------
   | row   | chunk_id | IS_host            | 
   | INT   | INT      | VARCHAR(22)        | 
   |       | REF      | REF                |
    ---------------------------------------
   | 1     | 100      | 10.10.127.102:5000 |
   | 1     | 101      | 10.10.127.102:5000 |
   | 1     | 102      | 10.10.127.102:5000 |
    ---------------------------------------
```

### How to install on Mac:
- Install [Posgres.app](https://postgresapp.com)
- `sudo -u <username> createdb -O <username> mgmt_db`
- `./import.sh`

### Test command:
- `SELECT h.type, c.* FROM host h, crawler c WHERE h.host = c.c_host;`
- `SELECT h.type, i.* FROM host h, index_builder i WHERE h.host = i.ib_host;`
- `SELECT h.type, i.* FROM host h, index_server i WHERE h.host = i.is_host;`