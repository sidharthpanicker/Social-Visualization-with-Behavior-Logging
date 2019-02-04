from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup', views.signup, name='signup'),
    url(r'^viewUserProfile', views.viewUserProfile, name='viewUserProfile'),
    url(r'^viewposts', views.viewPosts, name='viewPosts'),
    url(r'^analyticsView', views.analyticsView, name='analyticsView'),
    url(r'^barchart', views.barchart, name='barchart'),
    url(r'^groupMouseClicksAndSendJson', views.groupMouseClicksAndSendJson,
        name='groupMouseClicksAndSendJson'),
    url(r'^saveMouseMovements', views.saveMouseMovements, name='saveMouseMovements'),
    url(r'^getMouseMovements', views.getMouseMovements, name='getMouseMovements'),
    url(r'^saveMouseClicks', views.saveMouseClicks, name='saveMouseClicks'),
    url(r'^getGeneralClickCount', views.getGeneralClickCount,
        name='getGeneralClickCount'),
    url(r'^saveMouseScrolls', views.saveMouseScrolls, name='saveMouseScrolls'),
    url(r'^post/new/', views.addNewPost, name='addNewPost'),
    url(r'^post/(?P<pk>\d+)/edit/', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/comment/',
        views.add_comment_to_post, name='add_comment_to_post'),
    url('', views.viewPosts, name='viewPosts'),
]
