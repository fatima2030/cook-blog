from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from account.forms import RegistrationForm ,AccountAuthenticationForm,AccountUpdateForm,ProfileUpadteImageForms
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from account.models import Account
from django.db.models import Q


from operator import attrgetter
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from blog.views import BlogPost


# Create your views here.
def home_view(request):
    context={}

    return render(request,'account/home.html',context)


def usersingup(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['form'] = form

    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'account/singup.html', context)


def Login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form =AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email ,password=password)

            if user:
                login(request,user)
                return redirect('home')
    else :
        form = AccountAuthenticationForm()
    context ['login_form'] = form

    return render(request,"account/login.html", context)





def logout_view(request):
	logout(request)
	return redirect('/')


def must_auth(request):
	return render(request, 'account/must_auth.html', {})


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)
    return list(set(queryset))
	



BLOG_POST_PER_PAGE = 3


def home_screen_view(request,*args, **kwargs):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q' ,'')
        context['query'] = str(query)
    blog_post = sorted(get_blog_queryset(query),key=attrgetter('date_updated'),reverse=True)

    page =request.GET.get('page',1) 
    blog_posts_paginator = Paginator(blog_post,BLOG_POST_PER_PAGE)
    try:
        blog_post=blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_post = blog_posts_paginator.page(BLOG_POST_PER_PAGE)
    except EmptyPage:
        blog_post = blog_posts_paginator.page(blog_posts_paginator.num_pages)
    context['blog_posts']=blog_post
    return render(request, 'account/home.html',context)
    


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
                    "image": request.user.image,
				}
			)

	context['account_form'] = form

	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts

	return render(request, "account/account.html", context)

