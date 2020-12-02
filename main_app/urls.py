from django.urls import path

from . import views

urlpatterns = [
    path('test', views.TestView.as_view()),
    path('vk_data', views.VKDataView.as_view())
]