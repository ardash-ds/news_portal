from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from .models import Post, BaseRegisterForm, Category

from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.contrib.auth.models import User


# @receiver(post_save, sender=Post)


