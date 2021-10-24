from buzzcoin import app, block
from flask import render_template
from buzzcoin.forms import RegisterForm
from buzzcoin.models import User
from buzzcoin import blockchain

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

@app.route('/register')
def register_page():
    form = RegisterForm() 
    return render_template('register.html',form=form)