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

from io import BytesIO
from openpyxl import Workbook
import base64

def get_base64_by_res(res):
    wb = Workbook()
    sheet = wb.active

    sheet['A1'] = 'Источник'
    for k, public in enumerate(res, start=2):
        sheet[f'A{k}'] = public['info']['name']

    sheet['B1'] = 'Лайки'
    for k, public in enumerate(res, start=2):
        sheet[f'B{k}'] = public['info']['likes']

    sheet['C1'] = 'Комменатрии'
    for k, public in enumerate(res, start=2):
        sheet[f'C{k}'] = public['info']['comments']

    sheet['D1'] = 'Репосты'
    for k, public in enumerate(res, start=2):
        sheet[f'D{k}'] = public['info']['reposts']

    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        # Since Openpyxl 2.6, the column name is  ".column_letter" as .column became the column number (1-based)
        for cell in col:
            try:  # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        sheet.column_dimensions[column].width = adjusted_width

    virtual_workbook = BytesIO()
    wb.save(virtual_workbook)

    base64Str = base64.b64encode(virtual_workbook.getvalue())
    return base64Str

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
class VKDataViewXLSX(View):
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
                            base64 = get_base64_by_res(res)

                            return JsonResponse({'base64': base64.decode(), 'ok': True})
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

@method_decorator(csrf_exempt, name='dispatch')
class VKDataAnalytics(View):
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

                            if res != []:

                                sorted_by_likes = sorted(res, key=lambda k: k['info']['likes'], reverse=True)
                                sorted_by_comments = sorted(res, key=lambda k: k['info']['comments'], reverse=True)
                                sorted_by_reposts = sorted(res, key=lambda k: k['info']['reposts'], reverse=True)

                                k_likes = 5
                                k_comments = 10
                                k_reposts = 100

                                sorted_by_importanse = sorted(res,
                                                              key=lambda k: k['info']['likes'] * k_likes + k['info'][
                                                                  'comments'] * k_comments + k['info'][
                                                                                'reposts'] * k_reposts,
                                                              reverse=True)


                                analytic_data = {
                                    'mostly_commented': sorted_by_comments[0],
                                    'mostly_reposted': sorted_by_reposts[0],
                                    'mostly_liked': sorted_by_likes[0],
                                    'top': sorted_by_importanse[0: int(len(sorted_by_importanse) * 0.3)]
                                }

                                return JsonResponse({'analytics': analytic_data, 'ok': True})

                            else:
                                return JsonResponse({'analytics': [], 'ok': True})
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



