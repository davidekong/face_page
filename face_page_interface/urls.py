from unicodedata import name
from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.signup, name='signup'), 
    path('dashboard/<pk>', views.dashboard, name='dashboard'),
    path('reg_bio/', views.reg_bio, name='reg_bio'), 
    path('login/', views.logIn, name="logIn"), 
    path('forgot_password/', views.forgot_password, name='forgot_password'), 
    path('change_password/<pk>', views.change_password, name='change_password'),
    path('make_post/<pk>', views.make_post, name='make_post'), 
    path('home/<pk>', views.home, name="home"), 
    path('post/<pk>', views.post, name='post'),
    path('delete1/<pk>', views.delete1, name='delete1')
]
