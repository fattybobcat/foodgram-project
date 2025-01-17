from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from multiselectfield import MultiSelectField

User = get_user_model()


TAG_CHOICES = [
        ("breakfast", "Завтрак"),
        ("lunch", "Обед"),
        ("dinner", "Ужин"),
    ]


class Ingredient(models.Model):
    """Ингредиенты"""
    title = models.CharField(max_length=300,
                             verbose_name="Название ингредиента",
                             )
    dimension = models.CharField(max_length=30,
                                 verbose_name="Единица измерения",
                                 )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return str(self.title)


class IngredientAmount(models.Model):
    """Ингредиенты в рецепте"""
    amount = models.PositiveIntegerField(default=1,
                                         verbose_name="Количество",
                                         )
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name="amounts"
                                   )
    recipe = models.ForeignKey('Recipe',
                               on_delete=models.CASCADE,
                               related_name="amounts"
                               )

    def add_ingredient(self, recipe_id, title, amount):
        if int(amount) > 0:
            ingredient, create = Ingredient.objects.get_or_create(title=title)
            return self.objects.get_or_create(recipe_id=recipe_id,
                                              ingredient=ingredient,
                                              amount=amount)


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
    tags = MultiSelectField(choices=TAG_CHOICES,
                            blank=True,
                            null=True,
                            verbose_name="Теги",
                            )
    time = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                       verbose_name="Время приготовления")
    ingredients = models.ManyToManyField(Ingredient,
                                         through=IngredientAmount,
                                         through_fields=("recipe",
                                                         "ingredient"
                                                         ),
                                         verbose_name="Список ингредиентов",
                                         )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def get_ingredients(self):
        return "\n".join(
            self.ingredient.all().values_list("title", flat=True))

    get_ingredients.short_description = "Ингредиенты"
