'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

from flask import request, redirect, make_response
from app.sso import SSO_Page
import app.SsoEntity.LoginUser as LoginUser

class Signup_Page():

    @classmethod
    def signup_clicked(cls, username, password, email):
        if not isinstance(username, str):
            raise TypeError("username not string.")

        if not isinstance(password, str):
            raise TypeError("password not string")

        if not isinstance(email, str):
            raise TypeError("email not string")

        '''if not isinstance(remember, bool):
            raise TypeError("remember_me not boolean.")'''
        LoginUser.SsoUser.CreateNewUser(user=username, pwd=password, email=email)



