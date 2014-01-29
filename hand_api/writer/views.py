from flask import (Blueprint, render_template, flash, jsonify, abort,
                    request, redirect, url_for)
from flask.ext.security import current_user
from flask.ext.classy import FlaskView, route


from ..utils import validate_date
from models import Post, DailyPost, BlogPost

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
        """ Our main index view """
        posts = Post.objects(user_ref=current_user.id)
        return render_template('writer/index.html', posts=posts)

    @route('/today')
    @route('/<post_url>', endpoint='post')
    def get(self, post_url=None):
        """ View for a single post
        """
        today = date.today().strftime('%d-%b-%Y')
        is_today = True if post_url == today else False

        if 'today' in request.path:
            return redirect(url_for('.post', post_url=today))

        post = Post.objects(user_ref=current_user.id, url=post_url).first()

        if post is None:
            try:
                validated_date = validate_date(post_url).strftime('%d-%b-%Y')
            except:
                flash('No post found')
                return redirect(url_for('.post', post_url=today))

            if validated_date != post_url:
                return redirect(url_for('.post', post_url=validated_date))

            if is_today:
                # create a new post for today
                post = DailyPost(user_ref=current_user.id, url=today, kind='Daily')
                post.save()
            else:
                flash('No post found')
                return redirect(url_for('.post', post_url=today))

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

