'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''
import requests, json
from flask import render_template, session, request, redirect, abort, make_response
from app import app
import sys
sys.path.append('..')
import tinyssosdk
from tinyssosdk import tinyssocl


Tinysso_Server="http://localhost:5000/"
Tinysso_Client="http://localhost:56800/index"
Api_Executor = tinyssocl.Executor(Tinysso_Server, Tinysso_Client)

@app.route('/')
@app.route('/index')
def index():
    # check if the session exists.
    if "UserName" in session:
        username = session['UserName']
        display = str("Already signed in. The current user is %s." %(username))
        return render_template("index.html", label = display)
    else:
        if Api_Executor == None:
            executor = tinyssocl.Executor(Tinysso_Server, Tinysso_Client)
        else:
            executor = Api_Executor
        ticket = request.args.get("ticket")
        if ticket != None:
            if isinstance(ticket, str) and ticket != "":
                rtn_json = executor.ValidateTicket(ticket)
                if rtn_json != None and rtn_json != "":
                    result = json.loads(rtn_json)
                    if isinstance(result['valid'], bool) and result['valid'] == True:
                        username = result['user']
                        session['UserName'] = username
                        display = str("Already signed in. The current user is %s." %(username))
                        return render_template("index.html", label = display)
                    else:
                        display = "Hello World!"
                        return render_template("index.html", label = display)

        return redirect(executor.GenerateSsoRedirectUrl())
