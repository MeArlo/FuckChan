from django.urls import path
from .views import BoardListView, ThreadListView, ThreadView, CreateThreadView

urlpatterns = [
    path('', BoardListView.as_view(), name='board_list'),
    path('<str:board_abbr>/', ThreadListView.as_view(), name='thread_list'),
    path('<str:board_abbr>/thread/<int:thread_id>/', ThreadView.as_view(), name='thread'),
    path('<str:board_abbr>/new/', CreateThreadView.as_view(), name='create_thread'),
]