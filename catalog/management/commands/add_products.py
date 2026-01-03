from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Add test products to the database"

    def handle(self, *args, **kwargs):
        # 1. Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        # 2. Создаём список данных для категорий
        categories_data = [
            {"name": "Без категории", "descriptions": "Товары без указанной категории"},
            {"name": "Смартфоны", "descriptions": "Мобильные телефоны и смартфоны"},
            {"name": "Холодильники", "descriptions": "Холодильное оборудование"},
            {"name": "Компьютеры", "descriptions": "Персональные компьютеры"},
        ]

        # 3. Создаём словарь для хранения объектов категорий
        categories = {}

        # 4. Создаём категории в базе
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data["name"], defaults=category_data
            )
            categories[category.name] = category  # Сохраняем словарь

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Создана категория: {category.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Категория уже существует: {category.name}")
                )

        # 5. Создаём данные для товаров
        products_data = [
            {
                "name": "Смартфон Apple iPhone 17 Pro 256 ГБ оранжевый",
                "descriptions": "Новый флагманский смартфон Apple",
                "category": categories["Смартфоны"],
                "purchase_price": 132000.00,
            },
            {
                "name": "Холодильник с морозильником LG GA-B509MQSL белый",
                "descriptions": "Вместительный холодильник на 342 л. Стильный, белого цвета",
                "category": categories["Холодильники"],
                "purchase_price": 54999.00,
            },
            {
                "name": "Смартфон Samsung Galaxy S25 FE 256 ГБ черный",
                "descriptions": "Оснащен мощным процессором, который обеспечивает молниеносную производительность в любых задачах.",
                "category": categories["Смартфоны"],
                "purchase_price": 54999.00,
            },
            {
                "name": "ПК ARDOR GAMING RAGE H4259",
                "descriptions": "AMD Ryzen 5 7500F, 6 x 3.7 ГГц, 32 ГБ DDR5, GeForce RTX 5060, SSD 1000 ГБ, без ОС, 1 x HDMI, 3 x DisplayPort, Wi-Fi, Bluetooth, AMD B650, блок питания - 650 Вт",
                "category": categories["Компьютеры"],
                "purchase_price": 135000.00,
            },
            {
                "name": "Холодильник с морозильником LG GA-B459CLWL серый",
                "descriptions": "Холодильник на 341 л, внешнее покрытие-металл, размораживание - No Frost, дисплей, 59.5 см х 186 см х 68.2 см",
                "category": categories["Холодильники"],
                "purchase_price": 48999.00,
            },
            {
                "name": "Пижама теплая новогодняя с оленем ",
                "descriptions": "Это не просто домашняя одежда — это маленький праздник, который всегда с вами. Мягкая плюшевая ткань окутывает теплом, а очаровательная вышивка с оленем напоминает о волшебстве зимних дней.",
                "category": categories["Без категории"],
                "purchase_price": 1508.00,
            },
        ]

        # 6. Создаём товары в базе
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data["name"], defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Создан товар: {product.name} - {product.purchase_price} руб."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Товар уже существует: {product.name}")
                )

        # 7. Выводим итоги
        self.stdout.write(self.style.SUCCESS(f"ИТОГО: создано {created_count} товаров"))
        self.stdout.write(
            self.style.SUCCESS(f"Всего категорий: {Category.objects.count()}")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Всего товаров: {Product.objects.count()}")
        )
