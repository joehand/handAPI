from flask import (Blueprint, render_template, flash, jsonify,
                    request, redirect, url_for)
from flask.ext.security import current_user
from flask.ext.classy import FlaskView, route


from ..utils import validate_date
from models import Post

import json
from datetime import date

writer = Blueprint('writer', __name__, url_prefix='/writr',
                        template_folder='templates', static_folder='static')


class PostView(FlaskView):
    """ Our base ViewClass for any Post related endpoints 
    """
    route_base = '/'

    @route('/', endpoint='index')
    def index(self):
        """ Our main index view
        """
        posts = Post.objects(user_ref=current_user.id)
        return render_template('writer/index.html', posts=posts)

    @route('/today')
    @route('/<post_date>', endpoint='post')
    def get(self, post_date=None):
        """ View for a single post
        """
        today = date.today().strftime('%d-%b-%Y')

        if not post_date:
            post_date = today

        if 'today' in request.path:
            return redirect(url_for('.post', post_date=today))

        try:
            validated_date = validate_date(post_date).strftime('%d-%b-%Y')
        except:
            flash('Please enter a real date')
            return redirect(url_for('.post', post_date=today))

        if validated_date != post_date:
            return redirect(url_for('.post', post_date=validated_date))

        post = Post.objects(date=post_date).first()

        is_today = True if post_date == today else False

        if post is None:
            if is_today:
                # create a new post for today
                post = Post(user_ref=current_user.id)
                post.save()
            else:
                flash('No post for that date')
                return redirect(url_for('.post', post_date=today))

        return render_template('writer/write.html', post=post, is_today=is_today)

    def put(self, id):
        if 'content' in request.data:
            try:
                content = json.loads(request.data)['content']
                post = Post.objects(id=id).first()
                post.content = content
                post.save()
                return jsonify( post.to_dict() )
            except:
                abort(400)
        return abort(400)


#Register our View Classes
PostView.register(writer)

