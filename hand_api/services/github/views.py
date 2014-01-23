from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

from .api import GitHubAPI
from ..api_views import registerAPIViews
from ...user import User

github = Blueprint('github', __name__, url_prefix='/github')
bp = github

bp.api = GitHubAPI()
bp.oauth = bp.api.oauth_app

registerAPIViews(bp)

@bp.route('/user')
@login_required
def user():
    if bp.name in current_user.get('services'):
        resp = bp.oauth.get('user')
        return jsonify(resp.data)
    return redirect(url_for('.login'))
