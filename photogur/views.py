from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from photogur.models import Picture, Comment
from photogur.forms import LoginForm

def picture_page(request):
    context = {'pictures': Picture.objects.all(),
    'comments': Comment.objects.all()}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)

def picture_search(request):
    query = request.GET['query']
    search_results = Picture.objects.filter(artist=query)
    context = {'pictures': search_results}
    response = render(request, 'picture_search.html', context)
    return HttpResponse(response)

def create_comment(request):
    picture = request.POST['picture']
    comment_name = request.POST['comment_name']
    comment_message = request.POST['comment_message']
    comment_picture = Picture.objects.get(pk=request.POST['picture'])
    comment = Comment.objects.create(name=comment_name,
                                     message=comment_message,
                                     picture=comment_picture)
    return HttpResponseRedirect('/pictures/' + picture)

def login_view(request):
    form = LoginForm()
    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)    
