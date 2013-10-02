from flask import (Blueprint, render_template, jsonify, request)

from ..tasks import add

frontend = Blueprint('frontend', __name__, url_prefix='')

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/test')
def hello_world(x=16, y=16):
    x = int(request.args.get("x", x))
    y = int(request.args.get("y", y))
    res = add.apply_async((x, y))
    context = {"id": res.task_id, "x": x, "y": y}
    result = "add((x){}, (y){})".format(context['x'], context['y'])
    goto = "{}".format(context['id'])
    return jsonify(result= result, goto=goto) 

@frontend.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)