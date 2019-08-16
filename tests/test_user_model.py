# -*- coding: utf-8 -*-

import unittest
from app import create_app, db
from app.models import User, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='apple')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='apple')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='apple')
        self.assertTrue(u.verify_password('apple'))
        self.assertFalse(u.verify_password('orange'))

    def test_password_salts_are_random(self):
        u = User(password='apple')
        u2 = User(password='apple')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='729265425@qq.com', username='admin', password='apple')
        self.assertTrue(u.can(Permission.ADMINISTER))

        u2 = User(email='wangyuhui@163.com', username='user', password='orange')
        self.assertFalse(u2.can(Permission.MODERATE_COMMENTS))
        self.assertTrue(u2.can(Permission.WRITE_ARTICLES))
        self.assertTrue(u2.can(Permission.COMMENT))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
