from django.shortcuts import render
from django.views.generic.base import View

from django.http import HttpResponseRedirect

from MongoDB_work import VKRemoteMDB

from django.http import JsonResponse
from .models import TestModel

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
        app_id = request.POST.get('app_id')
        db = VKRemoteMDB(app_id)
        res = db.get_all()
        return JsonResponse({'app_info': res})