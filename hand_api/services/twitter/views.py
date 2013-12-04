from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

from .api import TwitterAPI
from ...user import User

twitter = Blueprint('twitter', __name__, url_prefix='/twitter')
bp = twitter

bp.api = TwitterAPI()
bp.oauth = bp.api.oauth_app

@bp.route('/')
@login_required
def login():
    if current_user.get(bp.name, None):
        return redirect(url_for('frontend.index'))
    return bp.oauth.authorize(callback=url_for('.authorized', _external=True))

@bp.route('/authorized')
@bp.oauth.authorized_handler
def authorized(resp):
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(url_for('frontend.index'))
        
    if bp.api.oauth_type == 'oauth2':
        resp['access_token'] = (resp['access_token'], '') #need to make it a tuple for oauth2 requests

    current_user[bp.name] = resp
    current_user.save()

    flash('You were signed in to %s' % bp.name.capitalize())
    return redirect(url_for('frontend.index'))

@bp.oauth.tokengetter
def get_token(token=None):
    if bp.api.oauth_type == 'oauth2':
        return current_user.get(bp.name, None)['access_token']
    return current_user.get(bp.name, None)['oauth_token']