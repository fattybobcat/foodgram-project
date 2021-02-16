from django.contrib import admin
from .models import Recipe, Ingredient

class RecipeAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("author", "title", "description", "pub_date")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("slug",)
    # добавляем возможность фильтрации по дате
    list_filter = ("author",)
    empty_value_display = "-пусто-"

class IngredientAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("title", "dimension")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("title",)
    # добавляем возможность фильтрации по дате
    list_filter = ("title",)
    empty_value_display = "-пусто-"

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)