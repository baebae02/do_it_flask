import functools
import json
from datetime import datetime

from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import (
    Unauthorized, Forbidden, NotFound, BadRequest, Conflict
)
from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


def serializeUser(self):
    return {
        'username': self.username,
        'password': self.password,
        'email': self.email,
        'phone': self.phone,
        'nickname': self.nickname,
        'baekjoon': self.baekjoon
    }


@bp.route('/signup', methods=['POST'])
def signup():
    form = json.loads(request.data)
    print(form['username'])
    user = User.query.filter_by(username=form['username']).first()
    if not user:
        user = User(username=form['username'],
                    password=generate_password_hash(form['password1']),
                    email=form['email'],
                    phone=form['phone'],
                    nickname=form['nickname'],
                    baekjoon=form['baekjoon'])
        db.session.add(user)
        db.session.commit()
        return json.dumps({'user_id': user.id, 'user_name': user.username})
    else:
        flash('이미 존재하는 사용자입니다.')
        raise Conflict
    #return json.dumps({'user_id': user.id, 'user_name': user.username})
    raise BadRequest
    #return render_template('auth/signup.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = json.loads(request.data)
    if request.method == 'POST':
        error = None
        user = User.query.filter_by(username=form['username']).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form['password']):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session['username'] = form['username']
            print(session['username'])
            return jsonify({'result': 'success', 'username': form['username']})
        flash(error)
        return jsonify({'result': 'fail', 'msg': error})

    return {'result': 'fail', 'msg': 'method is not post'}


@bp.route('/logout')
def logout():
    #session.clear()
    if 'username' in session:
        print(session['username'])
        session.pop('username', None)
        return {'result': 'success', 'msg': '로그아웃 되었습니다.'}
    return {'result': 'fail', 'msg': '이미 로그아웃 되어있습니다.'}


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view
