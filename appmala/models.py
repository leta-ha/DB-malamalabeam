# from django.db import models
# from user.models import CustomUser

# # Create your models here.
# class Appmala(models.Model):
#     user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     writer = models.CharField(max_length=10)
#     pub_date = models.DateTimeField()
#     body = models.TextField()
#     image = models.ImageField(upload_to="appmala/", blank=True, null=True)
from django.db import models
from user.models import CustomUser
from django.utils import timezone

# Create your models here.

class Store(models.Model): 
    #store_id = models.CharField(max_length=20)
    #user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=20)
    rating = models.FloatField(max_length=20)
    image = models.ImageField(upload_to="review/", blank=True, null=True)
    phone_num = models.CharField(max_length=20)
    def __str__(self):
	    return self.store_name

class Bookmark(models.Model): 
    #bookmark_id = models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    #store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    def __str__(self):
	    return self.bookmark_id

class Review(models.Model): 
    # review_id = models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    content = models.CharField(max_length=500, null=False)
    rating = models.FloatField(max_length=20, null=False)
    image = models.ImageField(upload_to="review/", blank=True, null=True)
    review_date = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['review_date']
    def __str__(self):
	    return self.title
        
class Comment(models.Model): 
    comment_id = models.CharField(max_length=20, null=True)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, related_name="comments")
    comment_content = models.CharField(max_length=500, null=False)
    comment_date = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['comment_date']
    def __str__(self):
	    return self.comment_id