from decimal import Decimal
from django.conf import settings
from product.models import Product
from coupon.models import Coupon
from delivery.models import  DeliveryLocation, DeliveryType


class Cart (object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')
        self.delivery_id = self.session.get('delivery_id')

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 'price': str(product.sale_price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        del self.session['delivery_id']
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount_percentage / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    @property
    def delivery(self):
        if self.delivery_id:
            try:
                return DeliveryLocation.objects.get(id=self.delivery_id)
            except DeliveryLocation.DoesNotExist:
                pass
        
        return  DeliveryLocation.objects.get(id=1)

    def delivery_free_shipping(self):
        if self.delivery:
            #delivery_type = DeliveryType.objects.get(location=self.delivery, type_of_delivery="Free")
            return self.delivery.delivery_target_amount



    def get_delivery_status(self):
        if self.delivery:
            if self.get_total_price_after_discount() >= self.delivery.delivery_target_amount:
                delivery_type = DeliveryType.objects.get(location=self.delivery, type_of_delivery="Free")
                return delivery_type.type_of_delivery
            else:
                delivery_type = DeliveryType.objects.get(location=self.delivery, type_of_delivery="Flat")
                return delivery_type.type_of_delivery

    def get_delivery_charge(self):
        if self.delivery:
            if self.get_total_price_after_discount() >= self.delivery.delivery_target_amount:
                delivery_type = DeliveryType.objects.get(location=self.delivery, type_of_delivery="Free")
                print("Delivery Types: Free ", delivery_type.delivery_charge)
                return delivery_type.delivery_charge
            else:
                delivery_type = DeliveryType.objects.get(location=self.delivery, type_of_delivery="Flat")
                print("Delivery Types: Flat ", delivery_type.delivery_charge)
                return delivery_type.delivery_charge
            #return self.delivery.delivery_charge
        return Decimal(0)

    def get_total_price_with_delivery(self):
        return self.get_total_price_after_discount() + self.get_delivery_charge()
