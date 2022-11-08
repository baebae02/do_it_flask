from pybo import db
from pybo.models import Major
from flask import session
import json

YEAR='2022'
TERM='20'

with open(f'departments-{YEAR}{TERM}.json', 'rt') as f:
    departments = json.loads(f.read())

cnt = 2
for i in departments:
    print(i)
    temp = departments[i]
    #for code, dept_nm, up_nm, up_dept, dept_div, colg in temp:
    #print(code, dept_nm)    
    major = Major(id=cnt, code=temp['code'], dept_nm=temp['dept_nm'], up_nm=temp['up_nm'], up_code=temp['dept_div'], colg=temp['colg'])
    cnt += 1
    print(major.code, major.id, major.dept_nm, major.up_nm, major.colg)
    #db.session.add(major)
#db.session.commit()
