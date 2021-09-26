from apis import db


class Txns(db.Model):
    __tablename__ = "txns"

    id = db.Column(db.Integer, primary_key=True)
    amount_x = db.Column(db.String())
    expiry_x = db.Column(db.String())
    fulfillTimestamp_x = db.Column(db.String())
    subgraphId = db.Column(db.String())
    preparedBlockNumber_x = db.Column(db.String())
    preparedTimestamp_x = db.Column(db.String())
    receivingAssetId = db.Column(db.String())
    sendingAssetId = db.Column(db.String())
    status_x = db.Column(db.String())
    user = db.Column(db.String())
    chain_x = db.Column(db.String())
    txn_type_x = db.Column(db.String())
    asset_movement = db.Column(db.String())
    asset_token = db.Column(db.String())
    decimals_x = db.Column(db.Integer())
    dollar_amount_x = db.Column(db.Float())
    time_prepared_x = db.Column(db.DateTime())
    time_fulfilled_x = db.Column(db.DateTime())
    amount_y = db.Column(db.String())
    expiry_y = db.Column(db.String())
    fulfillTimestamp_y = db.Column(db.String())
    preparedBlockNumber_y = db.Column(db.String())
    preparedTimestamp_y = db.Column(db.String())
    status_y = db.Column(db.String())
    chain_y = db.Column(db.String())
    txn_type_y = db.Column(db.String())
    decimals_y = db.Column(db.Integer())
    dollar_amount_y = db.Column(db.Float())
    time_prepared_y = db.Column(db.DateTime())
    time_fulfilled_y = db.Column(db.DateTime())
    time_taken = db.Column(db.Interval())
    time_taken_seconds = db.Column(db.String())

    def __init__(
        self,
        amount_x,
        expiry_x,
        fulfillTimestamp_x,
        subgraphId,
        preparedBlockNumber_x,
        preparedTimestamp_x,
        receivingAssetId,
        sendingAssetId,
        status_x,
        user,
        chain_x,
        txn_type_x,
        asset_movement,
        asset_token,
        decimals_x,
        dollar_amount_x,
        time_prepared_x,
        time_fulfilled_x,
        amount_y,
        expiry_y,
        fulfillTimestamp_y,
        preparedBlockNumber_y,
        preparedTimestamp_y,
        status_y,
        chain_y,
        txn_type_y,
        decimals_y,
        dollar_amount_y,
        time_prepared_y,
        time_fulfilled_y,
        time_taken,
        time_taken_seconds,
    ):
        self.amount_x = amount_x
        self.expiry_x = expiry_x
        self.fulfillTimestamp_x = fulfillTimestamp_x
        self.subgraphId = subgraphId
        self.preparedBlockNumber_x = preparedBlockNumber_x
        self.preparedTimestamp_x = preparedTimestamp_x
        self.receivingAssetId = receivingAssetId
        self.sendingAssetId = sendingAssetId
        self.status_x = status_x
        self.user = user
        self.chain_x = chain_x
        self.txn_type_x = txn_type_x
        self.asset_movement = asset_movement
        self.asset_token = asset_token
        self.decimals_x = decimals_x
        self.dollar_amount_x = dollar_amount_x
        self.time_prepared_x = time_prepared_x
        self.time_fulfilled_x = time_fulfilled_x
        self.amount_y = amount_y
        self.expiry_y = expiry_y
        self.fulfillTimestamp_y = fulfillTimestamp_y
        self.preparedBlockNumber_y = preparedBlockNumber_y
        self.preparedTimestamp_y = preparedTimestamp_y
        self.status_y = status_y
        self.chain_y = chain_y
        self.txn_type_y = txn_type_y
        self.decimals_y = decimals_y
        self.dollar_amount_y = dollar_amount_y
        self.time_prepared_y = time_prepared_y
        self.time_fulfilled_y = time_fulfilled_y
        self.time_taken = time_taken
        self.time_taken_seconds = time_taken_seconds

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {"id": self.id}


