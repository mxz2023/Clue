from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from apps.mxz_userinfo.models import MxzUser


@csrf_exempt
def user_reg(request):
    responsesData = {}
    while True:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            nickname = request.POST.get('nickname')

            if username is None or password is None:
                responsesData['msg'] = "用户名或密码为空"
                responsesData['code'] = 1
                break

            if MxzUser.objects.filter(username=username).exists():
                responsesData['msg'] = "用户已存在"
                responsesData['code'] = 2
                break
            else:
                d = dict(username=username, password=password, nickname=nickname, is_staff=1, is_active=1,
                         is_superuser=1)
                user = MxzUser.objects.create_user(**d)
                responsesData['msg'] = "注册成功"
                responsesData['code'] = 0
        else:
            responsesData['msg'] = "请求失败"
            responsesData['code'] = -1
        break

    return JsonResponse(responsesData)


@csrf_exempt
def user_login(request):
    responsesData = {}
    while True:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if username is None or password is None:
                responsesData['msg'] = "用户名或密码为空"
                responsesData['code'] = 1
                break

            if MxzUser.objects.filter(username=username).exists():
                # authenticate()函数用于验证用户的用户名和密码是否正确
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        # login()函数用于登录用户
                        login(request, user)
                        responsesData['msg'] = "登陆成功"
                        responsesData['code'] = 0
                    else:
                        responsesData['msg'] = "用户未激活"
                        responsesData['code'] = 2
                else:
                    responsesData['msg'] = '密码错误'
                    responsesData['code'] = 3
            else:
                responsesData['msg'] = '用户不存在'
                responsesData['code'] = 4
        else:
            responsesData['msg'] = "请求失败"
            responsesData['code'] = -1
        break

    return JsonResponse(responsesData)


@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
    else:
        return HttpResponse('请求失败')


def user_modify(request):
    users = MxzUser.objects.all()
    return HttpResponse(users)
