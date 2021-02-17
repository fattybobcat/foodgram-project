from django.db import models
from django.contrib.auth import get_user_model
#from multiselectfield import MultiSelectField
# Create your models here.

User = get_user_model()
# Возможные варианты выбора для поля tags

TAGS = (("breakfast", "Завтрак"),
               ("lunch", "Обед"),
               ("dinner", "Ужин"))


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="recipes",
                               verbose_name="Автор",
                               )
    title = models.CharField(max_length=300,
                             verbose_name="Название рецепта",
                             )
    description = models.TextField(max_length=4000,
                                   verbose_name="Описание"
                                   )
    pub_date = models.DateTimeField("Дата добавления",
                                    auto_now_add=True,
                                    db_index=True
                                    )
    image = models.ImageField(upload_to="recipes/",
                              blank=True,
                              null=True,
                              verbose_name="Изображение",
                              )
   # tag = MultiSelectField(choices=TAGS, verbose_name=_('Тег'))
    time = models.PositiveIntegerField(verbose_name="Время приготовления")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'


class Ingredient(models.Model):
    """Ингредиенты"""
    name = models.CharField(max_length=300,
                             verbose_name="Название ингредиента",
                             )
    dimension = models.CharField(max_length=30,
                            verbose_name="Единица измерения",
                            )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name
