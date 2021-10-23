import json
import hashlib
from time import time
from datetime import datetime
from pprint import pprint
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from uuid import uuid4
import jsonpickle

class Blockchain (object): 
    def __init__(self):
        self.chain = []
    def get_last_block(self):
        return self.chain[-1]
    def add_block(self, block):
        if(len(self.chain) > 0):
            block.prev = self.getLastBlock().hash
        else:
            block.prev = "none"
        self.chain.append(block)
    def create_genesis_block(self): # creates Genesis block or the first block of the blockchain
        transactions = []
        transactions.append(Transaction("Buzz", "George P. Burdell", 404))
        genesis = Block(transactions, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0)
        genesis.prev = "None"
        return genesis
    def get_last_block(self):
        return self.chain[-1]

    def chainJSONencode(self):
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
                tJSON['reciever'] = transaction.reciever
                tJSON['amt'] = transaction.amt
                tJSON['hash'] = transaction.hash
                transactionsJSON.append(tJSON)
            blockJSON['transactions'] = transactionsJSON
            blockArrJSON.append(blockJSON)
        return blockArrJSON
    
    def generate_keys(self): # generates the private and public keys
        key = RSA.generate(2048)
        private_key = key.exportKey()
        file_out = open("private.pem", "wb")
        file_out.write(private_key)

        public_key = key.public_key().export_key()
        file_out = open("receiver.pem", "wb")
        file_out.write(public_key)

        return key.public_key().exportKey().decode('ASCII') # returns an ascii decoded public keys

        

    def add_transaction(self, sender, receiver, amt, keystring, senderkey):
        pass

    

class Block (object):
    def __init__(self, transactions, time, index):
        self.index = index
        self.transactions = transactions #Transaction Data
        self.time = time #Time block was created
        self.prev = '' #Hash of Previous Block
        self.hash = self.calculateHash() #Hash of Block

    def calculateHash(self):
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions += transaction.hash
        hashString = str(self.time) + hashTransactions + self.prev + str(self.index)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()

class Transaction (object):
    def __init__(self, sender, reciever, amt):
        self.sender = sender
        self.reciever = reciever
        self.amt = amt
        self.time = time()
        self.hash = self.calculateHash()

    def calculateHash(self):
        hashString = self.sender + self.reciever + str(self.amt) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()


blockchain = Blockchain()
transactions = []
block1 = Block(transactions, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0)
blockchain.addBlock(block1)

pprint(blockchain.chainJSONencode())
