'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

from flask import make_response, jsonify
import app.SsoEntity.SsoToken as Token

class SSO_Api():
    PING_TOKEN = 'TSWC'

    @classmethod
    def ValidateTicket(cls, ticket_id):
        ret = Token.SSOToken.ValidateTicket(ticket_id)
        if ret != None:
            token = ret[0]
            ticket = ret[1]

            validate_result = {
                'valid': True,
                'user': token.UserName,
                'newticket': ticket
            }

            return make_response(jsonify(validate_result))
        else:
            validate_result = {
                'valid': False
            }

            return make_response(jsonify(validate_result))

    @classmethod
    def Ping(cls, token):
        if token != None:
            if isinstance(token, str):
                if token == SSO_Api.PING_TOKEN:
                    return make_response('OK')

        return make_response('NG', 400)



