from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Board
from .forms import BoardForm
from user1.models import User1
from tag.models import Tag
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

            tags = form.cleaned_data['tags'].split(',')
            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = user1
            board.save()

            # 태그는 보드가 먼저 만들어지고 만들어져야함 그래서 위에 전부 입력되고 save까지되면 id를 자동으로 생성하는데
            # 그 id 값이 생성이 된 뒤에 추가를 할 수 있음

            for tag in tags:
                if not tag:
                    continue

                # name=tag에서 tag의 이름이 있으면 그걸로 사용 없으면 새로 만듬 기본값도 넣을 수 있음 default로
                _tag, _ = Tag.objects.get_or_create(name=tag)
                # _tag, created = Tag.objects.get_or_create(name=tag) 값을 두개를 반환하는데 하나는 _tag에다가 생성된 객체 저장, 하나는(created) 새로 생성된앤지 아닌지 이 여부를 가져다줌 boolean값 리턴
                # 위처럼 created를 사용하지 않을경우엔 언더바 _ 로 쓰면 됨
                board.tags.add(_tag)

            print("user1 : ", user1)

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
