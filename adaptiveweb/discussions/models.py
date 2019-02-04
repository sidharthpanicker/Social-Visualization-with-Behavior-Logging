# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import json
import time
from django.contrib.auth.models import User

users = User.objects.all()

# Create your models here.
log = logging.getLogger(__name__)


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        'discussions.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class MouseClicks(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    operation_type = models.TextField()
    post_id = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.operation_type


class userLoginInfo(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    operation_type = models.TextField()
    ip_address = models.TextField(default='127.0.0.1')
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.operation_type


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    mc = userLoginInfo(author=user, operation_type='LOG_IN', ip_address=ip)
    mc.save()
    data = {}
    data['action'] = 'LOG_IN'
    data['user'] = user.username
    data['ip'] = str(ip)
    data['timestamp'] = int(time.time())
    filename = "logs/userlogin/" + str(user) + ".txt"
    f = open(filename, "a+")
    f.write(json.dumps(data))
    f.close()


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    mc = userLoginInfo(author=user, operation_type='LOG_OUT', ip_address=ip)
    mc.save()
    data = {}
    data['action'] = 'LOG_OUT'
    data['user'] = user.username
    data['ip'] = str(ip)
    data['timestamp'] = int(time.time())
    filename = "logs/userlogin/" + str(user) + ".txt"
    f = open(filename, "a+")
    f.write(json.dumps(data))
    f.close()

"""
@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, **kwargs):
    print('logout failed for: {credentials}'.format(
        credentials=credentials,
    ))
    for i in users:
        if (credentials['username']) == i.username:
            print(credentials['username'])
            data = {}
            data['action'] = 'LOGGING_FAILED'
            data['user'] = i.username
            data['timestamp'] = int(time.time())
            mc = userLoginInfo(
                author=i.username, operation_type='LOGGING_FAILED')
            mc.save()
            filename = "logs/userlogin/" + str(i.username) + ".txt"
            f = open(filename, "a+")
            f.write(json.dumps(data))
            f.close()
            break


            """
