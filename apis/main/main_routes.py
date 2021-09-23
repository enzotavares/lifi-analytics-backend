from re import fullmatch
from flask import request, jsonify, redirect, render_template
from data.models import Txns
from apis import db
from data.query import update_database
from data.constants import chain_case_mapping
import pandas as pd
import json

from . import main
# from backend.constants.theme_constants import *

from apscheduler.schedulers.background import BackgroundScheduler

def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=11)
sched.start()

def add_txns(df):
    rows = []
    for index, row in df.iterrows():
        new_row = Txns(amount_x=row["amount_x"], bidSignature=row["bidSignature"], callDataHash=row["callDataHash"], callTo=row["callTo"], cancelCaller_x=row["cancelCaller_x"], cancelTransactionHash_x=row["cancelTransactionHash_x"], chainId_x=row["chainId_x"], expiry_x=row["expiry_x"], fulfillCaller_x=row["fulfillCaller_x"], fulfillTimestamp_x=row["fulfillTimestamp_x"], fulfillTransactionHash_x=row["fulfillTransactionHash_x"], subgraphId=row["id"], prepareCaller_x=row["prepareCaller_x"], prepareTransactionHash_x=row["prepareTransactionHash_x"], preparedBlockNumber_x=row["preparedBlockNumber_x"], preparedTimestamp_x=row["preparedTimestamp_x"], receivingAddress=row["receivingAddress"], receivingAssetId=row["receivingAssetId"], receivingChainId=row["receivingChainId"], receivingChainTxManagerAddress=row["receivingChainTxManagerAddress"], router=row["router"], sendingAssetId=row["sendingAssetId"], sendingChainFallback=row["sendingChainFallback"], sendingChainId=row["sendingChainId"], status_x=row["status_x"], transactionId=row["transactionId"], user=row["user"], chain_x=row["chain_x"], txn_type_x=row["txn_type_x"], asset_movement=row["asset_movement"], asset_token=row["asset_token"], decimals_x=row["decimals_x"], dollar_amount_x=row["dollar_amount_x"], time_prepared_x=row["time_prepared_x"], time_fulfilled_x=row["time_fulfilled_x"], amount_y=row["amount_y"], cancelCaller_y=row["cancelCaller_y"], cancelTransactionHash_y=row["cancelTransactionHash_y"], chainId_y=row["chainId_y"], expiry_y=row["expiry_y"], fulfillCaller_y=row["fulfillCaller_y"], fulfillTimestamp_y=row["fulfillTimestamp_y"], fulfillTransactionHash_y=row["fulfillTransactionHash_y"], prepareCaller_y=row["prepareCaller_y"], prepareTransactionHash_y=row["prepareTransactionHash_y"], preparedBlockNumber_y=row["preparedBlockNumber_y"], preparedTimestamp_y=row["preparedTimestamp_y"], status_y=row["status_y"], chain_y=row["chain_y"], txn_type_y=row["txn_type_y"], decimals_y=row["decimals_y"], dollar_amount_y=row["dollar_amount_y"], time_prepared_y=row["time_prepared_y"], time_fulfilled_y=row["time_fulfilled_y"], time_taken=row["time_taken"], time_taken_seconds=row["time_taken_seconds"])
        rows.append(new_row)
    db.session.add_all(rows)
    db.session.commit()
    print(df.shape[0]+" rows added")

@main.route('/')
def hello_world():

    return "https://itsakshay.com/"

@main.route('/dadd')
def update_db():
    df = update_database()
    add_txns(df)
    return "https://itsakshay.com/"

@main.route('/volume_<movement>')
def get_volume(movement):
    merged_txns = pd.read_sql(sql = db.session.query(Txns).statement, con = db.session.bind)
    fulfilled_txns = merged_txns[(merged_txns.status_x == "Fulfilled") & (merged_txns.status_y == "Fulfilled")].copy(deep=True)
    
    if movement == "all":
        volume = fulfilled_txns.dollar_amount_x.sum()
    else:
        chain1, chain2 = movement.split("_")
        asset_movement = chain_case_mapping[chain1] + " -> " + chain_case_mapping[chain2]
        volume = fulfilled_txns[(fulfilled_txns.asset_movement == asset_movement)].dollar_amount_x.sum()


    data = {
        "volume": volume,
        "movement": movement
    }
    return json.dumps(data)



@main.route("/name/<name>")
def get_book_name(name):
    return "name : {}".format(name)

@main.route("/details")
def get_book_details():
    author=request.args.get('author')
    published=request.args.get('published')
    return "Author : {}, Published: {}".format(author,published)

@main.route("/add")
def add_book():
    name=request.args.get('name')
    author=request.args.get('author')
    published=request.args.get('published')
    try:
        book=Txns(
            name=name,
            author=author,
            published=published
        )
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.id)
    except Exception as e:
	    return(str(e))