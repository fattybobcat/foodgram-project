from django import template

from api.models import FavoriteRecipe, Follow, Wishlist

register = template.Library()

@register.filter
def get_recipe_tag(tags_list):
    tags = ""
    if "breakfast" in tags_list:
        tags += str('<li class="card__item"><span class="badge badge_style_orange">Завтрак</span></li>')
    if 'lunch' in tags_list:
        tags += str('<li class="card__item"><span class="badge badge_style_green">Обед</span></li>')
    if 'dinner' in tags_list:
        tags += str(
            '<li class="card__item"><span class="badge badge_style_purple">Ужин</span></li>'
        )
    return tags


@register.filter
def get_description_new_lines(description_recipe):
    description_list = description_recipe.split('\n')
    description = ""
    for i in range(len(description_list)):
        description += str(
            f'<p class=" single-card__section-text">{description_list[i]}</p>'
        )
    return description


@register.filter
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


@register.filter
def get_is_follow(recipe, user):
    return Follow.objects.filter(user=user, author=recipe.author).exists()


@register.filter
def get_is_follow2(author, user):
    return Follow.objects.filter(user=user, author=author).exists()

@register.filter
def is_shop(recipe, user):
    return Wishlist.objects.filter(user=user, recipe=recipe).exists()

@register.filter
def get_tags(request, tag):
    if "tag" in request.GET:
        print("request.GET", request.GET)
        print('0 error')
        tag_list = request.GET["tag"]
        print('1 error')
        print("tag_list", tag_list)
        print('2 error')
        tag_list = tag_list.split("__")
        if not tag in tag_list:
            tag_list.append(tag)
            print('3-1', tag_list)
        else:
            tag_list.remove(tag)
            print('3-2', tag_list)
        if "" in tag_list:
            tag_list.remove("")
            print('4-2', tag_list)
        result = "__".join(tag_list)
        print("result", result)
        return result
    return tag