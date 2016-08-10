from django.contrib.auth.models import User
from django.db import models


class LoginAttempt(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    attempted = models.DateTimeField()
