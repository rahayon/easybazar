from .models import Product
from django_filters.filters import RangeFilter

# class ProductRangeFilter(RangeFilter):
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         values = [p.sale_price() for p in Product.objects.all()]
#         min_value = min(values)
#         max_value = max(values)

#     class Meta:
#         model = Product
