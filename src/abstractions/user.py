# abstraction/user.py

import rsa
import json

from utils.cryptographic import hash_function, save_key, load_public, load_private
from utils.view import Colors
from abstractions.transaction import Transaction
from server.db import get_user


class User:
    def __init__(self, username=None, initial_balance=None, from_db=False, user_to_load=None, public=None,
                 transactions=[], private=None, mined_blocks=0, confirmed_blocks=0, total_reward=0):
        """

        :param username:
        :param initial_balance:
        :param from_db:
        :param user_to_load:
        :param public:
        :param transactions:
        :param private:
        :param mined_blocks:
        :param confirmed_blocks:
        :param total_reward:
        """
        if from_db:
            # user_to_load is a list read from db file
            self.load_user(user_to_load)
        else:
            self.balance = initial_balance  # initial balance
            self.username = username
            if public is None and private is None:
                (self.pubkey, self.privkey) = rsa.newkeys(512)
            else:
                self.pubkey = public
                self.privkey = private
            self.address = hash_function(str(self.username + str(self.pubkey)))  # unique user ID / address
            self.transactions = transactions
            self.mined_blocks = mined_blocks
            self.confirmed_blocks = confirmed_blocks
            self.total_reward = total_reward

    def to_dict(self, pvt=True):
        privkey = "Secret"
        if pvt:
            privkey = save_key(self.privkey)
        pubkey = save_key(self.pubkey)
        return {
            "balance": self.balance,
            "username": self.username,
            "pubkey": pubkey,
            "privkey": privkey,
            "address": self.address,
            "transactions": self.transactions,
            "mined_blocks": self.mined_blocks,
            "confirmed_blocks": self.confirmed_blocks,
            "total_reward": self.total_reward
        }

    @classmethod
    def load_json(cls, data):
        data = json.loads(data)
        if data['privkey'] == 'Secret':
            privkey = data['privkey']
        else:
            privkey = load_private(data['privkey'])
        pubkey = load_public(data['pubkey'])
        return cls(
            initial_balance=data['balance'],
            username=data['username'],
            public=pubkey,
            private=privkey,
            transactions=data['transactions'],
            mined_blocks=data['mined_blocks'],
            confirmed_blocks=data['confirmed_blocks'],
            total_reward=data['total_reward'],
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_serializable(self):
        return self.to_dict()

    def __repr__(self):
        return self.to_json()

    def get_balance(self):
        """Retrieves the current balance of the user"""
        return self.balance

    def load_user(self, user):
        """

        :param user: list
        :return:
        """
        from server.filesys import load_public_key, load_private_key
        self.username = user[0]
        self.pubkey = load_public_key(user[0])
        self.privkey = load_private_key(user[0])
        self.address = user[2]
        self.balance = user[3]
        self.transactions = []
        self.mined_blocks = user[4]
        self.confirmed_blocks = user[5]
        self.total_reward = user[6]
        self.transactions = json.loads(user[7])

    def make_transaction(self, destination_address, amount):
        """
        Simulates a transaction to the specified destination address
        :param destination_address:
        :param amount:
        :return:
        """
        if not self.transactions:
            # first transaction of the balance
            prev = 'None'
            amount_to_send = 0
        else:
            prev = self.transactions[-1]
            amount_to_send = amount
        # get receiver pub key
        recv = get_user(destination_address)
        receiver = User(from_db=True, user_to_load=recv)
        t = Transaction(self.address, destination_address, amount_to_send, receiver.pubkey, prev)
        # sign transaction
        signature = self.sign(t.hash)
        t.prev_owner_sig = signature
        if amount_to_send <= self.balance:  # new balance is added only after 6 confirmations
            # append transaction
            self.transactions.append(t.hash)
            # NOTE: this is just a local balance update. It won't be registered in the server until the block has been added
            self.balance -= amount_to_send
            return t
        else:
            raise ValueError("Insufficient funds")

    def encrypt(self, message):
        """
        encrypt using public RSA
        :param message
        :return:
        """
        return rsa.encrypt(message, self.pubkey)

    def decrypt(self, crypto):
        """
        decrypt using private RSA
        :param crypto:
        :return:
        """
        return rsa.decrypt(crypto, self.privkey)

    def sign(self, message):
        """
        sign with private key
        :param message:
        :return:
        """
        b_msg = bytes(message, 'utf-8')
        return rsa.sign(b_msg, self.privkey, 'SHA-1')

    def __str__(self):
        """
        redefine builtin func for printing
        :return:
        """
        return str(self.__class__) + ": " + str(self.__dict__)

