from django import template
from django.http import QueryDict
from django.contrib.auth.decorators import login_required

#from recipes.models import Cart, Favorite
from api.models import FavoriteRecipe

register = template.Library()

@register.filter
def get_recipe_tag(tags_list):
    tags = ""
    if "breakfast" in tags_list:
        tags += str('<li class="card__item"><span class="badge badge_style_orange">Завтрак</span></li>')
    if 'lunch' in tags_list:
        tags += str('<li class="card__item"><span class="badge badge_style_green">Обед</span></li>')
    if 'dinner' in tags_list:
        tags += str('<li class="card__item"><span class="badge badge_style_purple">Ужин</span></li>')
    return tags

@register.filter
def get_description_new_lines(description_recipe):
    description_list = description_recipe.split('\n')
    description = ""
    for i in range(len(description_list)):
        description += str(f'<p class=" single-card__section-text">{description_list[i]}</p>')
    return description

@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.value in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.value)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.value)

    return new_request.urlencode()

@register.filter
def get_is_favorite(recipe, user):
    return FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()
