from flask import (Blueprint, render_template, jsonify, request)

frontend = Blueprint('frontend', __name__, url_prefix='')

@frontend.route('/')
def index():
    return render_template('index.html')
