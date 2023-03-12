# abstraction/transaction.py

import json
import random
from datetime import datetime

from utils.cryptographic import hash_function
from utils.cryptographic import load_public, save_signature, load_signature

class Transaction:
    """
    Dummy Bitcoin Transaction
    """
    def __init__(self, source_address, destination_address, amount, receiver_pub, prev_hash, hash=None, time=None,
                 prev_owner_sig=None, is_verified=False, fee=0):
        self.source_address = source_address
        self.destination_address = destination_address
        if time is None:
            self.time = datetime.now().timestamp()
        else:
            self.time = time
        self.amount = amount
        self.prev_hash = prev_hash  # last transaction from source address
        self.receiver_pub = receiver_pub  # receiver public key
        if hash is None:
            self.hash = hash_function(str(self.prev_hash) + str(self.receiver_pub) + str(self.time))
        else:
            self.hash = hash
        self.prev_owner_sig = prev_owner_sig
        self.is_verified = is_verified  # True if the signature is verified
        if fee == 0:
            # assign random transaction fee
            fee = self.assign_transaction_fee()
        self.fee = fee

    def assign_transaction_fee(self):
        """
        based on the amount of the transaction it assign a transaction fee
        :return:
        """
        transaction_fee = self.amount * random.uniform(0.01, 0.2)
        return int(transaction_fee)

    def to_dict(self):
        """
        make transaction to dictionary for serialization
        :return:
        """
        recv_pub = self.receiver_pub.save_pkcs1(format="PEM").decode('utf-8')
        signature = save_signature(self.prev_owner_sig)
        return {
            "source_address": self.source_address,
            "destination_address": self.destination_address,
            "time": self.time,
            "amount": self.amount,
            "prev_hash": self.prev_hash,
            "receiver_pub": recv_pub,
            "hash": self.hash,
            "prev_owner_sig": signature,
            "is_verified": self.is_verified,
            "fee": self.fee
        }

    @classmethod
    def load_json(cls, data):
        data = json.loads(data)
        recv_pub = load_public(data['receiver_pub'])
        prev_owner_sig = load_signature(data["prev_owner_sig"])
        return cls(
            source_address=data['source_address'],
            destination_address=data['destination_address'],
            time=data['time'],
            amount=data['amount'],
            prev_hash=data['prev_hash'],
            hash=data["hash"],
            receiver_pub=recv_pub,
            prev_owner_sig=prev_owner_sig,
            is_verified=data['is_verified'],
            fee=data['fee'],
        )

    def __str__(self):
        """
        redefine builtin func for printing
        :return:
        """
        return str(self.__class__) + ": " + str(self.__dict__)