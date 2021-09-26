from os import RTLD_NOW, cpu_count
from re import fullmatch
from flask import request, jsonify, redirect, render_template
from flask_migrate import init
from data.models import CopyTxns, Txns
from apis import db, app
from data.query import fetch_txns_df
from data.expiry_manager import update_cut_off
from data.constants import chain_case_mapping
import pandas as pd
import json
import click
from sqlalchemy import text

from . import blueprint

from apscheduler.schedulers.background import BackgroundScheduler

from flask_apscheduler import APScheduler

current_table = "og"
Table = Txns

scheduler = APScheduler()
expiry_cut_off = "1632695200"


def clear_table(Table):
    rows_deleted = db.session.query(Table).delete()
    db.session.commit()
    print(rows_deleted, "rows deleted from")
    # except:
    #     db.session.rollback()


def clear_table_with_expiry(Table):
    delete_q = Table.__table__.delete().where(Table.expiry_x > expiry_cut_off)
    rows_deleted = db.session.execute(delete_q)
    db.session.commit()
    # except:
    #     db.session.rollback()


def init_db(df):
    rows = []
    for index, row in df.iterrows():
        new_row = CopyTxns(
            amount_x=row["amount_x"],
            bidSignature=row["bidSignature"],
            callDataHash=row["callDataHash"],
            callTo=row["callTo"],
            cancelCaller_x=row["cancelCaller_x"],
            cancelTransactionHash_x=row["cancelTransactionHash_x"],
            chainId_x=row["chainId_x"],
            expiry_x=row["expiry_x"],
            fulfillCaller_x=row["fulfillCaller_x"],
            fulfillTimestamp_x=row["fulfillTimestamp_x"],
            fulfillTransactionHash_x=row["fulfillTransactionHash_x"],
            subgraphId=row["id"],
            prepareCaller_x=row["prepareCaller_x"],
            prepareTransactionHash_x=row["prepareTransactionHash_x"],
            preparedBlockNumber_x=row["preparedBlockNumber_x"],
            preparedTimestamp_x=row["preparedTimestamp_x"],
            receivingAddress=row["receivingAddress"],
            receivingAssetId=row["receivingAssetId"],
            receivingChainId=row["receivingChainId"],
            receivingChainTxManagerAddress=row["receivingChainTxManagerAddress"],
            router=row["router"],
            sendingAssetId=row["sendingAssetId"],
            sendingChainFallback=row["sendingChainFallback"],
            sendingChainId=row["sendingChainId"],
            status_x=row["status_x"],
            transactionId=row["transactionId"],
            user=row["user"],
            chain_x=row["chain_x"],
            txn_type_x=row["txn_type_x"],
            asset_movement=row["asset_movement"],
            asset_token=row["asset_token"],
            decimals_x=row["decimals_x"],
            dollar_amount_x=row["dollar_amount_x"],
            time_prepared_x=row["time_prepared_x"],
            time_fulfilled_x=row["time_fulfilled_x"],
            amount_y=row["amount_y"],
            cancelCaller_y=row["cancelCaller_y"],
            cancelTransactionHash_y=row["cancelTransactionHash_y"],
            chainId_y=row["chainId_y"],
            expiry_y=row["expiry_y"],
            fulfillCaller_y=row["fulfillCaller_y"],
            fulfillTimestamp_y=row["fulfillTimestamp_y"],
            fulfillTransactionHash_y=row["fulfillTransactionHash_y"],
            prepareCaller_y=row["prepareCaller_y"],
            prepareTransactionHash_y=row["prepareTransactionHash_y"],
            preparedBlockNumber_y=row["preparedBlockNumber_y"],
            preparedTimestamp_y=row["preparedTimestamp_y"],
            status_y=row["status_y"],
            chain_y=row["chain_y"],
            txn_type_y=row["txn_type_y"],
            decimals_y=row["decimals_y"],
            dollar_amount_y=row["dollar_amount_y"],
            time_prepared_y=row["time_prepared_y"],
            time_fulfilled_y=row["time_fulfilled_y"],
            time_taken=row["time_taken"],
            time_taken_seconds=row["time_taken_seconds"],
        )
        rows.append(new_row)

    db.session.add_all(rows)
    db.session.commit()

    rows = []
    for index, row in df.iterrows():
        new_row = Txns(
            amount_x=row["amount_x"],
            bidSignature=row["bidSignature"],
            callDataHash=row["callDataHash"],
            callTo=row["callTo"],
            cancelCaller_x=row["cancelCaller_x"],
            cancelTransactionHash_x=row["cancelTransactionHash_x"],
            chainId_x=row["chainId_x"],
            expiry_x=row["expiry_x"],
            fulfillCaller_x=row["fulfillCaller_x"],
            fulfillTimestamp_x=row["fulfillTimestamp_x"],
            fulfillTransactionHash_x=row["fulfillTransactionHash_x"],
            subgraphId=row["id"],
            prepareCaller_x=row["prepareCaller_x"],
            prepareTransactionHash_x=row["prepareTransactionHash_x"],
            preparedBlockNumber_x=row["preparedBlockNumber_x"],
            preparedTimestamp_x=row["preparedTimestamp_x"],
            receivingAddress=row["receivingAddress"],
            receivingAssetId=row["receivingAssetId"],
            receivingChainId=row["receivingChainId"],
            receivingChainTxManagerAddress=row["receivingChainTxManagerAddress"],
            router=row["router"],
            sendingAssetId=row["sendingAssetId"],
            sendingChainFallback=row["sendingChainFallback"],
            sendingChainId=row["sendingChainId"],
            status_x=row["status_x"],
            transactionId=row["transactionId"],
            user=row["user"],
            chain_x=row["chain_x"],
            txn_type_x=row["txn_type_x"],
            asset_movement=row["asset_movement"],
            asset_token=row["asset_token"],
            decimals_x=row["decimals_x"],
            dollar_amount_x=row["dollar_amount_x"],
            time_prepared_x=row["time_prepared_x"],
            time_fulfilled_x=row["time_fulfilled_x"],
            amount_y=row["amount_y"],
            cancelCaller_y=row["cancelCaller_y"],
            cancelTransactionHash_y=row["cancelTransactionHash_y"],
            chainId_y=row["chainId_y"],
            expiry_y=row["expiry_y"],
            fulfillCaller_y=row["fulfillCaller_y"],
            fulfillTimestamp_y=row["fulfillTimestamp_y"],
            fulfillTransactionHash_y=row["fulfillTransactionHash_y"],
            prepareCaller_y=row["prepareCaller_y"],
            prepareTransactionHash_y=row["prepareTransactionHash_y"],
            preparedBlockNumber_y=row["preparedBlockNumber_y"],
            preparedTimestamp_y=row["preparedTimestamp_y"],
            status_y=row["status_y"],
            chain_y=row["chain_y"],
            txn_type_y=row["txn_type_y"],
            decimals_y=row["decimals_y"],
            dollar_amount_y=row["dollar_amount_y"],
            time_prepared_y=row["time_prepared_y"],
            time_fulfilled_y=row["time_fulfilled_y"],
            time_taken=row["time_taken"],
            time_taken_seconds=row["time_taken_seconds"],
        )
        rows.append(new_row)

    db.session.add_all(rows)
    db.session.commit()


