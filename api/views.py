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
    ing_list = Ingredient.objects.filter(title__istartswith=text
                                         ).order_by('title')
    result = [
        {"title": item.title, "dimension": item.dimension} for item in ing_list
    ]
    return JsonResponse(result, safe=False)


class BaseView(View):
    model = None
    item_id = None
    model_get = None
    item_get = None
    filter_kwargs = {"key": "value"}
    fields = (None,)

    def post(self, request, filter_kwargs):
        req = json.loads(request.body)
        self.item_id = req.get("id", None)
        if self.item_id:
            self.item_get = get_object_or_404(self.model_get, id=self.item_id)
            self.filter_kwargs[self.fields[0]] = self.item_get
            obj, created = self.model.objects.get_or_create(
                **self.filter_kwargs
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, id):
        self.item_get = get_object_or_404(
            self.model, **self.filter_kwargs
        )
        self.item_get.delete()
        return JsonResponse({"success": True})


class FavoriteApi(LoginRequiredMixin, BaseView):
    model = FavoriteRecipe
    model_get = Recipe
    fields = ("recipe",)

    def post(self, request):
        self.filter_kwargs = {"user": request.user,
                              "recipe": self.item_get, }
        return super(FavoriteApi, self).post(request, self.filter_kwargs)

    def delete(self, request, id):
        self.filter_kwargs = {"user": request.user,
                              "recipe": id, }
        return super(FavoriteApi, self).delete(request, self.filter_kwargs)


class SubscriptionApi(LoginRequiredMixin, BaseView):
    model = Follow
    model_get = User
    fields = ("author",)

    def post(self, request):
        self.filter_kwargs = {"user": request.user,
                              "author": self.item_get, }
        return super(SubscriptionApi, self).post(request, self.filter_kwargs)

    def delete(self, request, id):
        self.filter_kwargs = {"user": request.user,
                              "author": id, }
        return super(SubscriptionApi, self).delete(request, self.filter_kwargs)


class WishlistApi(BaseView):
    model = Wishlist
    model_get = Recipe
    fields = ("recipe",)

    def post(self, request):
        self.filter_kwargs = {"user": request.user,
                              "recipe": self.item_get, }
        return super(WishlistApi, self).post(request, self.filter_kwargs)

    def delete(self, request, id):
        self.filter_kwargs = {"user": request.user,
                              "recipe": id, }
        return super(WishlistApi, self).delete(request, self.filter_kwargs)
