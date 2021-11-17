from gql import Client, gql


txn_columns = [
    "amount",
    "chainId",
    "expiry",
    "fulfillTimestamp",
    "id",
    "preparedBlockNumber",
    "preparedTimestamp",
    "receivingAssetId",
    "receivingChainId",
    "sendingAssetId",
    "sendingChainId",
    "status",
    "user",
]

# Provide a GraphQL query
txns_query = gql(
    """
query fetchAllTransactions($preparedTime: BigInt!) {
  transactions (
    first:1000, 
    where: { preparedTimestamp_gt: $preparedTime },
    orderBy: preparedTimestamp
    orderDirection: asc
  ){
    id
    status
    chainId
    user {
      id
    }
    sendingAssetId
    receivingAssetId
    sendingChainId
    receivingChainId
    amount
    expiry
    preparedBlockNumber
    preparedTimestamp
    fulfillTimestamp
  }
}
"""
)

txns_params = {"preparedTime": "1632355200"}

chain_mapping = {
    "1": "Ethereum",
    "4": "Rinkeby",
    "5": "Goerli",
    "10": "Optimism",
    "28": "OMGX-Rinkeby",
    "40": "Telos",
    "56": "BSC",
    "66": "OKExChain",
    "69": "Optimism-Kovan",
    "97": "BSC",
    "100": "xDAI",
    "128": "Huobi",
    "137": "Polygon",
    "250": "Fantom",
    "256": "HT",
    "321": "KCC",
    "336": "Shiden Network",
    "1285": "Moonriver",
    "4689": "IoTeX",
    "32659": "Fusion",
    "42161": "Arbitrum",
    "42220": "Celo",
    "43114": "Avalanche",
    "421611": "Arbitrum-Rinkeby",
    "1666600000": "Harmony",
    "BTC": "Bitcoin",
    "LTC": "Litecoin",
    "BLOCK": "Blocknet",
    "COLX": "ColossusXT",
}
chain_case_mapping = {
    "bsc": "BSC",
    "polygon": "Polygon",
    "fantom": "Fantom",
    "xdai": "xDai",
    "arbitrum": "Arbitrum",
    "avalanche": "Avalanche",
    "all": "all",
}


chain_asset_data = {
    "Ethereum": {
        "0x0000000000000000000000000000000000000000": {"token": "ETH", "decimals": 18},
        "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0": {
            "token": "MATIC",
            "decimals": 18,
        },
        "0xb8c77482e45f1f44de1745f52c74426c631bdd52": {"token": "BNB", "decimals": 18},
        "0x6b175474e89094c44da98b954eedeac495271d0f": {"token": "DAI", "decimals": 18},
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": {"token": "USDC", "decimals": 6},
        "0xdac17f958d2ee523a2206206994597c13d831ec7": {"token": "USDT", "decimals": 6},
    },
    "BSC": {
        "0x2170ed0880ac9a755fd29b2688956bd959f933f8": {"token": "ETH", "decimals": 18},
        "0xcc42724c6683b7e57334c4e856f4c9965ed682bd": {
            "token": "MATIC",
            "decimals": 18,
        },
        "0x0000000000000000000000000000000000000000": {"token": "BNB", "decimals": 18},
        "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3": {"token": "DAI", "decimals": 18},
        "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d": {"token": "USDC", "decimals": 18},
        "0x55d398326f99059ff775485246999027b3197955": {"token": "USDT", "decimals": 18},
        "0xd9a54933b000d2c2eac81e8db7b294db16a73bfe": {"token": "FAKE", "decimals": 18},
        "0xabc6790673a60b8a7f588450f59d2d256b1aef7f": {"token": "OMN", "decimals": 18},
    },
    "Polygon": {
        "0xfd8ee443ab7be5b1522a1c020c097cff1ddc1209": {"token": "ETH", "decimals": 18},
        "0x0000000000000000000000000000000000000000": {
            "token": "MATIC",
            "decimals": 18,
        },
        "0xa649325aa7c5093d12d6f98eb4378deae68ce23f": {"token": "BNB", "decimals": 18},
        "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063": {"token": "DAI", "decimals": 18},
        "0x2791bca1f2de4661ed88a30c99a7a9449aa84174": {"token": "USDC", "decimals": 6},
        "0xc2132d05d31c914a87c6611c10748aeb04b58e8f": {"token": "USDT", "decimals": 6},
        "0xb32786dc23a6511f88cba528c1e5175c182091b9": {"token": "FAKE", "decimals": 18},
        "0xabc6790673a60b8a7f588450f59d2d256b1aef7f": {"token": "OAI", "decimals": 18},
    },
    "xDai": {
        "0xa5c7cb68cd81640d40c85b2e5ec9e4bb55be0214": {"token": "ETH", "decimals": 18},
        "0x7122d7661c4564b7c6cd4878b06766489a6028a2": {
            "token": "MATIC",
            "decimals": 18,
        },
        "0xca8d20f3e0144a72c6b5d576e9bd3fd8557e2b04": {"token": "BNB", "decimals": 18},
        "0x0000000000000000000000000000000000000000": {"token": "DAI", "decimals": 18},
        "0xddafbb505ad214d7b80b1f830fccc89b60fb7a83": {"token": "USDC", "decimals": 6},
        "0x4ecaba5870353805a9f068101a40e0f32ed605c6": {"token": "USDT", "decimals": 6},
    },
    "Fantom": {
        "0x658b0c7613e890ee50b8c4bc6a3f41ef411208ad": {"token": "ETH", "decimals": 18},
        "0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e": {"token": "DAI", "decimals": 18},
        "0x04068da6c83afcfa0e13ba15a6696662335d5b75": {"token": "USDC", "decimals": 6},
        "0x049d68029688eabf473097a2fc38ef61633a3c7a": {"token": "USDT", "decimals": 6},
    },
    "Arbitrum": {
        "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8": {"token": "USDC", "decimals": 6},
        "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9": {"token": "USDT", "decimals": 6},
        "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1": {"token": "DAI", "decimals": 18},
    },
    "Avalanche": {
        "0xa7d7079b0fead91f3e65f86e8915cb59c1a4c664": {"token": "USDC", "decimals": 6},
        "0xc7198437980c041c805a1edcba50c1ce5db95118": {"token": "USDT", "decimals": 6},
        "0xd586e7f844cea2f87f50152665bcbc2c279d8d70": {"token": "DAI", "decimals": 18},
    },
}
