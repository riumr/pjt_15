from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, ReviewForm, CommentForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Review, Comment
from django.contrib import messages
from django.http import JsonResponse
import folium

# Create your views here.


# Account_View
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)
    
def accounts_list(request):
    users = get_user_model().objects.all()
    context = {
        "users": users,
    }
    return render(request, "accounts/accounts_list.html", context)

@login_required
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    reviews = user.review_set.all()
    comments = user.comment_set.all()
    context = {
        'user': user,
        'reviews': reviews,
        'comments': comments,

    }
    return render(request, 'accounts/detail.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    messages.warning(request, '로그아웃 하였습니다.')
    return redirect('index')

@login_required
def edit(request, pk):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('detail', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/edit.html', context)


@login_required
def password_change(request):
    if request.method =='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)

@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('index')

# Review_View
@login_required
def review_create(request):
    if request.method == 'POST':
        # user = get_user_model().objects.get(pk=request.user.pk)
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = request.user
            review.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('index')
    else: 
        review_form = ReviewForm()
    context = {
        'review_form': review_form
    }
    return render(request, 'reviews/form.html', context=context)

@login_required
def review_update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.author:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                messages.success(request, '글이 수정되었습니다.')
                return redirect('review-detail', review.pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {
            'review_form': review_form
        }
        return render(request, 'reviews/form.html', context)
    else:
        # return HttpResponseForbidden()
        messages.warning(request, '작성자만 글을 수정할 수 있습니다.')
        return redirect('review-detail', review.pk)

@login_required
def review_delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect('index')


def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews
    }
    return render(request, 'base/base.html', context)

def review_detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()
    m = folium.Map(location=[35.889, 128.6094])

    maps=m._repr_html_()
    context = {
        'review': review,
        'comments': review.comment_set.all(),
        'comment_form': comment_form,
        'map':maps,
    }
    return render(request, 'reviews/detail.html', context)

# Comment_View
@login_required
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    # user = get_user_model().objects.get(pk=request.user.pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.author = request.user
        comment.save()
        context = {
            'content': comment.content,
            'userName': comment.user.username
        }
    return JsonResponse(context)



# Like_View
@login_required
def like(request, pk):
    review = Review.objects.get(pk=pk)
    print(request.body)
    if request.user in review.like_users.all(): 
        review.like_users.remove(request.user)
        is_liked = False
    else:
        review.like_users.add(request.user)
        is_liked = True
    data = {
        'isLiked': is_liked,
        'likeCount': review.like_users.count()
    }
    return JsonResponse(data)

# Follow_View
@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        messages.warning(request, '본인을 팔로우 할 수 없습니다')
        return redirect('detail', pk)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return redirect('detail', pk)
