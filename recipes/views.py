import json
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import View
from django.shortcuts import get_object_or_404, render, redirect
from .form import RecipeForm
from api.models import FavoriteRecipe, Follow
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
    return render(request, 'index.html', {'recipe_list': recipe_list,
                                          'page': page,
                                          'paginator': paginator, })


def new_recipe(request):
    """Create new recipe"""
    headline = "Создание рецепта"
    button = "Создать рецепт"
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    #print(form.data)
    ingredients_names = get_ingredients(request)
    #print("ingredietn", ingredients_names)
    if request.method == "POST":
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            print(recipe.id)
            for key in ingredients_names:
                IngredientAmount.add_ingredient(
                    IngredientAmount,
                    recipe.id,
                    key,
                    ingredients_names[key][0]
                )
            form.save_m2m()
            return redirect('recipe_single', recipe_id=recipe.id)
    form = RecipeForm()
    return render(request,
                  "formRecipe.html",
                  {"form": form,
                   "headline": headline,
                   "button": button,
                   }
                  )

class  EditRecipe(View):
    """ Form for Edit Recipe """

    def get(self, request, recipe_id):
        headline = "Редактирование рецепта"
        button = "Редактировать рецепт"
        print(request)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredients = recipe.amounts.all()
        print("2", ingredients)
        if request.user != recipe.author:
            return redirect('index')
        form = RecipeForm(instance=recipe)

        return render(request,
                  "editRecipe.html",
                  context={'form': form,
                           'headline': headline,
                           'recipe': recipe,
                           'ingredients': ingredients}
                  )

    def post(self, request, recipe_id):
        headline = "Редактирование рецепта"
        print(request)
        ingredients_names = get_ingredients(request)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
        print(form.data)
        if request.user != recipe.author:
            return redirect('index')
        if form.is_valid():
            IngredientAmount.objects.filter(recipe=recipe).delete()
            form.save()
            for key in ingredients_names:
                IngredientAmount.add_ingredient(
                    IngredientAmount,
                    recipe.id,
                    key,
                    ingredients_names[key][0]
                )
            print(ingredients_names)
            return redirect('recipe_single', recipe_id=recipe_id)

        return render(request,
                      "singlePage.html",
                      {'id': recipe.id,
                       'headline': headline,
                       'recipe': recipe,
                       'ingredients': ingredients,
                       }
                      )


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author == request.user:
        recipe.delete()
    return render(request, 'deleteRecipeDone.html')

def recipe_single(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.amounts.all()
    print(ingredients)
    return render(request, "singlePage.html",
                  {"recipe": recipe,
                   "ingredients": ingredients,
                   }
                  )


def shopping_list(request):
    pass


def follow_index(request):
    follow_list = Follow.objects.filter(
        user__id=request.user.id).all()
    print(follow_list)
    paginator = Paginator(follow_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'followPage.html',
                  {'follow_list': follow_list,
                   'page': page,
                   'paginator': paginator, }
                 )




def favorite(request):
    recipe_list = Recipe.objects.filter(
        favorite_recipe__user__id=request.user.id).all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'favoriteRecipes.html',
                  {'recipe_list': recipe_list,
                   'page': page,
                   'paginator': paginator, })
