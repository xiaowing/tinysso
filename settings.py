'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

import os.path, operator, configparser
import pdb

PG_HOST = 'host'
PG_PORT = 'port'
PG_DATABASE = 'dbname'
PG_USER = 'user'
PG_PWD = 'password'
SSO_PORT = 'listenport'

PGSV_SETTINGS_KEYS = [PG_HOST, PG_PORT, PG_DATABASE, PG_USER, PG_PWD]
SSOSV_SETTINGS_KEYS = [SSO_PORT]
SETTING_MAPPING_DICT = {'pg_server': PGSV_SETTINGS_KEYS, 'sso_server': SSOSV_SETTINGS_KEYS}

class Error(Exception):
    """Base class for settings"""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__

class NoPgsettingSectionError(Error):
    def __init__(self):
        Error.__init__(self, 'No postgres settings in this file.')

    def __repr__(self):
        return self.message

    __str__ = __repr__

class ParseError(Error):
    def __init__(self, innerError):
        if isinstance(innerError, configparser.Error):
            Error.__init__(self, innerError.message)
            self.innerError = innerError
        else:
            Error.__init__(self, "Unexpected error occured during parsing the setting file.")
            self.innerError = innerError

    def __repr__(self):
        return self.innerError.message

    __str__ = __repr__

def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton  

@singleton
class TinyssoSettings(object):
    def __init__(self, settingfile = 'tinysso.ini'):    # TODO: Get to know how to pass the argument when calling the constructor
        self.confile = settingfile
        self.config = configparser.ConfigParser()
        #pdb.set_trace()

        if not os.path.isfile(self.confile):
            raise ParseError(Error("File %s does not exist." %(self.confile)))

        try:
            self.config.read(self.confile)
        except Exception as e:
            raise ParseError(e)

        sec_list = self.config.sections()
        
        # check the sections
        if isinstance(sec_list, list):
            if len(sec_list) == 0:
                raise NoPgsettingSectionError()

        setting_standard_keylist = list(SETTING_MAPPING_DICT.keys())

        if len(setting_standard_keylist) >= len(sec_list):
            for item in sec_list:
                try:
                    setting_standard_keylist.index(item)
                except ValueError as e:
                    raise ParseError(Error("Unrecognised section(s)."))

                for item_element in SETTING_MAPPING_DICT[item]:
                    if not self.config.has_option(item, item_element):
                        raise ParseError(Error("Insufficient option(s)."))
            else:
                if not 'pg_server' in sec_list:
                    raise NoPgsettingSectionError()
        else:
            raise ParseError(Error("Unrecognised section(s)."))

        # check the keys
        for k in SETTING_MAPPING_DICT.keys():

            if self.config.has_section(k):
                element_list = list(self.config[k].keys())
                for element in element_list:
                    if not element in SETTING_MAPPING_DICT[k]:
                        raise ParseError(Error("Unrecognised option(s)."))


    def getConfigPath(self):
        return self.confile

    def getPgHost(self):
        return self.config.get('pg_server', PG_HOST)

    def getPgPort(self):
        return self.config.getint('pg_server', PG_PORT)

    def getPgDatabase(self):
        return self.config.get('pg_server', PG_DATABASE)

    def getPgUser(self):
        return self.config.get('pg_server', PG_USER)

    def getPgUserPassword(self):
        return self.config.get('pg_server', PG_PWD)

    def getSsoListenPort(self):
        if self.config.has_section('sso_server'):
            return self.config.getint('sso_server', SSO_PORT)
        else:
            return 5000

# for unit test.
if __name__ == '__main__':
    print("Test starts....")
    try:
        setting = TinyssoSettings()
        print("%s loaded successfully." %(setting.getConfigPath()))
        print("Host: %s, Port: %d" %(setting.getPgHost(), setting.getPgPort()))
    except Exception as e:
        print(e)
    print("Test ends....")
