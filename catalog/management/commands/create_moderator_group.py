from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создает группу модераторов и назначает права'

    def handle(self, *args, **options):
        # Создаем или получаем группу
        group, created = Group.objects.get_or_create(
            name='moderator_product'
        )

        # Получаем нужные права
        unpublish_perm = Permission.objects.get(
            codename='can_unpublish_product'
        )
        delete_perm = Permission.objects.get(
            codename='delete_product'
        )

        # Назначаем права
        group.permissions.add(unpublish_perm, delete_perm)

        if created:
            print('✅ Группа "Модератор продуктов" создана!')
        else:
            print('↻ Группа уже существовала, обновлена.')

        print(f'Назначенные права:')
        for perm in group.permissions.all():
            print(f'  - {perm.name}')