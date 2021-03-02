from django import template

from api.models import FavoriteRecipe, Follow, Wishlist

register = template.Library()


@register.filter
def get_recipe_tag(tags_list):
    tags = ""
    if "breakfast" in tags_list:
        tags += str('<li class="card__item">'
                    '<span class="badge badge_style_orange">'
                    'Завтрак</span></li>')
    if 'lunch' in tags_list:
        tags += str('<li class="card__item">'
                    '<span class="badge badge_style_green">'
                    'Обед</span></li>')
    if 'dinner' in tags_list:
        tags += str(
            '<li class="card__item">'
            '<span class="badge badge_style_purple">'
            'Ужин</span></li>'
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
        tag_list = request.GET["tag"]
        tag_list = tag_list.split("__")
        if tag not in tag_list:
            tag_list.append(tag)
        else:
            tag_list.remove(tag)
        if "" in tag_list:
            tag_list.remove("")
        result = "__".join(tag_list)
        return result
    return tag


@register.simple_tag
def set_tags(request, tags, value):
    """Устанавливает get параметры в зависимости
    от выбранных тегов"""
    request_object = request.GET.copy()
    if request.GET.get(value):
        request_object.pop(value)
    elif value in tags:
        for tag in tags:
            if tag != value:
                request_object[tag] = "tag"
    else:
        request_object[value] = "tag"

    return request_object.urlencode()


@register.simple_tag
def set_page(request, value):
    """Устанавливает get параметры в зависимости
    от выбранной страницы"""
    request_object = request.GET.copy()
    request_object["page"] = value
    return request_object.urlencode()
