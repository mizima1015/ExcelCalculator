from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from random import *
from sendEmail.views import *

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def signup(request):
    return render(request, 'main/signup.html')

def join(request):
    print("테스트",request)
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name=name, user_email = email, user_password = pw)
    user.save()
    print("사용자 정보 저장 완료됨!!")
    code = randint(1000, 9999)
    print("인증코드 생성 ---------------", code)
    response = redirect('main_verifyCode')
    response.set_cookie('code',code)
    response.set_cookie('user_id',user.id )
    print("응답 객체 완성__________", response)
    # 이메일 발송 함수 호출
    send_result = send(email,code)
    if send_result:
        return response
    else:
        return HttpResponse("이메일 발송에 실패했습니다.")



    # return response
    # return redirect('main_verifyCode')

def signin(request):
    return render(request, 'main/signin.html')

def verifyCode(request):
    return render(request, 'main/verifyCode.html')

def verify(request):
    # 사용자가 입력한 code 값을 받아야함
    user_code = request.POST['verifyCode']

    # 쿠키에 저장되어 있는 code 값을 가져온다. (join 함수 확인)
    cookie_code = request.COOKIES.get('code')
    print("코드 확인: ", user_code,cookie_code )
    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('user_id'))
        user.user_validate = 1 # True 1 False 0 
        user.save()
        print("DB에 user_validate 업데이트---------------")

        response = redirect('main_index')

        # 저장되어 있는 쿠키를 삭제
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        # response.set_cookie('user',user)
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return response
    else:
        return redirect('main_verifyCode')

def result(request):
    return render(request, 'main/result.html')