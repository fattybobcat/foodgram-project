import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import Ingredient, Recipe

from .models import FavoriteRecipe, Follow, Wishlist


def ingredient_hints(request):
    text = request.GET.get("query").lower()
    ing_list = Ingredient.objects.filter(title__startswith=text
                                         ).order_by('title')
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


class SubscriptionApi(LoginRequiredMixin, View):
    def post(self, request):
        req = json.loads(request.body)
        author_id = req.get("id", None)
        if author_id:
            author = get_object_or_404(User, id=author_id)
            obj, created = Follow.objects.get_or_create(
                user=request.user,
                author=author
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, id):
        subscript = get_object_or_404(
            Follow, author=id, user=request.user
        )
        subscript.delete()
        return JsonResponse({"success": True})


class WishlistApi(View):
    def post(self, request):
        req = json.loads(request.body)
        recipe_id = req.get("id", None)
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = Wishlist.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, id):
        recipe = get_object_or_404(
            Wishlist, recipe=id, user=request.user
        )
        recipe.delete()
        return JsonResponse({"success": True})
