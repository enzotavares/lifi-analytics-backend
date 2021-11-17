from data.tvl_nxtp import get_nxtp_tvl
from data.constants import chain_mapping
import pandas as pd
import requests
import json

anyswap_bridges_url = "https://netapi.anyswap.net/bridge/v2/info"


def get_liquidity_anyswap():

    initial_url = anyswap_bridges_url
    response = requests.get(initial_url)

    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    return response.json()


def anyswap_chain_mapping(x):
    try:
        return chain_mapping[x]
    except KeyError as e:
        print("CAUGHT_ERROR: KeyError", e)


def get_anyswap_tvl():
    result = get_liquidity_anyswap()
    cols_anyswap = [
        "chainId",
        "srcChainId",
        "token",
        "srcToken",
        "symbol",
        "decimals",
        "name",
        "depositAddr",
        "isProxy",
        "DelegateToken",
        "price",
        "sortid",
        "logoUrl",
        "type",
        "underlying",
        "balance",
        "tvl",
    ]
    anyswap_df = pd.DataFrame(columns=cols_anyswap)

    def structure_anyswap_data(dataframe):
        for bridge in result["bridgeList"]:
            dataframe = dataframe.append(bridge, True)
        return dataframe

    anyswap_df = structure_anyswap_data(anyswap_df)
    anyswap_df.tvl = anyswap_df.tvl.replace("", 0.0)
    try:
        anyswap_df["chain"] = anyswap_df.chainId.apply(anyswap_chain_mapping)
    except KeyError as e:
        print("CAUGHT_ERROR: KeyError", e)
    anyswap_df.drop(
        anyswap_df[anyswap_df.chain == "Goerli"].index, axis=0, inplace=True
    )
    anyswap_tvl = anyswap_df[["chain", "symbol", "tvl"]].copy(deep=True)
    anyswap_tvl.rename({"symbol": "token"}, axis=1, inplace=True)
    anyswap_tvl.token = anyswap_tvl.token.str.replace("any", "")
    return anyswap_tvl


def get_liquidity_hop(chain):
    request_data = {
        "query": "\n    query Tvl {\n      tvls(\n        orderDirection: desc\n      ) {\n        id\n        amount\n        token\n      }\n    }\n  ",
        "variables": {},
    }
    initial_url = "https://api.thegraph.com/subgraphs/name/hop-protocol/hop-" + chain
    response = requests.post(initial_url, json.dumps(request_data))

    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    return response.json()


def get_hop_tvl():
    hop_df = pd.DataFrame(columns=["chain", "token", "amount", "decimals", "tvl"])

    for chain in ["optimism", "arbitrum", "xdai", "mainnet", "polygon"]:
        result = get_liquidity_hop(chain)
        if chain == "mainnet":
            chain = "ethereum"
        for tvl in result["data"]["tvls"]:
            amount = tvl["amount"]
            if len(amount) > 18:
                decimals = 18
            else:
                decimals = 6
            new_row = {
                "chain": chain,
                "amount": amount,
                "token": tvl["token"],
                "decimals": decimals,
                "tvl": int(amount) / 10 ** decimals,
            }
            hop_df = hop_df.append(new_row, True)

    hop_tvl = hop_df[["chain", "token", "tvl"]].copy(deep=True)
    return hop_tvl


def get_celer_tvl():
    celer_bridges_url = (
        "https://cbridge-stat.s3.us-west-2.amazonaws.com/mainnet/cbridge-stat.json"
    )
    initial_url = celer_bridges_url
    response = requests.get(initial_url)

    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )

    result = response.json()

    celer_tvl = pd.DataFrame(columns=["chain", "token", "tvl"])

    for chain in result["aggregateAvailableLiquidityDetail"]:
        for token in chain["liquidityDetail"]:
            entry = {
                "chain": chain_mapping[chain["chainId"]],
                "token": token["tokenSymbol"],
                "tvl": float(token["liquidity"].replace("$", "")),
            }
            celer_tvl = celer_tvl.append(entry, ignore_index=True)
    return celer_tvl


def get_combined_tvl():
    anyswap_tvl = get_anyswap_tvl()
    hop_tvl = get_hop_tvl()
    nxtp_tvl = get_nxtp_tvl()
    celer_tvl = get_celer_tvl()

    anyswap_tvl["bridge"] = "anyswap"
    hop_tvl["bridge"] = "hop"
    nxtp_tvl["bridge"] = "nxtp"
    celer_tvl["bridge"] = "celer"

    combined_tvl = pd.concat([anyswap_tvl, hop_tvl, nxtp_tvl, celer_tvl])

    combined_tvl.chain = combined_tvl.chain.apply(lambda x: x.lower())
    combined_duplicate_tokens = (
        combined_tvl.groupby(["token", "chain", "bridge"])
        .agg({"tvl": "sum"})
        .reset_index()
    )
    return combined_duplicate_tokens
