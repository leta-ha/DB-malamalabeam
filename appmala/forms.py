from django import forms    # 장고가 제공하는 form라이브러리
from .models import Store
from .models import Review

class AppmalaForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name','address','image', 'phone_num']

# 리뷰 작성 form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title','content', 'rating', 'image', 'review_date']
        