from blockchain import *
from block import *
from transaction import* 

blockchain = Blockchain()
pprint(blockchain.chain_JSON_encode())
blockchain.get_last_block().mine_block()