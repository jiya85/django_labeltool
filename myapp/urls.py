from django.urls import path
from . import views



urlpatterns = [
    path('transcribe/<transwalk_ASRid>', views.labeltool, name='transcribe'),
    path('list/', views.audioList, name='list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('account/', views.account, name='account'),
    path('', views.home, name='home'),
]

