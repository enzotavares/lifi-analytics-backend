from data.models import Txns, Misc, OldTxns
from apis import db, app
import pandas as pd
from data.query import fetch_txns_df, time_taken
from datetime import datetime, timedelta


def clear_table_with_expiry(Txns, prep_cut_off):
    delete_q = Txns.__table__.delete().where(Txns.preparedTimestamp > prep_cut_off)
    db.session.execute(delete_q)
    db.session.commit()
    # except:
    #     db.session.rollback()


def init_db(df):
    rows = []
    for index, row in df.iterrows():
        new_row = Txns(
            amount=row["amount"],
            expiry=row["expiry"],
            fulfillTimestamp=row["fulfillTimestamp"],
            subgraphId=row["id"],
            preparedBlockNumber=row["preparedBlockNumber"],
            preparedTimestamp=row["preparedTimestamp"],
            receivingAssetId=row["receivingAssetId"],
            sendingAssetId=row["sendingAssetId"],
            status=row["status"],
            user=row["user"],
            chain=row["chain"],
            txn_type=row["txn_type"],
            asset_movement=row["asset_movement"],
            asset_token=row["asset_token"],
            decimals=row["decimals"],
            dollar_amount=row["dollar_amount"],
            time_prepared=row["time_prepared"],
            time_fulfilled=row["time_fulfilled"],
        )
        rows.append(new_row)

    db.session.add_all(rows)
    db.session.commit()


def add_txns(df, prep_cut_off):
    rows = []
    clear_table_with_expiry(Txns, prep_cut_off)

    for index, row in df.iterrows():
        new_row = Txns(
            amount=row["amount"],
            expiry=row["expiry"],
            fulfillTimestamp=row["fulfillTimestamp"],
            subgraphId=row["id"],
            preparedBlockNumber=row["preparedBlockNumber"],
            preparedTimestamp=row["preparedTimestamp"],
            receivingAssetId=row["receivingAssetId"],
            sendingAssetId=row["sendingAssetId"],
            status=row["status"],
            user=row["user"],
            chain=row["chain"],
            txn_type=row["txn_type"],
            asset_movement=row["asset_movement"],
            asset_token=row["asset_token"],
            decimals=row["decimals"],
            dollar_amount=row["dollar_amount"],
            time_prepared=row["time_prepared"],
            time_fulfilled=row["time_fulfilled"],
        )
        rows.append(new_row)

    db.session.add_all(rows)
    db.session.commit()

    print(df.shape[0], "rows added to Postgres")


def update_cached_data():
    print("updatin cached databases")
    old_data_txns = pd.read_sql(
        sql=db.session.query(OldTxns).statement, con=db.session.bind
    )
    new_data_txns = pd.read_sql(
        sql=db.session.query(Txns).statement, con=db.session.bind
    )

    compact_data_txns = pd.concat([old_data_txns, new_data_txns])

    compact_data_txns = compact_data_txns.drop("id", axis=1)
    repeat_txns = compact_data_txns[compact_data_txns["txn_type"] == "repeat"].copy(
        deep=True
    )
    one_sided_txns = compact_data_txns[compact_data_txns["txn_type"] == "single"].copy(
        deep=True
    )
    repeat_txns.reset_index(drop=True, inplace=True)
    one_sided_txns.reset_index(drop=True, inplace=True)

    dem2_merge_cols = [
        "subgraphId",
        "receivingAssetId",
        "asset_token",
        "user",
        "sendingAssetId",
        "asset_movement",
    ]
    merged_txns = pd.merge(
        left=one_sided_txns,
        right=repeat_txns,
        how="outer",
        left_on=dem2_merge_cols,
        right_on=dem2_merge_cols,
    )
    print("Merged", merged_txns.shape)
    merged_txns["time_taken"] = merged_txns.apply(time_taken, axis=1)
    merged_txns["time_taken_seconds"] = merged_txns["time_taken"].apply(
        lambda x: x.seconds
    )

    # merged_txns.replace({np.NaN: None}, inplace=True)

    fulfilled_txns = merged_txns[
        (merged_txns.status_x == "Fulfilled") & (merged_txns.status_y == "Fulfilled")
    ].copy(deep=True)
    fulfilled_txns["date"] = fulfilled_txns["time_fulfilled_y"].apply(
        lambda x: x.date()
    )
    date_volume = (
        fulfilled_txns.groupby("date")
        .agg({"subgraphId": "count", "dollar_amount_x": "sum"})
        .reset_index()
        .rename(columns={"subgraphId": "txns", "dollar_amount_x": "volume"})
    )
    date_volume.to_sql("date_volume", db.engine, if_exists="replace", index_label="id")

    fulfilled_txns["time_taken_seconds"] = pd.to_numeric(
        fulfilled_txns["time_taken_seconds"], downcast="float"
    )

    asset_movement = (
        fulfilled_txns.groupby("asset_movement")
        .agg(
            {
                "subgraphId": "count",
                "dollar_amount_x": "sum",
                "time_taken_seconds": "mean",
            }
        )
        .reset_index()
        .rename(
            columns={
                "subgraphId": "txns",
                "dollar_amount_x": "volume",
                "time_taken_seconds": "time_taken",
            }
        )
    )
    asset_movement.to_sql(
        "asset_movement", db.engine, if_exists="replace", index_label="id"
    )

    past_day_volume = fulfilled_txns[
        fulfilled_txns["time_fulfilled_y"] >= datetime.now() - timedelta(1)
    ]["dollar_amount_x"].sum()
    misc_data = Misc.query.filter_by(data="past_day_volume").first()
    misc_data.value = str(past_day_volume)
    db.session.commit()

    past_day_count = fulfilled_txns[
        fulfilled_txns["time_fulfilled_y"] >= datetime.now() - timedelta(1)
    ]["dollar_amount_x"].count()
    misc_data = Misc.query.filter_by(data="past_day_count").first()
    misc_data.value = str(past_day_count)
    db.session.commit()

    total_unique_users = fulfilled_txns.user.nunique()
    misc_data = Misc.query.filter_by(data="total_unique_users").first()
    misc_data.value = str(total_unique_users)
    db.session.commit()

    total_volume = fulfilled_txns.dollar_amount_x.sum()
    misc_data = Misc.query.filter_by(data="total_volume").first()
    misc_data.value = str(total_volume)
    db.session.commit()

    total_txns_no = fulfilled_txns.shape[0]
    misc_data = Misc.query.filter_by(data="total_txns_no").first()
    misc_data.value = str(total_txns_no)
    db.session.commit()
    print("updated cache")
