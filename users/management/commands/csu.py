from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@1jz.ru',
            fio='Admin Admin Admin',
            comment='Admin',
            is_staff=True,
            is_superuser=True

        )

        user.set_password('12345')
        user.save()