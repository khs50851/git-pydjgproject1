from django.shortcuts import render, redirect
from .models import Board
from .forms import BoardForm
from user1.models import User1
from django.http import Http404
# Create your views here.


def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')

    return render(request, 'board_detail.html', {'board': board})


def board_write(request):
    if not request.session.get('user'):
        return redirect('/user1/login')

    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            user1 = User1.objects.get(pk=user_id)

            print("user1 : ", user1)
            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = user1
            board.save()

            return redirect('/board/list/')
    else:
        form = BoardForm()

    return render(request, 'board_write.html', {'form': form})


def board_list(request):
    # 모든 게시글을 가지고 오면서 정렬도 가능 id의 역순 대쉬 -를 쓰면 거꾸로 가져옴
    boards = Board.objects.all().order_by('-id')
    print("type : ", type(boards))
    print("boards : ", boards.values_list())

    return render(request, 'board_list.html', {'boards': boards})
