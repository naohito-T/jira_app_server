from django.contrib import admin
from .models import Category, Task, Profile

# みたいモデルを登録する
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Profile)
