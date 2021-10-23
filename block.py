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
