from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import RequestsHTTPTransport
from data.constants import (
    txn_columns,
    txns_params,
    txns_query,
    chain_asset_data,
    chain_mapping,
)
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pickle

transport_matic = RequestsHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpmatic"
)
transport_bsc = RequestsHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpbsc"
)
transport_xdai = RequestsHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpxdai"
)
transport_fantom = RequestsHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtpfantom"
)
transport_arbitrum = RequestsHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/0xakshay/nxtparbitrum"
)


def concat_dfs(main_df, new_df):
    new_df.drop_duplicates(inplace=True)
    result = pd.concat([main_df, new_df])
    result.drop_duplicates(inplace=True)
    result.reset_index(inplace=True, drop=True)
    return result


def fetch_chain_transactions(query, params, transport, chain, prep_cut_off):

    dataframe = pd.DataFrame(columns=txn_columns)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    params["preparedTime"] = prep_cut_off
    while True:  # Just a random no.
        result = client.execute(query, params)

        for tr in result["transactions"]:
            list_values = list(tr.values())
            list_values[12] = list_values[12]["id"]
            dataframe.loc[len(dataframe.index)] = list_values
        if len(result["transactions"]) == 0:
            break
        params["preparedTime"] = result["transactions"][-1]["preparedTimestamp"]
        if len(result["transactions"]) < 1000:
            break
    print(dataframe.shape[0], end="-")
    print("Fetched from", chain)
    return dataframe


def transacting_chains(row):
    val = (
        chain_mapping[row["sendingChainId"]]
        + " -> "
        + chain_mapping[row["receivingChainId"]]
    )
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
    dollar_value = int(row["amount"]) / 10 ** row["decimals"]
    return dollar_value


def time_taken(row):
    time_taken = row["time_fulfilled_y"] - row["time_prepared_x"]
    return time_taken


def fetch_txns_df(prep_cut_off):
    matic_txns = pd.DataFrame(columns=txn_columns)
    bsc_txns = pd.DataFrame(columns=txn_columns)
    xdai_txns = pd.DataFrame(columns=txn_columns)
    fantom_txns = pd.DataFrame(columns=txn_columns)
    arbitrum_txns = pd.DataFrame(columns=txn_columns)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_matic, "Polygon", prep_cut_off
    )
    matic_txns = concat_dfs(matic_txns, new_df)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_bsc, "BSC", prep_cut_off
    )
    bsc_txns = concat_dfs(bsc_txns, new_df)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_xdai, "xDai", prep_cut_off
    )
    xdai_txns = concat_dfs(xdai_txns, new_df)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_fantom, "Fantom", prep_cut_off
    )
    fantom_txns = concat_dfs(fantom_txns, new_df)

    new_df = fetch_chain_transactions(
        txns_query, txns_params, transport_arbitrum, "Arbitrum", prep_cut_off
    )
    arbitrum_txns = concat_dfs(arbitrum_txns, new_df)

    matic_txns["chain"] = "Polygon"
    bsc_txns["chain"] = "BSC"
    xdai_txns["chain"] = "xDai"
    fantom_txns["chain"] = "Fantom"
    arbitrum_txns["chain"] = "Arbitrum"

    two_sided_txns = pd.concat(
        [matic_txns, bsc_txns, xdai_txns, fantom_txns, arbitrum_txns]
    )
    if two_sided_txns.shape[0] == 0:
        print("No new rows to add")
        return two_sided_txns
    two_sided_txns["txn_type"] = two_sided_txns.apply(
        lambda x: "single" if x["sendingChainId"] == x["chainId"] else "repeat", axis=1
    )

    two_sided_txns["asset_movement"] = two_sided_txns.apply(transacting_chains, axis=1)

    two_sided_txns["asset_token"] = two_sided_txns.apply(asset_token_mapper, axis=1)
    two_sided_txns["decimals"] = two_sided_txns.apply(asset_decimal_mapper, axis=1)

    two_sided_txns["dollar_amount"] = two_sided_txns.apply(dollar_amount, axis=1)
    two_sided_txns = two_sided_txns.drop(
        two_sided_txns[two_sided_txns.asset_token == "FAKE"].index, axis=0
    )

    two_sided_txns["time_prepared"] = two_sided_txns["preparedTimestamp"].apply(
        lambda x: pd.to_datetime(x, unit="s")
    )

    two_sided_txns["time_fulfilled"] = two_sided_txns["fulfillTimestamp"].apply(
        lambda x: pd.to_datetime(x, unit="s")
    )

    print(two_sided_txns.shape)
    compact_data_txns = two_sided_txns.drop(
        ["receivingChainId", "chainId", "sendingChainId"], axis=1
    )
    compact_data_txns.replace({np.NaN: None}, inplace=True)
    # load database

    return compact_data_txns


def fetch_txns_df_test(prep_cut_off):
    with open("two_sided_txns.pickle", "rb") as handle:
        compact_data_txns = pickle.load(handle)
    compact_data_txns.replace({np.NaN: None}, inplace=True)
    return compact_data_txns
