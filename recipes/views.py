from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from api.models import Follow
from foodgram.settings import COUNT_RECIPE

from .auxiliary import get_ingredients, tag_collect
from .form import RecipeForm
from .models import IngredientAmount, Recipe


def index(request):
    tags, tags_filter = tag_collect(request)
    if tags_filter:
        recipe_list = Recipe.objects.filter(tags_filter).distinct()
    else:
        recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, COUNT_RECIPE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request,
                  "index.html",
                  {"tags": tags,
                   "page": page,
                   "paginator": paginator, }
                  )


@login_required
def new_recipe(request):
    """Create new recipe"""
    headline = "Создание рецепта"
    button = "Создать рецепт"
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients_names = get_ingredients(request)
    if request.method == "POST":
        keys_form = [*form.data.keys()]
        if 'tags' in keys_form:
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
                form.save_m2m()
                return redirect('recipe_single', recipe_id=recipe.id)
        error_tag = "Выберите один из предложенных 'тегов'"
        return render(request,
                      "formRecipe.html",
                      {"form": form,
                       "headline": headline,
                       "button": button,
                       "error_tag": error_tag,
                       }
                      )
    return render(request,
                  "formRecipe.html",
                  {"form": form,
                   "headline": headline,
                   "button": button,
                   }
                  )


class EditRecipe(View):
    """ Form for Edit Recipe """
    def get(self, request, recipe_id):
        headline = "Редактирование рецепта"
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredients = recipe.amounts.all()
        if request.user != recipe.author:
            return redirect('index')
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None,
                          instance=recipe)
        return render(request,
                      "editRecipe.html",
                      context={'form': form,
                               'headline': headline,
                               'recipe': recipe,
                               'ingredients': ingredients}
                      )

    def post(self, request, recipe_id):
        headline = "Редактирование рецепта"
        ingredients_names = get_ingredients(request)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredients = recipe.amounts.all()
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None,
                          instance=recipe,
                          )
        if request.user != recipe.author:
            return redirect('index')
        if form.is_valid():
            keys_form = [*form.data.keys()]
            if 'tags' in keys_form:
                IngredientAmount.objects.filter(recipe=recipe).delete()
                recipe = form.save(commit=False)
                recipe.author = request.user
                recipe.save()
                form.save()
                for key in ingredients_names:
                    IngredientAmount.add_ingredient(
                        IngredientAmount,
                        recipe.id,
                        key,
                        ingredients_names[key][0]
                    )
                form.save_m2m()
                return redirect('recipe_single', recipe_id=recipe_id)
            error_tag = "Выберите один из предложенных 'тегов'"
            return render(request,
                          "editRecipe.html",
                          context={"form": form,
                                   "headline": headline,
                                   "recipe": recipe,
                                   "ingredients": ingredients,
                                   "error_tag": error_tag,
                                   }
                          )
        return render(request,
                      "singlePage.html",
                      {'id': recipe.id,
                       'headline': headline,
                       'recipe': recipe,
                       'ingredients': ingredients_names,
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
    return render(request, "singlePage.html",
                  {"recipe": recipe,
                   "ingredients": ingredients,
                   }
                  )


def profile(request, username):
    username = get_object_or_404(User, username=username)
    not_follow = False
    if username.username == request.user.username:
        not_follow = True
    tags, tags_filter = tag_collect(request)
    if tags_filter:
        recipes = Recipe.objects.filter(
            tags_filter
            ).filter(
            author=username
            ).distinct()
    else:
        recipes = Recipe.objects.filter(author=username)
    paginator = Paginator(recipes, COUNT_RECIPE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'pageAuthor.html',
                  {'recipes': recipes,
                   'page': page,
                   'paginator': paginator,
                   'username1': username,
                   "tags": tags,
                   "not_follow": not_follow,
                   }
                  )


@login_required()
def shopping_list(request):
    shop_list = Recipe.objects.filter(
        wishlist_recipe__user__id=request.user.id).all()
    shop_list_count = shop_list.count()
    print(shop_list_count)
    return render(request,
                  "shopList.html",
                  {"shop_list": shop_list,
                   "shop_list_count": shop_list_count,
                   }
                  )


def download_wishlist(request):
    recipes_shop_list = Recipe.objects.filter(
        wishlist_recipe__user__id=request.user.id).all()
    ingredient_list = IngredientAmount.objects.filter(
        recipe__in=recipes_shop_list)
    summary = []
    ingredients = {}
    for item in ingredient_list:
        if item.ingredient in ingredients.keys():
            ingredients[item.ingredient] += item.amount
        else:
            ingredients[item.ingredient] = item.amount
    for ing, amount in ingredients.items():
        summary.append('{} - {} {} \n'.format(
            ing.title, amount, ing.dimension)
        )
    response = HttpResponse(
        summary, content_type='application/text charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response


def follow_index(request):
    follow_list = Follow.objects.filter(
        user__id=request.user.id).all()
    paginator = Paginator(follow_list, COUNT_RECIPE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'followPage.html',
                  {'follow_list': follow_list,
                   'page': page,
                   'paginator': paginator, }
                  )


def favorite(request):
    tags, tags_filter = tag_collect(request)
    if tags_filter:
        recipe_list = Recipe.objects.filter(
            tags_filter).filter(
            favorite_recipe__user__id=request.user.id).distinct()
    else:
        recipe_list = Recipe.objects.filter(
            favorite_recipe__user__id=request.user.id).all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'favoriteRecipes.html',
                  {'recipe_list': recipe_list,
                   'page': page,
                   'paginator': paginator,
                   "tags": tags,
                   }
                  )


def about(request):
    return render(request, "about.html")


def tech(request):
    return render(request, "tech.html")


def page_not_found(request, exception):
    return render(request, "404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "500.html", status=500)
