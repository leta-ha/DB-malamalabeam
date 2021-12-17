from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
#from .models import Appmala
from .models import Store, Bookmark, Review, Comment, CustomUser
from .forms import AppmalaForm, ReviewForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Avg, Count
import json

# Create your views here.
#메인, 홈 화면
def home(request):
    print(Review.objects.values('rating').annotate(Avg('rating')).order_by())
    query = request.GET.get('query')
    
    if query:
        stores= Store.objects.filter(store_name__icontains=query) #입력한 쿼리에 맞는 가게 이름들을 필터
    else:
        stores= Store.objects.all() #쿼리가 없는 경우 모든 가게를 받아오기
    
    bookmarks = [] 
    print(stores)
    if request.user.id:
        bookmarks = [bmk.store_id for bmk in Bookmark.objects.all() if bmk.user_id == request.user.id] 
    
    if request.path_info=="/bookmarks":
        stores = Store.objects.filter(pk__in=bookmarks)
    
    #페이지네이터
    paginator= Paginator(stores, 6) #한 페이지에 가게 6개 보여주도록 설정
    page= request.GET.get('page')
    paginated_stores= paginator.get_page(page)
    
    if query: #쿼리가 있는 경우 (search)
        return render(request, 'home.html', {'stores': paginated_stores, 'query': query,'bookmarks': bookmarks}) #쿼리 정보까지 포함하여 홈 화면 불러오기
    else:
        return render(request, 'home.html', {'stores': paginated_stores, 'bookmarks': bookmarks}) #가게 정보와 즐겨찾기 기능만 포함하여 홈 화면 불러오기

#가게 상세 정보
def detail(request, id):
    store = get_object_or_404(Store, pk = id)
    reviews = Review.objects.filter(store=id) #해당 가게에 작성된 리뷰들을 필터
    return render(request, 'detail.html', {'store': store, 'reviews': reviews}) #가게와 리뷰 정보를 가지고 가게 상세 페이지로 이동

# 리뷰 상세 페이지
def review(request, id):
    review = get_object_or_404(Review, pk = id) 
    comments = Comment.objects.filter(review=id) # 해당 리뷰에 달린 댓글들을 필터
    return render(request, 'review.html', {'review': review, 'comments': comments}) #리뷰와 댓글 정보를 가지고 리뷰 상세 페이지로 이동

# 가게 등록 페이지 호출
def newstore(request):
    form = AppmalaForm()
    return render(request, 'newstore.html', {'form':form})

# 리뷰 등록 페이지 호출
def newreview(request, id):
    form = ReviewForm() 
    store = get_object_or_404(Store, pk=id) 
    return render(request, 'newreview.html', {'form':form, 'store': store})

#가게 등록 함수
def create(request):
    form = AppmalaForm(request.POST, request.FILES) #form 데이터를 처리하기 위해서 request.POST와 request.FILES가 필요
    if form.is_valid(): #유효성 검사 
        new_store = form.save(commit=False) #임시 저장 나머지 필드(칼럼)를 채우기 위함
        new_store.pub_date = timezone.now() #현재시간
        new_store.save()
        return redirect('appmala:detail', new_store.id) #가게가 정상적으로 등록되었다면 해당 가게 정보 페이지로 이동
    return redirect('home') #메인 페이지(home)으로 이동

#가게 정보 삭제 함수
def delete(request, id):
    store = Store.objects.get(id=id)
    store.delete()
    return redirect("home") #삭제한 후 메인 페이지(home)으로 이동

# 리뷰 등록 함수
def createReview(request, store_id):
    form = ReviewForm(request.POST, request.FILES) 
    item =  get_object_or_404(Store, pk = store_id) 
    
    if form.is_valid():  # 유효성 검사
        new_review = form.save(commit=False) #임시 저장 나머지 필드(칼럼)를 채우기 위함
        new_review.pub_date = timezone.now() #현재시간
        if request.user.is_authenticated: 
            new_review.user = request.user
            new_review.store = item
        new_review.save() 
        rating = Review.objects.filter(store_id=store_id).aggregate(Avg('rating')) #가게의 리뷰들의 별점의 평균
        stores = Store.objects.get(id = store_id)
        stores.rating = rating["rating__avg"] # 가게 평균 별점 정보 갱신
        stores.save() 
        return redirect('appmala:review', new_review.id) #리뷰가 정상적으로 등록되었다면 해당 리뷰 정보 페이지로 이동
    return redirect('home') #메인 페이지(home)으로 이동

# 리뷰 삭제 함수
def deleteReview(request, id):
    review = Review.objects.get(id=id)
    rating = Review.objects.filter(store_id= review.store_id).aggregate(Avg('rating')) # 리뷰의 평점
    stores = Store.objects.get(id = review.store_id) 
    stores.rating = rating["rating__avg"] # 가게 평균 별점 정보 갱신
    stores.save() 
    review.delete() # 리뷰 삭제
    return redirect("appmala:detail", review.store_id) #삭제한 후 메인 페이지(home)으로 이동


def create_comment(request):
    if request.method == "POST":
        comment = Comment()
        comment.comment_content = request.POST.get('comment_content', '')
        comment.review = Review.objects.get(pk=request.POST.get('reveiw_id'))
        writer = request.user
        print(writer)
        if writer:
            comment.user = CustomUser.objects.get(username=writer)
        else:
            return redirect('appmala:review', comment.review_id)
        comment.comment_date = timezone.now()
        comment.save()
        return redirect('appmala:review', comment.review_id)
    else:
        return redirect('home')
    
@csrf_exempt
def createBookmark(request):
    data = json.loads(request.body)
    about_store = Store.objects.get(id = int(data["store_id"]))
    bookmark = Bookmark.objects.create(user = request.user, store = about_store)
    bookmark.save()
    return HttpResponse()
    
@csrf_exempt
def deleteBookmark(request):
    data = json.loads(request.body)
    about_store = Store.objects.get(id = int(data["store_id"]))
    Bookmark.objects.filter(user = request.user, store = about_store).delete()
    return HttpResponse()
    
