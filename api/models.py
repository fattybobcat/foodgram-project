from django.contrib.auth import get_user_model
from django.db import models
from recipes.models import Recipe


User = get_user_model()


class Follow(models.Model):
    """Model for subscriptions"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             related_name="follower",
                             verbose_name="Пользователь",
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               null=True,
                               related_name="following",
                               verbose_name="Автор",
                               )

    class Meta:
        unique_together = [["user", "author"]]

    def __str__(self):
        return f'User: {self.user}, author: {self.author}'

class FavoriteRecipe(models.Model):
    """Favorite recipes"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             related_name="favoriter",
                             verbose_name="Пользователь",
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="favorite_recipe",
                               verbose_name="Избранный рецепт",
                               )

class Wishlist(models.Model):
    """List wishlist ingredient of recipes"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlist_subscriber")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="wishlist_recipe")