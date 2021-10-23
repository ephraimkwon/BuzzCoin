import json
import hashlib
from time import time, sleep
from datetime import datetime
from pprint import pprint
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from uuid import uuid4
import jsonpickle
from urllib.parse import urlparse
from transaction import *
from block import *


class Blockchain (object): 
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.miner_reward = 10
        self.nodes = {}
        self.starting_amount = 100

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, block):
        if(len(self.chain) > 0):
            block.prev = self.getLastBlock().hash
        else:
            block.prev = "none"
        self.chain.append(block)

    def register_node(self, node_address):
        url = urlparse(node_address)
        self.nodes.add(url.netloc)

    def create_genesis_block(self): # creates Genesis block or the first block of the blockchain
        transactions = []
        transactions.append(Transaction("Buzz", "George P. Burdell", 404))
        genesis = Block(transactions, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0)
        genesis.prev = "None"
        return genesis

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount, keystring, sender_key):
        key_byte = keystring.encode("ASCII")
        sender_key_byte = sender_key.encode("ASCII")

        key = RSA.import_key(key_byte)
        sender_key = RSA.import_key(sender_key_byte)

        if not sender or not receiver or not amount: # checks if any of the inputs are null
            print("Transaction error: Null error")
            return False
        
        # creating and signing the transaction
        transaction = Transaction(sender, receiver, amount)
        transaction.sign_transaction(key, sender_key)
        
        if not transaction.is_valid_transaction():
            print("Transaction error: not valid transaction")
            return False
        
        self.pending_transactions.append(transaction)

        return len(self.chain) + 1
    
    def mine_pending_transactions(self, miner):
        if len(self.pending_transactions <= 1):
            # can only mine if there are more than one transaction in the pending
            return False
        
        # iterates through the pending transactions and creates blocks and mines them
        # at the end it adds itself as a transaction to the pending transactions
        for i in range(len(self.pending_transactions)):
            remaining_transactions = self.pending_transactions[i:len(remaining_transactions)]
            new_block = Block(remaining_transactions, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            prev_hash = self.get_last_block().hash
            new_block.prev = prev_hash
            new_block.mine_block()
            self.chain.append(new_block)

        print("Mining success")

        pay_miner = Transaction("George P. Burdell", miner, self.miner_reward)
        self.pending_transactions = [pay_miner]
        return True

    def chain_JSON_encode(self): # encoding a chain object into a JSON we can use on the web
        blockArrJSON = []
        for block in self.chain:
            blockJSON = {}
            blockJSON['hash'] = block.hash
            blockJSON['index'] = block.index
            blockJSON['prev'] = block.prev
            blockJSON['time'] = block.time
            transactionsJSON = []
            tJSON = {}
            for transaction in block.transactions:
                tJSON['time'] = transaction.time
                tJSON['sender'] = transaction.sender
                tJSON['receiver'] = transaction.receiver
                tJSON['amount'] = transaction.amount
                tJSON['hash'] = transaction.hash
                transactionsJSON.append(tJSON)
            blockJSON['transactions'] = transactionsJSON
            blockArrJSON.append(blockJSON)
        return blockArrJSON

    def chain_JSON_decode(self, chainJSON): # decoding a chainJSON from the web into Blockchain object
        chain = []
        for blockJSON in chainJSON:
            tArr = []
            for tJSON in blockJSON['transactions']:
                transaction = Transaction(tJSON['sender'], tJSON['receiver'], tJSON['amount'])
                transaction.time = tJSON['time']
                transaction.hash = tJSON['hash']
                tArr.append(transaction)
            block = Block(tArr, blockJSON['time'], blockJSON['index'])
            block.hash = blockJSON['hash']
            block.prev = blockJSON['prev']
            block.nonse = blockJSON['nonse']
            chain.append(block)
        return chain

    def get_balance(self, user):
        balance = 0
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            # need try except because there might not be a transaction of this particular user at each block
            try:
                for transaction in block.transactions:
                    if transaction.sender == user:
                        balance -= transaction.amount
                    if transaction.receiver == user:
                        balance += transaction.amount
            except:
                print("no transaction here")

        return balance + self.starting_amount
    
    def generate_keys(self): # generates the private and public keys
        key = RSA.generate(2048)
        private_key = key.exportKey()
        # creates private key file
        file_out = open("private.pem", "wb")
        file_out.write(private_key)

        public_key = key.public_key().export_key()
        # creates public key file
        file_out = open("public.pem", "wb")
        file_out.write(public_key)

        return key.public_key().exportKey().decode('ASCII') # returns an ascii decoded public keys

blockchain = Blockchain()
pprint(blockchain.chain_JSON_encode())
blockchain.generate_keys()
blockchain.get_last_block().mine_block()