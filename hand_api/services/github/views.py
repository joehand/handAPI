from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

from .api import GitHubAPI
from ...user import User

github = Blueprint('github', __name__, url_prefix='/github')

githubAPI = GitHubAPI().oauth_app

@githubAPI.tokengetter
def get_github_oauth_token():
    return current_user.get('github', None)['access_token']

@github.route('/')
@login_required
def github_login():
    if current_user.get('github', None):
        return redirect(url_for('frontend.index'))
    return githubAPI.authorize(callback=url_for('.authorized', _external=True))

@github.route('/authorized')
@githubAPI.authorized_handler
def authorized(resp):
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(url_for('frontend.index'))
        
    current_user.github = resp
    current_user.save()

    flash('You were signed in to Github')
    return redirect(url_for('frontend.index'))
