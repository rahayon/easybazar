from coupon.models import Coupon
from coupon.forms import CouponApplyForm
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.dates import timezone_today
from django.utils import timezone
# Create your views here.


class CouponApply(View):

    def post(self, request):
        now = timezone.now()
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            print('Coupon COde: ', code)
            try:
                coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
                print("coupon: ",coupon)
                request.session['coupon_id'] = coupon.id
                print(request.session['coupon_id'])

            except Coupon.DoesNotExist:
                request.session['cuopon_id'] = None
        return redirect('cart:cart-detail')
