from django.urls import path
from . import views #현재 폴더에 있는 views에 접근

app_name = 'appmala' #앱 이름

# path([도메인 뒤에 붙는 path], [views.py에서 정의한 함수], name=[path의 이름 지정])

urlpatterns = [
    path('<int:id>', views.detail, name='detail'),
    path('newstore/', views.newstore, name='newstore'),
    path('create/', views.create, name='create'),
    path('delete/<int:id>', views.delete, name="delete"),
    path('create_comment/', views.create_comment, name='create_comment'),
    
    path('<int:id>/newreview/', views.newreview, name='newreview'), 
    path('newreview/createReview/<int:store_id>', views.createReview, name='createReview'), 
    path('deleteReview/<int:id>', views.deleteReview, name="deleteReview"), 
    path('<int:id>/review/', views.review, name='review'), 
    
]