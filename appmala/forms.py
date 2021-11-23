from django import forms    # 장고가 제공해주는 form라이브러리
from .models import Store

class AppmalaForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_id','store_name','address', 'rating','image', 'phone_num']