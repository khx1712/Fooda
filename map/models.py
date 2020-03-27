from django.db import models
from django.contrib.auth.models import User
from map import file_upload_path_for_db


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=50, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['create_date']

# Create your models here.
class Restaurant(models.Model):
    CATEGORIES = (
        ('K', 'Korean'),
        ('J', 'Japanese'),
        ('C', 'Chinese'),
        ('W', 'Western'),
        ('A', 'Asian'),
        ('E', 'Southeast_Asia'),
        ('S', 'South_America'),
        ('M', 'Mideast'),
        ('F', 'Cafe'),
        ('N', 'Night_Life'),
    )
    folder = models.ForeignKey(Folder, default=1, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=50)
    lat = models.TextField(max_length=100) # 실수
    lon = models.TextField(max_length=100) # 실수
    location = models.TextField(max_length=100)
    phoneNumber = models.TextField(max_length=20)
    category = models.CharField(max_length=1, choices=CATEGORIES, blank=True)
    business_hour = models.TextField(max_length=100, blank=True)
    #imageURL = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-folder']


class RestImage(models.Model):

    # 식당과 연결되는 외래키
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restimages')
    # 실제 디스크에 저장되는 파일 절대 경로
    file_save_name = models.ImageField(upload_to=file_upload_path_for_db, blank=False, null=False)
    # 파일의 원래 이름
    file_origin_name = models.CharField(max_length=100)
    # 파일 저장 경로
    file_path = models.CharField(max_length=100)
    # 파일 생성일
    create_date = models.DateTimeField(auto_now_add=True)
    # 파일 확장자
    file_ext = models.CharField(max_length=10)

    def __str__(self):
        return self.file_origin_name

    class Meta:
        ordering = ['create_date']


