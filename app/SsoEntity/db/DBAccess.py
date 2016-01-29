'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

import psycopg2
import sys
sys.path.append('...')
import settings

class DbUtil():
    def __init__(self):
        self.conn = None
        self.config = settings.TinyssoSettings()

    def OpenDbConnection(self):
        try:
            self.conn = psycopg2.connect(host = self.config.getPgHost(),
                                         port = self.config.getPgPort(),
                                         database = self.config.getPgDatabase(),
                                         user = self.config.getPgUser(),
                                         password = self.config.getPgUserPassword())
            self.conn.autocommit = True
            return self.conn
        except psycopg2.DatabaseError as dberror:
            # TODO: record the error into log
            return None

    def CloseDbConnection(self):
        if self.conn != None:
            if isinstance(self.conn, psycopg2.extensions.connection):
                self.conn.close()


class SSOUserAccess(DbUtil):
    def __init__(self):
        super().__init__()

    def GetUserMail(self, username, password):
        if self.conn != None:
            if isinstance(self.conn, psycopg2.extensions.connection):
                cur = self.conn.cursor()
                cur.execute("SELECT user_mail FROM m_sch.m_user_auth WHERE user_id=%(user)s AND user_password=%(pass)s AND user_actived=true;",
                    {'user': username, 'pass': password})
                res = cur.fetchone()
                cur.close()
                return res[0]

    def AddUser(self, username, password, email):
        if self.conn != None:
            if isinstance(self.conn, psycopg2.extensions.connection):
                try:
                    cur = self.conn.cursor()
                    cur.execute("INSERT INTO m_sch.m_user_auth (user_id, user_password, user_mail, user_actived) VALUES (%(uname)s, %(pwd)s, %(email)s, true);",
                        {'uname': username, 'pwd': password, 'email': email})
                    cur.close()
                except psycopg2.DatabaseError as dberror:
                    raise dberror