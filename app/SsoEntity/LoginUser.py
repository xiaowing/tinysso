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

    @classmethod
    def CreateNewUser(cls, user, pwd, email):
        access = SSOUserAccess()
        access.OpenDbConnection()
        access.AddUser(username=user, password=pwd, email=email)
        access.CloseDbConnection()

if __name__ == '__main__':
    u = 'xyz'
    p = 'pass1234'
    m = 'test@xyz.com'

    SsoUser.CreateNewUser(user=u, pwd=p, email=m)
    user = SsoUser()
    mail = user.GetInfo(user=u, pwd=p)
    print("mail=%s, assert result=%s" %(mail, (mail == m)))
