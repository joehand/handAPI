from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

from .api import FitbitAPI
from ..api_views import registerAPIViews
from ...user import User

fitbit = Blueprint('fitbit', __name__, url_prefix='/fitbit')
bp = fitbit

bp.api = FitbitAPI()
bp.oauth = bp.api.oauth_app

registerAPIViews(bp)

@bp.route('/user')
@login_required
def get_user():
    """ Get user info from FitbitAPI
        https://wiki.fitbit.com/display/API/API-Get-User-Info
        GET /<api-version>/user/<user-id>/profile.<response-format>
    """
    resp = bp.oauth.request('/%s/user/-/profile.json' % bp.api.api_version)
    # TODO: this isn't sending the oauth token so we are not getting real user info
    if resp.status == 200:
        return jsonify(resp.data)
    else:
        return jsonify(resp.data)