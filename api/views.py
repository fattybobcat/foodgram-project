import json
from django.shortcuts import redirect
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views import View
from recipes.models import Ingredient, Recipe
from .models import FavoriteRecipe
from django.shortcuts import get_object_or_404, render, redirect


def ingredient_hints(request):
    #text = request.GET['query']
    text = request.GET.get("query").lower()
    ing_list = Ingredient.objects.filter(title__startswith=text).order_by('title')
    result = [{"title": item.title, "dimension": item.dimension} for item in ing_list]
    return JsonResponse(result, safe=False)


class FavoriteApi(LoginRequiredMixin, View):
     def post(self, request):
         req = json.loads(request.body)
         recipe_id = req.get("id", None)
         if recipe_id:
             recipe = get_object_or_404(Recipe, id=recipe_id)
             obj, created = FavoriteRecipe.objects.get_or_create(
                 user=request.user, recipe=recipe
             )
             if created:
                 return JsonResponse({"success": True})
             return JsonResponse({"success": False})
         return JsonResponse({"success": False}, status=400)

     def delete(self, request, id):
         recipe = get_object_or_404(
             FavoriteRecipe, recipe=id, user=request.user
         )
         recipe.delete()
         return JsonResponse({"success": True})