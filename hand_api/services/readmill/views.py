from .api import ReadmillAPI
from ...user import User


from flask import Blueprint, render_template, url_for, flash, redirect, session, request, jsonify
from flask.ext.security import login_required, current_user


readmill = Blueprint('readmill', __name__, url_prefix='/readmill')

readmillAPI = ReadmillAPI().oauth_app


@readmillAPI.tokengetter
def get_token(token=None):
    return current_user.get('readmill')['access_token']


@readmill.route('/')
@login_required
def login():
    if current_user.get('readmill', None):
        return redirect(url_for('frontend.index'))
    return readmillAPI.authorize(callback=url_for('.authorized', _external=True))


@readmill.route('/authorized')
@readmillAPI.authorized_handler
def authorized(resp):
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(url_for('frontend.index'))
        
    current_user.readmill = resp
    current_user.save()

    flash('You were signed in to Readmill')
    return redirect(url_for('frontend.index'))

