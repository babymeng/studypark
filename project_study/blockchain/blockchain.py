#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import hashlib
import json
from uuid import uuid4
from flask import Flask, jsonify, request
import getopt
import sys
from urllib.parse import urlparse
import requests
import socket
import redis
import signal
import sys

_HOST= socket.gethostbyname(socket.getfqdn(socket.gethostname()))
global _PORT

class Blockchain(object):
    def __init__(self):
        self._chain = []
        self._current_transactions = []
        self._nodes = set()

        #Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_transaction(self, sender, recipient, amount):
        '''
        Create a new transaction to go into the next mined Block
        :param sender: <str> Address of sender
        :param recipient: <str> Address of Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        '''

        self._current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })       

        return self.last_block['index'] + 1

    def new_block(self, proof, previous_hash=None):
        '''
        Create a new block add to the _chain list.
        :param proof: <int> the work proof by Algorithm
        :previous_hash: <str> the hash value of previous block
        :return: <dict> block
        '''

        block = {
            'index': len(self._chain) + 1,
            'timestamp': time.time(),
            'transactions': self._current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self._chain[-1]),
        }

        #reset the current_transactions record
        self._current_transactions = []

        self._chain.append(block)
        return block

    @property
    def last_block(self):
        return self._chain[-1]        

    def hash(self, block):
        '''
        Create a SHA-256 hash value for a block
        :param block: <dict> Block
        :return: <str>
        '''

        #we must ensure that the dict has been sorted, otherwise we should get a different hash value.
        block_string = json.dumps(block, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def work_of_proof(self, last_proof):
        '''
        Simple Proof of Work Algorithm
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        '''
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        '''
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading 0?
        :param last_proof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> True if corrent, False if not.
        '''
        
        guess = f'{last_proof}{proof}'.encode('utf-8')
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def register_node(self, address):
        '''
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg:'http://192.168.0.5:5000'
        :return: None
        '''

        parsed_url = urlparse(address)
        print("parsed_url", parsed_url)
        self._nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        '''
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        '''

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n---------------\n')
            #check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # check that proof of work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolv_conflicts(self):
        '''
        This is our Consensus Algorithm, it resolves conflicts by replacing
        our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not.
        '''

        neighbours = self._nodes
        new_chain = None

        #We're only looking for chains longer than ours
        max_length = len(self._chain)

        #Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                #check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours.
        if new_chain:
            self._chain = new_chain
            return True

        return False
        
#Instantiate our node
app = Flask(__name__)

#Generate a globally unique address for this node
node_id = str(uuid4()).replace('-', '')

#Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    print('-----------mine------------')
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.work_of_proof(last_proof)

    blockchain.new_transaction(
        sender='0',
        recipient=node_id,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New block forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transactions():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain._chain,
        'length': len(blockchain._chain),
    }

    return jsonify(response), 200

@app.route('/nodes/register', methods=['GET'])
def register_nodes():
    '''
    values = request.get_json()
    print('register_nodes:values=', values)
    
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)
    '''

    
    rc = redis.StrictRedis(host='47.52.67.159', port=6379, db=0)
    urls = rc.smembers('url')
    print('urls-------:', urls)
    urls.discard(f'http://{_HOST}:{_PORT}'.encode())
    print('remove:', f'http://{_HOST}:{_PORT}'.encode())
    print('urls-------remove:', urls)

    if urls is None:
        return "Error: Please supply a valid list of nodes", 400

    for url in urls:
        blockchain.register_node(url.decode())
    
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain._nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/reslove', methods=['GET'])
def consensus():
    replaced = blockchain.resolv_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain._chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'new_chain': blockchain._chain
        }

    return jsonify(response), 200

def get_opt():
    global _PORT
    shortopts = 'hmp:'
    longopts = ['help', 'multi', 'port=']

    optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
    for key, value in optlist:
        if key in ('-h', '--help'):
            return False
        elif key in ('-m', '--multi'):
            return True
        elif key in ('-p', '--port'):
            _PORT = int(value)
            return True

    return False

def run():
    global _PORT
    get_opt()
    
    rc = redis.StrictRedis(host='47.52.67.159', port=6379, db=0)
    rc.sadd('url', f'http://{_HOST}:{_PORT}')

    def handle_exit(signum, _):
        rc.srem('url', f'http://{_HOST}:{_PORT}')
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
        
    app.run(host=_HOST, port=int(_PORT))
    
if __name__ == '__main__':
    run()
    
