from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
    path('',views.home.as_view(), name = 'home'),
    path('posts', views.posts.as_view(), name = 'posts'),
    path('posts/<slug:slug>',views.post_detailsViews.as_view(),name = 'post-detail-page'),
    path('read-later', views.ReadLaterView.as_view(), name = 'read-later'),

]
