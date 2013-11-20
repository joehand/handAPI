from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

from .api import FoursquareAPI
from ...user import User

foursquare = Blueprint('foursquare', __name__, url_prefix='/foursquare')

foursquareAPI = FoursquareAPI().oauth_app

@foursquareAPI.tokengetter
def get_token(token=None):
    return current_user.get('foursquare', None)['oauth_token']


@foursquare.route('/')
@login_required
def login():
    if current_user.get('foursquare', None):
        return redirect(url_for('frontend.index'))
    return foursquareAPI.authorize(callback=url_for('.authorized', _external=True))


@foursquare.route('/authorized')
@foursquareAPI.authorized_handler
def authorized(resp):
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(url_for('frontend.index'))
        
    print resp
    current_user.foursquare = resp
    current_user.save()

    flash('You were signed in to Foursquare')
    return redirect(url_for('frontend.index'))
