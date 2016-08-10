import datetime

from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from .models import LoginAttempt

class LimiterAuthenticationForm(AuthenticationForm):
    """
    Login Limiter Authentication
    ----------------------------
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
    def clean(self):
        try:
            cleaned_data = super(LimiterAuthenticationForm, self).clean()
            return cleaned_data
        except forms.ValidationError, ex:
            if ex.code == 'invalid_login':
                # add a strike to ip
                attempt = LoginAttempt(
                        ip_address=self.request.META.get('REMOTE_ADDR'))
                try:
                    # associate with user account if found
                    attempt.user = User.objects.get(
                            username=self.cleaned_data.get('username'))
                except:
                    pass
                attempt.save()
            raise ex


    def confirm_login_allowed(self, user):
        # make sure user is active
        if not user.is_active:
            raise forms.ValidationError(
                ("This account is inactive."),
                code='inactive',
            )

        # check user lockout
        user_attempts = LoginAttempt.objects.filter(user=user)
        if user_attempts.count() >= settings.LOCKOUT_USER_ATTEMPTS:
            last_attempt = user_attempts.order_by('-attempted')[0]
            attempted_ago = (
                    timezone.now() - last_attempt.attempted).total_seconds()
            if attempted_ago < settings.LOCKOUT_USER_SECONDS:
                lock_mins = int(
                        (settings.LOCKOUT_USER_SECONDS - attempted_ago)\
                        / 60) + 1
                raise forms.ValidationError(
                    ("Your account has been locked out for %s minutes."\
                    % lock_mins), code='locked',
                )

        # check for ip lockout
        ip_attempts = LoginAttempt.objects.filter(
                ip_address=self.request.META.get('REMOTE_ADDR'))
        if ip_attempts.count() >= settings.LOCKOUT_IP_ATTEMPTS:
            last_attempt = ip_attempts.order_by('-attempted')[0]
            attempted_ago = (
                    timezone.now() - last_attempt.attempted).total_seconds()
            if attempted_ago < settings.LOCKOUT_IP_SECONDS:
                lock_mins = int(
                        (settings.LOCKOUT_IP_SECONDS - attempted_ago)\
                        / 60) + 1
                raise forms.ValidationError(
                    ("Your computer has been locked out for %s minutes."\
                    % lock_mins), code='locked',
                )

        # successful login; clear failed attempts
        LoginAttempt.objects.filter(Q(user=user)\
                | Q(ip_address=self.request.META.get('REMOTE_ADDR')))\
                .delete()
