from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.views import View
from flask.ext.security import login_required, current_user


class APIRootView(View):
    decorators = [login_required]
    
    def __init__(self, blueprint):
        self.blueprint = blueprint

    def dispatch_request(self):
        print self.blueprint.name
        if current_user.get(self.blueprint.name, None):
            return redirect(url_for('frontend.index'))
        return self.blueprint.oauth.authorize(callback=url_for('.authorized', _external=True))

class APIAuthorizedView(View):
    decorators = [login_required]

    def __init__(self, blueprint):
        self.blueprint = blueprint

    def dispatch_request(self, resp):
        print self.blueprint.name
        if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(url_for('frontend.index'))
            
        if self.blueprint.api.oauth_type == 'oauth2':
            resp['access_token'] = (resp['access_token'], '') #need to make it a tuple for oauth2 requests

        current_user[self.blueprint.name] = resp
        current_user.save()

        flash('You were signed in to %s' % self.blueprint.name.capitalize())
        return redirect(url_for('frontend.index'))

def registerAPIViews(blueprint):
    root_view = APIRootView.as_view('login', blueprint=blueprint)
    blueprint.add_url_rule('/', view_func=root_view)

    auth_view = blueprint.oauth.authorized_handler(
                        APIAuthorizedView.as_view('authorized', blueprint=blueprint))
    blueprint.add_url_rule('/authorized', view_func=auth_view)

    return blueprint
