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

@bp.oauth.tokengetter
def get_token(token=None):
    if bp.api.oauth_type == 'oauth2':
        return current_user.get(bp.name, None)['access_token']
    return current_user.get(bp.name, None)['oauth_token']
