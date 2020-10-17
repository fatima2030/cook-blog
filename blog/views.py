from django.shortcuts import render ,redirect ,get_list_or_404, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from blog.models import BlogPost ,Comment
from account.models import Account
from blog.forms import createBlogePostForm,UPdateBlogPost,NewCommentForm
from django.views.generic import DetailView
from django.core.mail import send_mail





def craete_blog_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_auth')

    form = createBlogePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = createBlogePostForm()
    context['form'] = form
    return render(request , 'blog/create_blog.html')





class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/detail_blog.html'
    context_object_name = 'blog_post'
 

    def get_context_data(self,**kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('data_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['form'] = NewCommentForm(instance=self.request.user) 
        return data
    
    def post(self, request, *args,**kwargs):
        new_comment = Comment(cotent=request.POST.get('cotent'), author=self.request.user, post_connected=self.get_object() )
        new_comment.save()

        return self.get(self , request,*args,**kwargs)



def edit_blog_view(request,slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_auth')

    blog_post =get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse('ha your not author of this post ')
    if request.POST:
        form = UPdateBlogPost(request.POST or None , request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj=form.save()
            context['success_messeage'] = "It Updated"
            blog_post=obj
    form=UPdateBlogPost(
        initial={
            "title": blog_post.title,
			"body": blog_post.body,
			"image": blog_post.image,

        }
    )
    context['form'] = form
    return render(request, 'blog/edit_blog.html', context )



def contact(request):

    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']
        

        send_mail(
            message_name,
            message,
            message_email,
            ['fatimhalbshir@gmail.com'],


        )
        return render(request,'contact.html',{'message_name':message_name})

    else:
        return render(request,'blog/contact.html',{})



