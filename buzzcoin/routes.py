from buzzcoin import app
from flask import render_template
from buzzcoin.models import User

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/<username>')
def userpage(username):
    return f'<h1>About {username}</h1>'

@app.route('/blockchain')
def blockchain_page():
    items = [
    {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template('blockchain.html', items = items)

@app.route('/mine')
def mine_page():
    return render_template('mine.html')