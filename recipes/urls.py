from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/new/', views.new_recipe, name='recipe_new'),

   # path('<username>/', views.profile, name='profile'),
]