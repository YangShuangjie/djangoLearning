from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# def links(request):
#     return HttpResponse('links')

from django.views.generic import ListView
from blog.views import CommonView
from .models import Link

class LinkView(CommonView,ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'links'