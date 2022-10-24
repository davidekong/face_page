from distutils.command.upload import upload
from multiprocessing import context
from subprocess import list2cmdline
from turtle import pos, title
from urllib import response

from django.shortcuts import redirect, render
import schedule
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from chat.models import Room
from face_page_interface.models import CommentModel, CustomUser, Post

from django.core.mail import send_mail
from django.urls import reverse
# Create your views here.
def signup(request):
    context = {
        'error_message': ''
    }
    valid = False
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if username == '' or email == '' or password1 == '' or password2 == '':
            valid = False
            context['error_message'] = 'Please ensure all fields are appropriately filled.'
        elif len(password1) < 5:
            valid = False
            context['error_message'] = 'Please ensure password is not less than 5 characters.'
        else:
            valid = True
        
        if valid == True:
            if password1 == password2:
                user = authenticate(username=username, email=email)
                if user is None:
                    new_user = User.objects.create_user(username=username, email=email, password=password1)
                    new_user.save()
                    login(request, new_user)
                    return redirect('reg_bio')
                else:
                    context['error_message'] = "There is already a user associated with the following credentials. Would you like to login?"
            else:
                context['error_message'] = 'Please make sure both passwords match.'
    return render(request, 'face_page_interface/signup.html', context)

def reg_bio(request):
    if request.method == 'POST':
        picture = request.FILES['picture']

        bio = request.POST['bio']
        custom_user = CustomUser.objects.create(user=request.user, about=bio, picture=picture)
        custom_user.save()
        return redirect('dashboard', pk=custom_user.id)
    return render(request, 'face_page_interface/reg_bio.html')

def logIn(request):
    logout(request)
    context = {
        'error_message': ''
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard', pk=CustomUser.objects.get(user=user).id)
        else:
            context['error_message'] = "Did you put in the right credentials? Try registering"
    return render(request, 'face_page_interface/login.html', context)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user_id = User.objects.get(email=email).id
        send_mail(
            'Thanks for using my services', 
            request.build_absolute_uri(reverse('change_password', args=(user_id, ))), 
            'davidukemeekong1@gmail.com', 
            [email], 
            fail_silently=False)
    return render(request, 'face_page_interface/forgot_password.html')

def change_password(request, pk):
    context = {
        'error_message': ''
    }
    if request.method == "POST":
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user = User.objects.get(pk=pk)
            user.set_password(password1)
            user.save()
            return redirect('logIn')
        else:
            context['error_message'] = 'Please make sure both passwords match.'
    return render(request, 'face_page_interface/change_password.html', context)



def dashboard(request, pk):
    context = {
        'user': request.user, 
        'customuser': CustomUser.objects.get(pk=pk), 
        'id': pk,
        'other_user': CustomUser.objects.get(pk=pk).user,
        'current_custom_user': CustomUser.objects.get(user=request.user),
        'posts': list(CustomUser.objects.get(pk=pk).user.post_set.all()), 
        'other_followers': list(CustomUser.objects.get(pk=pk).followers.all()),
        'other_following':  list(CustomUser.objects.get(pk=pk).following.all()),
        'followers': list(CustomUser.objects.get(user=request.user).followers.all()),
        'following': list(CustomUser.objects.get(user=request.user).following.all())
    }
    if request.method == "GET":
        if 'follow' in request.GET:
            CustomUser.objects.get(user=request.user).following.add(CustomUser.objects.get(pk=pk).user)
            CustomUser.objects.get(pk=pk).followers.add(request.user)
            return redirect('dashboard', pk)
        if 'unfollow' in request.GET:
            CustomUser.objects.get(user=request.user).following.remove(CustomUser.objects.get(pk=pk).user)
            CustomUser.objects.get(pk=pk).followers.remove(request.user)
            return redirect('dashboard', pk)
    return render(request, 'face_page_interface/dashboard.html', context)

def make_post(request, pk):
    context = {
        'error_message': "",
        'id': pk, 
        
    }
    if request.method == "POST":
        image = request.FILES['picture']
        text = request.POST['text_field']
        title = request.POST['title']
        new_post = Post.objects.create(user=request.user, pic=image, text=text, title=title)
        new_post.save()
    return render(request, 'face_page_interface/make_post.html', context)

def home(request, pk):
    context = {
        'error_message': "",
        'id': pk,
        'posts': list(Post.objects.all()),
    }

    if request.method == "GET":
        if 'get_search' in request.GET:
            search = request.GET.get('search')
            user = User.objects.get(username=search)
            context['posts'] = list(Post.objects.filter(user=user))
        if 'your_posts' in request.GET:
            context['posts'] = list(Post.objects.filter(user=request.user))
        if 'all_posts' in request.GET:
            context['posts'] = list(Post.objects.all())
        if 'following_posts' in request.GET:
            following = []
            for _ in list(CustomUser.objects.get(user=request.user).following.all()):
                following += list(_.post_set.all())
            context['posts'] = following
    return render(request, 'face_page_interface/home.html', context)

def post(request, pk):
    context = {
        'error_message': "",
        'id': pk,
        'user': Post.objects.get(pk=pk).user,
        'current_user': request.user,
        'pic': Post.objects.get(pk=pk).pic,
        'title': Post.objects.get(pk=pk).title,
        'text': Post.objects.get(pk=pk).text,
        'likes': len(Post.objects.get(pk=pk).users_liked.all()),
        'comments': list(Post.objects.get(pk=pk).commentmodel_set.all()),
        'is_liked': request.user in list(Post.objects.get(pk=pk).users_liked.all()), 
        'custom_user': CustomUser.objects.get(user=request.user), 
        'other_custom_user': CustomUser.objects.get(user=Post.objects.get(pk=pk).user)
    }

    if request.method == 'GET':
        if 'post_comment' in request.GET:
            comment = request.GET.get('comment')
            post = Post.objects.get(pk=context['id'])
            new_comment = CommentModel.objects.create(user=request.user, comment=comment, likes=0, post=post)
            new_comment.save()
            context['comments'] = list(Post.objects.get(pk=pk).commentmodel_set.all())
            return redirect('post', pk)
        if 'like_button' in request.GET:
            post = Post.objects.get(pk=context['id'])
            if request.user not in list(post.users_liked.all()):
                post.users_liked.add(request.user)
                post.likes = len(post.users_liked.all())
                post.save()
                context['likes'] = len(Post.objects.get(pk=pk).users_liked.all())
            else:
                post.users_liked.remove(request.user)
                post.likes = len(post.users_liked.all())
                post.save()
                context['likes'] = len(Post.objects.get(pk=pk).users_liked.all())
            return redirect('post', pk)
    return render(request, 'face_page_interface/post.html', context)

def delete1(request, pk):
    context = {
        'id': pk
    }
    if request.method == 'GET':
        if 'delete' in request.GET:
            post = Post.objects.get(pk=pk)
            post.delete()
            return redirect('dashboard', CustomUser.objects.get(user=request.user).id)
    return render(request, 'face_page_interface/delete.html', context)
