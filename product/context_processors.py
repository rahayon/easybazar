from .models import Category, Product
from math import ceil


def category(request):
    return {'all_categories': Category.objects.filter(is_active=True)}

# def latest_product(request):
#     products = Product.objects.all()
#     n = len(products)
#     nslides = n//3 + ceil((n/3)-(n//3))
#     print(nslides)
#     latest_products = [products, range(1,nslides) ]
#     return {'latest_products': latest_products}
    