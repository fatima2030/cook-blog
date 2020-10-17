from account import views
from django.conf.urls import url
from django.urls import path


app_name = 'account'


urlpatterns = [
    #path('',views.home_view,name='home'),



    path('signup/',views.usersingup,name='register_user'),
    path('login/',views.Login_view,name='Login'),
    path('logout/',views.logout_view, name="logout"),
    path('account/',views.account_view, name="accountt"),









]


