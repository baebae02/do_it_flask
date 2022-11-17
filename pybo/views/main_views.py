from flask import Response, jsonify, request, Blueprint, url_for, render_template, current_app
from werkzeug.utils import redirect
from pybo.models import Major, CreditUser
from pybo import db

import json

bp = Blueprint('main', __name__, url_prefix='/')

def serialize(self):
    return {
            'id': self.id, 
            'code': self.code, 
            'dept_nm': self.dept_nm, 
            'up_nm': self.up_nm, 
            'up_code': self.up_code,
            'colg' : self.colg,
            }


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    current_app.logger.info("INFO 레벨로 출력")
    return {'msg': 'hello'}
    #return redirect(url_for('question._list'))


@bp.route('/search')
def search():
    kw = request.args.get('kw', type=str, default='')
    answer = []
    global department_list
    if kw:
        search = '%%{}%%'.format(kw)
        department_list = Major.query.filter(Major.dept_nm.like(search)).all()
        for i in department_list:
            dept = {}
            dept['id'] = i.id
            dept['code'] = i.code
            dept['dept_nm'] = i.dept_nm
            dept['up_nm'] = i.up_nm
            dept['colg'] = i.colg
            answer.append(dept)
            print(answer)
    return json.dumps({'result': [x.dept_nm for x in department_list]},ensure_ascii=False, default=str).encode('utf8')


@bp.route('/credit_signin', methods=['POST'])
def credit_login():
    nickname = request.args.get('nickname', type=str, default='')
    major_req = request.args.get('major', type=str, default='')
    password = request.args.get('password', type=str, default='')

    user = CreditUser.query.filter_by(nickname = nickname).first()

    if user:
        return {'err' : '이미 사용중인 닉네임입니다'}
    else :
        major = Major.query.filter_by(dept_nm = major_req).first()

        if major:
            credit_user = CreditUser(nickname=nickname, major = major, password = password)
            db.session.add(credit_user)
        else:
            return {'err': '잘못된 학과명입니다.'}
    db.session.commit()
    return { 'success' : '회원가입이 성공적으로 완료되었습니다'}


@bp.route('/credit_login', methods=['GET'])
def credit_signin():
    nickname = request.args.get('nickname', type=str, default='')
    password = request.args.get('password', type=str, default='')

    user = CreditUser.query.filter_by(nickname = nickname).first()
    if user:
        if user.password == password:
            return { 'msg' : '로그인에 성공했습니다', 'status' : 200 }
        else:
            return { 'msg' : '로그인에 실패했습니다', 'status' : 400 }
    else:
        return { 'msg' : '해당 유저가 존재하지 않습니다', 'status' : 404 }

