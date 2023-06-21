from django.urls import path
import django.contrib.admin as admin
from django.contrib.admin import site
from chatbot_app import views

urlpatterns = [
    path('admin', admin.site.urls, name='home'),
    path('home', views.home, name='home'),
    path('main', views.main, name='main'),
    path('get_bot_response/', views.get_bot_response, name='get_bot_response'),
    # path('', views.signupPage, name='signup'),
    # path('login', views.loginPage, name='login'),
    path('logout', views.LogoutPage, name='logout'),
    path('', views.signup, name='signup'),
    path('login', views.login, name='login')
    ]