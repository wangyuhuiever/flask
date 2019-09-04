# -*- coding: utf-8 -*-
from . import api
from app import db
from app.models import User
from flask import request, g, jsonify, url_for, current_app
from .authentication import auth
from .errors import forbidden
from .decorators import permission_required


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

