from flask import current_app as APP


from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)


lift = Blueprint('lift', __name__, url_prefix='/lift')


@lift.route('/')
def lift_upload():
    return dict()
