
import json
from decimal import Decimal
import requests
from sqlalchemy import or_
from app import db
from app import url, digital_currency
from app.common.functions import floating_decimals
from app.common.notification import create_notification
from app.classes.wallet_bch import \
    Bch_Wallet, \
    Bch_WalletUnconfirmed, \
    Bch_WalletTransferOrphan, \
    Bch_WalletTransactions
from app.classes.auth import Auth_User

"""
# this script nonstop.
# This cron job gets the user unconfirmed.
# It searches for incomming transactions.
"""

def addtounconfirmed(amount, user_id, txid):
    """
    this function can track multiple incomming unconfirmed amounts
    :param amount:
    :param user_id:
    :param txid:
    :return:
    """

    # get unconfirmed transactions
    unconfirmedtable = db.session\
        .query(Bch_WalletUnconfirmed)\
        .filter_by(user_id=user_id)\
        .first()

    # put to decimal
    decamount = floating_decimals(amount, 8)

    # if doesnt exist, create a new unconfirmed tranactions
    if unconfirmedtable is None:

        newunconfirmed = Bch_WalletUnconfirmed(
            user_id=user_id,
            unconfirmed1=0,
            unconfirmed2=0,
            unconfirmed3=0,
            unconfirmed4=0,
            unconfirmed5=0,

        )
        db.session.add(newunconfirmed)
    else:
        # find matching in unconfirmed table
        if unconfirmedtable.unconfirmed1 == 0:
            unconfirmedtable.unconfirmed1 = decamount
            unconfirmedtable.txid1 = txid
            db.session.add(unconfirmedtable)

        elif unconfirmedtable.unconfirmed2 == 0:
            unconfirmedtable.txid2 = txid
            unconfirmedtable.unconfirmed2 = decamount
            db.session.add(unconfirmedtable)

        elif unconfirmedtable.unconfirmed3 == 0:
            unconfirmedtable.txid3 = txid
            unconfirmedtable.unconfirmed3 = decamount
            db.session.add(unconfirmedtable)

        elif unconfirmedtable.unconfirmed4 == 0:
            unconfirmedtable.txid4 = txid
            unconfirmedtable.unconfirmed4 = decamount
            db.session.add(unconfirmedtable)

        elif unconfirmedtable.unconfirmed5 == 0:
            unconfirmedtable.unconfirmed5 = decamount
            unconfirmedtable.txid5 = txid
            db.session.add(unconfirmedtable)
        else:
            pass


def removeunconfirmed(user_id, txid):

    """
    this function removes the amount from unconfirmed
    """

    # get unconfirmed in database
    unconfirmeddelete = db.session\
        .query(Bch_WalletUnconfirmed)\
        .filter_by(user_id=user_id)\
        .first()

    # find matching txid in table
    if unconfirmeddelete.txid1 == txid:
        unconfirmeddelete.txid1 = ''
        unconfirmeddelete.unconfirmed1 = 0
        db.session.add(unconfirmeddelete)

    elif unconfirmeddelete.txid2 == txid:
        unconfirmeddelete.txid2 = ''
        unconfirmeddelete.unconfirmed2 = 0
        db.session.add(unconfirmeddelete)

    elif unconfirmeddelete.txid3 == txid:
        unconfirmeddelete.txid3 = ''
        unconfirmeddelete.unconfirmed3 = 0
        db.session.add(unconfirmeddelete)

    elif unconfirmeddelete.txid4 == txid:
        unconfirmeddelete.txid4 = ''
        unconfirmeddelete.unconfirmed4 = 0
        db.session.add(unconfirmeddelete)

    elif unconfirmeddelete.txid5 == txid:
        unconfirmeddelete.txid5 = ''
        unconfirmeddelete.unconfirmed5 = 0
        db.session.add(unconfirmeddelete)

    else:
        pass


def getbalanceunconfirmed(user_id):
    """
    this function removes the amount from unconfirmed
    """
    unconfirmeddelete = db.session\
        .query(Bch_WalletUnconfirmed)\
        .filter_by(user_id=user_id)\
        .first()
    a = Decimal(unconfirmeddelete.unconfirmed1)
    b = Decimal(unconfirmeddelete.unconfirmed2)
    c = Decimal(unconfirmeddelete.unconfirmed3)
    d = Decimal(unconfirmeddelete.unconfirmed4)
    e = Decimal(unconfirmeddelete.unconfirmed5)

    total = a + b + c + d + e

    wallet = db.session\
        .query(Bch_Wallet)\
        .filter_by(user_id=user_id)\
        .first()
        
    totalchopped = floating_decimals(total, 8)
    wallet.unconfirmed = totalchopped
    db.session.add(wallet)


def orphan(txid, amount2, address):
    """
    this function is if they cant find a matching address
    """
    getorphan = db.session\
        .query(Bch_WalletTransferOrphan)\
        .filter_by(txid=txid)\
        .first()
    if getorphan:
        pass
    else:
        # orphan transaction. put in background.
        # they prolly sent to old address
        trans = Bch_WalletTransferOrphan(
            bch=amount2,
            bchaddress=address,
            txid=txid,
        )
        db.session.add(trans)


