# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.join(os.path.abspath('.'), 'lib'))
from bottle import route,run,template,default_app,jinja2_view
from bottle import request,response,abort
import bottle

from google.appengine.ext import db

import time


api = lambda x: '/api/' + x.lstrip('/')

""" Models """
class Activity(db.Model):
    # need to be filled
    str_from = db.StringProperty()
    str_subject = db.StringProperty()
    
    bool_star_activity = db.BooleanProperty(default=False)

    # automatically generated
    auto_create_time = db.DateTimeProperty(auto_now_add=True)

    def to_json(self):
        return {
                'id': str(self.key()),
                'from': self.str_from,
                'subject': self.str_subject,
                'star_activity': self.bool_star_activity,
                'create_time': time.mktime(self.auto_create_time.timetuple())
                }



""" Request Handlers """
# GET /acitivity/<id>/
@route(api('/activity/<obj_id>/'), method=['GET'])
def get_activity(obj_id=None):
    if not obj_id:
        abort(404, "activity not found")

    obj_key = db.Key(obj_id)

    q = Activity.all()
    q.filter('__key__ =', obj_key)
    result = q.get()

    return result.to_json()



# POST /activity
@route(api('/activity/'), method=['POST'])
def post_activity():
    forms = request.forms
    activity_params = {
        'str_from': forms.getunicode('from'),
        'str_subject': forms.getunicode('subject'),
        'bool_star_activity': True if forms.getunicode('star_activity') == 'true' else False
        }

    new_activity = Activity(**activity_params)
    new_activity.put()

    return new_activity.to_json()
    



application = default_app()
bottle.run(server='gae', app=application, debug=True)
