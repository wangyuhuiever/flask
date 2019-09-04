# -*- coding: utf-8 -*-

from app import db
from datetime import datetime
from markdown import markdown
import bleach
from flask import url_for
from app.exceptions import ValidationError
# from . import User


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong',
                      'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'), tags=allow_tags, strip=True))

    def to_json(self):
        json_post = {
            'url': url_for("api.get_post", id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
            'comments': url_for('api.get_post_comments', id=self.id, _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('数据中无文章内容')
        return Post(body=body)

    # @staticmethod
    # def generate_fake(count=100):
    #     from random import seed, randint
    #     import forgery_py
    #
    #     seed()
    #     user_count = User.query.count()
    #     for i in range(count):
    #         u = User.query.offset(randint(0, user_count - 1)).first()
    #         p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
    #                  timestamp=forgery_py.date.date(True),
    #                  author=u)
    #         db.session.add(p)
    #         db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def to_json(self):
        json_post = {
            # 'url': url_for("api.get_post", id=self.id, _external=True),
            # 'body': self.body,
            # 'body_html': self.body_html,
            # 'timestamp': self.timestamp,
            # 'author': url_for('api.get_user', id=self.author_id, _external=True),
            # 'comments': url_for('api.get_post_comments', id=self.id, _external=True),
            # 'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i', 'strong']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'), tags=allow_tags, strip=True))


db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Comment.body, 'set', Comment.on_changed_body)

