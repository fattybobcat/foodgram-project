import json
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from recipes.models import Ingredient


SUCCESS_RESPONSE = JsonResponse({"success": True})
FAIL_RESPONSE = HttpResponse()


@require_http_methods(["GET"])
def get_ingredients(request):
    query = request.GET.get("query").lower()
    ingredients = Ingredient.objects.filter(
        title__contains=query).values("title", "dimension")
    return JsonResponse(list(ingredients), safe=False)


def ingredient_hints(request):
    text = request.GET['query']
    ing_list = Ingredient.objects.filter(title__startswith=text).order_by('title')
    result = [{"title": item.title, "dimension": item.dimension} for item in ing_list]
    return JsonResponse(result, safe=False)

#def favorites(request):
 #