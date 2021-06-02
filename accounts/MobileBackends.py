from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class MobileBackend(ModelBackend):
    def authenticate(self, request, mobile=None, password=None, **kwargs):
        if mobile is None:
            return None
        else:
            try:
                user = CustomUser.objects.get(mobile=mobile)
            except CustomUser.DoesNotExist:
                return None

        if user.check_password(password):
            return user
            
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None