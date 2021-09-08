from django.urls import path
from .views import CategoryDetail, ProductListView, ProductDetail, SearchProductView, SubmitReview

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('search/', SearchProductView.as_view(), name='search-products'),
    path('<slug:slug>/', ProductDetail.as_view(), name='Product_detail'),
    path('submit_review/<int:product_id>/', SubmitReview.as_view(), name='submit_review'),
    path('category/<slug:slug>/', CategoryDetail.as_view(), name='category_detail'),

]
