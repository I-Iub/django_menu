from django.db import models


class Menu(models.Model):
    title = models.CharField('Название меню', max_length=100, db_index=True)
    name = models.CharField('Название пункта', max_length=100)
    # todo: убрать name_slug и сделать автоматическое создание с помощью python-slugify
    #  из поля `name`
    # name_slug = models.SlugField()
    path = models.CharField('Путь', max_length=255, db_index=True)
    level = models.IntegerField(db_index=True)
    url = models.URLField()

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Список меню'
        # todo: constraint -- parent должен быть уникальным в пределах title

    def __str__(self):
        return f'Menu id={self.id} {self.title} {self.name} path={self.path}'
