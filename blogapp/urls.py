from django.urls import path
from . import views
from . views import IndexView, SinglePostView, AddPostView, UpdatePostView, DeletePostView, AddCategorytView, CategoryView, LikeView, AddCommentView

urlpatterns = [
    #path('', views.index, name="index"),
    path('', IndexView.as_view(), name = "index"),
    path('article/<int:pk>', SinglePostView.as_view(), name = 'single-post'),
    path('add_post/', AddPostView.as_view(), name = 'add_post'),
    path('add_category/', AddCategorytView.as_view(), name = 'add_category'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('like/<int:pk>', LikeView, name ='like_post'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name = 'add_comment'),
]