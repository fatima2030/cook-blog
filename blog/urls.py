from django.urls import path
from blog.views import craete_blog_view,edit_blog_view,contact,PostDetailView



app_name = 'blog'

urlpatterns = [
    path("craete/" , craete_blog_view,name="craete"),
    path('<slug>/',PostDetailView.as_view(),name='detail'),

    path('<slug>/edit',edit_blog_view,name="edit"),
    path('contact',contact,name='contact'),





]
