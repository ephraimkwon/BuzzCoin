from wtforms.validators import Email
from buzzcoin import app
from flask import render_template, redirect, url_for, flash, request, jsonify
from buzzcoin.forms import LoginForm, RegisterForm, TransactionForm, TransactionNotLoggedInForm
from buzzcoin.models import User
from buzzcoin import blockchain, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
    return render_template('mine.html', blockchain=blockchain)

@app.route("/node")
def node():
	return render_template('node.html', title = "Node")

@app.route('/account')
def account_page():
    return render_template('account.html')

@app.route("/transaction", methods=['GET', 'POST'])
def transaction_page():
    form = TransactionForm()
    formNL = TransactionNotLoggedInForm()
    if form.validate_on_submit():
        feedback = blockchain.add_transaction(form.sender.data, form.reciever.data, form.amount.data, form.key.data, form.key.data)
        if feedback:
            flash(f'Transaction Made!', 'success')
        else:
            flash(f'Error!', 'danger')
        return render_template('transaction.html', title = "Transaction", blockchain = blockchain, form=form, formNL= formNL)

    if formNL.validate_on_submit():
        return redirect(url_for('login'))

    return render_template('transaction.html', title = "Transaction", blockchain = blockchain, form=form, formNL= formNL)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        keys = blockchain.generate_keys()
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=hashed_password,
                              key = keys)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        next_page = request.args.get('next')
        flash(f'Account created for {form.username.data}! You are now logged in.', 'success')
        return redirect(next_page) if next_page else redirect(url_for('home_page'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('register.html', form=form)



# backend stuff
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
    
@app.route('/login', methods = ['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            nextPage = request.args.get('next')
            flash(f'Welcome! You are now logged in', 'success')
            return redirect(nextPage) if nextPage else redirect(url_for('home_page'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        print("ur gay")
    return render_template('login.html', form=form)