def add_txns(df):
    rows = []
    global Table
    global current_table
    if current_table == "og":
        CurrentTable = CopyTxns
    else:
        CurrentTable = Txns

    clear_table_with_expiry(CurrentTable)

    for index, row in df.iterrows():
        new_row = CurrentTable(
            amount_x=row["amount_x"],
            expiry_x=row["expiry_x"],
            fulfillTimestamp_x=row["fulfillTimestamp_x"],
            subgraphId=row["id"],
            preparedBlockNumber_x=row["preparedBlockNumber_x"],
            preparedTimestamp_x=row["preparedTimestamp_x"],
            receivingAssetId=row["receivingAssetId"],
            sendingAssetId=row["sendingAssetId"],
            status_x=row["status_x"],
            user=row["user"],
            chain_x=row["chain_x"],
            txn_type_x=row["txn_type_x"],
            asset_movement=row["asset_movement"],
            asset_token=row["asset_token"],
            decimals_x=row["decimals_x"],
            dollar_amount_x=row["dollar_amount_x"],
            time_prepared_x=row["time_prepared_x"],
            time_fulfilled_x=row["time_fulfilled_x"],
            amount_y=row["amount_y"],
            expiry_y=row["expiry_y"],
            fulfillTimestamp_y=row["fulfillTimestamp_y"],
            preparedBlockNumber_y=row["preparedBlockNumber_y"],
            preparedTimestamp_y=row["preparedTimestamp_y"],
            status_y=row["status_y"],
            chain_y=row["chain_y"],
            txn_type_y=row["txn_type_y"],
            decimals_y=row["decimals_y"],
            dollar_amount_y=row["dollar_amount_y"],
            time_prepared_y=row["time_prepared_y"],
            time_fulfilled_y=row["time_fulfilled_y"],
            time_taken=row["time_taken"],
            time_taken_seconds=row["time_taken_seconds"],
        )
        rows.append(new_row)

    db.session.add_all(rows)
    db.session.commit()

    if current_table == "og":
        current_table = "copy"
        Table = CopyTxns
    else:
        current_table = "og"
        Table = Txns

    print(df.shape[0], "rows added to", current_table)


