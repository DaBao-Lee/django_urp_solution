from .online import *
import json, time, os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')

def process(request):   
    return render(request, 'process.html')

def error(request):
    return render(request, 'error.html')

def notallow(request):
    return render(request, 'notallow.html')

@csrf_exempt
def allowance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')

            with open('./urp_solution/static/allows.json', 'r') as f:
                allowList = json.load(f)

            if username in allowList.get('allow_user', []):
                return JsonResponse({"status": "success"})
            elif str(password) == "B11-406":
                allowList['allow_user'].append(username)
                with open('./urp_solution/static/allows.json', 'w') as f:
                    json.dump(allowList, f, indent=4)
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "fail"})
        except Exception as e:
            print(f"Error processing allowance request: {e}")
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "invalid method"})
    

@csrf_exempt
def show_grade(request):
    global session

    username = request.POST.get('username')
    password = request.POST.get('password')
    tmp_flag = 0
    name = "未授权用户"
    file_path = f'./urp_solution/static/{time.strftime("%Y-%m-%d", time.localtime())}.json'
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        users = {}
    else:
        users = json.load(open(file_path, 'r', encoding='utf-8'))

    allows = json.load(open('./urp_solution/static/allows.json', 'r'))
    if not str(username) in allows['allow_user']:
        users[f'{time.time()}'] = {"name": f"{name}", 'username': username, 'password': password,
                                   "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                   "status": "fail"}
        json.dump(users, open(f'{file_path}', 'w', encoding="utf-8"), indent=4, ensure_ascii=False)

        return render(request, 'error.html')

    while True:
        response, session = get_session(username, password)
        if '学分制综合教务' in response.text:
            name, result = get_grades(session)
            users[f'{time.time()}'] = {"name": f"已授权用户 ==> {name}", 'username': username, 'password': password,
                                       "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                       "status": "success"}
            json.dump(users, open(f'{file_path}', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
            break
        else:
            tmp_flag += 1
            if tmp_flag == 10:
                name = "密码错误"
                users[f'{time.time()}'] = {"name": f"已授权用户 ==> {name}", 'username': username, 'password': password,
                                           "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                           "status": "fail"}
                json.dump(users, open(f'{file_path}', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

                return render(request, 'error.html')
    
    results = []
    for i in range(len(result['courseName'])):
        results.append({
            'courseName': result['courseName'][i],
            'courseAttr': result['courseAttr'][i],
            'coursePoints': result['coursePoints'][i],
            'courseGrades': result['courseGrades'][i]
        })

    return render(request, 'process.html', {'results': results})

def show_credits(request):
    result = get_credits(session)
    return JsonResponse(result)

def getEvalInfo(request):
    result = evaluateInfoShow(session)
    return JsonResponse(result)

def startEval(request):
    response = evaluate(session)
    if "评估成功！" in response.text:
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "fail"})
