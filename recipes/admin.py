from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q
from django_admin_multiple_choice_list_filter.list_filters import \
    MultipleChoiceListFilter

from .models import Ingredient, IngredientAmount, Recipe, User

TAG_CHOICES = [
        ("breakfast", "Завтрак"),
        ("lunch", "Обед"),
        ("dinner", "Ужин"),
    ]


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    min_num = 1


def tag_filt(request):
    """Собирает теги для фильтрации рецептов на странице"""
    tags = request
    if tags:
        or_condition = Q()
        for i in tags:
            or_condition.add(Q(tags__contains=i), Q.OR)
        return tags, or_condition
    else:
        return tags, None


class TagsListFilter(MultipleChoiceListFilter):
    title = 'tags'
    parameter_name = 'tags__contains'

    def lookups(self, request, model_admin):
        return TAG_CHOICES

    def queryset(self, request, queryset):
        if request.GET.get(self.parameter_name):
            a = request.GET[self.parameter_name].split(",")
            tags, tags_filter = tag_filt(a)
            if tags_filter:
                queryset = queryset.filter(tags_filter).distinct()
        return queryset


class UserAdmin(BaseUserAdmin):
    list_filter = ('first_name', 'email')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "time", "description",
                    "pub_date", "author", "count_favorite", "tags")
    search_fields = ("title", "tags", )
    list_filter = ("pub_date", "author", TagsListFilter)
    empty_value_display = "-пусто-"
    inlines = [
        IngredientAmountInline,
    ]
    autocomplete_fields = ("ingredients",)

    def count_favorite(self, obj):
        return obj.favorite_recipe.count()

    count_favorite.short_description = "в избранном кол."


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "dimension")
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
