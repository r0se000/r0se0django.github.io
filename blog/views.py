from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Blog, Comment
from django.core.paginator import Paginator
from django.utils import timezone
from .form import BlogPost
# from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    blogs=Blog.objects
    blog_list=Blog.objects.all()        #블로그 객체 전체
    paginator=Paginator(blog_list, 3)   #블로그 객체를 3개씩 구분
    page= request.GET.get('page')       #request 변수 => page 'page'의 value값에 해당하는 페이지 불러옴
    posts=paginator.get_page(page)      #posts=>paginator로 잘라놓은 묶음
    return render(request, 'home.html', {'blogs':blogs, 'posts':posts})


def detail(request, blog_id):
    details=get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'detail': details}) 

def new(request):
    return render(request, 'new.html')

def create(request):
    if request.method== 'POST' :
        form= BlogPost(request.POST)
        if form.is_valid():
            blog.title=form.save(commit=False)
            blog.body=form.save(commit=False)
            blog.pub_date=timezone.datetime.now()
            blog.save()
            return redirect('/blog/'+ str(blog.id))
    else:
        form=BlogPost()
    return HttpResponse('잘못된 접근')

def edit(request, blog_id):
    blog=get_object_or_404(Blog, pk=blog_id)
    if request.method=="POST":
        form = BlogPost(request.POST, instance=blog)
        if form.is_valid():
            blog.title=form.save(commit=False)
            blog.body=form.save(commit=False)
            blog.pub_date=timezone.datetime.now()
            blog.save()
        return redirect('/blog/'+str(blog.id))
    else: 
        form=BlogPost(instance=blog)
    return render(request,'edit.html',{'blog':blog})

def delete(request, blog_id):
    blog=get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('/')

# @login_required
def comment_add(request, blog_id):
    if request.method=="POST":
        post=Blog.objects.get(pk=blog_id)      #어떤글로 작성했는지 알아야함. 1번글에 썼을때 1번글 찾아줌
        comment=Comment()
        comment.user=request.user
        comment.body=request.POST['body']   #request받은 post message중에 body를 받음.
        comment.post=post

        comment.save()
        return redirect('/blog/'+ str(blog_id) )
    else:
        return HttpResponse("잘못된 접근입니다.")

def comment_edit(request, comment_id):
    comment=get_object_or_404(Comment, pk=comment_id)  #현재 댓글 정보 가져옴
    if request.user==comment.user:           #유효성 검사(user가 같은지)
        if request.method=="POST":     
            comment.body=request.POST['body']
            comment.save()
            return redirect('/blog/'+str(comment.post.id))

        elif request.method=="GET":
            context={
                'comment' : comment
            }
            return render(request, 'comment_edit.html', context)
def comment_delete(request, comment_id):
    comment=get_object_or_404(Comment, pk=comment_id)
    if request.user==comment.user:
        if request.method=="POST":
            post_id=comment.post.id
            comment.delete()
            return redirect('/blog'+str(post_id))
    return HttpResponse('error')
