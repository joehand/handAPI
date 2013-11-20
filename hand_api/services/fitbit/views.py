from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

from .api import FitbitAPI
from ...user import User

fitbit = Blueprint('fitbit', __name__, url_prefix='/fitbit')

fitbitAPI = FitbitAPI().oauth_app

@fitbitAPI.tokengetter
def get_token(token=None):
    return current_user.get('fitbit', None)['oauth_token']


@fitbit.route('/')
@login_required
def login():
    if current_user.get('fitbit', None):
        return redirect(url_for('frontend.index'))
    return fitbitAPI.authorize(callback=url_for('.authorized', _external=True))


@fitbit.route('/authorized')
@fitbitAPI.authorized_handler
def authorized(resp):
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(url_for('frontend.index'))
        
    current_user.fitbit = resp
    current_user.save()

    flash('You were signed in to Fitbit')
    return redirect(url_for('frontend.index'))
