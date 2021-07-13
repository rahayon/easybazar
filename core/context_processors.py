from delivery.models import DeliveryLocation
from delivery.forms import DeliveryForm

def delivery_location(request):
    initial_location = request.session.get('delivery_id')
    delivery_location_form = DeliveryForm(initial={'delivery': initial_location})
    loacation = DeliveryLocation.objects.get(id=1)
    return {
        'delivery_location': delivery_location_form,
        'location': loacation,
        }
