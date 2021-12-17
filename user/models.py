from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# 회원 테이블; Django의 기본 테이블을 상속받음
class CustomUser(AbstractUser):
  nickname = models.CharField(max_length=100)