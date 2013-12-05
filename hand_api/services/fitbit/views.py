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
def get_user():
    """ Get user info from FitbitAPI
        https://wiki.fitbit.com/display/API/API-Get-User-Info
        GET /<api-version>/user/<user-id>/profile.<response-format>
    """
    user_id = str(current_user.get('services')[bp.name]['encoded_user_id'])
    user = bp.oauth.request('/%s/user/%s/profile.json' % (bp.api.api_version, user_id))
    # TODO: this isn't sending the oauth token so we are not getting real user info
    if user.status == 200:
        return jsonify(user.data)
    else:
        return user.data