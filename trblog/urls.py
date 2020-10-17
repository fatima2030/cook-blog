"""new URL Configuration

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
from django.contrib import admin
from django.urls import path,include
from account import views
from account.views import home_view,must_auth,home_screen_view

from blog import views

from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings





urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_screen_view,name='home'),

    path('account/', include('account.urls', 'account')),

    path('blog/', include('blog.urls', 'blog')),
    path('must_auth/',must_auth, name="must_auth"),


    #path('activate/<slug:uidb64>/<slug:token>/',views.activate1,name='activate'),

    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),


]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

