from django.db import models
from user.models import CustomUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# 가게 테이블
class Store(models.Model): 
    store_name = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=20)
    rating = models.DecimalField(default=0, null=True, max_digits=5, decimal_places=1)#models.FloatField(default=0, null=True)
    image = models.ImageField(upload_to="store/", blank=True, null=True)
    phone_num = models.CharField(max_length=20)
    def __str__(self):
	    return self.store_name

# 즐겨찾기 테이블
class Bookmark(models.Model): 
    user = models.ForeignKey(CustomUser,  null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(Store , null=True, on_delete=models.CASCADE)
    def __str__(self):
	    return self.bookmark_id

# 리뷰 테이블
class Review(models.Model): 
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    content = models.CharField(max_length=500, null=False)
    rating = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(5)])
    image = models.ImageField(upload_to="review/", blank=True, null=True)
    review_date = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['review_date']
    def __str__(self):
	    return self.title

# 댓글 테이블         
class Comment(models.Model): 
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, related_name="comments")
    comment_content = models.CharField(max_length=500, null=False)
    comment_date = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['comment_date']
    def __str__(self):
	    return self.comment_content