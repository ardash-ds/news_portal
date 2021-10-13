from celery import shared_task
import time
from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, BaseRegisterForm, Category


@shared_task
@receiver(post_save, sender=Post)
def notify_users_post(sender, instance, created, **kwargs):
    categories = Category.objects.filter(postcategory__postThrough=instance)
    subscribers_mail = []
    for category in categories:
        for sub in category.subscribers.values('email'):
            subscribers_mail.append(sub['email'])

    # получаем наш html
    content = render_to_string('account/email/sub_mail.html', {
        'title': instance.title,
        'text': instance.preview(),
        'url_id': instance.id,
    }
                               )

    msg = EmailMultiAlternatives(
        subject=f'На сайте опубликованна новая статья: {instance.title} ',
        from_email='info1981@yandex.ru',
        to=subscribers_mail,
    )

    msg.attach_alternative(content, "text/html")  # добавляем html
    msg.send()  # отсылаем


@shared_task
def monday_newsletter():
    week = datetime.date(localtime()) - timedelta(weeks=1)
    categories = Category.objects.all()

    for category in categories:
        subscribers = User.objects.filter(category__name=category)
        subscribers_emails = []
        for subscriber in subscribers:
            subscribers_emails.append(subscriber.email)
            posts = Post.objects.filter(postCategory__name=category, dateCreation__gt=week)

            content = render_to_string('account/email/newsletter.html', {
                'posts': posts,
                'category': category,
            }
                                       )

            msg = EmailMultiAlternatives(
                subject=f'Новые статьи за неделю',
                from_email='info1981@yandex.ru',
                to=subscribers_emails,
            )

            msg.attach_alternative(content, "text/html")  # добавляем html
            msg.send()  # отсылаем