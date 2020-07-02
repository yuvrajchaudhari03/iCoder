from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post
# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def contact(request):
    
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Please fill the form Correctly')
        else:
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save() 
            messages.success(request, 'Your Message Has been Send Succesfully!')
    return render(request, 'home/contact.html')

def about(request):
    
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(content__icontains=query)
        allPostAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostTitle.union(allPostContent,allPostAuthor)
    if len(allPosts) == 0:
        messages.warning(request, 'No Search Result Found. Please Refine your query.')
    params = {'allPosts':allPosts,'query':query}
    return render(request, 'home/search.html',params)


def handleSignUp(request):
    if request.method=="POST":
        username= request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if len(username) > 10:
            messages.error(request,"Your Username must be under 10 character")
            return redirect('home')
        if not username.isalnum():
            messages.error(request,"Your Username should only contains letters and numbers")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request,"Your Passwords Do Not Match")
            return redirect('home')


        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your iCoder account has been Succesfully created")
        return redirect('home')
    else:
        HttpResponse("404 - Not Found")


def handleLogIn(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home') 
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
            
    return HttpResponse('404 - Not Found')


def handleLogOut(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('home')

