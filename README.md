# django-loginlimiter
A sample login limiter app for django

* Allow the user 5 attempts before locking them out for 1 minute.
* Allow the ip_address 30 attempts before locking them out for 5 minutes.
* Upon successful login clear all failed login attempts by that user/IP from the DB.
* After the lockout period, clear all failed login attempts from the DB.

(the above settings are configurable in settings.py)

To use, attach to you application and override the login view to use the LimiterAuthenticationForm, like so:
    url(r'^accounts/login/$', auth_views.login, {
            'authentication_form': LimiterAuthenticationForm
            }, name='login'),
