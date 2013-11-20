from .api import TwitterAPI
from ...user import User

from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

twitter = Blueprint('twitter', __name__, url_prefix='/twitter')

twitterAPI = TwitterAPI().oauth_app

@twitterAPI.tokengetter
def get_token(token=None):
    return current_user.get('twitter', None)['oauth_token']

@twitter.route('/')
@login_required
def login():
    if current_user.get('twitter', None):
        return redirect(url_for('frontend.index'))
    return twitterAPI.authorize(callback=url_for('.authorized', _external=True))

@twitter.route('/authorized')
@twitterAPI.authorized_handler
def authorized(resp):
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(url_for('frontend.index'))

    current_user.twitter = resp
    current_user.save()

    flash('You were signed in to Twitter as %s' % resp['screen_name'])
    return redirect(url_for('frontend.index'))

