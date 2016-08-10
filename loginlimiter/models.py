from django.contrib.auth.models import User
from django.db import models


class LoginAttempt(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    attempted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s (%s) - %s" % (self.user, self.ip_address,
                self.attempted)
