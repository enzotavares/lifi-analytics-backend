from data.constants import chain_asset_data
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd

query = gql(
    """
query fetchRouters($batch: Int!) {
  routers(first:100, skip: $batch) {
    id
    assetBalances {
      id
      amount
    }
  }
}
"""
)

params = {"batch": 0}


def fetch_routers(query, params, transport, dataframe, chain):
    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    per_batch = 100
    # Execute single query
    for batch in range(42):  # Just a random no. It has to be just > 6.
        result = client.execute(query, variable_values=params)
        for router in result["routers"]:
            for asset in router["assetBalances"]:

                asset_id = asset["id"].split("-")[0]
                token = chain_asset_data[chain][asset_id]["token"]
                decimals = chain_asset_data[chain][asset_id]["decimals"]
                amount = asset["amount"]
                tvl = int(amount) / 10 ** decimals

                list_values = []
                list_values.append(router["id"])
                list_values.append(chain)
                list_values.append(asset_id)
                list_values.append(token)
                list_values.append(amount)
                list_values.append(decimals)
                list_values.append(tvl)
                dataframe.loc[len(dataframe.index)] = list_values
        if len(result["routers"]) < per_batch:
            break
        params["batch"] += per_batch
    params["batch"] = 0


def get_nxtp_tvl():

    transport_matic = RequestsHTTPTransport(
        url="https://api.thegraph.com/subgraphs/name/connext/nxtp-matic"
    )
    transport_bsc = RequestsHTTPTransport(
        url="https://api.thegraph.com/subgraphs/name/connext/nxtp-bsc"
    )
    transport_xdai = RequestsHTTPTransport(
        url="https://api.thegraph.com/subgraphs/name/connext/nxtp-xdai"
    )
    transport_fantom = RequestsHTTPTransport(
        url="https://api.thegraph.com/subgraphs/name/connext/nxtp-fantom"
    )
    transport_arbitrum = RequestsHTTPTransport(
        url="https://api.thegraph.com/subgraphs/name/connext/nxtp-arbitrum-one"
    )
    transport_avalanche = RequestsHTTPTransport(
        url="https://api.thegraph.com/subgraphs/name/connext/nxtp-avalanche"
    )

    router_columns = [
        "router_id",
        "chain",
        "asset_id",
        "token",
        "amount",
        "decimals",
        "tvl",
    ]

    matic_routers = pd.DataFrame(columns=router_columns)
    bsc_routers = pd.DataFrame(columns=router_columns)
    xdai_routers = pd.DataFrame(columns=router_columns)
    fantom_routers = pd.DataFrame(columns=router_columns)
    arbitrum_routers = pd.DataFrame(columns=router_columns)
    avalanche_routers = pd.DataFrame(columns=router_columns)

    fetch_routers(query, params, transport_matic, matic_routers, "Polygon")
    fetch_routers(query, params, transport_bsc, bsc_routers, "BSC")
    fetch_routers(query, params, transport_xdai, xdai_routers, "xDai")
    fetch_routers(query, params, transport_fantom, fantom_routers, "Fantom")
    fetch_routers(query, params, transport_arbitrum, arbitrum_routers, "Arbitrum")
    fetch_routers(query, params, transport_avalanche, avalanche_routers, "Avalanche")

    nxtp_df = pd.concat(
        [
            matic_routers,
            bsc_routers,
            xdai_routers,
            fantom_routers,
            arbitrum_routers,
            avalanche_routers,
        ]
    )

    nxtp_tvl = nxtp_df.groupby(["chain", "token"]).sum("tvl")

    nxtp_tvl.reset_index(inplace=True)

    nxtp_tvl.chain = nxtp_tvl.chain.apply(lambda x: x.lower())
    nxtp_tvl.drop(nxtp_tvl[nxtp_tvl.token == "FAKE"].index, axis=0, inplace=True)

    return nxtp_tvl
