'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

from app import app
import settings

if __name__ == '__main__':
    app.config.from_object('config')
    setting = settings.TinyssoSettings()
    app.debug = True    # only for DEBUG!
    app.run(port=setting.getSsoListenPort())
