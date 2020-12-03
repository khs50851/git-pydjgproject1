from django.shortcuts import render, redirect
from django.core.paginator import Paginator
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
    all_boards = Board.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1))  # 페이지 값은 p로 가져오고 없으면 default값 1
    # all_boards(전체 오브젝트)에서 한번에 5개씩 글을 가져옴
    paginator = Paginator(all_boards, 5)
    # 원래은 all_boards를 쿼리셋형태로 가져오는데 paginator로
    # 바꿔서 페이지에 대한 정보를 가지고 있음
    boards = paginator.get_page(page)

    return render(request, 'board_list.html', {'boards': boards})
