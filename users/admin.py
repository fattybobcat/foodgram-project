from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()

class Follow(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             related_name="follower",
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               null=True,
                               related_name="following",
                               )

    class Meta:
        unique_together = [["user", "author"]]


class Favorites(models.Model):
    """Модель Избранных рецептов"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="favorite_subscriber",
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="favorite_recipe",
                               )

class Wishlist(models.Model):
    """Модель Списока покупок"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="wishlist_subscriber",
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="wishlist_recipe",
                               )