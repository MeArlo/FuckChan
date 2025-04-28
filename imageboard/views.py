
from rest_framework import viewsets

from .models import Post, Comment, User
from .serializers import PostSerializer, UserSerializer

from imageboard.serializers import CommentSerializer


class CommentListView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostListView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer