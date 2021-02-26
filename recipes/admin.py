from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Ingredient, Recipe, User


class UserAdmin(BaseUserAdmin):
    list_filter = ('first_name', 'email')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "time", "description", "pub_date", "author")
    search_fields = ("title",)
    list_filter = ("pub_date", "author",)
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "dimension")
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
