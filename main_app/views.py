from django.shortcuts import render
from django.views.generic.base import View

from django.http import HttpResponseRedirect

from MongoDB_work import VKRemoteMDB

from django.http import JsonResponse
from .models import TestModel

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json


@method_decorator(csrf_exempt, name='dispatch')
class TestView(View):
    def get(self, request):
        objs = TestModel.objects.all().values()
        data = {
            'test': 'success',
            'test model': list(objs)
        }
        return JsonResponse(data)

    @csrf_exempt
    def post(self, request):
        form = TestModel.objects.create(name=request.POST.get('name'))
        objs = TestModel.objects.all().values()
        data = {
            'test': 'success',
            'test model': list(objs)
        }
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class VKDataView(View):
    def get(self, request):
        try:
            app_id = request.GET.get('app_id', None)
            login = request.GET.get('login', None)
            password = request.GET.get('password', None)

            if login is not None and password is not None:
                db = VKRemoteMDB('Users')
                user = db.find({'login': login})
                print(f'\n\n\n{user}')
                if user != []:
                    user_filed = user[0]
                    if user_filed['password'] == password:
                        if app_id is not None:
                            db = VKRemoteMDB(app_id)
                            res = db.get_all()
                            return JsonResponse({'app_info': res, 'ok': True})
                        else:
                            return JsonResponse({'error': {'msg': 'no \'app_id\' parameter', 'code': 1}, 'ok': False}, status=400)
                    else:
                        return JsonResponse({'error': {'msg': 'wrong login/password', 'code': 4}, 'ok': False},
                                            status=400)
                else:
                    return JsonResponse({'error': {'msg': 'wrong login/password', 'code': 4}, 'ok': False}, status=400)
            else:
                return JsonResponse({'error': {'msg': 'wrong login/password', 'code': 4}, 'ok': False}, status=400)


        except Exception as e:
            return JsonResponse({'error': {'msg': f'{e}', 'code': 0}}, status=400)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        app_id = body['app_id']
        print(app_id)
        db = VKRemoteMDB(app_id)
        res = db.get_all()
        return JsonResponse({'app_info': res})

@method_decorator(csrf_exempt, name='dispatch')
class Registration(View):
    @csrf_exempt
    def post(self, request):
        try:

            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            login = body['login']
            password = body['password']
            if login is not None and password is not None:
                db = VKRemoteMDB('Users')
                user = db.find({'login': login})
                if user == []:
                    db.insert([{'login': login, 'password': password}])
                    return JsonResponse({'status': 'registered', 'ok': True})
                else:
                    return JsonResponse({'error': {'msg': 'already registered', 'code': 101}, 'ok': False}, status=400)
            else:
                return JsonResponse({'error': {'msg': 'wrong login/password', 'code': 4}, 'ok': False}, status=400)
        except Exception as e:
            return JsonResponse({'error': {'msg': f'{e}', 'code': 0}}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class Login(View):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        login = body['login']
        password = body['password']
        db = VKRemoteMDB('Users')
        user = db.find({'login': login})
        if user != []:
            user_filed = user[0]
            if user_filed['password'] == password:
                return JsonResponse({'status': 'registered', 'ok': True})
            else:
                return JsonResponse({'error': {'msg': 'wrong login/password', 'code': 4}, 'ok': False}, status=400)
        else:
            return JsonResponse({'error': {'msg': 'wrong login/password', 'code': 4}, 'ok': False}, status=400)



