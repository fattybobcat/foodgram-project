from django.urls import path

from . import views


urlpatterns = [
    path("ingredients", views.ingredient_hints, name="ingredient_hints"),
    path("subscriptions", views.ingredient_hints, name="ingredient_hints"),
    #path("", )
]