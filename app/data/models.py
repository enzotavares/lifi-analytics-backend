from apis import db


class Txns(db.Model):
    __tablename__ = "txns"

    id = db.Column(db.Integer, primary_key=True)
    amount_x = db.Column(db.String())
    bidSignature = db.Column(db.String())
    callDataHash = db.Column(db.String())
    callTo = db.Column(db.String())
    cancelCaller_x = db.Column(db.String())
    cancelTransactionHash_x = db.Column(db.String())
    chainId_x = db.Column(db.String())
    expiry_x = db.Column(db.String())
    fulfillCaller_x = db.Column(db.String())
    fulfillTimestamp_x = db.Column(db.String())
    fulfillTransactionHash_x = db.Column(db.String())
    subgraphId = db.Column(db.String())
    prepareCaller_x = db.Column(db.String())
    prepareTransactionHash_x = db.Column(db.String())
    preparedBlockNumber_x = db.Column(db.String())
    preparedTimestamp_x = db.Column(db.String())
    receivingAddress = db.Column(db.String())
    receivingAssetId = db.Column(db.String())
    receivingChainId = db.Column(db.String())
    receivingChainTxManagerAddress = db.Column(db.String())
    router = db.Column(db.String())
    sendingAssetId = db.Column(db.String())
    sendingChainFallback = db.Column(db.String())
    sendingChainId = db.Column(db.String())
    status_x = db.Column(db.String())
    transactionId = db.Column(db.String())
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
    cancelCaller_y = db.Column(db.String())
    cancelTransactionHash_y = db.Column(db.String())
    chainId_y = db.Column(db.String())
    expiry_y = db.Column(db.String())
    fulfillCaller_y = db.Column(db.String())
    fulfillTimestamp_y = db.Column(db.String())
    fulfillTransactionHash_y = db.Column(db.String())
    prepareCaller_y = db.Column(db.String())
    prepareTransactionHash_y = db.Column(db.String())
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
        bidSignature,
        callDataHash,
        callTo,
        cancelCaller_x,
        cancelTransactionHash_x,
        chainId_x,
        expiry_x,
        fulfillCaller_x,
        fulfillTimestamp_x,
        fulfillTransactionHash_x,
        subgraphId,
        prepareCaller_x,
        prepareTransactionHash_x,
        preparedBlockNumber_x,
        preparedTimestamp_x,
        receivingAddress,
        receivingAssetId,
        receivingChainId,
        receivingChainTxManagerAddress,
        router,
        sendingAssetId,
        sendingChainFallback,
        sendingChainId,
        status_x,
        transactionId,
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
        cancelCaller_y,
        cancelTransactionHash_y,
        chainId_y,
        expiry_y,
        fulfillCaller_y,
        fulfillTimestamp_y,
        fulfillTransactionHash_y,
        prepareCaller_y,
        prepareTransactionHash_y,
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
        self.bidSignature = bidSignature
        self.callDataHash = callDataHash
        self.callTo = callTo
        self.cancelCaller_x = cancelCaller_x
        self.cancelTransactionHash_x = cancelTransactionHash_x
        self.chainId_x = chainId_x
        self.expiry_x = expiry_x
        self.fulfillCaller_x = fulfillCaller_x
        self.fulfillTimestamp_x = fulfillTimestamp_x
        self.fulfillTransactionHash_x = fulfillTransactionHash_x
        self.subgraphId = subgraphId
        self.prepareCaller_x = prepareCaller_x
        self.prepareTransactionHash_x = prepareTransactionHash_x
        self.preparedBlockNumber_x = preparedBlockNumber_x
        self.preparedTimestamp_x = preparedTimestamp_x
        self.receivingAddress = receivingAddress
        self.receivingAssetId = receivingAssetId
        self.receivingChainId = receivingChainId
        self.receivingChainTxManagerAddress = receivingChainTxManagerAddress
        self.router = router
        self.sendingAssetId = sendingAssetId
        self.sendingChainFallback = sendingChainFallback
        self.sendingChainId = sendingChainId
        self.status_x = status_x
        self.transactionId = transactionId
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
        self.cancelCaller_y = cancelCaller_y
        self.cancelTransactionHash_y = cancelTransactionHash_y
        self.chainId_y = chainId_y
        self.expiry_y = expiry_y
        self.fulfillCaller_y = fulfillCaller_y
        self.fulfillTimestamp_y = fulfillTimestamp_y
        self.fulfillTransactionHash_y = fulfillTransactionHash_y
        self.prepareCaller_y = prepareCaller_y
        self.prepareTransactionHash_y = prepareTransactionHash_y
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
    bidSignature = db.Column(db.String())
    callDataHash = db.Column(db.String())
    callTo = db.Column(db.String())
    cancelCaller_x = db.Column(db.String())
    cancelTransactionHash_x = db.Column(db.String())
    chainId_x = db.Column(db.String())
    expiry_x = db.Column(db.String())
    fulfillCaller_x = db.Column(db.String())
    fulfillTimestamp_x = db.Column(db.String())
    fulfillTransactionHash_x = db.Column(db.String())
    subgraphId = db.Column(db.String())
    prepareCaller_x = db.Column(db.String())
    prepareTransactionHash_x = db.Column(db.String())
    preparedBlockNumber_x = db.Column(db.String())
    preparedTimestamp_x = db.Column(db.String())
    receivingAddress = db.Column(db.String())
    receivingAssetId = db.Column(db.String())
    receivingChainId = db.Column(db.String())
    receivingChainTxManagerAddress = db.Column(db.String())
    router = db.Column(db.String())
    sendingAssetId = db.Column(db.String())
    sendingChainFallback = db.Column(db.String())
    sendingChainId = db.Column(db.String())
    status_x = db.Column(db.String())
    transactionId = db.Column(db.String())
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
    cancelCaller_y = db.Column(db.String())
    cancelTransactionHash_y = db.Column(db.String())
    chainId_y = db.Column(db.String())
    expiry_y = db.Column(db.String())
    fulfillCaller_y = db.Column(db.String())
    fulfillTimestamp_y = db.Column(db.String())
    fulfillTransactionHash_y = db.Column(db.String())
    prepareCaller_y = db.Column(db.String())
    prepareTransactionHash_y = db.Column(db.String())
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
        bidSignature,
        callDataHash,
        callTo,
        cancelCaller_x,
        cancelTransactionHash_x,
        chainId_x,
        expiry_x,
        fulfillCaller_x,
        fulfillTimestamp_x,
        fulfillTransactionHash_x,
        subgraphId,
        prepareCaller_x,
        prepareTransactionHash_x,
        preparedBlockNumber_x,
        preparedTimestamp_x,
        receivingAddress,
        receivingAssetId,
        receivingChainId,
        receivingChainTxManagerAddress,
        router,
        sendingAssetId,
        sendingChainFallback,
        sendingChainId,
        status_x,
        transactionId,
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
        cancelCaller_y,
        cancelTransactionHash_y,
        chainId_y,
        expiry_y,
        fulfillCaller_y,
        fulfillTimestamp_y,
        fulfillTransactionHash_y,
        prepareCaller_y,
        prepareTransactionHash_y,
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
        self.bidSignature = bidSignature
        self.callDataHash = callDataHash
        self.callTo = callTo
        self.cancelCaller_x = cancelCaller_x
        self.cancelTransactionHash_x = cancelTransactionHash_x
        self.chainId_x = chainId_x
        self.expiry_x = expiry_x
        self.fulfillCaller_x = fulfillCaller_x
        self.fulfillTimestamp_x = fulfillTimestamp_x
        self.fulfillTransactionHash_x = fulfillTransactionHash_x
        self.subgraphId = subgraphId
        self.prepareCaller_x = prepareCaller_x
        self.prepareTransactionHash_x = prepareTransactionHash_x
        self.preparedBlockNumber_x = preparedBlockNumber_x
        self.preparedTimestamp_x = preparedTimestamp_x
        self.receivingAddress = receivingAddress
        self.receivingAssetId = receivingAssetId
        self.receivingChainId = receivingChainId
        self.receivingChainTxManagerAddress = receivingChainTxManagerAddress
        self.router = router
        self.sendingAssetId = sendingAssetId
        self.sendingChainFallback = sendingChainFallback
        self.sendingChainId = sendingChainId
        self.status_x = status_x
        self.transactionId = transactionId
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
        self.cancelCaller_y = cancelCaller_y
        self.cancelTransactionHash_y = cancelTransactionHash_y
        self.chainId_y = chainId_y
        self.expiry_y = expiry_y
        self.fulfillCaller_y = fulfillCaller_y
        self.fulfillTimestamp_y = fulfillTimestamp_y
        self.fulfillTransactionHash_y = fulfillTransactionHash_y
        self.prepareCaller_y = prepareCaller_y
        self.prepareTransactionHash_y = prepareTransactionHash_y
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
