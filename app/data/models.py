from apis import db


class Txns(db.Model):
    __tablename__ = "txns"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String())
    expiry = db.Column(db.String())
    fulfillTimestamp = db.Column(db.String())
    subgraphId = db.Column(db.String())
    preparedBlockNumber = db.Column(db.String())
    preparedTimestamp = db.Column(db.String())
    receivingAssetId = db.Column(db.String())
    sendingAssetId = db.Column(db.String())
    status = db.Column(db.String())
    user = db.Column(db.String())
    chain = db.Column(db.String())
    txn_type = db.Column(db.String())
    asset_movement = db.Column(db.String())
    asset_token = db.Column(db.String())
    decimals = db.Column(db.Integer())
    dollar_amount = db.Column(db.Float())
    time_prepared = db.Column(db.DateTime())
    time_fulfilled = db.Column(db.DateTime())

    def __init__(
        self,
        amount,
        expiry,
        fulfillTimestamp,
        subgraphId,
        preparedBlockNumber,
        preparedTimestamp,
        receivingAssetId,
        sendingAssetId,
        status,
        user,
        chain,
        txn_type,
        asset_movement,
        asset_token,
        decimals,
        dollar_amount,
        time_prepared,
        time_fulfilled,
    ):
        self.expiry = expiry
        self.fulfillTimestamp = fulfillTimestamp
        self.subgraphId = subgraphId
        self.preparedBlockNumber = preparedBlockNumber
        self.preparedTimestamp = preparedTimestamp
        self.receivingAssetId = receivingAssetId
        self.sendingAssetId = sendingAssetId
        self.status = status
        self.user = user
        self.chain = chain
        self.txn_type = txn_type
        self.asset_movement = asset_movement
        self.asset_token = asset_token
        self.decimals = decimals
        self.dollar_amount = dollar_amount
        self.time_prepared = time_prepared
        self.time_fulfilled = time_fulfilled

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {"id": self.id}


class DateVolume(db.Model):
    __tablename__ = "date_volume"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date())
    txns = db.Column(db.Integer())
    volume = db.Column(db.Float())

    def __init__(self, date, txns, volume):
        self.date = date
        self.txns = txns
        self.volume = volume

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "txns": self.txns,
            "volume": self.volume,
        }


class AssetMovement(db.Model):
    __tablename__ = "asset_movement"

    id = db.Column(db.Integer, primary_key=True)
    asset_movement = db.Column(db.String())
    txns = db.Column(db.Integer())
    volume = db.Column(db.Float())
    time_taken = db.Column(db.Float())

    def __init__(self, asset_movement, txns, volume, time_taken):
        self.asset_movement = asset_movement
        self.txns = txns
        self.volume = volume
        self.time_taken = time_taken

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "asset_movement": self.asset_movement,
            "txns": self.txns,
            "volume": self.volume,
            "time_taken": self.time_taken,
        }


class Misc(db.Model):
    __tablename__ = "misc"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String())
    value = db.Column(db.String())

    def __init__(self, data, value):
        self.data = data
        self.value = value

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {"id": self.id, "data": self.data, "value": self.value}
