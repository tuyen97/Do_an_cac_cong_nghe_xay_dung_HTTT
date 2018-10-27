from bakery_store.models import User

class MyBackend:

    def authenticate(self, user_name=None, password=None):
        try:
            user = User.objects.get(user_name=user_name, password=password)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None