@scheduler.task(
    "interval",
    id="job_sync",
    seconds=120,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def update_db():
    print("Updating database")
    global expiry_cut_off
    with scheduler.app.app_context():
        expiry_cut_off = update_cut_off(expiry_cut_off)

        count = db.session.query(Table).count()
        if count == 0:
            expiry_cut_off = "1232571303"
            df = fetch_txns_df(expiry_cut_off)
            init_db(df)
            return
        df = fetch_txns_df(expiry_cut_off)
        add_txns(df)


@blueprint.route("/")
def hello_world():
    rows = db.session.query(Table).count()
    count = rows
    # sql = text("select count(*) from txns")
    # result = db.engine.execute(sql)
    # rows = [row[0] for row in result]
    # count = rows[0]
    return "Thanks for using our data :)" + str(count)


@blueprint.route("/expiry")
def get_expi():
    return expiry_cut_off


@blueprint.route("/volume")
def get_volume():
    print("Volume")
    from_chain = chain_case_mapping[request.args.get("from")]
    to_chain = chain_case_mapping[request.args.get("to")]
    merged_txns = pd.read_sql(
        sql=db.session.query(Table).statement, con=db.session.bind
    )
    print("done with fetching")
    fulfilled_txns = merged_txns[
        (merged_txns.status_x == "Fulfilled") & (merged_txns.status_y == "Fulfilled")
    ].copy(deep=True)

    if from_chain == "all" and to_chain == "all":
        volume = fulfilled_txns.dollar_amount_x.sum()
    elif from_chain == "all":
        volume = fulfilled_txns[
            fulfilled_txns.chain_y == to_chain
        ].dollar_amount_x.sum()
    elif to_chain == "all":
        volume = fulfilled_txns[
            fulfilled_txns.chain_x == from_chain
        ].dollar_amount_x.sum()
    else:
        asset_movement = from_chain + " -> " + to_chain
        volume = fulfilled_txns[
            (fulfilled_txns.asset_movement == asset_movement)
        ].dollar_amount_x.sum()

    data = {"volume": volume, "from": from_chain, "to": to_chain}
    return json.dumps(data)


@blueprint.route("/add")
def add_book():
    name = request.args.get("name")
    author = request.args.get("author")
    published = request.args.get("published")
    try:
        book = Txns(name=name, author=author, published=published)
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.id)
    except Exception as e:
        return str(e)