def newincomming(user, userwallet, amount2, txid, howmanyconfs):
    """
    this function creates a new transaction for incomming coin
    """
    dcurrency = digital_currency

    # calculate balance of incomming and current
    currentamount = Decimal(userwallet.currentbalance)
    addcurrent = currentamount + amount2
    shortaddcurrent = floating_decimals(addcurrent, 8)

    # create and watch transaction
    trans = Bch_WalletTransactions(
        category=3,
        user_id=userwallet.user_id,
        confirmations=howmanyconfs,
        txid=txid,
        amount=amount2,
        address='',
        blockhash='',
        timerecieved=0,
        timeoft=0,
        commentbch='',
        otheraccount=0,
        balance=shortaddcurrent,
        fee=0,
        confirmed=0,
        orderid=0,
        senderid=0,
        digital_currency=dcurrency,
        confirmed_fee=0,
    )
    db.session.add(trans)

    # stats - the transaction account
    usertranscount = userwallet.transactioncount
    newcount = usertranscount + 1
    userwallet.transactioncount = newcount
    db.session.add(userwallet)

    # add total of incomming
    addtounconfirmed(amount=amount2,
                     user_id=userwallet.user_id,
                     txid=txid
                     )

    # get total unconfirmed balance
    getbalanceunconfirmed(userwallet.user_id)

    # notify user
    create_notification(username=user.display_name,
                 user_uuid=user.uuid,
                 msg="You have a new incomment BCH deposit.")



def updateincomming(howmanyconfs, transactions, userwallet, txid, amount2):
    if transactions.confirmed == 1:
        pass
    else:
        # if confirmations less than 12 .update them .else
        # check to see if in table and delete
        if 0 <= howmanyconfs <= 5:

            # set confirmation count in transaction
            transactions.confirmations = howmanyconfs
            db.session.add(transactions)

            # get total unconfirmed balance
            getbalanceunconfirmed(userwallet.user_id)
   
        elif 6 <= howmanyconfs <= 25:

            # remove from unconfirmed
            removeunconfirmed(user_id=userwallet.user_id, txid=txid)

            # get new address
            # getnewaddress(user_id=userwallet.user_id)

            # calculate balance
            bal = floating_decimals(userwallet.currentbalance, 8)
            addit = floating_decimals(bal, 8) + amount2
            addittotal = floating_decimals(addit, 8)

            # set balance in database
            userwallet.currentbalance = addittotal

            # updated transaction
            transactions.confirmations = howmanyconfs
            transactions.confirmed = 1
            transactions.balance = addittotal

            db.session.add(transactions)
            db.session.add(userwallet)

            # get total unconfirmed balance
            getbalanceunconfirmed(userwallet.user_id)

        else:
            pass




def getincommingcoin():
    # standard json header
    headers = {'content-type': 'application/json'}

    # method and params
    rpc_input = {
        "method": "listunspent",
        "params":
            {
             "minconf": 0,
             "maxconf": 100,
             }
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "1.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
    )

    response_json = response.json()
    print(response_json)
    return response_json

def main():
    # get the json response
    response_json = getincommingcoin()

    # this is a complicated response
    # turns array of json object

    # turns array of json object

    amount_added = 0

    for i in (response_json['result']):

        address = i['address']
        print(("address: ", i['address']))
        amount = i['amount']
        print(("amount: ", i['amount']))
        txid = i['txid']
        print(("txid: ", i['txid']))
        confirmations = i['confirmations']
        print(("confirmations: ", i['confirmations']))
        print("*"*10)

        # get the decimal of amount
        amount2 = floating_decimals(amount, 8)

        # get confirmations
        howmanyconfs = int(confirmations)

        # find the wallet that matches the address
        userwallets = db.session\
            .query(Bch_Wallet) \
            .filter(or_(Bch_Wallet.address1 == address,
                        Bch_Wallet.address2 == address,
                        Bch_Wallet.address3 == address
                        )
                    ) \
            .first()
        user = db.session\
            .query(Auth_User)\
            .filter(Auth_User.id==userwallets.user_id)\
            .first()
        # if wallet doesnt exist oprphan
        if not userwallets:
            orphan(txid=txid, amount2=amount2, address=address)
        else:
            # get the transactions
            transactions = db.session\
                .query(Bch_WalletTransactions)\
                .filter(Bch_WalletTransactions.txid == txid)\
                .first()
            newamount = amount_added + 1
            amount_added = newamount
            # create in database a new transaction or watch it
            if transactions:
                # update if there is a transaction
                updateincomming(
                                howmanyconfs,
                                transactions,
                                userwallets,
                                txid,
                                amount2)
            else:
                # create a transaction
                newincomming(
                    user,
                    userwallets,
                    amount2,
                    txid,
                    howmanyconfs)


    db.session.commit()

