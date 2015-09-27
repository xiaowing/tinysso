'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

from flask import render_template, flash, redirect, abort, jsonify, send_from_directory, request, make_response
from app import app
from app.sso import SSO_Page
from app.login import Login_Page
from app.forms import LoginForm, SignupForm
from app.api import SSO_Api

import os

@app.route('/')
@app.route('/sso')
def sso():
    try:
        rtnUrl = SSO_Page.sso_loader()
        return redirect(rtnUrl)
        # for test only
        
    except ValueError:
        abort(404)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if form.validate_on_submit():
            return Login_Page.login_clicked(form.userid.data, form.pwd.data)
    except ValueError:
        abort(401)

    return render_template('login.html',
        title = 'Sign In',
        form = form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    try:
        if form.validate_on_submit():
            pass
    except ValueError:
        about(401)

    return render_template('signup.html',
        title = 'Sign Up', 
        form = form)

@app.route('/default')
def default():
    abort(404)

@app.route('/error')
def error():
    abort(404)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# REST API
@app.route('/api/v1.0/validation/<ticket_id>', methods = ['GET'])
def validate_ticket(ticket_id):
    return SSO_Api.ValidateTicket(ticket_id)

@app.route('/api/v1.0/ping', methods = ['GET'])
def ping():
    token = request.args.get('token', '')
    return SSO_Api.Ping(token)




