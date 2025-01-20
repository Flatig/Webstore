from django.contrib.auth.models import User


class EmailAuthBackend:
    @staticmethod  # The method will not require passing a class instance (self) when calling
    def authenticate(request, username=None, password=None):  # Specify default values if no arguments are passed
        user = User.objects.filter(email=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)  # Trying to find User model object with primary key (pk)
        except User.DoesNotExist:
            return None
