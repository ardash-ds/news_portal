from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from .models import Post, BaseRegisterForm, Category




# @receiver(post_save, sender=Post)
# @receiver(m2m_changed, sender=Post.postCategory.through)

@receiver(post_save, sender=Post)
def notify_users_post(sender, instance, created, **kwargs):
    categories = Category.objects.filter(postcategory__postThrough=instance)
    subscribers_mail = []
    for category in categories:
        for sub in category.subscribers.values('email'):
            subscribers_mail.append(sub['email'])
    # print(instance.id)
    # send_mail(
    #     subject=f'Заголовок сообщения',
    #     message=f'На сайте появилась новая статья {instance.title} : {instance.text}',
    #     from_email='info1981@yandex.ru',
    #     recipient_list=subscribers_mail
    # )

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

