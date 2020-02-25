from django.http import HttpResponse
from django.shortcuts import render
from .task import send_email_task


def send_mail(request):
    send_email_task()
    return HttpResponse('<h1>Check Mail<h1>')
