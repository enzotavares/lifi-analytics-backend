from gql import Client, gql


last_blocs2 = {
    "Polygon" : "18421338",
    "BSC" : "10370113",
    "Fantom" : "15584609",
    "xDai" : "17774514",
    "Arbitrum" : "244433"
}

last_blocs = {'Polygon': '19412478',
 'BSC': '11159019',
 'Fantom': '17528234',
 'xDai': '18228753',
 'Arbitrum': '13274990'}

txn_columns = ['amount', 'bidSignature', 'callDataHash', 'callTo', 'cancelCaller', 'cancelTransactionHash', 'chainId', 'expiry', 'fulfillCaller', 'fulfillTimestamp', 'fulfillTransactionHash', 'id', 'prepareCaller', 'prepareTransactionHash', 'preparedBlockNumber', 'preparedTimestamp', 'receivingAddress', 'receivingAssetId', 'receivingChainId', 'receivingChainTxManagerAddress', 'router', 'sendingAssetId', 'sendingChainFallback', 'sendingChainId', 'status', 'transactionId', 'user']



# Provide a GraphQL query
txns_query = gql(
    """
query fetchAllTransactions($lastBloc: BigInt!) {
  transactions (
    first:1000, 
    where: { preparedBlockNumber_gt: $lastBloc },
    orderBy: preparedBlockNumber
    orderDirection: asc
  ){
    id
    status
    chainId
    preparedTimestamp
    user {
      id
    }
    router {
      id
    }
    receivingChainTxManagerAddress
    sendingAssetId
    receivingAssetId
    sendingChainFallback
    receivingAddress
    callTo
    sendingChainId
    receivingChainId
    callDataHash
    transactionId
    amount
    expiry
    preparedBlockNumber
    bidSignature
    prepareCaller
    fulfillCaller
    cancelCaller
    prepareTransactionHash
    fulfillTransactionHash
    fulfillTimestamp
    cancelTransactionHash
  }
}
"""
)

txns_params = {
        "lastBloc": 18421338
    }

chain_mapping = {"56": "BSC", "137": "Polygon", "250": "Fantom", "100": "xDai", "42161": "Arbitrum"}
chain_case_mapping = {"bsc": "BSC", "polygon": "Polygon", "fantom": "Fantom", "xdai": "xDai", "arbitrum": "Arbitrum"}

chain_asset_data = {
   "Ethereum":{
      "0x0000000000000000000000000000000000000000":{
         "token":"ETH",
         "decimals":18
      },
      "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0":{
         "token":"MATIC",
         "decimals":18
      },
      "0xb8c77482e45f1f44de1745f52c74426c631bdd52":{
         "token":"BNB",
         "decimals":18
      },
      "0x6b175474e89094c44da98b954eedeac495271d0f":{
         "token":"DAI",
         "decimals":18
      },
      "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48":{
         "token":"USDC",
         "decimals":6
      },
      "0xdac17f958d2ee523a2206206994597c13d831ec7":{
         "token":"USDT",
         "decimals":6
      }
   },
   "BSC":{
      "0x2170ed0880ac9a755fd29b2688956bd959f933f8":{
         "token":"ETH",
         "decimals":18
      },
      "0xcc42724c6683b7e57334c4e856f4c9965ed682bd":{
         "token":"MATIC",
         "decimals":18
      },
      "0x0000000000000000000000000000000000000000":{
         "token":"BNB",
         "decimals":18
      },
      "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3":{
         "token":"DAI",
         "decimals":18
      },
      "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d":{
         "token":"USDC",
         "decimals":18
      },
      "0x55d398326f99059ff775485246999027b3197955":{
         "token":"USDT",
         "decimals":18
      }
   },
   "Polygon":{
      "0xfd8ee443ab7be5b1522a1c020c097cff1ddc1209":{
         "token":"ETH",
         "decimals":18
      },
      "0x0000000000000000000000000000000000000000":{
         "token":"MATIC",
         "decimals":18
      },
      "0xa649325aa7c5093d12d6f98eb4378deae68ce23f":{
         "token":"BNB",
         "decimals":18
      },
      "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063":{
         "token":"DAI",
         "decimals":18
      },
      "0x2791bca1f2de4661ed88a30c99a7a9449aa84174":{
         "token":"USDC",
         "decimals":6
      },
      "0xc2132d05d31c914a87c6611c10748aeb04b58e8f":{
         "token":"USDT",
         "decimals":6
      }
   },
   "xDai":{
      "0xa5c7cb68cd81640d40c85b2e5ec9e4bb55be0214":{
         "token":"ETH",
         "decimals":18
      },
      "0x7122d7661c4564b7c6cd4878b06766489a6028a2":{
         "token":"MATIC",
         "decimals":18
      },
      "0xca8d20f3e0144a72c6b5d576e9bd3fd8557e2b04":{
         "token":"BNB",
         "decimals":18
      },
      "0x0000000000000000000000000000000000000000":{
         "token":"DAI",
         "decimals":18
      },
      "0xddafbb505ad214d7b80b1f830fccc89b60fb7a83":{
         "token":"USDC",
         "decimals":6
      },
      "0x4ecaba5870353805a9f068101a40e0f32ed605c6":{
         "token":"USDT",
         "decimals":6
      }
   },
   "Fantom":{
      "0x658b0c7613e890ee50b8c4bc6a3f41ef411208ad":{
         "token":"ETH",
         "decimals":18
      },
      "0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e":{
         "token":"DAI",
         "decimals":18
      },
      "0x04068da6c83afcfa0e13ba15a6696662335d5b75":{
         "token":"USDC",
         "decimals":6
      },
      "0x049d68029688eabf473097a2fc38ef61633a3c7a":{
         "token":"USDT",
         "decimals":6
      }
   },
   "Arbitrum":{
      "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8":{
         "token":"USDC",
         "decimals":6
      },
      "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9":{
         "token":"USDT",
         "decimals":6
      }
   }
}