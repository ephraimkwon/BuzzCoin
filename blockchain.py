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

class Block (object):
    def __init__(self, transactions, time, index):
        self.nonse = 0 
        self.index = index
        self.transactions = transactions #Transaction Data
        self.time = time #Time block was created
        self.prev = '' #Hash of Previous Block
        self.gold = "404"
        self.hash = self.calculate_hash() #Hash of Block
        
    def calculate_hash(self):
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions += transaction.hash
        hashString = str(self.time) + hashTransactions + self.prev + str(self.index) + str(self.nonse)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
    
    def JSONencode(self): # returns a json version of itself
        return jsonpickle.encode(self)
    
    def mine_block(self):
        
        # checks the hash until the first 3 chars of the hash are "404" hehe
        while self.hash[0:len(self.gold)] != self.gold:
            self.nonse += 1
            self.hash = self.calculate_hash()
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
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hashString = self.sender + self.receiver + str(self.amount) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
    
    # returns True if transaction is valid
    def sign_transaction(self, key, sender_key) -> bool:
        if self.hash != self.calculate_hash():
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
        if self.hash != self.calculate_hash():
            return False
        if self.sender == self.receiver:
            return False
        if not self.signature or len(self.signature) == 0: # means there is no signature
            return False
        
        return True




blockchain = Blockchain()
pprint(blockchain.chain_JSON_encode())
blockchain.generate_keys()
blockchain.get_last_block().mine_block()