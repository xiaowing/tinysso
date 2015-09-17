'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

import uuid, time, threading

lock = threading.Lock()

class SSOToken():
    SSOTokenList = []
    
    def __init__(self):
        self.ID = uuid.uuid1().hex
        self.__authTime = time.time()
        self.Timeout = 60*10    # Timeout: 10minites by default

    def __init__(self, username):
        if type(username) == str:
            self.UserName = username
            self.ID = uuid.uuid1().hex
            self.__authTime = time.time()
            self.Timeout = 60*10    # Timeout: 10minites by default
            self.__tickets = []
        else:
            raise TypeError()

    def GetLocalAuthTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.__authTime))

    def __isTimeout(self):
        # True: timeout
        # False: not timeout
        return (self.__authTime + self.Timeout) < time.time()

    def SetUser(self, username):
        if type(username) == str:
            self.UserName = username
        else:
            raise TypeError()

    def SetLoginID(self, loginId):
        pass

    def AddNewTicket(self):
        new_ticket = uuid.uuid1().hex
        if lock.acquire():
            self.__tickets.append(new_ticket)
            lock.release()
        return new_ticket

    def FindTicket(self, ticket):
        try:
            idx = self.__tickets.index(ticket)
            if idx >= 0:
                return True
            else:
                return False
        except Exception as e:
            return False

    def ReplaceTicket(self, oldTicket):
        try:
            idx = self.__tickets.index(oldTicket)
            if lock.acquire():
                del self.__tickets[idx]
                new_ticket = uuid.uuid1().hex
                self.__tickets.append(new_ticket)
                lock.release()
            return new_ticket
        except Exception as e:
            return None

    @classmethod
    def Find(cls, tokenid):
        for item in SSOToken.SSOTokenList:
            if item.ID == tokenid:
                return item
        else:
            return None

    @classmethod
    def __validateToken(cls, token):
        if token == None:
            raise ValueError("Null reference for token.")

        if not isinstance(token, SSOToken):
            raise TypeError("Incorrect type for token.")

        if not token.__isTimeout():
            return token
        else:
            try:
                if lock.acquire():
                    SSOToken.SSOTokenList.remove(token)
                    lock.release()
            except ValueError as e:
                pass
            finally:
                return False

    @classmethod
    def AddToken(cls, token):
        if token == None:
            raise ValueError("Null reference for token.")

        if not isinstance(token, SSOToken):
            raise TypeError("Incorrect type for token.")

        if lock.acquire():
            SSOToken.SSOTokenList.append(token)
            lock.release()

    @classmethod
    def ValidateTokenid(cls, tokenid):
        if not isinstance(tokenid, str):
            raise TypeError("Incorrect type for tokenid.")

        token = SSOToken.Find(tokenid)
        if token:
            if SSOToken.__validateToken(token):
                return token
        return False

    @classmethod
    def ValidateTicket(cls, ticket):
        for item in SSOToken.SSOTokenList:
            if item.FindTicket(ticket):
                #target_token = item
                if SSOToken.__validateToken(item):
                    target_token = item
                    new_ticket = item.ReplaceTicket(ticket)
                    if new_ticket != None:
                        return (target_token, new_ticket)
                    else:
                        return None
        else:
            return None




# used for unit test.
if __name__ == '__main__':
    token = SSOToken('xiaowing')
    SSOToken.SSOTokenList.append(token)

    tokid = token.ID
    ret = SSOToken.ValidateTokenid(tokid)

    if ret == False:
        print(type(ret))
        print('ret = %s' %(str(ret)))
    else:
        print(type(ret))

    ticket = token.AddNewTicket()
    print(ticket)
    result = SSOToken.ValidateTicket(ticket)

    print(result[0].UserName)
    print(result[1])


    
