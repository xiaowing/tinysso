'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

from app.SsoEntity.db.DBAccess import SSOUserAccess

class SsoUser():
    def __init__(self):
        self.username = ''
        self.usermail = ''

    def GetInfo(self, user, pwd):
        access = SSOUserAccess()
        access.OpenDbConnection()
        res = access.GetUserMail(username=user, password=pwd)
        access.CloseDbConnection()

        if res != None:
            self.username = user
            self.usermail = res
        else:
            # TODO: need to implement the following code with a customized error.
            raise ValueError("No result retrieved from database.")

if __name__ == '__main__':
    user = SsoUser('xiaowing', 'asdf1234')
    print("username = %s, email = %s" %(user.username, user.usermail))
