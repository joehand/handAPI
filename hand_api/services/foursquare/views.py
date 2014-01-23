from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

import time

from .api import FoursquareAPI
from ..api_views import registerAPIViews
from ...user import User

foursquare = Blueprint('foursquare', __name__, url_prefix='/foursquare')
bp = foursquare

bp.api = FoursquareAPI()
bp.oauth = bp.api.oauth_app

registerAPIViews(bp)

@bp.route('/user')
@login_required
def get_user():
    """ Get user info from FoursquareAPI
        https://developer.foursquare.com/docs/users/users
        GET https://api.foursquare.com/v2/users/USER_ID OR users/self for authenticated user
    """
    data = { 'oauth_token' : bp.oauth.get_request_token()[0], 
             'v' : time.strftime("%Y%m%d")
            }
    resp = bp.oauth.request('/%s/users/self/' % bp.api.api_version, data=data)
    if resp.status == 200:
        return jsonify(resp.data)
    else:
        return jsonify(resp.data)