from datetime import date
from typing import Any
from django.urls import reverse
from django.http import HttpResponseRedirect  
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Post , Author, Comment
from django.views.generic import ListView,DetailView
from .forms import CommentForm
from django.views import View



# def get_date(post):
#     return post['date']

# Create your views here.






# def home(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     # sorted_posts =sorted(all_posts,key=get_date)
#     # latest_posts = sorted_posts[-3:]
#     return render(request,"blog/index.html",{
#         "posts": latest_posts
#     })

class home(ListView):
    template_name = "blog/index.html"
    model = Post
    order = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset =  super().get_queryset()
        data = queryset[:3]
        return data




# def posts(request):
#     return render(request,"blog/all-posts.html",{
#         "all_posts":Post.objects.all()
#     })

class posts(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class post_detailsViews(View):
    # template_name = "blog/post-detail.html" 
    # model = Post

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["comment_form"] = CommentForm()
    #     return context
    
    def get(self,request,slug):
        post = Post.objects.get(slug = slug)
        context = {
            "post":post,
            "comment_form": CommentForm(),
            "comments" : post.comments.all().order_by("-id")
        }
        return render(request,"blog/post-detail.html",context)
    
    def post(self,request,slug):
        post = Post.objects.get(slug = slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit = False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args = [slug]))
        context = {
            "post":post,
            "comment_form": comment_form,
            "comments" : post.comments.all().order_by("-id")
        }

        return render(request,"blog/post-detail.html",context)  


# def post_details(request,slug):
#     identified_post = next(post for post in Post.objects.all() if post.slug==slug)
#     identify_author =  identified_post.author
#     return render(request, "blog/post-detail.html",{"post":identified_post, 'author':identify_author})
    




class ReadLaterView(View):
    def get(self,request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts)==0:
            context["posts"] = [] 
            context["has_posts"] = False 
        else:
            posts = Post.objects.filter(id__in = stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request,"blog/stored_posts.html",context) 



    def post(self,request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")
        
        
