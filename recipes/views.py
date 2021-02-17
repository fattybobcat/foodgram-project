import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from .form import RecipeForm
from .models import (
    Ingredient,
    Recipe,
)


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

@login_required
def new_recipe(request):
    """Create new recipe"""
    headline = "Создание рецепта"
    button = "Создать рецепт"
   # new_recipes = True
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            print("Ok!!!!!")
            return redirect('recipes:index')
    form = RecipeForm()
    return render(request,
                  'recipeNew.html',
                  {form: form,
                   'headline': headline,
               #    'new_recipe': new_recipe,
                   "button": button,
                   }
                  )