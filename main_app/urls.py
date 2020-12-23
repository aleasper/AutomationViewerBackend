from django.urls import path

from . import views

urlpatterns = [
    path('test', views.TestView.as_view()),
    path('vk_data', views.VKDataView.as_view()),
    path('vk_data_xlsx', views.VKDataViewXLSX.as_view()),
    path('vk_data_analytics', views.VKDataAnalytics.as_view()),
    path('vk_data2', views.VKDataView.as_view()),
    path('register', views.Registration.as_view()),
    path('login', views.Login.as_view())
]