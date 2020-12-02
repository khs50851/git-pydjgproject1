
from django.urls import path
from . import views
urlpatterns = [

    # 숫자형으로 받을거고 pk라는 변수명으로 받겠다라는 뜻
    path('detail/<int:pk>/', views.board_detail),
    path('list/', views.board_list),
    path('write/', views.board_write),
]
