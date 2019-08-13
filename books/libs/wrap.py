from functools import wraps
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response


def login_auth(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get('name'):
            return func(request, *args, **kwargs)
        if request.is_ajax():
            return Response({
                'start': 302,
                'url': '/user/login'
            })
        return redirect('/user/login')
    return inner