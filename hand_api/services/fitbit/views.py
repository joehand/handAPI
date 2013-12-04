from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.views import View
from flask.ext.security import login_required, current_user

from .api import FitbitAPI
from ...user import User

fitbit = Blueprint('fitbit', __name__, url_prefix='/fitbit')
bp = fitbit

bp.api = FitbitAPI()
bp.oauth = bp.api.oauth_app

class APIRootView(View):
    decorators = [login_required]

    def dispatch_request(self):
        if current_user.get(bp.name, None):
            return redirect(url_for('frontend.index'))
        return bp.oauth.authorize(callback=url_for('.authorized', _external=True))

class APIAuthorizedView(View):
    decorators = [login_required]

    def dispatch_request(self, resp):
        if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(url_for('frontend.index'))
            
        if bp.api.oauth_type == 'oauth2':
            resp['access_token'] = (resp['access_token'], '') #need to make it a tuple for oauth2 requests

        current_user[bp.name] = resp
        current_user.save()

        flash('You were signed in to %s' % bp.name.capitalize())
        return redirect(url_for('frontend.index'))


root_view = APIRootView.as_view('login')
bp.add_url_rule('/', view_func=root_view)

auth_view = bp.oauth.authorized_handler(APIAuthorizedView.as_view('authorized'))
bp.add_url_rule('/authorized', view_func=auth_view)


@bp.oauth.tokengetter
def get_token(token=None):
    if bp.api.oauth_type == 'oauth2':
        return current_user.get(bp.name, None)['access_token']
    return current_user.get(bp.name, None)['oauth_token']
    