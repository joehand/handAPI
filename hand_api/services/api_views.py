from flask import Blueprint, render_template, url_for, flash, redirect, session, request, jsonify
from flask.ext.security import login_required, current_user

class API_View():

    api = None
    blueprint = None
    name = ''

    def __init__(self, blueprint):
        blueprint = blueprint
        api = blueprint.api
        name = blueprint.name

        print name
        print blueprint.api
    
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
            
        if bp.oauth_type == 'oauth2':
            resp['access_token'] = (resp['access_token'], '') #need to make it a tuple for oauth2 requests

        current_user[bp.name] = resp
        current_user.save()

        flash('You were signed in to %s' % bp.name.capitalize())
        return redirect(url_for('frontend.index'))

    @bp.oauth.tokengetter
    def get_token(token=None):
        if bp.oauth_type == 'oauth2':
            return current_user.get(bp.name, None)['access_token']
        return current_user.get(bp.name, None)['oauth_token']
        