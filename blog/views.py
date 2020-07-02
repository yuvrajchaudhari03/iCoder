from django.shortcuts import render, HttpResponse , redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request,'blog/blogHome.html',context)

def blogPost(request,slug):
    posts = Post.objects.filter(slug=slug).first()
    posts.views = posts.views +1
    posts.save()
    comments = BlogComment.objects.filter(post=posts, parent=None)
    replies = BlogComment.objects.filter(post=posts).exclude(parent=None)
    repDict={}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno]=[reply]
        else:
            repDict[reply.parent.sno].append(reply)
    context = {'posts':posts,'comments':comments, 'user': request.user, 'repDict':repDict}
    return render(request,'blog/blogPost.html',context)

def postComment(request):
    if request.method=="POST":  
        comment= request.POST.get("comment")
        user= request.user
        postSno= request.POST.get("postSno")
        post= Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno=="":
            comment = BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request, "Your comment has been posted succesfully!")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment,user=user,post=post, parent=parent)

            comment.save()
            messages.success(request, "Your reply has been posted succesfully!")

    return redirect(f"/blog/{post.slug}")

    