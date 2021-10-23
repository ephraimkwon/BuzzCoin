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

class Blockchain (object): 
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.miner_reward = 10
        self.nodes = {}

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

    def chainJSONencode(self): # encoding a chain object into a JSON we can use on the web
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

    def chainJSONdecode(self, chainJSON): # decoding a chainJSON into Blockchain object
        chain=[]
        for blockJSON in chainJSON:
            tArr = []
            for tJSON in blockJSON['transactions']:
                transaction = Transaction(tJSON['sender'], tJSON['reciever'], tJSON['amt'])
                transaction.time = tJSON['time']
                transaction.hash = tJSON['hash']
                tArr.append(transaction)
            block = Block(tArr, blockJSON['time'], blockJSON['index'])
            block.hash = blockJSON['hash']
            block.prev = blockJSON['prev']
            block.nonse = blockJSON['nonse']
            chain.append(block)
        return chain
    
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
        self.nonse = 0 
        self.index = index
        self.transactions = transactions #Transaction Data
        self.time = time #Time block was created
        self.prev = '' #Hash of Previous Block
        self.gold = "404"
        self.hash = self.calculateHash() #Hash of Block
        
    def calculateHash(self):
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions += transaction.hash
        hashString = str(self.time) + hashTransactions + self.prev + str(self.index) + str(self.nonse)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
    
    def JSONencode(self): # returns a json version of itself
        return jsonpickle.encode(self)
    
    def JSONdecode(self):
        return jsonpickle.decode(self)
    
    def mine_block(self):
        
        # checks the hash until the first 3 chars of the hash are "404" hehe
        while self.hash[0:len(self.gold)] != self.gold:
            self.nonse += 1
            self.hash = self.calculateHash()
            # print("Nonse: " , self.nonse)
            # print("Hash Attempt: " , self.hash)
            # print("Target Hash: " + self.gold + "...")
            # print("")
        print("Block mined! Nonse to prove work: ", self.nonse)

        return True
    
    def has_valid_transactions(self):
        for transaction in self.transactions:
            temp = transaction
            if not temp.is_valid_transaction(): # if any transaction is fraudulent then return False
                return False
            return True


class Transaction (object):
    def __init__(self, sender, reciever, amt):
        self.sender = sender
        self.receiver = receiver
        self.amt = amt
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.hash = self.calculateHash()

    def calculateHash(self):
        hashString = self.sender + self.reciever + str(self.amt) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
    
    # returns True if transaction is valid
    def sign_transaction(self, key, sender_key) -> bool:
        if self.hash != self.calculateHash():
            # means the transaction has been messed with
            return False
        if str(key.publickey().exportkey()) != str(sender_key.publickey().exportkey()):
            # This means that the transaction is trying to be done by someone other than
            # the sender
            return False
        
        pkcs1_15.new(key)
        self.signature = "Buzz Buzz"

        return True
    
    def is_valid_transaction(self):
        if self.hash != self.calculateHash():
            return False
        if self.sender == self.receiver:
            return False
        if not self.signature or len(self.signature) == 0: # means there is no signature
            return False
        
        return True




blockchain = Blockchain()
pprint(blockchain.chainJSONencode())
blockchain.get_last_block().mine_block()