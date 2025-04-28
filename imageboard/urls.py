from django.urls import path, include
from rest_framework.routers import DefaultRouter

from imageboard.views import CommentListView, PostListView, UserListView


router = DefaultRouter()
router.register(r'users', UserListView)
router.register(r'posts', PostListView, basename='task')
router.register(r'comments', CommentListView, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    ]