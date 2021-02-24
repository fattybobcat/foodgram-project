from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('recipes/new/', views.new_recipe, name="recipe_new"),
    path('recipes/edit/<int:recipe_id>/', views.EditRecipe.as_view(), name="recipe_edit"),
    path('recipes/edit/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    #path('ingredients/', views.Ingredients.as_view(), name='ingredients'),
    path('follow/', views.follow_index, name="follow_index"),
    path('favorites/', views.favorites, name="favorites"),
    path('shopping_list/', views.shopping_list, name="shopping_list"),

   # path('<username>/', views.profile, name='profile'),
]