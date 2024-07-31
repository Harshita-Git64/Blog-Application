from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages
import re 
#EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
#EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[gmail]+.[com])"
EMAIL_REGEX = r"([a-zA-Z0-9]+@[gmail]+.[com])"


def blog(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "blog.html", {'posts':posts})

def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','')
        blog_id =request.POST.get('blog_id','')
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
    return render(request, "blog_comments.html", {'post':post, 'comments':comments})

def Delete_Blog_Post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts':posts})

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=BlogPost.objects.none()
    else:
        allPostsTitle= BlogPost.objects.filter(title__icontains=query)
        allPostsContent =BlogPost.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'search.html', params)

@login_required(login_url = '/login')
def add_blogs(request):
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html",{'obj':obj, 'alert':alert})
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image']


def Register(request):
    
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if len(username)<5: #username should be under 10 characters
            messages.error(request, " Username must be under 5 character")
            return redirect('register')

        if not username.isalnum(): #username should be alphanumeric
            messages.error(request, " User name should contain letters and numbers")
            return redirect('register')
        
        '''if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]',username):
            messages.error(request,"Username must contain atleast one special symbol")
            return redirect("register")'''

        if email and not re.match(EMAIL_REGEX, email):#username should have valid email id.
            messages.error(request, " invalid email address ")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if not re.findall('\d', password2):
           messages.error(request,"The password must contain at least 1 digit, 0-9.")
           return redirect('register')

        elif not re.findall('[A-Z]' and '[a-z]', password2):   
            messages.error(request,"The password must contain at least 1 uppercase and 1 lowercase letter")
            return redirect('register')
        elif len(password2)<5: 
            messages.error(request,"Your password must contain at least 5 characters")
            return redirect('register')   
        
        elif not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password2):
            messages.error(request,"Your password must contain at least 1 special symbol")
            return redirect('register')   

        if User.objects.filter(username=username).exists():
            messages.error(request, "username already exists. try to register with different username")
            return redirect('register')    
        
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, " Your account has been successfully created!! Please proceed to login..")
        return redirect('login') 
   
    return render(request, "register.html")

def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request,username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:

            messages.error(request, "Invalid Credentials! please try again")
            return redirect('/') 
            
    return render(request, "login.html")




def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')