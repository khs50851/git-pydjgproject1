from django.shortcuts import render, redirect
from .models import User1
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


def home(request):
    user_id = request.session.get('user')

    if user_id:
        user1 = User1.objects.get(pk=user_id)
        return HttpResponse(user1.username+"님 환영합니다")
    else:
        return HttpResponse('Home!')


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    # 템플릿코드랑 컨트롤 코드가 연결
    # 어떤 주소로 들왔을때 이 뷰를 연결할지 설정
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        res_data = {}
        if not (username and password):
            res_data['error'] = '모든 값을 입력해야합니다!'
        else:
            # 앞에는 필드명(모델안에 어떤 속성값 뒤에는 입력받은 username)
            user1 = User1.objects.get(username=username)
            # 앞 password는 입력받은 패스워드
            if check_password(password, user1.password):
                # 세션처리
                # 로그인 후 redirect
                request.session['user'] = user1.id
                # 세션도 각 키마다 값을 가지고 있음
                # user라는 키에다가 지금 로그인한 유저의 id값 저장
                return redirect('/')  # '/' 이건 홈으로 가는거 현재 만든 웹사이트의 루트로 이동
            else:
                res_data['error'] = '비밀번호를 틀렸습니다.'
        return render(request, 'login.html', res_data)


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    # 템플릿 폴더를 바라보고 있기 때문에 바로 찾으낼 수 있음
    # 템플릿 안에 다른 폴더가 있으면 folder/folder2/register.html 이런식으로 하면 됨
    # 다음은 py_community urls로 가서 url 설정
    elif request.method == 'POST':
        # 포스트 안에 있는 폼태그 안에 username
        username = request.POST.get('username', None)
        # 이렇게 폼데이터로 넘어오는건 딕셔너리 형태로 되어있음 request.POST['username'] 원랜 이런식
        # 키에 대한 값을 가져오는데 없으면 none으로
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

        res_data = {}
        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            user1 = User1(
                username=username,
                useremail=useremail,
                password=make_password(password)
            )
            user1.save()  # 저장

        # 이렇게 하면 res_data가 html 코드로 전달됨
        return render(request, 'register.html', res_data)
