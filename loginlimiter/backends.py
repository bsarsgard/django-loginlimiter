from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class LimiterBackend(object):
    """
    Login Limiter backend
    ---------------------
    Limit the number of attempts by the user based on their username and/or
    their ip address.

    Please use the following specs to design the app with some flexibility to
    allow an administrator to adjust these numbers.

    * Allow the user 5 attempts before locking them out for 1 minute.
    * Allow the ip_address 30 attempts before locking them out for 5 minutes.
    * Upon successful login clear all failed login attempts by that user/IP
    * from the DB.
    * After the lockout period, clear all failed login attempts from the DB.
    * Please use a sqlite database.
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                # add a strike
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
