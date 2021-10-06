# API documentation of LiFi Data Backend

## Introduction
The API Endpoint is 
```
http://3.131.21.10/
```
All requests are GET requests appended to the above endpoint. 

# NXTP APIs
Note: All volume based data is in USD. 
## General Stats
Here you'll find 24 hour volume, 24hr txns, total volume, total txns and total unique users. 
GET request to 
```
http://3.131.21.10/general_stats
```
Click [here](http://3.131.21.10/general_stats) to check out the json. 


## Date wise volume distributed
Datewise volume data on NXTP 
GET request to 
```
http://3.131.21.10/date_volume
```
Click [here](http://3.131.21.10/date_volume) to check out the json. 

## Asset movement across chains
Volume movement of assets between different chains
GET request to 
```
http://3.131.21.10/asset_movement
```
Click [here](http://3.131.21.10/date_volume) to check out the json. 

# All Bridges data APIs
Note: All TVL/Liquidity is represented in USD. 

## Liquidity locked in various bridges
You'll find a theme of 3 main variables here. Chain, Token and TVL. 
GET request to 
```
http://3.131.21.10/bridges_tvl
```
Click [here](http://3.131.21.10/bridges_tvl) to check out the json. 
