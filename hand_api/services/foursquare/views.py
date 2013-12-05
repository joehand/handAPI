from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)
from flask.ext.security import login_required, current_user

from .api import FoursquareAPI
from ..api_views import registerAPIViews
from ...user import User

foursquare = Blueprint('foursquare', __name__, url_prefix='/foursquare')
bp = foursquare

bp.api = FoursquareAPI()
bp.oauth = bp.api.oauth_app

registerAPIViews(bp)
