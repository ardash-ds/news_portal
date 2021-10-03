from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from .filters import PostFilter, F, C, X  # импортируем недавно написанный фильтр
from .models import Post, BaseRegisterForm, Category, PostCategory
from .forms import PostForm


class PostList(ListView):
    model = Post, Category
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 5  # поставим постраничный вывод в один элемент

    # form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.all().count()
        context['category'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, *kwargs)


class CategoryDetail(ListView):
    model = Post, Category
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.all().count()
        context['category'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def get_queryset(self):
        return Post.objects.filter(postCategory__id=self.kwargs['pk'])


def subscribe_view(request, pk):
    category = Category.objects.get(id=pk)
    user = request.user
    category.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-dateCreation')
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }


def user_list(request):
    f = F(request.GET, queryset=User.objects.all())
    return render(request, 'user_t.html', {'filter': f})


def post_list(request):
    c = C(request.GET, queryset=Post.objects.all())
    return render(request, 'post_t.html', {'filter': c})


def comment_list(request):
    x = X(request.GET, queryset=Post.objects.all())
    return render(request, 'comment_t.html', {'filter': x})


class PostDetail(DetailView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=kwargs['queryset'])
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('articles.add_post',)
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('articles.change_post',)
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('articles.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    autors_group = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='Authors').exists():
        autors_group.user_set.add(user)
    return redirect('/')
