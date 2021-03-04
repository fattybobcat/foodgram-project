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
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

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

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"


class Wishlist(models.Model):
    """List wishlist ingredient of recipes"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="wishlist_subscriber",
                             verbose_name="Пользователь",
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="wishlist_recipe",
                               verbose_name="Список для покупок ",
                               )

    class Meta:
        verbose_name = "Список"
        verbose_name_plural = "Списки"
