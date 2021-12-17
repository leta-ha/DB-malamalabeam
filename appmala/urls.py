from django.urls import path
from . import views #현재 폴더에 있는 views에 접근하기 때문

app_name = 'appmala' # app_name에는 앱 이름을 넣어줍니다.

urlpatterns = [
    path('<int:id>', views.detail, name='detail'),
    path('newstore/', views.newstore, name='newstore'),
    path('create/', views.create, name='create'),
    path('delete/<int:id>', views.delete, name="delete"),
    path('create_comment/', views.create_comment, name='create_comment'),
    
    # 리뷰 작성, 삭제, 조회를 위한 url 
    path('<int:id>/newreview/', views.newreview, name='newreview'), # 리뷰 작성 페이지 url
    path('newreview/createReview/<int:store_id>', views.createReview, name='createReview'), # 리뷰 생성 기능 url
    path('deleteReview/<int:id>', views.deleteReview, name="deleteReview"), # 리뷰 삭제 기능 url
    path('<int:id>/review/', views.review, name='review'), # 리뷰 상세 페이지 url
    
]

