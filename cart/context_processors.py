from .cart import Cart
from wish.models import WishList


def cart(request):
    return {'cart': Cart(request)}


def wish(request):
    if request.user.is_authenticated:
        wish_item = WishList.objects.filter(user=request.user).count()
    else:
        wish_item = None

    return {'wish': wish_item}
