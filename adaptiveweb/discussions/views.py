# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, MouseClicks, userLoginInfo
from .forms import PostForm, CommentForm
from django.utils import timezone
import json
import os.path
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
from django.core import serializers
from django.db.models import Count
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import csv


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return viewUserProfile(request)
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def viewPosts(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, 'viewPosts.html', {'posts': posts, 'comments': comments})


def viewUserProfile(request):
    loginInfo = userLoginInfo.objects.filter(author=request.user)
    return render(request, 'profile.html', {'loginInfo': loginInfo})


def analyticsView(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, 'analyticsView.html', {'posts': posts, 'comments': comments})


def barchart(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, 'analyticsView2.html', {'posts': posts, 'comments': comments})


def addNewPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return(viewPosts(request))
    else:
        form = PostForm()
        return render(request, 'addPost.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return(viewPosts(request))
    else:
        form = PostForm(instance=post)
        return render(request, 'editPost.html', {'form': form})


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return(viewPosts(request))
    else:
        form = CommentForm()
    return render(request, 'add_ctp.html', {'form': form})


def saveMouseMovements(request):
    if request.method == "POST":
        jsondata = {}
        user = request.user
        data = request.POST[u'mousemovements']
        jsondata = json.loads(data)
        filename = "logs/mousemovements/" + str(user) + ".json"
        appendToJsonFile(filename, jsondata)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def appendToJsonFile(filename, data):
    if not(os.path.exists(filename)):
        with open(filename, "w") as f:
            m = []
            json.dump(m, f)
            f.close()
    with open(filename, "r") as f2:
        asd = json.load(f2)
        if(isinstance(data, list)):
            asd = asd + data
        else:
            asd.append(data)
        f2.close()
    with open(filename, "w") as f3:
        json.dump(asd, f3)
        f3.close()


def saveMouseScrolls(request):
    if request.method == "POST":
        jsondata = {}
        user = request.user
        data = request.POST[u'mousescrolls']
        print(data)
        filename = "logs/mousescrolls/" + str(user) + ".json"
        appendToJsonFile(filename, data)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def saveMouseClicks(request):
    if request.method == "POST":
        jsondata = {}
        user = request.user
        data = request.POST[u'mouseclicks']
        jsondata = json.loads(data)
        mc = MouseClicks(author=user, operation_type=jsondata[
                         'type'], post_id=jsondata['postId'])
        mc.save()
        filename = "logs/mouseclicks/" + str(user) + ".json"
        appendToJsonFile(filename, jsondata)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def getMouseMovements(request):
    user = request.user
    jsondata = {}
    filename = "logs/mousemovements/" + str(user) + ".json"
    f = open(filename, "r")
    data = json.dumps(json.load(f))
    return HttpResponse(data, status=200)


def groupMouseClicksAndSendJson(request):
    user = request.user
    jsondata = {}
    startDate = request.GET.get('startDate', '2018-09-08')
    endDate = request.GET.get('endDate', '2018-09-14')
    print(startDate, endDate)
    from django.db import connection
    cursor = connection.cursor()
    sql = """SELECT operation_type,created_date, count(*) as cnt
             FROM discussions_mouseclicks
             where author_id = '{0}' and created_date BETWEEN '{1}' and  '{2}'
             group by DATE(created_date), operation_type""".format(request.user.id, startDate, endDate)
    print(sql)
    cursor.execute(sql)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cumulativeData.csv"'
    fieldnames = ['DATE', 'ADD_COMMENT', 'ADD_POST', 'EDIT_POST',
                  'OPEN_DISCUSSION', 'READ_COMMENT', 'VIEW_ANALYTICS']
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    dict = {}
    for i in cursor:
        dte = (i[1].date())
        if dte not in dict.keys():
            dict[dte] = {'DATE': str(dte), 'ADD_COMMENT': 0, 'ADD_POST': 0, 'EDIT_POST': 0,
                         'OPEN_DISCUSSION': 0, 'READ_COMMENT': 0, 'VIEW_ANALYTICS': 0}
            dict[dte][str(i[0])] = i[2]
        else:
            dict[dte][str(i[0])] = i[2]
    if(len(dict.keys()) == 0):
        return HttpResponse(status=400)
    for f in sorted(dict.keys()):
        # print(dict[f])
        writer.writerow(dict[f])
    return response


def getGeneralClickCount(request):
    user = request.user
    filename = "logs/mouseclicks/" + str(user) + ".json"
    f = open(filename, "r")
    data = str(json.load(f))
    openDiscussion = data.count("OPEN_DISCUSSION")
    readComment = data.count("READ_COMMENT")
    addComment = data.count("ADD_COMMENT")
    editPost = data.count("EDIT_POST")
    viewAnalytics = data.count("VIEW_ANALYTICS")
    addPost = data.count("ADD_POST")
    jsonm = {"openDiscussion": openDiscussion, "readComment": readComment, "addComment": addComment,
             "editPost": editPost, "viewAnalytics": viewAnalytics, "addPost": addPost}
    print(jsonm)
    data = json.dumps(jsonm)
    return HttpResponse(data, status=200)
