# -*- coding: utf-8 -*-
from . import api
from app.models import Comment, Permission
from flask import request, g, jsonify, url_for, current_app
from .authentication import auth
from .errors import forbidden
from .decorators import permission_required


@api.route('/post/<int:id>/comments')
@auth.login_required
def get_post_comments(id):
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(post_id=id).paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_post_comments', id=id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_post_comments', id=id, page=page+1, _external=True)
    return jsonify({'comments': [comment.to_json() for comment in comments], 'prev': prev, 'next': next, 'count': pagination.total})
