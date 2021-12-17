from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .forms import SignupForm

# Create your views here.

#로그인 함수
def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid(): #유효성 검사
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = auth.authenticate(
        request=request,
        username=username,
        password=password
      )

      if user is not None: #유저 생성 성공
        auth.login(request, user) #로그인
        return redirect('home') #메인 페이지(home)로 이동

    return redirect('user:login') #유효성 검사에서 False가 리턴되거나 유저가 존재하지 않는 경우 로그인 화면 유지
  
  else: #form 데이터가 제출되지 않은 경우
    form = AuthenticationForm()
    return render(request, 'login.html', {'form' : form}) #form 변수를 담아서 로그인 페이지에 띄우기

#로그아웃 함수
def logout(request):
	auth.logout(request)
	return redirect('home') #로그아웃 후 메인 페이지(home)로 이동

#회원가입 함수
def signup_view(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid(): #유효성 검사
      user = form.save()
      auth.login(request, user) #로그인
      return redirect('home') #메인 페이지(home)로 이동
    return redirect('user:signup') #유효성 검사에서 False가 리턴되는 경우 회원가입 화면 유지

  else: #form 데이터가 제출되지 않은 경우
    form = SignupForm()
    return render(request, 'signup.html', {'form' : form}) #form 변수를 담아서 회원가입 페이지에 띄우기