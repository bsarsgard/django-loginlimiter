from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LimiterAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # make sure user is active
        if not user.is_active:
            raise forms.ValidationError(
                ("This account is inactive."),
                code='inactive',
            )
        # check user and ip for strikes
        if user.username.startswith('b'):
            raise forms.ValidationError(
                ("Sorry, accounts starting with 'b' aren't welcome here."),
                code='no_b_users',
            )
