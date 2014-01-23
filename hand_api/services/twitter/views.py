from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

from .api import TwitterAPI
from ..api_views import registerAPIViews
from ...user import User

twitter = Blueprint('twitter', __name__, url_prefix='/twitter')
bp = twitter

bp.api = TwitterAPI()
bp.oauth = bp.api.oauth_app

registerAPIViews(bp)

@bp.route('/user')
@login_required
def user():
    if bp.name in current_user.get('services'):
        data = {'user_id': current_user.get('services')[bp.name]['user_id']}
        resp = bp.oauth.get('users/show.json', data=data)
        return jsonify(resp.data)
    return redirect(url_for('.login'))
