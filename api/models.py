from django.contrib.auth import get_user_model
from django.db import models


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