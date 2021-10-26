from django.core.management.base import BaseCommand, CommandError
from articles.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка'   # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_messege = 'Недостаточно аргументов'
    requires_migrations_checks = True   # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('category', nargs='+', type=int)

    def handle(self, *args, **options):
        category = options['category'][0]
        try:
            namecat = Category.objects.get(pk=category)
            answer = input(f'Удалить все посты в категории: "{namecat}"? y/n:')
            if answer == 'y':  # в случае подтверждения действительно удаляем все товары
                Post.objects.filter(postCategory__id=category).delete()
                self.stdout.write(self.style.SUCCESS('Category № "%s" cleared' % str(category)))
            else:
                self.stdout.write(self.style.ERROR('Отмена'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категории с ID {category} не существует.'))
