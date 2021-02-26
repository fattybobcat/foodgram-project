from django.urls import path

from . import views

urlpatterns = [
    path("ingredients",
         views.ingredient_hints,
         name="ingredient_hints"),
    path("favorites",
         views.FavoriteApi.as_view(),
         name="favorites"),
    path("favorites/<int:id>",
         views.FavoriteApi.as_view(),
         name="favorite_delete"),
    path("subscriptions",
         views.SubscriptionApi.as_view(),
         name="subscriptions"),
    path("subscriptions/<int:id>",
         views.SubscriptionApi.as_view(),
         name="subscriptions_delete"),
    path("purchases",
         views.WishlistApi.as_view(),
         name="purchases"),
    path("purchases/<int:id>",
         views.WishlistApi.as_view(),
         name="purchases_delete"),
]
