from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    PostList, PostDetail, PostSearch, user_list, post_list, comment_list,
    PostCreateView, PostDeleteView, PostUpdateView, BaseRegisterView, upgrade_me,
    subscribe, CategoryDetail, Index,
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
    path('create/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('accounts/', include('allauth.urls')),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('category/<int:pk>', CategoryDetail.as_view(), name='category'),
    path('translatre/', Index.as_view()),
]
