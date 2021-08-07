from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFromToRangeFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from django.contrib.auth.models import User
from .models import Post, Category, Comment


# создаём фильтр
class PostFilter(FilterSet):
    dateCreation = DateFromToRangeFilter()
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться
    # (т. е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],  # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то что запросил пользователь
            'author__authorUser__username': ['contains'],
            'postCategory__name': ['contains'],
            'dateCreation': ['range']
        }

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
        # fields = {'dateCreation': ['range']}
        fields = ['dateCreation']