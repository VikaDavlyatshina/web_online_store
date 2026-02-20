from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User


class Command(BaseCommand):
    help = 'Создает группу модераторов и тестовых пользователей'

    def handle(self, *args, **options):
        print("Создание группы модераторов...")

        # Создаем или получаем группу модераторов
        group, group_created = Group.objects.get_or_create(
            name='moderator_product'
        )

        try:
            # Получаем кастомное разрешение на снятие с публикации
            unpublish_perm = Permission.objects.get(
                codename='can_unpublish_product'
            )

            # Получаем разрешение на удаление продукта
            # Замените 'products' на имя вашего приложения
            content_type = ContentType.objects.get(
                app_label='products',
                model='product'
            )
            delete_perm = Permission.objects.get(
                content_type=content_type,
                codename='delete_product'
            )

            # Очищаем старые разрешения и добавляем новые
            group.permissions.clear()
            group.permissions.add(unpublish_perm, delete_perm)

            if group_created:
                print('Группа "Модератор продуктов" создана')
            else:
                print('Группа "Модератор продуктов" обновлена')

        except Permission.DoesNotExist:
            print('Ошибка: Разрешения не найдены. Выполните миграции.')
            return
        except ContentType.DoesNotExist:
            print('Ошибка: Модель Product не найдена.')
            return

        print("\nСоздание пользователей...")

        # Создаем суперпользователя
        if not User.objects.filter(email='admin@example.com').exists():
            admin = User.objects.create(
                email='admin@example.com',
                is_superuser=True,
                is_staff=True,
                is_active=True,
                first_name='Админ',
                last_name='Админов'
            )
            admin.set_password('admin123')
            admin.save()
            print('Создан суперпользователь: admin@example.com (пароль: admin123)')
        else:
            print('Суперпользователь уже существует: admin@example.com')

        # Создаем модератора
        if not User.objects.filter(email='moderator@example.com').exists():
            moderator = User.objects.create(
                email='moderator@example.com',
                is_superuser=False,
                is_staff=True,
                is_active=True,
                first_name='Модератор',
                last_name='Модераторов'
            )
            moderator.set_password('moderator123')
            moderator.save()
            moderator.groups.add(group)
            print('Создан модератор: moderator@example.com (пароль: moderator123)')
        else:
            moderator = User.objects.get(email='moderator@example.com')
            moderator.groups.add(group)
            print('Модератор обновлен: moderator@example.com')

        # Создаем обычного пользователя
        if not User.objects.filter(email='user@example.com').exists():
            user = User.objects.create(
                email='user@example.com',
                is_superuser=False,
                is_staff=False,
                is_active=True,
                first_name='Пользователь',
                last_name='Пользователев'
            )
            user.set_password('user123')
            user.save()
            print('Создан пользователь: user@example.com (пароль: user123)')
        else:
            print('Пользователь уже существует: user@example.com')

        print("\nГотово!")