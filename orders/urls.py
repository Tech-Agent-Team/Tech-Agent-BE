from django.urls import path
from .views import CreateCommentView, CommentListView
# from .views import CreateCommentView, CommentListView, CommentDetailView

urlpatterns = [
    path('comment/<int:order_id>/', CreateCommentView.as_view(), name='create-comment'),
    path('comments/<int:order_id>/', CommentListView.as_view(), name='list-comments'),
    # path('commentdetail/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
]