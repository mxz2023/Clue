from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from apps.mxz_userinfo.models import MxzUser


def user_reg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            msg = '用户已存在'
        else:
            d = dict(username=username, password=password, is_staff=1, is_active=1, is_superuser=1)
            user = User.objects.create_user(**d)
            msg = '注册成功'
        return HttpResponse(msg)
    else:
        return HttpResponse('请求失败')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            # authenticate()函数用于验证用户的用户名和密码是否正确
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    # login()函数用于登录用户
                    login(request, user)
                    msg = '登录成功'
                else:
                    msg = '用户未激活'
            else:
                msg = '密码错误'
        else:
            msg = '用户不存在'
        return HttpResponse(msg)
    else:
        return HttpResponse('请求失败')


def user_logout(request):
    if request.method == 'POST':
        logout(request)
    else:
        return HttpResponse('请求失败')


def user_index(request):
    users = MxzUser.objects.all()
    return HttpResponse(users)