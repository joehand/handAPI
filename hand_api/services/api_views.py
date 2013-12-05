from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.views import View
from flask.ext.security import login_required, current_user


class APILoginView(View):
    """ Login to the API
        Checks whether user has token already,
            otherwise redirects seeks approval then redirects to authorized url
    """
    decorators = [login_required]
    
    def __init__(self, blueprint):
        self.blueprint = blueprint

    def dispatch_request(self):
        if self.blueprint.name in current_user.get('services'):
            return redirect(url_for('frontend.index'))
        return self.blueprint.oauth.authorize(callback=url_for('.authorized', _external=True))

class APIAuthorizedView(View):
    """ Authorized URL
        Visits in second step of OAuth Handshake
        Save access token here
    """
    decorators = [login_required]

    def __init__(self, blueprint):
        self.blueprint = blueprint

    def dispatch_request(self, resp):
        if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(url_for('frontend.index'))
            
        if self.blueprint.api.oauth_type == 'oauth2':
            resp['access_token'] = (resp['access_token'], '') #need to make it a tuple for oauth2 requests

        current_user['services'][self.blueprint.name] = resp
        current_user.save()

        flash('You were signed in to %s' % self.blueprint.name.capitalize())
        return redirect(url_for('frontend.index'))

class APIToken():
    """ Class for OAuthLib to get token
    """
    def __init__(self, blueprint):
        self.blueprint = blueprint

    def get_token(self, token=None):
        if self.blueprint.api.oauth_type == 'oauth2':
            return current_user.get('services')[self.blueprint.name]['access_token']
        return current_user.get('services')[self.blueprint.name]['oauth_token']

def registerAPIViews(blueprint):
    """Register all the necessary default API views

       Some views need decorators for OAuthLib
    """
    login_view = APILoginView.as_view('login', blueprint=blueprint)
    auth_view = blueprint.oauth.authorized_handler(
                        APIAuthorizedView.as_view('authorized', blueprint=blueprint))

    blueprint.add_url_rule('/', view_func=login_view)
    blueprint.add_url_rule('/authorized', view_func=auth_view)

    apiToken = APIToken(blueprint)
    token_getter = blueprint.oauth.tokengetter(apiToken.get_token)

    return blueprint
