from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from photogur.models import Picture, Comment
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



def picture_page(request):
    context = {'pictures': Picture.objects.all(), 'comments': Comment.objects.all()}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

@login_required
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/pictures')
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

@login_required
def add_picture(request):
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            form.user = request.user
            new_picture = form.save()
            return HttpResponseRedirect('/pictures/' + str(new_picture.id))
    else:
        form = PictureForm()
    response = render(request, 'new_picture.html', {'form': form})
    return HttpResponse(response)

@login_required
def edit_picture(request, id):
    picture = get_object_or_404(Picture, id=id, user=request.user.pk)
    if request.method == 'GET':
        form = PictureForm(instance=picture)
        context = {'form': form, 'picture': picture}
        return render(request, 'edit.html', context)

    elif request.method == 'POST':
        form = PictureForm(request.POST, instance=picture)
        if form.is_valid():
            updated_picture = form.save()
            return HttpResponseRedirect(reverse('show', args=[picture.id]))
        else:
            context = {'form': form, 'picture': picture}
            response = render(request, 'edit.html', context)
            return HttpResponse(response)
