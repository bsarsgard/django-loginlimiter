from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie


"""
Public areas
"""


def error(request):
    return render(request, 'loginlimiter/error.html')


"""
Protected areas
"""


@login_required
def index(request):
    return render(request, 'loginlimiter/index.html')
