'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

'''The extension of flask "flask.ext.wtf" needs to be installed first.'''
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, ValidationError
from wtforms.validators import Required

def pwd_length_check(form, field):
    if len(field.data) > 16:
        raise ValidationError('Filed must be less than 16 characters.')

def name_input_check(form, field):
    if len(field.data) > 16:
        raise ValidationError('Filed must be less than 16 characters.')

    if not field.data.isalnum():
        raise ValidationError('Username should only contains alphabets or digits')


class LoginForm(Form):
    userid = TextField('userid', validators = [Required(), name_input_check])
    pwd = PasswordField('pwd', validators = [Required(), pwd_length_check])
    #remember_me = BooleanField('remember_me', default = False)
