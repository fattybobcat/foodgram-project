def shop_list_size(request):
    if request.user.is_authenticated:
        count = request.user.wishlist_subscriber.all().count()
    else:
        count = 0
    return {
        "shop_list_size": count
    }
