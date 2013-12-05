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