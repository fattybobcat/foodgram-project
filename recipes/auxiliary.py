from django.db.models import Q

from .models import TAG_CHOICES


def get_ingredients(request):
    ing_dict = {}
    for key in request.POST:
        if key.startswith("nameIngredient"):
            value = key[15:]
            ing_dict[request.POST[key]] = (
                request.POST["valueIngredient_" + value],
                request.POST["unitsIngredient_" + value]
            )
    return ing_dict


def tag_collect(request):
    """Собирает теги для фильтрации рецептов на странице"""
    tags = []
    for label, _ in TAG_CHOICES:
        if request.GET.get(label, ""):
            tags.append(label)
    if tags:
        or_condition = Q()
        for i in tags:
            or_condition.add(Q(tags__contains=i), Q.OR)
        return tags, or_condition
    else:
        return tags, None
