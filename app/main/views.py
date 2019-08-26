# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template, redirect, url_for, session, abort, flash
from flask_login import current_user, login_required
from . import main
from .forms import NameForm, EditProfileForm
from ..models import User
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            session['known'] = False
            return redirect(url_for('auth.register', username=form.name.data))
        else:
            session['known'] = True
        session['name'] = user.username
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False),
                           current_time=datetime.utcnow())


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('个人资料已经更新！')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', user=current_user, form=form)
