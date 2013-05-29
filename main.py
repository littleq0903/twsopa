import sys,os
sys.path.append(os.path.join(os.path.abspath('.'), 'lib'))
from bottle import route,run,template,default_app

@route('/helloworld')
def index():
    return "hello world"

application = default_app()
