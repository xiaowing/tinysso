'''
@author:    xiaowing
@license:   Apache Lincese 2.0 
'''

from app import app

if __name__ == '__main__':
    app.config.from_object('config')
    app.debug = True    # only for DEBUG!
    app.run()
