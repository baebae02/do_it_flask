import json
import xml.etree.ElementTree as ET

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
    if result.tag == 'deptList':
        deptList = result
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
            # None
    dept_info = depts.get(dept, {'depts': list()})
    dept_info['code'] = dept
    dept_info['dept_nm'] = dept_nm
    dept_info['up_nm'] = up_nm
    dept_info['up_dept'] = up_dept
    dept_info['dept_div'] = dept_div
    dept_info['colg'] = colg

    if 210 <= int(dept_info['div']) <= 221:
        depts[f'{dept}'] = dept_info
    print()

with open(f'departments-{YEAR}{TERM}', 'wt') as f:
    f.write(json.dumps(depts, ensure_ascii=False))
