#
# class Favorites(models.Model):
#     """Модель Избранных рецептов"""
#     user = models.ForeignKey(User,
#                              on_delete=models.CASCADE,
#                              related_name="favorite_subscriber",
#                              )
#     recipe = models.ForeignKey(Recipe,
#                                on_delete=models.CASCADE,
#                                related_name="favorite_recipe",
#                                )
#
# class Wishlist(models.Model):
#     """Модель Списока покупок"""
#     user = models.ForeignKey(User,
#                              on_delete=models.CASCADE,
#                              related_name="wishlist_subscriber",
#                              )
#     recipe = models.ForeignKey(Recipe,
#                                on_delete=models.CASCADE,
#                                related_name="wishlist_recipe",
#                                )