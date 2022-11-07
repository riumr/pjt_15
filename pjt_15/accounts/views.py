from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm, ReviewForm, CommentForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Review, Comment
from django.contrib import messages
from django.http import JsonResponse

# 지도 구현 라이브러리
import folium

# 구글 맵
import googlemaps

# Create your views here.


# def test(request, pk):

#     review = Review.objects.get(pk=pk)
#     comment_form = CommentForm()

#     location = review.location
#     gmaps = googlemaps.Client(key="AIzaSyCyVj2SsrSGeHVWM1uawHssRzDyTuW8Yuo")
#     geocode_result = gmaps.geocode((location), language="ko")

#     lat = geocode_result[0]["geometry"]["location"]["lat"]
#     lng = geocode_result[0]["geometry"]["location"]["lng"]

#     context = {
#         "review": review,
#         "comments": review.comment_set.all(),
#         "comment_form": comment_form,
#         "geocode_result": geocode_result,
#         "lat": lat,
#         "lng": lng,
#     }
#     return render(request, "reviews/test.html", context)


# Account_View
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            login = form.save()
            auth_login(request, login)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


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
        "user": user,
        "reviews": reviews,
        "comments": comments,
    }
    return render(request, "accounts/detail.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    messages.warning(request, "로그아웃 하였습니다.")
    return redirect("index")


@login_required
def edit(request, pk):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "accounts/edit.html", context)


@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("index")
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, "accounts/change_password.html", context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("index")


# Review_View
@login_required
def review_create(request):
    if request.method == "POST":
        # user = get_user_model().objects.get(pk=request.user.pk)
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = request.user
            review.save()
            messages.success(request, "글 작성이 완료되었습니다.")
            return redirect("index")
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form}
    return render(request, "reviews/form.html", context=context)


@login_required
def review_update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.author:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                messages.success(request, "글이 수정되었습니다.")
                return redirect("review-detail", review.pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {"review_form": review_form}
        return render(request, "reviews/form.html", context)
    else:
        # return HttpResponseForbidden()
        messages.warning(request, "작성자만 글을 수정할 수 있습니다.")
        return redirect("review-detail", review.pk)


@login_required
def review_delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect("index")


def index(request):
    reviews = Review.objects.order_by("-pk")
    context = {"reviews": reviews}
    return render(request, "accounts/index.html", context)


def review_detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()
    rate = 0
    for query in review.comment_set.all():
        rate += query.grade

    
    if review.comment_set.all(): 
        rate_result = round(rate/len(review.comment_set.all()),2)
    else:
        rate_result = '평점없음'

    if review.location:
        location = review.location
        gmaps = googlemaps.Client(key="AIzaSyCyVj2SsrSGeHVWM1uawHssRzDyTuW8Yuo")
        geocode_result = gmaps.geocode((location), language="ko")

        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lng = geocode_result[0]["geometry"]["location"]["lng"]
    else:
        lat = 37.5014
        lng = 127.0396

    context = {
        "review": review,
        "comments": review.comment_set.all(),
        "comment_form": comment_form,
        "lat": lat,
        "lng": lng,
        "category": review.category,
        "rate": rate_result,
    }
    return render(request, "reviews/detail.html", context)


# Comment_View
@login_required
def comment_create(request, pk):
    # review = Review.objects.get(pk=pk)
    review = get_object_or_404(Review, pk=pk)
    # user = get_user_model().objects.get(pk=request.user.pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.author = request.user
        comment.save()
        context = {
            "content": comment.content,
            "userName": comment.author.username,
            "stars": comment.grade,
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
    data = {"isLiked": is_liked, "likeCount": review.like_users.count()}
    return JsonResponse(data)


# Follow_View
@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        messages.warning(request, "본인을 팔로우 할 수 없습니다")
        return redirect("detail", pk)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return redirect("detail", pk)


# 검색기능 : 검색 텍스트만 보내주는 페이지
def search_input(request):
    if request.method == "POST":
        search_text = request.POST.get("user_search")
        return redirect("search_result", search_text)  # 검색 텍스트를 전송한다.
    else:
        return render(request, "reviews/search_input.html")


# 검색결과 : 검색 결과만 보여주는 페이지
def search_result(request, search_text):
    # Review 테이블에 리뷰가 있으면
    if Review:
        result = Review.objects.filter(
            location__icontains=search_text  # 검색창에서 값을 받을 수 있다
        ).values()  # 결과는 검색한 텍스트를 포함하고 있는 위치 컬럼을 기준으로 필터링한다.
        if result.exists():  # 필터링한 결과가 존재하면
            result = Review.objects.filter(
                location__icontains=search_text
            ).values()  # 값을 반환한다.
            context = {
                "result": result,
            }
        else:  # 필터링한 결과가 존재하지 않으면, 아무 리뷰나 표시하도록 한다.
            context = {
                "result": "anything",
            }
    # Review 테이블에 값이 없으면
    else:
        result = "no review"
        context = {
            "result": result,
        }
    return render(request, "reviews/search_result.html", context)
