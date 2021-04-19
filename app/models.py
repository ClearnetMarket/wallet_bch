from app import db
from datetime import datetime



class User(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    username = db.Column(db.TEXT)
    password_hash = db.Column(db.TEXT)
    member_since = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    email = db.Column(db.TEXT)
    wallet_pin = db.Column(db.TEXT)
    profileimage = db.Column(db.TEXT)
    stringuserdir = db.Column(db.TEXT)
    bio = db.Column(db.TEXT)
    country = db.Column(db.TEXT)
    currency = db.Column(db.INTEGER)
    vendor_account = db.Column(db.INTEGER)
    selling_from = db.Column(db.TEXT)
    last_seen = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    admin = db.Column(db.INTEGER)
    admin_role = db.Column(db.INTEGER)
    dispute = db.Column(db.INTEGER)
    fails = db.Column(db.INTEGER)
    locked = db.Column(db.INTEGER)
    vacation = db.Column(db.INTEGER)
    shopping_timer = db.Column(db.TIMESTAMP())
    lasttraded_timer = db.Column(db.TIMESTAMP())
    shard = db.Column(db.INTEGER)
    protosuser = db.Column(db.INTEGER)
    usernode = db.Column(db.INTEGER)
    affiliate_account = db.Column(db.INTEGER)
    confirmed = db.Column(db.INTEGER)
    passwordpinallowed = db.Column(db.INTEGER)


class Notifications(db.Model):
    __tablename__ = 'notifications'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.INTEGER)
    username = db.Column(db.TEXT)
    userid = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    salenumber = db.Column(db.INTEGER)
    bitcoin = db.Column(db.DECIMAL(20, 8))
    read = db.Column(db.INTEGER)


class BchWallet(db.Model):
    __tablename__ = 'bch_wallet'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    currentbalance = db.Column(db.DECIMAL(20, 8))
    address1 = db.Column(db.TEXT)
    address1status = db.Column(db.INTEGER)
    address2 = db.Column(db.TEXT)
    address2status = db.Column(db.INTEGER)
    address3 = db.Column(db.TEXT)
    address3status = db.Column(db.INTEGER)
    locked = db.Column(db.INTEGER)
    transactioncount = db.Column(db.INTEGER)
    unconfirmed = db.Column(db.DECIMAL(20, 8))


class BchPrices(db.Model):
    __tablename__ = 'prices_bch'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.DECIMAL(50, 2))


class BchTransOrphan(db.Model):
    __tablename__ = 'bch_transorphan'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bch = db.Column(db.DECIMAL(20, 8))
    bchaddress = db.Column(db.TEXT)
    txid = db.Column(db.TEXT)


class BchUnconfirmed(db.Model):
    __tablename__ = 'bch_unconfirmed'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.INTEGER)

    unconfirmed1 = db.Column(db.DECIMAL(20, 8))
    unconfirmed2 = db.Column(db.DECIMAL(20, 8))
    unconfirmed3 = db.Column(db.DECIMAL(20, 8))
    unconfirmed4 = db.Column(db.DECIMAL(20, 8))
    unconfirmed5 = db.Column(db.DECIMAL(20, 8))

    txid1 = db.Column(db.TEXT)
    txid2 = db.Column(db.TEXT)
    txid3 = db.Column(db.TEXT)
    txid4 = db.Column(db.TEXT)
    txid5 = db.Column(db.TEXT)


class BchWalletWork(db.Model):
    __tablename__ = 'bch_walletwork'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    amount = db.Column(db.DECIMAL(20, 8))
    sendto = db.Column(db.TEXT)
    comment = db.Column(db.TEXT)
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    txtcomment = db.Column(db.TEXT)


class BchWalletAddresses(db.Model):
    __tablename__ = 'bch_walletaddresses'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bchaddress = db.Column(db.TEXT)
    status = db.Column(db.INTEGER)


class BchWalletFee(db.Model):
    __tablename__ = 'bch_walletfee'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bch = db.Column(db.DECIMAL(20, 8))


class TransactionsBch(db.Model):
    __tablename__ = 'bch_transactions'
    __bind_key__ = 'agora'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER)
    senderid = db.Column(db.INTEGER)
    confirmations = db.Column(db.INTEGER)
    txid = db.Column(db.TEXT)
    amount = db.Column(db.DECIMAL(20, 8))
    blockhash = db.Column(db.TEXT)
    timeoft = db.Column(db.INTEGER)
    timerecieved = db.Column(db.INTEGER)
    commentbch = db.Column(db.TEXT)
    otheraccount = db.Column(db.INTEGER)
    address = db.Column(db.TEXT)
    fee = db.Column(db.DECIMAL(20, 8))
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    balance = db.Column(db.DECIMAL(20, 8))
    orderid = db.Column(db.INTEGER)
    confirmed = db.Column(db.INTEGER)
    confirmed_fee = db.Column(db.DECIMAL(20, 8))
    digital_currency = db.Column(db.INTEGER)
