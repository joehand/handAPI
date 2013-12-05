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
