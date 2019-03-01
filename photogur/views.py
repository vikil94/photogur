from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from photogur.models import Picture, Comment

def picture_page(request):
    context = {'pictures': Picture.objects.all(),
    'comments': Comment.objects.all()}
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)
