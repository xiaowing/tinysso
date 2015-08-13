'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

from flask import Flask

app = Flask(__name__)

from app import views
