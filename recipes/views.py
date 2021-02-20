import json
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import View
from django.shortcuts import get_object_or_404, render, redirect
from .form import RecipeForm
from .models import (
    Ingredient,
    Recipe,
    IngredientAmount,
)


def get_ingredients(request):
     ing_dict = {}
     for key in request.POST:
         if key.startswith('nameIngredient'):
             value = key[15:]
             ing_dict[request.POST[key]] = (request.POST['valueIngredient_' + value],
                                            request.POST['unitsIngredient_' + value]
                                            )
     return ing_dict
#
# class Ingredients(View):
#     """
#     Фильтрация ингредиентов по GET запросу от js
#     """
#     def get(self, request):
#         ingredient = request.GET['query']
#         ingredients = list(Ingredient.objects.filter(
#             title__icontains=ingredient).values('title', 'dimension'))
#         return JsonResponse(ingredients, safe=False)


def index(request):
    #filters = request.GET.getlist('filters')
    #if filters:
    #    recipe_list = Recipe.objects.filter(
    #        tags__value__in=filters).distinct()
    #else:
    #    recipe_list = Recipe.objects.all()
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    print(recipe_list)
    return render(request, 'index.html', {'recipe_list': recipe_list,
                                          'page': page,
                                          'paginator': paginator, })


def new_recipe(request):
    """Create new recipe"""
    headline = "Создание рецепта"
    button = "Создать рецепт"
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    print(form.data)
    ingredients_names = get_ingredients(request)
    print("ingredietn" , ingredients_names)
    if request.method == "POST":
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for key in ingredients_names:
                IngredientAmount.add_ingredient(
                    IngredientAmount,
                    recipe.id,
                    key,
                    ingredients_names[key][0]
                )

            return redirect('index')
    form = RecipeForm()
    return render(request,
                  "formRecipe.html",
                  {"form": form,
                   "headline": headline,
               #    'new_recipe': new_recipe,
                   "button": button,
                   }
                  )

class  EditRecipe(View):
    """ Form for Edit Recipe """
   # pass
    def get(self, request, recipe_id):
        headline = "Редактирование рецепта"
        button = "Редактировать рецепт"
        print(request)

        recipe = Recipe.objects.get(id=recipe_id)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredients = recipe.amounts.all()
        for i in ingredients:
            print(i)
        print(ingredients)
        print(recipe.ingredients)
        if request.user != recipe.author:
            return redirect('index')
        form = RecipeForm(instance=recipe)

        return render(request,
                  "formRecipe.html",
                  context={'form': form, 'headline': headline}
                  )

def shopping_list(request):
    pass

def follow_index(request):
    pass

def favorites(request):
    pass

