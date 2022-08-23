import email
import imp

import bcrypt
from sqlalchemy import false, null, true
from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import LoginForm, RegisterForm, PurchaseForm, SellForm
from market import db
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def homepage():
    return render_template('home.html')

@app.route('/market', methods=["GET"])
@login_required
def market_page():
    purchase_form = PurchaseForm()
    sell_form = SellForm()
    items = Item.query.filter_by(owner=None)
    owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)

@app.route('/purchase', methods=["POST"])
def purchase():
    purchased_item = request.form.get('purchased_item')
    p_item_object = Item.query.filter_by(name=purchased_item).first()
    if p_item_object:
        if current_user.can_purchase(p_item_object):
            current_user.budget -= p_item_object.price
            p_item_object.owner = current_user.id
            db.session.commit()
    return redirect(url_for('market_page'))


@app.route('/sell', methods=["POST"])
def sell():
    item_to_sell = request.form.get('item_to_sell')
    itemtosell = Item.query.filter_by(id=item_to_sell).first()
    if itemtosell:
            current_user.budget += itemtosell.price
            itemtosell.owner = None
            db.session.commit()
    return redirect(url_for('market_page'))

# @app.route('/market')
# @login_required
# def market_page():
#     if current_user.is_authenticated == True:
#         items = Item.query.all() 
#         return render_template('market.html', items=items)
#     else:
#         return redirect(url_for('login_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data, email = form.email_address.data,
        password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error being registered : {err_msg}')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"You're logged in as: {attempted_user.username}")
            return redirect(url_for('market_page'))
        else:
            flash("Username and password are not match! Please try again!")

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/addtocart', methods="POST")
def addtocart():
    

@app.route('/addTocart/<int:itemId>', methods=['POST'])
def market_pagee(itemId):
    items = Item.query.filter_by(id=itemId)
    return render_template('market.html', items=items)