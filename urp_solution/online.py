from ddddocr import DdddOcr
from pandas import read_html
from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import quote


def get_session(username, password):
    session = Session()

    login_url = "http://192.168.16.209/loginAction.do"

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': login_url
    }

    vchart_link = "http://192.168.16.209/validateCodeAction.do?" 
    vchart_response = session.get(vchart_link, headers=headers)
    ocr = DdddOcr(use_gpu=False)
    result = ocr.classification(vchart_response.content)

    payload = {
        'zjh': username,
        'mm': password,
        'v_yzm': f'{result}',
    }

    response = session.post(login_url, data=payload, headers=headers)

    return response, session


def get_grades(session):
    info = session.get("http://192.168.16.209/menu/top.jsp#")
    name = read_html(info.text)[0].iloc[0, 0].split(")")[0].split("(")[-1]

    result_dict = {'courseName': [], 'courseAttr': [], 'coursePoints': [], 'courseGrades': []}
    grades = session.get("http://192.168.16.209/gradeLnAllAction.do?type=ln&oper=qbinfo")
    gradesTable = read_html(grades.text)

    for index in range(10, len(gradesTable), 6):
        tmp_frame = gradesTable[index].iloc[:, [2, 4, 5, 7]]
        tmp_frame.columns = ['课程名', '学分', '课程属性', '成绩']  # 给列命名（你可改成你自己喜欢的顺序）

        for i, row in tmp_frame.iterrows():
            result_dict['courseName'] = result_dict.get('courseName') + [str(row['课程名'])]
            result_dict['courseAttr'] = result_dict.get('courseAttr') + [str(row['课程属性'])]
            result_dict['coursePoints'] = result_dict.get('coursePoints') + [str(row['学分'])]
            result_dict['courseGrades'] = result_dict.get('courseGrades') + [str(row['成绩'])]

        result_dict['courseName'] = result_dict.get('courseName') + ['-']
        result_dict['courseAttr'] = result_dict.get('courseAttr') + ['-']
        result_dict['coursePoints'] = result_dict.get('coursePoints') + ['-']
        result_dict['courseGrades'] = result_dict.get('courseGrades') + ['-']

    return name, result_dict


def get_credits(session) -> dict:
    result_dict = {'courseName': [], 'courseAttr': [], 'coursePoints': [], 'courseGrades': []}

    credits = session.get("http://192.168.16.209/gradeLnAllAction.do?oper=queryXfjd")
    creditsTable = read_html(credits.text)

    for i, row in creditsTable[11].iterrows():
        result_dict['courseName'] = result_dict.get('courseName') + [str(row['学年学期'])]
        result_dict['courseAttr'] = result_dict.get('courseAttr') + [str(row['学分绩点'])]
        result_dict['coursePoints'] = result_dict.get('coursePoints') + [str(row['学位绩点'])]
        result_dict['courseGrades'] = result_dict.get('courseGrades') + [str(row['加权学分学位绩点'])]

    return result_dict


def evaluateInfoShow(session):
    result_dict = {'term': [], 'courseTeacher': [], 'courseName': [], 'evualuation': []}

    evaluation = session.get("http://192.168.16.209/jxpgXsAction.do?oper=listWj")
    evaluationTable = read_html(evaluation.text)[4]

    for i, row in evaluationTable.iterrows():
        result_dict['term'] = result_dict.get('term') + [str(row['问卷名称'])]
        result_dict['courseTeacher'] = result_dict.get('courseTeacher') + [str(row['被评人'])]
        result_dict['courseName'] = result_dict.get('courseName') + [str(row['评估内容'])]
        result_dict['evualuation'] = result_dict.get('evualuation') + [str(row['是否已评估'])]

    return result_dict


def evaluate(session):
    response = session.get("http://192.168.16.209/jxpgXsAction.do?oper=listWj")
    response.encoding = 'gb2312'
    doc = BeautifulSoup(response.text, 'html.parser')
    imgs = [x for x in doc.find_all(name="img") if x.get("title") == "评估"]
    for img in imgs:
        n = img.get("name").split("#@")
        playload = {
            "wjbm": n[0],
            "bpr": n[1],
            "pgnr": n[5],
            "oper": "wjpg",
            "0000000005": "20_1",
            "0000000007": "0_0",
            "0000000008": "0_0",
            "0000000011": "0_0",
            "0000000012": "0_0",
            "0000000013": "0_0",
            "0000000018": "5_1",
            "0000000019": "0_0",
            "0000000014": "0_0",
            "0000000006": "20_1",
            "0000000002": "5_1",
            "0000000003": "10_1",
            "0000000017": "10_1",
            "0000000020": "20_1",
            "0000000015": "5_1",
            "0000000016": "5_1",
            "zgpj": "",
            "xumanyzg": "zg"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0 Safari/537.36",
            "Referer": "http://192.168.16.209/jxpgXsAction.do?oper=wjpg"
        }

        link1 = f"http://192.168.16.209/jxpgXsAction.do?wjbm={n[0]}&bpr={n[1]}&pgnr={n[5]}&oper=wjShow&wjmc={quote(n[3], encoding='gb2312')}&bprm={quote(n[2], encoding='gb2312')}&pgnrm={quote(n[4], encoding='gb2312')}&wjbz=&pageSize=20&page=1&currentPage=1&pageNo="
        session.get(link1, headers=headers)

        link = f"http://192.168.16.209/jxpgXsAction.do?"
        response = session.post(link, data=playload, headers=headers)

    return response
