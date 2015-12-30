'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

import requests, urllib.parse

class Executor():
    PING_API_PATH = "api/v1.0/ping"
    VALIDATE_API_PATH = "api/v1.0/validation"
    SSO_PAGE_PATH = "sso"
    NEGO_TOKEN = "TSWC"

    def __init__(self, ssosv_url, ssocl_returnurl):
        if not isinstance(ssosv_url, str):
            raise TypeError("Incorrect type for ssosv_url.")
        if not isinstance(ssocl_returnurl, str):
            raise TypeError("Incorrect type for ssocl_returnurl.")

        self.__Ssosv_url = ssosv_url
        self.__Ssocl_returnurl = ssocl_returnurl

        if (self.__PingSsoServer() != True):
            raise ValueError("Invalid request format.")

    def GetSsoserverUrl(self):
        return self.__Ssosv_url

    def GetClientReturnUrl(self):
        return self.__Ssocl_returnurl

    def GenerateSsoRedirectUrl(self):
        query = {"returnUrl" : self.__Ssocl_returnurl}
        url = urllib.parse.urljoin(self.__Ssosv_url, Executor.SSO_PAGE_PATH)
        url = url + "?" + urllib.parse.urlencode(query)
        return url

    def ValidateTicket(self, ticket_id):
        if not ticket_id:
            raise ValueError("Ticket must be specified.")

        if isinstance(ticket_id, str):
            apiPath = urllib.parse.urljoin(self.__Ssosv_url, Executor.VALIDATE_API_PATH)
            return Executor.__CallGetRestfulApi(apiPath, parameters = None, ticket = ticket_id)
        else:
            raise TypeError("Ticket must be string.")

    def __PingSsoServer(self):
        pingPath = urllib.parse.urljoin(self.__Ssosv_url, Executor.PING_API_PATH)
        queryValue = {"token": Executor.NEGO_TOKEN}
        r = requests.get(pingPath, params = queryValue)
        if (r.headers['content-type'].startswith("text/html")) and (r.status_code == 200):
            if(r.text == "OK"):
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def __CallGetRestfulApi(cls, url, parameters = None, **queryparams):
        callingurl = url
        if queryparams != None:
            if not isinstance(queryparams, dict):
                raise TypeError("Incorrect type for queryparams.")

        if parameters != None:
            if isinstance(parameters, tuple):
                for element in parameters:
                    callingurl = urllib.parse.urljoin(callingurl, element)
            else:
                if isinstance(parameters, str):
                    callingurl = urllib.parse.urljoin(url, parameters)
        else:
            pass

        if not queryparams:
            r = requests.get(callingurl, params = None)
        else:
            r = requests.get(callingurl, params = queryparams)

        if (r.headers['content-type'].startswith("application/json")) and (r.status_code == 200):
            return r.text
        else:
            return ""
