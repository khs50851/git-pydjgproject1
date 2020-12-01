from django.db import models

# Create your models here.


class User1(models.Model):
    username = models.CharField(max_length=32,
                                verbose_name='사용자명')
    useremail = models.EmailField(max_length=128,  # 이메일필드는 char필드랑 비슷한데 이메일 형식으로 받게함
                                  verbose_name='이메일')  # 만약에 이메일 필드를 추가할 경우 먼저 데이터베이스에 이메일 필드 없이 데이터가 있을때
    # 이메일 필드를 추가해서 migrations하면 내가 직접 default값 넣을건지 default='', verbose_name='이메일'
    # 아니면 지정되 default값 넣을건지 물어봄
    # 우선 여기서 1번을 눌러 기본값 넣음
    password = models.CharField(max_length=64,
                                verbose_name='비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')

    def __str__(self):  # 장고 페이지에서 아이디 명에 표현된건 그냥 클래스를 문자로 나타낸거
        #  파이썬에는 이 클래스가 문자열로 변환할때 어떻게 변환할지 하는 함수를 호출하는데 그게 str임
        # 그렇게 유저네임을 반환하게함
        return self.username

    class Meta:
        db_table = 'pydjgproject_user1'
        # 위에 필드에 verbose name한것처럼 여기서도 지정
        verbose_name = '유저'
        verbose_name_plural = '유저'
