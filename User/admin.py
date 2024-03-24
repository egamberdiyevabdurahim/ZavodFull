from django.contrib import admin

from .models import User
from Post.models import Xodim


admin.site.register(User)
admin.site.register(Xodim)