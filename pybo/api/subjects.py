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
    if result.tag == 'deptList':
        deptList = result
    elif result.tag == 'deptDivList':
        deptDivList = result
    elif result.tag == 'subDeptList':
        subDeptList = result

dept_dict = dict()

for list_ in deptDivList:
    for col in list_:
        if col.tag == 'dept':
            dept = col.text
            # 'A200000100'
        elif col.tag == 'dept_nm':
            dept_nm = col.text
            # '대학'
        elif col.tag == 'up_dept':
            up_dept = col.text
            # 'A000000100'
        elif col.tag == 'dept_div':
            dept_div = col.text
            # '200'
    dept_dict[dept] = {
        'name': dept_nm,
        'up': up_dept,
        'dept_div': dept_div,
        'depts': dict()
    }

depts = dict()
for list_ in deptList:
    for col in list_:
        if col.tag == 'prt_ord':
            prt_ord = col.text
            # '00000'
        elif col.tag == 'dept':
            dept = col.text
            # 'A000000100'
        elif col.tag == 'dept_code_nm':
            dept_code_nm = col.text
            # 'A000000100-서울시립대'
        elif col.tag == 'dept_nm':
            dept_nm = col.text
            # '서울시립대'
        elif col.tag == 'up_nm':
            up_nm = col.text
            # None
        elif col.tag == 'up_dept':
            up_dept = col.text
            # None
        elif col.tag == 'dept_div':
            dept_div = col.text
            # '000'
    dept_info = depts.get(dept, {'depts': list()})
    dept_info['id'] = dept
    dept_info['name'] = dept_nm
    dept_info['div'] = dept_div
    print(dept_info)

    if up_dept:
        if up_dept not in depts:
            depts[f'{up_dept}'] = {'depts': list()}
        depts[f'{up_dept}']['depts'].append(dept_info)
    depts[f'{dept}'] = dept_info

for list_ in subDeptList:
    for col in list_:
        print([col.tag, col.text])

dept_list = list()


def print_dept(dept_path):
    dept = dept_path[-1]
    depth = len(dept_path) - 1
    code = dept['id']
    name = dept['name']
    print(str(depth) + ' ' + ' ' * depth + code + ':' + name)
    if depth >= 2:
        dept_list.append((dept_path[0]['id'][1:6], dept_path[1]['id'], dept_path[-1]['id']))
    for d in dept['depts']:
        print_dept(dept_path + [d])


print_dept([depts['A200000100']])
print_dept([depts['A300000100']])
subjects = list()

# 전공
for deptDiv, dept, subDept in dept_list:
    sleep(0.2)
    print(deptDiv, dept, subDept)
    res = requests.get('https://wise.uos.ac.kr/uosdoc/api.ApiUcrMjTimeInq.oapi', params={
        'apiKey': API_KEY,
        'year': YEAR,
        'term': f'A{TERM}',
        'deptDiv': deptDiv,
        'dept': dept,
        'subDept': subDept
    })
    root = ET.fromstring(res.text)
    for list_ in root[0]:
        for col in list_:
            if col.tag == 'subject_no':
                subject_no = col.text
            elif col.tag == 'class_div':
                class_div = col.text
            elif col.tag == 'subject_nm':
                subject_nm = col.text
            elif col.tag == 'shyr':
                shyr = col.text
            elif col.tag == 'credit':
                credit = col.text
            elif col.tag == 'prof_nm':
                prof_nm = col.text
            elif col.tag == 'class_nm':
                class_nm = col.text
        subjects.append([subDept, subject_no, class_div, subject_nm, shyr, credit, prof_nm, class_nm])


# 교양
for subjectDiv in ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10']:
    sleep(0.2)
    res = requests.get('https://wise.uos.ac.kr/uosdoc/api.ApiUcrCultTimeInq.oapi', params={
        'apiKey': API_KEY,
        'year': YEAR,
        'term': f'A{TERM}',
        'subjectDiv': subjectDiv,
    })
    root = ET.fromstring(res.text)
    for list_ in root[0]:
        for col in list_:
            if col.tag == 'sub_dept':
                sub_dept = col.text
            elif col.tag == 'subject_no':
                subject_no = col.text
            elif col.tag == 'class_div':
                class_div = col.text
            elif col.tag == 'subject_nm':
                subject_nm = col.text
            elif col.tag == 'shyr':
                shyr = col.text
            elif col.tag == 'credit':
                credit = col.text
            elif col.tag == 'prof_nm':
                prof_nm = col.text
            elif col.tag == 'class_nm':
                class_nm = col.text
        subjects.append([sub_dept, subject_no, class_div, subject_nm, shyr, credit, prof_nm, class_nm])


with open(f'subjects-{YEAR}{TERM}.json', 'wt') as f:
    f.write(json.dumps(subjects, ensure_ascii=False))
