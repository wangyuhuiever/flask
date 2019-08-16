# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                              Regexp(
                                                  '^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能有下划线，数字，字母'
                                              )])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='两次输入的密码必须一致')])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('当前邮箱已注册!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('当前用户名已被注册！')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired()])
    new_password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('new_password', message='两次输入的新密码必须一致')])
    submit = SubmitField('提交')
