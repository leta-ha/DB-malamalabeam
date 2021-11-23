# from django.contrib import admin
# from .models import Appmala # 같은 폴더(.) 내에 있는 models모듈에서 Blog를 import해오겠다는 의미입니다. 

# # Register your models here.

# admin.site.register(Appmala)
from django.contrib import admin
from .models import Store, Bookmark, Review, Comment

# Register your models here.

admin.site.register(Store)
admin.site.register(Bookmark)
admin.site.register(Review)
admin.site.register(Comment)