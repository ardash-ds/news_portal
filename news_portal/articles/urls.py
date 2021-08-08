from django.urls import path
from django.conf.urls import url
from .views import (
    PostList, PostDetail, PostSearch, user_list, post_list, comment_list,
    PostCreateView, PostDeleteView, PostUpdateView
)


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_list'),
    path('search/', PostSearch.as_view()),
    url(r'^user_list/', user_list),
    # path('post_list/', post_list),
    path('comment_list/', comment_list),
    path('create/', PostCreateView.as_view(), name='create'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='update')
]