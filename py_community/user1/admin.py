from django.contrib import admin
from .models import User1
# Register your models here.


class User1Admin(admin.ModelAdmin):  # 한눈에 유저 정보를 명시하도록 안에 내용을 정의할수있음
    list_display = ('username', 'password', 'useremail')  # 필드들을 튜플로 만듬


admin.site.register(User1, User1Admin)
