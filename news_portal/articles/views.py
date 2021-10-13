from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from .filters import PostFilter, F, C, X  # импортируем недавно написанный фильтр
from .models import Post, BaseRegisterForm, Category
from .forms import PostForm



class PostList(ListView):
    model = Post
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


class CategoryDetail(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(postCategory__id=self.kwargs['pk']).order_by('-dateCreation')
        context['news'] = Post.objects.filter(postCategory__id=self.kwargs['pk']).count()
        return context


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
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.all().count()
        context['category'] = Category.objects.all()
        context['filter'] = self.get_filter()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


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


@login_required
def subscribe(request, pk):
    user = request.user
    subscriber = User.objects.filter(username=user).last()
    category = Category.objects.filter(id=pk).last()
    if category.subscribers.filter(id=request.user.id).exists():
        category.subscribers.remove(subscriber)
        return HttpResponse(f'{subscriber.username}, вы отписались от категории {category.name}')
    else:
        category.subscribers.add(subscriber)
        return HttpResponse(f'{subscriber.username}, вы подписались на категорию {category.name}')

def user_list(request):
    f = F(request.GET, queryset=User.objects.all())
    return render(request, 'user_t.html', {'filter': f})


def post_list(request):
    c = C(request.GET, queryset=Post.objects.all())
    return render(request, 'post_t.html', {'filter': c})


def comment_list(request):
    x = X(request.GET, queryset=Post.objects.all())
    return render(request, 'comment_t.html', {'filter': x})

