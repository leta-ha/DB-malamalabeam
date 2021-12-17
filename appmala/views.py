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
def home(request):          #home페이지에 전송할 정보. store정보와 bookmark정보를 전달한다.
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
    return render(request, 'review.html', {'review': review, 'comments': comments}) # 리뷰와 댓글 정보를 가지고 리뷰 상세 페이지로 이동

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

def createReview(request, store_id):    #리뷰를 생성하고, 생성된 리뷰를 포함한 별점평균을 store에 업데이트한다.
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

def deleteReview(request, id):          #리뷰를 삭제하고, 삭제된 리뷰를 제외한 별점평균을 store에 업데이트한다.
    review = Review.objects.get(id=id)
    rating = Review.objects.filter(store_id= review.store_id).aggregate(Avg('rating')) # 리뷰의 평점
    stores = Store.objects.get(id = review.store_id) 
    stores.rating = rating["rating__avg"] # 가게 평균 별점 정보 갱신
    stores.save() 
    review.delete() # 리뷰 삭제
    return redirect("appmala:detail", review.store_id) #삭제한 후 메인 페이지(home)으로 이동


def create_comment(request):
    if request.method == "POST":
        comment = Comment()    # Comment 테이블 불러오기
        comment.comment_content = request.POST.get('comment_content', '')    # comment_content 애트리뷰트 저장
        comment.review = Review.objects.get(pk=request.POST.get('reveiw_id'))    # 댓글을 작성하려는 리뷰의 id Comment 테이블에 저장
        writer = request.user   # 현재 로그인 돼 있는 유저 대입
        print(writer)
        if writer:    # 로그인이 돼 있어서 정상적으로 값이 대입 됐다면 해당 user Comment 테이블에 저장
            comment.user = CustomUser.objects.get(username=writer)
        else:
            return redirect('appmala:review', comment.review_id)    # 로그인이 안 돼 있다면 상세 리뷰창으로 돌아감
        comment.comment_date = timezone.now()    # 댓글 작성하고 있는 현재 시간 Comment 테이블에 저장
        comment.save()
        return redirect('appmala:review', comment.review_id)    # 댓글이 정상적으로 등록되었다면 상세 리뷰창으로 돌아감
    else:
        return redirect('home')
    
@csrf_exempt               
def createBookmark(request):        #북마크를 저장한다.
    data = json.loads(request.body)
    about_store = Store.objects.get(id = int(data["store_id"]))
    bookmark = Bookmark.objects.create(user = request.user, store = about_store)
    bookmark.save()
    return HttpResponse()           #http 응답 코드 반환
    
@csrf_exempt
def deleteBookmark(request):        #북마크를 삭제한다.
    data = json.loads(request.body)
    about_store = Store.objects.get(id = int(data["store_id"]))
    Bookmark.objects.filter(user = request.user, store = about_store).delete()
    return HttpResponse()           #http 응답 코드 반환
    
