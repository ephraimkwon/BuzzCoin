from wtforms.validators import Email
from buzzcoin import app
from flask import render_template, redirect, url_for, flash
from buzzcoin.forms import RegisterForm
from buzzcoin.models import User
from buzzcoin import db

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