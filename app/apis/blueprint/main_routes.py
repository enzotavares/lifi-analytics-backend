from datetime import datetime
from os import RTLD_NOW, cpu_count
from flask import jsonify
import pandas as pd


from data.tvl import get_combined_tvl
from data.models import AssetMovement, Txns, Misc, DateVolume, BridgesTvl
from apis import db
from data.query import fetch_txns_df
from data.expiry_manager import get_prep_cut_off
from apis.blueprint.update_db import init_db, add_txns, update_cached_data

from . import blueprint


from flask_apscheduler import APScheduler

scheduler = APScheduler()


@scheduler.task(
    "interval",
    id="job_sync",
    seconds=120,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def update_db():
    print("Updating database")
    with scheduler.app.app_context():
        prep_cut_off = get_prep_cut_off()

        count = db.session.query(Txns).count()
        if count == 0:
            prep_cut_off = "1232571303"
            df = fetch_txns_df(prep_cut_off)
            init_db(df)
            return
        df = fetch_txns_df(prep_cut_off)
        # add_txns(df, prep_cut_off)
        # update_cached_data()


@scheduler.task(
    "interval",
    id="bridges_tvl",
    seconds=130,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def recurring_bridges_tvl():
    with scheduler.app.app_context():
        print("Updating tvl")
        combined_duplicate_tokens = get_combined_tvl()

        combined_duplicate_tokens.to_sql(
            "bridges_tvl", db.engine, if_exists="replace", index_label="id"
        )


@blueprint.route("/")
def hello_world():
    rows = db.session.query(Txns).count()
    # update_db()
    count = rows
    # sql = text("select count(*) from txns")
    # result = db.engine.execute(sql)
    # rows = [row[0] for row in result]
    # count = rows[0]
    return "Thanks for using our data :)" + str(count)


@blueprint.route("/expiry")
def get_expi():
    update_cached_data()
    return "asdfasfas"


@blueprint.route("/general_stats")
def get_general_data():
    data = [row.serialize() for row in Misc.query.all()]
    return jsonify({"data": data})


@blueprint.route("/date_volume")
def get_date_volume():
    data = [row.serialize() for row in DateVolume.query.all()]
    return jsonify({"data": data})


@blueprint.route("/asset_movement")
def get_asset_movement():
    data = [row.serialize() for row in AssetMovement.query.all()]
    return jsonify({"data": data})


@blueprint.route("/bridges_tvl")
def bridges_tvl():
    print("Hello there, general liquidity", datetime.now())
    combined_duplicate_tokens = pd.read_sql(
        sql=db.session.query(BridgesTvl).statement, con=db.session.bind
    )
    combined_duplicate_tokens = combined_duplicate_tokens.drop("id", axis=1)

    grouped_tvl = (
        combined_duplicate_tokens.groupby(["token", "chain"])
        .agg(
            tvl=("tvl", "sum"),
            bridges=("bridge", ",".join),
            bridge_count=("bridge", "count"),
        )
        .reset_index()
    )

    sorted_tvl = grouped_tvl.sort_values(["bridge_count", "tvl"], ascending=False)
    tvl_pairs = sorted_tvl.to_dict(orient="records")
    tvl_bridges = (
        combined_duplicate_tokens.groupby("bridge")
        .sum("tvl")
        .reset_index()
        .to_dict(orient="records")
    )
    tvl_individual = combined_duplicate_tokens.to_dict(orient="records")
    return_data = {
        "tvl_bridges": tvl_bridges,
        "tvl_pairs": tvl_pairs,
        "tvl_individual": tvl_individual,
    }

    print("Au revoir", datetime.now())
    return jsonify({"data": return_data})
