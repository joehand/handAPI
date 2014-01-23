from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

from .api import ReadmillAPI
from ..api_views import registerAPIViews
from ...user import User

readmill = Blueprint('readmill', __name__, url_prefix='/readmill')
bp = readmill

bp.api = ReadmillAPI()
bp.oauth = bp.api.oauth_app

registerAPIViews(bp)

@bp.route('/user')
@login_required
def user():
    if bp.name in current_user.get('services'):
        resp = bp.oauth.get('me')
        return jsonify(resp.data)
    return redirect(url_for('.login'))
