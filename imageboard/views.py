from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Board, Thread, Post
from .forms import PostForm


class BoardListView(View):
    def get(self, request):
        boards = Board.objects.all()
        return render(request, 'imageboard/board_list.html', {'boards': boards})


class ThreadListView(View):
    def get(self, request, board_abbr):
        board = get_object_or_404(Board, abbreviation=board_abbr)
        threads = Thread.objects.filter(board=board).order_by('-is_pinned', '-updated_at')
        return render(request, 'imageboard/thread_list.html', {
            'board': board,
            'threads': threads
        })


class ThreadView(View):
    def get(self, request, board_abbr, thread_id):
        board = get_object_or_404(Board, abbreviation=board_abbr)
        thread = get_object_or_404(Thread, id=thread_id, board=board)
        posts = Post.objects.filter(thread=thread).order_by('created_at')

        # Форма для нового поста
        form = PostForm()

        return render(request, 'imageboard/thread.html', {
            'board': board,
            'thread': thread,
            'posts': posts,
            'form': form
        })

    def post(self, request, board_abbr, thread_id):
        board = get_object_or_404(Board, abbreviation=board_abbr)
        thread = get_object_or_404(Thread, id=thread_id, board=board)
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.save()
            return redirect('thread', board_abbr=board.abbreviation, thread_id=thread.id)

        posts = Post.objects.filter(thread=thread).order_by('created_at')
        return render(request, 'imageboard/thread.html', {
            'board': board,
            'thread': thread,
            'posts': posts,
            'form': form
        })


class CreateThreadView(View):
    def get(self, request, board_abbr):
        board = get_object_or_404(Board, abbreviation=board_abbr)
        form = PostForm()
        return render(request, 'imageboard/create_thread.html', {
            'board': board,
            'form': form
        })

    def post(self, request, board_abbr):
        board = get_object_or_404(Board, abbreviation=board_abbr)
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            # Создаём новый тред
            thread = Thread.objects.create(
                board=board,
                subject=form.cleaned_data['subject'] or "Без темы"
            )

            # Создаём OP-пост
            post = form.save(commit=False)
            post.thread = thread
            post.is_op = True
            post.save()

            return redirect('thread', board_abbr=board.abbreviation, thread_id=thread.id)

        return render(request, 'imageboard/create_thread.html', {
            'board': board,
            'form': form
        })