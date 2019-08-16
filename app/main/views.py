# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template, redirect, url_for, session

from . import main
from .forms import NameForm
from ..models import User


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

