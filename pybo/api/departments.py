import json
import xml.etree.ElementTree as ET

from pybo import db
from pybo.models import Major
from time import sleep
import requests

API_KEY = '202109651SZO37412'
YEAR = '2022'
TERM = '20'

res = requests.get('https://wise.uos.ac.kr/uosdoc/api.ApiApiDeptList.oapi', params={
    'apiKey': API_KEY,
})

root = ET.fromstring(res.text)

for result in root:
    # 대학 구분
    if result.tag == 'depList':
        depList = result
    # 소속 구분
    elif result.tag == 'deptDivList':
        deptDivList = result
    # 학부, 과
    elif result.tag == 'subDeptList':
        subDeptList = result

print(subDeptList)
depts = dict()

for list_ in subDeptList:
    for col in list_:
        # 학과 코드
        if col.tag == 'dept':
            dept = col.text
        # 학과명
        elif col.tag == 'dept_nm':
            dept_nm = col.text
        # 소속 대학 
        elif col.tag == 'up_nm':
            up_nm = col.text
        # 소속 대학 코드
        elif col.tag == 'colg':
            colg = col.text
        # 소속 대학 코드
        elif col.tag == 'dept_div':
            dept_div = col.text
        elif col.tag == 'up_dept':
            up_dept = col.text
    dept_info = depts.get(dept, {'depts':list()})
    dept_info['code'] = dept
    dept_info['dept_nm'] = dept_nm
    dept_info['up_nm'] = up_nm
    dept_info['up_dept'] = up_dept
    dept_info['dept_div'] = dept_div
    dept_info['colg'] = colg

    if 210 <= int(dept_info['dept_div']) < 221:
        if '대학' in dept_info['up_nm']:
            depts[f'{dept}'] = dept_info
        print()

with open (f'departments-{YEAR}{TERM}.json', 'wt') as f:
    f.write(json.dumps(depts, ensure_ascii=False))

for i in depts:
    print(depts[i])
    dept = Major(code=depts[i]['code'], dept_nm=depts[i]['dept_nm'], up_nm=depts[i]['up_nm'], up_code=depts[i]['up_dept'], colg=depts[i]['colg'])
    db.session.add(dept)

db.session.commit()


