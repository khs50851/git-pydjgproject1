from django import forms
from .models import User1
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={'required': '아이디를 입력하세요'}, max_length=32, label="이름")
    password = forms.CharField(error_messages={
                               'required': '비밀번호를 입력하세요'}, widget=forms.PasswordInput, label="비밀번호")
    # required로 내가 원하는 에러메세지 출력 가능

    def clean(self):  # 오버라이딩 하는거임
        # 이건 이미 기본적으로 만들어져있어서 user를 통해 기존에 Form안에 들어있던 클린 함수를 먼저 호출해줌
        cleaned_data = super().clean()
        # 값이 비어있는지 확인함
        # 만약 값이 들어있지 않으면 super().clean()여기서 실패처리가 되서 나감
        username = cleaned_data.get('username')  # 검증이 끝난 데이터들을 가지고 옴
        password = cleaned_data.get('password')

        if username and password:
            user1 = User1.objects.get(username=username)
            if not check_password(password, user1.password):
                # 원하는 필드에 원하는 에러메세지 추가  password 필드에 에러 추가
                self.add_error('password', '비밀번호가 틀렸습니다.')
            else:
                self.user_id = user1.id  # 이렇게 하면 이 클래스 변수에 user_id가 저장이 됨
