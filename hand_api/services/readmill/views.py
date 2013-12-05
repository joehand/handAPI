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

@readmill.route('/books')
@login_required
def books():
    if current_user.get('readmill', None):
        user_id = str(current_user.get('readmill')['id'])
        books = readmill.api.get('users/%s/readings' % user_id)
        return jsonify(books.data)
    return readmill.api.authorize(callback=url_for('.authorized', _external=True))
