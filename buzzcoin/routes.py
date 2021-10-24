from wtforms.validators import Email
from buzzcoin import app
from flask import render_template, redirect, url_for, flash, request, jsonify
from buzzcoin.forms import RegisterForm
from buzzcoin.models import User
from buzzcoin import blockchain, db

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/<username>')
def userpage(username):
    return f'<h1>About {username}</h1>'

@app.route('/blockchain')
def blockchain_page():
    blockchain.determine_master_chain()
    return render_template('blockchain.html', blockchain = blockchain)

@app.route('/mine')
def mine_page():
    return render_template('mine.html', blockchain = blockchain)

@app.route('/transactions')
def transaction_page():
    return render_template('transaction.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        ##db.session.commit()
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')

    return render_template('register.html', form=form)

@app.route('/mine', methods = ['GET'])
def mine():
    miner = request.args.get('miner')
    last_block = blockchain.get_last_block()

    if len(blockchain.pending_transactions <= 1):
        flash(f'Not enough pending transactions to mine!', 'danger')
    else:
        feedback = blockchain.mine_pending_transactions()
        if feedback:
            flash(f'Success! You have mined a block and have been rewarded', 'success')
        else:
            flash(f'Error', 'danger')
    return render_template('mine.html', title = "Mine", blockchain = blockchain)

@app.route('/transactions/new', methods = ['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'receiver', 'amount']
    if not all([k in values for k in required]):
        return "Missing values", 400
    
    index = blockchain.add_transaction(values['sender'], values['receiver'], values['amount'])

    response = {'message': f'Transaction was successful. Will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods = ['GET'])
def master_chain():
    response = {'chain': blockchain.chain_JSON_encode(), 'length': len(blockchain.chain)}

    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.determine_master_chain()

    if replaced:
        response = {'message': 'Our chain was replaced', 'new_chain': blockchain.chain_JSON_encode()}
    else:
        response = {'message': 'Our chain is authoritative', 'chain': blockchain.chain_JSON_encode()}

    return jsonify(response), 200
