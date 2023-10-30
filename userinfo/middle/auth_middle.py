# -*- coding: utf-8 -*-
"""
@Time ： 2023/10/31 07:18
@Auth ： 浮生半日闲
@File ： auth_middle.py
@IDE ： PyCharm
@Motto：Code changes Everything

"""


from django.shortcuts import HttpResponse, render, redirect
from django.utils.deprecation import MiddlewareMixin

import re


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        print('AuthMiddleWare::process_request()方法')

        # 白名单
        white_list = ['/login/', '/admin/.*']
        # 获取当前请求的路径
        current_path = request.path
        # 判断当前请求的路径是否在白名单中
        for reg in white_list:
            ret = re.match(reg, current_path)
            if ret:
                return None

        # 判断用户是否登录
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponse("请先登录")
        return None

    def process_exception(self, request, exception):
        return HttpResponse(exception)


    def process_response(self, request, response):
        return response

