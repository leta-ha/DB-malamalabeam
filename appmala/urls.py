from django.urls import path
from . import views #현재 폴더에 있는 views에 접근하기 때문

app_name = 'appmala' # app_name에는 앱 이름을 넣어줍니다.

urlpatterns = [
    path('<int:id>', views.detail, name='detail'),
    path('newstore/', views.newstore, name='newstore'),
    path('create/', views.create, name='create'),
    path('delete/<int:id>', views.delete, name="delete"),
    
    path('<int:id>/newreview/', views.newreview, name='newreview'),
    path('newreview/createReview/<int:store_id>', views.createReview, name='createReview'),
    path('deleteReview/<int:id>', views.deleteReview, name="deleteReview"),
    path('<int:id>/review/', views.review, name='review'),
    # path('<int:id>/', views.detail, name="review-detail"),
    # path('<int:id>/review/create/', views.review_create, name='review-create'),
    # path('<int:id>/review/delete/<int:review_id>', views.review_delete, name='review-delete')
]