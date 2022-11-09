from flask import jsonify, request, Blueprint, url_for, render_template, current_app
from werkzeug.utils import redirect
from pybo.models import Major
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
