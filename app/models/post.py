# -*- coding: utf-8 -*-

from app import db
from datetime import datetime
from markdown import markdown
import bleach
# from . import User


class Post(db.Model):
    ___tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong',
                      'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'), tags=allow_tags, strip=True))

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


db.event.listen(Post.body, 'set', Post.on_changed_body)

