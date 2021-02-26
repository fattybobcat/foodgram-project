from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('recipes/<int:recipe_id>', views.recipe_single, name="recipe_single"),
    path('recipes/new/', views.new_recipe, name="recipe_new"),
    path('recipes/edit/<int:recipe_id>/', views.EditRecipe.as_view(), name="recipe_edit"),
    path('recipes/edit/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('follow/', views.follow_index, name="follow_index"),
    path('favorite', views.favorite, name="favorite_recipes"),
    path('shopping_list/', views.shopping_list, name="shopping_list"),
    path('tech', views.tech, name='tech'),
    path('about', views.about, name='about'),

    path('<username>/', views.profile, name='profile'),

]