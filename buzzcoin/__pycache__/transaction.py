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