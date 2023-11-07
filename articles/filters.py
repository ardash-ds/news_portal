from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFromToRangeFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from django.contrib.auth.models import User
from .models import Post, Category, Comment


class PostFilter(FilterSet):
    dateCreation = DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = ['title', 'author__authorUser__username', 'postCategory__name', 'dateCreation',]


class F(FilterSet):
    username = CharFilter(method='my_filter')

    class Meta:
        model = User
        fields = ['username']

    def my_filter(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })

class C(FilterSet):
    category = ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['postCategory']

class X(FilterSet):
    dateCreation = DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = ['dateCreation']
        