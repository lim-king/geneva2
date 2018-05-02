# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from main.forms import LoginForm
from management.admin import UserCreationForm, UserChangeForm as AdminUserChangeForm
from management.forms import UserChangeForm
from blog.models import Post
from management.models import MainTimeBoard, User
# from management.forms import UserCreationForm


def main(request):
    # if request.method == 'POST':
    #     create_user_form = UserCreationForm(request.POST)
    #     if create_user_form.is_valid():
    #         create_user_form.save()
    # else:
    #     create_user_form = UserCreationForm()
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')[:5]
    timeboards = MainTimeBoard.objects.all()
    return render(request, 'main/main.html', {'posts': posts, 'timeboards': timeboards})


def login(request):
    # if request.method == 'POST':
    #     create_user_form = UserCreationForm(request.POST)
    #     if create_user_form.is_valid():
    #         create_user_form.save()
    # else:
    #     create_user_form = UserCreationForm()
    # return render(request, 'main/main.html', {'create_user_form': create_user_form})

    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
                django_login(request, user)
                # Post목록 화면으로 이동
                return redirect('/')

            # 인증에 실패하면 login_form에 non_field_error를 추가한다
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()

    context = {'login_form': login_form, }

    return render(request, 'main/login.html', context)


def signup(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        # 유효성 검증에 통과한 경우 (username의 중복과 password1, 2의 일치 여부)
        if signup_form.is_valid():
            # SignupForm의 인스턴스 메서드인 signup() 실행, 유저 생성
            signup_form.save()
            return redirect('login')
    else:
        signup_form = UserCreationForm()

    context = {
        'create_user_form': UserCreationForm,
    }

    return render(request, 'main/sigup.html', context)


def my_info(request):
    if request.user.is_active:
        posts = Post.objects.filter(author_id=request.user.id).order_by('-created_date')
        posts_count = Post.objects.filter(author_id=request.user.id).count()
        user_info = get_object_or_404(User, pk=request.user.id)

        return render(request, 'main/user/my_info.html', {'posts': posts,
                                                          'posts_count': posts_count,
                                                          'user_info': user_info})

    login_form = LoginForm()
    context = {'login_form': login_form, }
    return redirect('/login', context)


def my_info_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('my_info')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'main/user/my_info_edit.html', {'form': form})
