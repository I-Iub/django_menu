from django.db import models


class Menu(models.Model):
    title = models.CharField('Название меню', max_length=100, db_index=True)
    # todo: убрать title_slug и сделать автоматическое создание слага из поля
    #  `title` в нужном месте в коде с помощью python-slugify, например
    title_slug = models.SlugField('Слаг для меню')
    name = models.CharField('Название пункта', max_length=100)
    path = models.CharField('Путь', max_length=255, db_index=True)
    level = models.IntegerField(db_index=True)
    url = models.URLField()

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Список меню'
        # todo: constraint -- parent должен быть уникальным в пределах title

    def __str__(self):
        return f'Menu /{self.title_slug}/{self.path}/ ({self.name})'
