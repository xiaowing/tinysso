'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

import psycopg2

class DbUtil():
    __CONNECTION_STRING = "host=192.168.1.128 port=26500 dbname=postgres user=postgres password=asdf1234"

    def __init__(self):
        self.conn = None

    def OpenDbConnection(self):
        try:
            self.conn = psycopg2.connect(DbUtil.__CONNECTION_STRING)
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