"""HeaClub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.static import serve

from HeaClub import settings
from HeaClub.settings import MEDIA_ROOT
from users.views import login, RegisterView, LoginView, IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('course/', include('course.urls', namespace='course')),
    path('teacher/', include('teachers.urls', namespace='teacher')),
    path('users/', include('users.urls',namespace='users')),
    path('bbs/', include('bbs.urls', namespace='bbs')),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
