from flask import request, redirect
import urllib.parse
import hashlib
import app.SsoEntity.SsoToken as Token

class SSO_Page():    
    SecurityValidationKey = str(hashlib.md5('TinySSO'.encode(encoding='utf8')).hexdigest())
    FormsAuthCookieName = 'TinySSO.Security'
    AuthTktUserdataDelimiter = '|'

    @classmethod
    def sso_loader(cls):
        if request.method == 'GET':
            returnUrl = request.args.get('returnUrl', '')
            if returnUrl.strip():
                tokenid = SSO_Page.sso_logined()

                if tokenid:
                    if len(tokenid) == 0:
                        raise ValueError()
                    else:
                        '''token = Token.SSOToken(uname)
                        Token.SSOToken.SSOTokenList.append(token)  # QUESTION: tokenID:Username = N : 1?
                        dic = {'tokenid' : str(token.ID)}
                        if returnUrl.find('?') >= 0:
                            splitchr = '&'
                        else:
                            splitchr = '?'
                        
                        rtnUrl = returnUrl + splitchr + urllib.parse.urlencode(dic)
                        return rtnUrl'''

                        token = Token.SSOToken.ValidateTokenid(tokenid)
                        if token != False:
                            ticket = token.AddNewTicket()
                            if not isinstance(ticket, str):
                                raise TypeError("Incorrect data type for ticket.")

                            dic = {'ticket' : ticket}
                            if returnUrl.find('?') >= 0:
                                splitchr = '&'
                            else:
                                splitchr = '?'
                        
                            rtnUrl = returnUrl + splitchr + urllib.parse.urlencode(dic)
                            return rtnUrl
                
                dic = {'returnUrl' : ('/sso?returnUrl='+returnUrl)}
                loginUrl = '/login?' + urllib.parse.urlencode(dic)
                return loginUrl

            else:
                url = '/error'
                return url

    @classmethod
    def sso_logined(cls):
        authCookie = request.cookies.get(SSO_Page.FormsAuthCookieName)
        if authCookie:
            if type(authCookie) == str:
                deliPos = authCookie.find(SSO_Page.AuthTktUserdataDelimiter)
                if deliPos >= 0:
                    scurityStr = authCookie[:deliPos]
                    if scurityStr == SSO_Page.SecurityValidationKey:
                        token = authCookie[(deliPos + 1):]
                    return token
        return None


