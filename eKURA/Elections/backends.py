from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class NationalIDBackend(ModelBackend):
    def authenticate(self, request, national_id=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(national_id=national_id)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