class CopyTxns(db.Model):
    __tablename__ = "copy_txns"

    id = db.Column(db.Integer, primary_key=True)
    amount_x = db.Column(db.String())
    expiry_x = db.Column(db.String())
    fulfillTimestamp_x = db.Column(db.String())
    subgraphId = db.Column(db.String())
    preparedBlockNumber_x = db.Column(db.String())
    preparedTimestamp_x = db.Column(db.String())
    receivingAssetId = db.Column(db.String())
    sendingAssetId = db.Column(db.String())
    status_x = db.Column(db.String())
    user = db.Column(db.String())
    chain_x = db.Column(db.String())
    txn_type_x = db.Column(db.String())
    asset_movement = db.Column(db.String())
    asset_token = db.Column(db.String())
    decimals_x = db.Column(db.Integer())
    dollar_amount_x = db.Column(db.Float())
    time_prepared_x = db.Column(db.DateTime())
    time_fulfilled_x = db.Column(db.DateTime())
    amount_y = db.Column(db.String())
    expiry_y = db.Column(db.String())
    fulfillTimestamp_y = db.Column(db.String())
    preparedBlockNumber_y = db.Column(db.String())
    preparedTimestamp_y = db.Column(db.String())
    status_y = db.Column(db.String())
    chain_y = db.Column(db.String())
    txn_type_y = db.Column(db.String())
    decimals_y = db.Column(db.Integer())
    dollar_amount_y = db.Column(db.Float())
    time_prepared_y = db.Column(db.DateTime())
    time_fulfilled_y = db.Column(db.DateTime())
    time_taken = db.Column(db.Interval())
    time_taken_seconds = db.Column(db.String())

    def __init__(
        self,
        amount_x,
        expiry_x,
        fulfillTimestamp_x,
        subgraphId,
        preparedBlockNumber_x,
        preparedTimestamp_x,
        receivingAssetId,
        sendingAssetId,
        status_x,
        user,
        chain_x,
        txn_type_x,
        asset_movement,
        asset_token,
        decimals_x,
        dollar_amount_x,
        time_prepared_x,
        time_fulfilled_x,
        amount_y,
        expiry_y,
        fulfillTimestamp_y,
        preparedBlockNumber_y,
        preparedTimestamp_y,
        status_y,
        chain_y,
        txn_type_y,
        decimals_y,
        dollar_amount_y,
        time_prepared_y,
        time_fulfilled_y,
        time_taken,
        time_taken_seconds,
    ):
        self.amount_x = amount_x
        self.expiry_x = expiry_x
        self.fulfillTimestamp_x = fulfillTimestamp_x
        self.subgraphId = subgraphId
        self.preparedBlockNumber_x = preparedBlockNumber_x
        self.preparedTimestamp_x = preparedTimestamp_x
        self.receivingAssetId = receivingAssetId
        self.sendingAssetId = sendingAssetId
        self.status_x = status_x
        self.user = user
        self.chain_x = chain_x
        self.txn_type_x = txn_type_x
        self.asset_movement = asset_movement
        self.asset_token = asset_token
        self.decimals_x = decimals_x
        self.dollar_amount_x = dollar_amount_x
        self.time_prepared_x = time_prepared_x
        self.time_fulfilled_x = time_fulfilled_x
        self.amount_y = amount_y
        self.expiry_y = expiry_y
        self.fulfillTimestamp_y = fulfillTimestamp_y
        self.preparedBlockNumber_y = preparedBlockNumber_y
        self.preparedTimestamp_y = preparedTimestamp_y
        self.status_y = status_y
        self.chain_y = chain_y
        self.txn_type_y = txn_type_y
        self.decimals_y = decimals_y
        self.dollar_amount_y = dollar_amount_y
        self.time_prepared_y = time_prepared_y
        self.time_fulfilled_y = time_fulfilled_y
        self.time_taken = time_taken
        self.time_taken_seconds = time_taken_seconds

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {"id": self.id}
