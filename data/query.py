from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from data.constants import txn_columns, txns_params, txns_query, last_blocs, chain_asset_data, chain_mapping
import requests
import pickle
import pandas as pd
from datetime import datetime,timedelta

transport_matic = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpmatic")
transport_bsc = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpbsc")
transport_xdai = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpxdai")
transport_fantom = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpfantom")
transport_arbitrum = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtparbitrum")

def merge_dfs(main_df, new_df):
    new_df.drop_duplicates(inplace=True)
    result = pd.concat([main_df, new_df])
    result.drop_duplicates(inplace=True)
    result.reset_index(inplace=True, drop=True)
    return result


def fetch_chain_transactions(query, params, transport, chain):

    dataframe = pd.DataFrame(columns=txn_columns)
    
    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    params["lastBloc"] = last_blocs[chain]
    for batch in range(6420): #Just a random no.
        result = client.execute(query, params)

        for tr in result["transactions"]:
            list_values = list(tr.values())
            list_values[20] = list_values[20]["id"]
            list_values[26] = list_values[26]["id"]
            dataframe.loc[len(dataframe.index)] = list_values
        if len(result["transactions"]) == 0:
            break
        params['lastBloc'] = result["transactions"][-1]["preparedBlockNumber"]
        if len(result["transactions"]) < 1000:
            break
    print(dataframe.shape[0], end="-")
    print("Fetched from", chain)
    last_blocs[chain] = params["lastBloc"]
    return dataframe
    

def transacting_chains(row):
    val = chain_mapping[row["sendingChainId"]] + " -> " + chain_mapping[row["receivingChainId"]]
    return val

def asset_token_mapper(row):
    chain_asset_dict = chain_asset_data[row["chain"]]
    if row["txn_type"] == "repeat":
        asset = chain_asset_dict[row["receivingAssetId"]]
    else:
        asset = chain_asset_dict[row["sendingAssetId"]]
    return asset["token"]

def asset_decimal_mapper(row):
    chain_asset_dict = chain_asset_data[row["chain"]]
    if row["txn_type"] == "repeat":
        asset = chain_asset_dict[row["receivingAssetId"]]
    else:
        asset = chain_asset_dict[row["sendingAssetId"]]
    return asset["decimals"]
def dollar_amount(row):
    dollar_value = int(row["amount"]) / 10**row["decimals"]
    return dollar_value

def time_taken(row):
    time_taken = row["time_fulfilled_y"] - row["time_prepared_x"]
    return time_taken
def update_database():
    matic_txns = pd.DataFrame(columns=txn_columns)
    bsc_txns = pd.DataFrame(columns=txn_columns)
    xdai_txns = pd.DataFrame(columns=txn_columns)
    fantom_txns = pd.DataFrame(columns=txn_columns)
    arbitrum_txns = pd.DataFrame(columns=txn_columns)

    # new_df = fetch_chain_transactions(txns_query, txns_params, transport_matic, "Polygon")
    # matic_txns = merge_dfs(matic_txns, new_df)

    # new_df = fetch_chain_transactions(txns_query, txns_params, transport_bsc, "BSC")
    # bsc_txns = merge_dfs(bsc_txns, new_df)

    # new_df = fetch_chain_transactions(txns_query, txns_params, transport_xdai, "xDai")
    # xdai_txns = merge_dfs(xdai_txns, new_df)

    # new_df = fetch_chain_transactions(txns_query, txns_params, transport_fantom, "Fantom")
    # fantom_txns = merge_dfs(fantom_txns, new_df)

    # new_df = fetch_chain_transactions(txns_query, txns_params, transport_arbitrum, "Arbitrum")
    # arbitrum_txns = merge_dfs(arbitrum_txns, new_df)

    matic_txns["chain"] = "Polygon"
    bsc_txns["chain"] = "BSC"
    xdai_txns["chain"] = "xDai"
    fantom_txns["chain"] = "Fantom"
    arbitrum_txns["chain"] = "Arbitrum"


    two_sided_txns = pd.concat([matic_txns,bsc_txns,xdai_txns,fantom_txns,arbitrum_txns])

    #load database
    with open('two_sided_txns.pickle', 'rb') as handle:
        two_sided_txns = pickle.load(handle)

    print(two_sided_txns.shape)
    if two_sided_txns.shape[0] == 0:
        print("No new rows to add")
        return two_sided_txns
    two_sided_txns["txn_type"] = two_sided_txns.apply(lambda x: "single" if x["sendingChainId"] == x["chainId"] else "repeat", axis=1)


    two_sided_txns['asset_movement'] = two_sided_txns.apply(transacting_chains, axis=1)

    two_sided_txns["asset_token"] = two_sided_txns.apply(asset_token_mapper, axis=1)
    two_sided_txns["decimals"] = two_sided_txns.apply(asset_decimal_mapper, axis=1)

    two_sided_txns["dollar_amount"] = two_sided_txns.apply(dollar_amount, axis=1)
    
    
    two_sided_txns["time_prepared"] = two_sided_txns["preparedTimestamp"].apply(lambda x: pd.to_datetime(x,unit="s"))

    two_sided_txns["time_fulfilled"] = two_sided_txns["fulfillTimestamp"].apply(lambda x: pd.to_datetime(x,unit="s"))

    print(two_sided_txns.shape)
    repeat_txns = two_sided_txns[two_sided_txns["txn_type"]=="repeat"].copy(deep=True)
    one_sided_txns = two_sided_txns[two_sided_txns["txn_type"]=="single"].copy(deep=True)
    repeat_txns.reset_index(drop=True,inplace=True)
    one_sided_txns.reset_index(drop=True,inplace=True)

    dem2_merge_cols = ["id", "bidSignature", "receivingAssetId", "callTo", "asset_token", "sendingChainFallback", "receivingChainTxManagerAddress", "transactionId", "user", "sendingAssetId", "receivingChainId", "receivingAddress", "router", "asset_movement", "sendingChainId", "callDataHash"]

    merged_txns = pd.merge(left=one_sided_txns, right=repeat_txns, how="outer", left_on=dem2_merge_cols, right_on=dem2_merge_cols)
    print("Merged", merged_txns.shape)
    merged_txns["time_taken"] = merged_txns.apply(time_taken, axis=1)
    merged_txns["time_taken_seconds"] = merged_txns["time_taken"].apply(lambda x: x.seconds)
    fulfilled_txns = merged_txns[(merged_txns.status_x == "Fulfilled") & (merged_txns.status_y == "Fulfilled")].copy(deep=True)
    print(fulfilled_txns.shape)

    return merged_txns