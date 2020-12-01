from django.shortcuts import render
from .models import User1
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
# Create your views here.


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
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

        res_data = {}
        if not (username and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            user1 = User1(
                username=username,
                password=make_password(password)
            )
            user1.save()  # 저장

        # 이렇게 하면 res_data가 html 코드로 전달됨
        return render(request, 'register.html', res_data)
