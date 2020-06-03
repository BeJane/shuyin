"""shuyin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from app1 import views
urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('main', views.main),
    path('personal', views.personal),

    path('first',views.first),
    path('login', views.login),
    path('chapter',views.chapter),
    path('upload',views.upload),
    path('play',views.play),
    path('showchapterthumnum',views.showchapterthumbs),
    path('ccomment',views.ccomment),
    path('acomment',views.acomment),
    path('showaudiothumnum',views.showaudiothumbs),
    path('book',views.book),
    path('adminlogin',views.adminlogin),
    path('search',views.search),
    path('addfeedback',views.addfeedback),
    path('feedback', views.showAll),
    path('deleteAudio', views.deleteAudio),
]
