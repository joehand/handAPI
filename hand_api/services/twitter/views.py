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