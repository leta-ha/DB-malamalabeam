from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
#from .models import Appmala
from .models import Store, Bookmark, Review, Comment
from .forms import AppmalaForm
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    stores = Store.objects.all()
    query = request.GET.get('query')
    if query:
        stores = Store.objects.filter(title__icontains=query)

    paginator = Paginator(stores, 5) # stores를 5개씩 쪼갠다
    page = request.GET.get('page') # 해당 정보가 오지 않아도 넘어간다
    paginated_stores = paginator.get_page(page)
    return render(request, 'home.html', {'stores': paginated_stores})

def detail(request, id):
    store = get_object_or_404(Store, pk = id)
    reviews = Review.objects.filter(number=id)
    comments = Comment.objects.filter(number=id)
    return render(request, 'detail.html', {'store': store, 'reviews': reviews, 'comments': comments})

def newstore(request):
    form = AppmalaForm()
    return render(request, 'newstore.html', {'form':form})

def create(request):
    form = AppmalaForm(request.POST, request.FILES) # form 데이터를 처리하기 위해서 request.POST와 request.FILES가 필요함을 의미합니다.
    if form.is_valid(): # 유효성 검사 
        new_store = form.save(commit=False) # 임시 저장 나머지 필드(칼럼)를 채우기 위함
        new_store.pub_date = timezone.now()
        if request.user.is_authenticated:
            new_store.user = request.user
        new_store.save()
        return redirect('appmala:detail', new_store.id)
    return redirect('home')

def delete(request, id):
	store = Store.objects.get(id=id)
	store.delete()
	return redirect("home")