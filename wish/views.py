from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from cart.forms import CartAddProductForm
from .models import WishList
from product.models import Product
from django.contrib import messages


# Create your views here.
class WishListView(View):
    def get(self, request):
        wishes = WishList.objects.filter(user=self.request.user).prefetch_related('product')
        print(wishes)
        form = CartAddProductForm()
        context = {
            'wishes': wishes,
            'form': form
        }
        return render(request, 'wish/wishes.html', context)


@login_required
def add_to_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)

    wish_item = WishList.objects.filter(user=request.user, product=product)
    if wish_item.exists():
        messages.warning(request, 'This item was already added in your wishlist')
    else:
        wish = WishList(user=request.user)
        wish.save()
        wish.product.add(product)
        wish.save()
        messages.info(request, 'This product is added in your wishlist')
    return redirect("wish:wishes")


@login_required()
def remove_from_wish(request, slug):
    product = get_object_or_404(Product, slug=slug)
    wish_item = WishList.objects.filter(user=request.user, product=product)
    if wish_item.exists():
        wish_item.delete()
    return redirect('wish:wishes')
