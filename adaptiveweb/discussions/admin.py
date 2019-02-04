# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Post, Comment, MouseClicks, userLoginInfo


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(MouseClicks)
admin.site.register(userLoginInfo)
