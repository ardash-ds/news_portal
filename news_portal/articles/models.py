from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    # def update_rating(self):



class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)    # нужно ли каскадное удаление...
    select = models.CharField(max_length=2, choices=POSITIONS)
    date_add = models.DateField(auto_now_add = True)
    category = models.ManyToManyField(Category, through=PostCategory)
    head = models.CharField(max_length=64, unique=True)    # добавим уникальность заголовку
    text = models.CharField()
    rating_text = models.IntegerField(default=0)

    news = 'NE'
    articles = 'AR'
    POSITIONS = ((news, 'new'), (articles, 'article'))

    def like(self):
        self.rating_text += 1
        self.save()

    def dislike(self):
        self.rating_text -= 1
        self.save()

    def preview(self):
        return text[0:128] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post)
    category = models.ForeignKey(Category)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = CharField()
    date_comment = models.DateField(auto_now_add = True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()

