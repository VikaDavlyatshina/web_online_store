from django import template

register = template.Library()


@register.filter()
def media_filter(value):
    """
    Универсальный безопасный фильтр.
    Не падает на пустых полях!
    """
    # 1. Если пусто
    if not value:
        return None

    # 2. Если это ImageField объект
    if hasattr(value, "name"):
        # Сначала проверяем name, потом пробуем url
        if value.name:
            try:
                return value.url
            except ValueError:
                return None
        else:
            return None

    # 3. Если это строка
    if isinstance(value, str):
        clean = value.strip()
        if clean:
            return f"/media/{clean.lstrip('/')}"

    # 4. Всё остальное
    return None
