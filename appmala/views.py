from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
#from .models import Appmala
from .models import Store, Bookmark, Review, Comment
from .forms import AppmalaForm, ReviewForm
from django.core.paginator import Paginator
from user.models import CustomUser

# Create your views here.
def home(request):
    query= request.GET.get('query')
    if query:
        stores= Store.objects.filter(store_name__icontains=query)
    else:
        stores= Store.objects.all()

    paginator= Paginator(stores, 6)
    page= request.GET.get('page')
    query = request.GET.get('query')
    paginated_stores= paginator.get_page(page)
    if query:
        return render(request, 'home.html', {'stores': paginated_stores, 'query': query})
    else:
        return render(request, 'home.html', {'stores': paginated_stores})

# def detail(request):
#     reviews = Review.objects.all()
#     query = request.GET.get('query')
#     if query:
#         reviews = Review.objects.filter(title__icontains=query)

#     paginator = Paginator(reviews, 5) # stores를 5개씩 쪼갠다
#     page = request.GET.get('page') # 해당 정보가 오지 않아도 넘어간다
#     paginated_reviews = paginator.get_page(page)
#     return render(request, 'review.html', {'reviews': paginated_reviews})

def detail(request, id):
    store = get_object_or_404(Store, pk = id)
    reviews = Review.objects.filter(store=id)
    # comments = Comment.objects.filter(comment_id=id)
    return render(request, 'detail.html', {'store': store, 'reviews': reviews})

def review(request, id):
    review = get_object_or_404(Review, pk = id)
    comments = Comment.objects.filter(review=id)
    return render(request, 'review.html', {'review': review, 'comments': comments})

def newstore(request):
    form = AppmalaForm()
    return render(request, 'newstore.html', {'form':form})

def newreview(request, id):
    form = ReviewForm()
    store = get_object_or_404(Store, pk=id)
    return render(request, 'newreview.html', {'form':form, 'store': store})

def create(request):
    form = AppmalaForm(request.POST, request.FILES) # form 데이터를 처리하기 위해서 request.POST와 request.FILES가 필요함을 의미합니다.
    if form.is_valid(): # 유효성 검사 
        new_store = form.save(commit=False) # 임시 저장 나머지 필드(칼럼)를 채우기 위함
        new_store.pub_date = timezone.now()
        # if request.user.is_authenticated:
        #     new_store.user = request.user
        new_store.save()
        return redirect('appmala:detail', new_store.id)
    return redirect('home')

def delete(request, id):
    store = Store.objects.get(id=id)
    store.delete()
    return redirect("home")

def createReview(request, store_id):
    form = ReviewForm(request.POST, request.FILES)
    item =  get_object_or_404(Store, pk = store_id)

    if form.is_valid():  
        new_review = form.save(commit=False) 
        new_review.pub_date = timezone.now()
        if request.user.is_authenticated:
            new_review.user = request.user
            new_review.store = item
        new_review.save()
        return redirect('appmala:review', new_review.id)
    return redirect('home')

def deleteReview(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect("appmala:detail", review.store_id)

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