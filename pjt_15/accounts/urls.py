from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # accounts
    path("", views.index, name="index"),
    path("accounts/list", views.accounts_list, name="list"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/<int:pk>/detail", views.detail, name="detail"),
    path("accounts/login/", views.login, name="login"),
    path("accounts/logout/", views.logout, name="logout"),
    path("accounts/<int:pk>/edit", views.edit, name="edit"),
    path("accounts/password/", views.password_change, name="change_password"),
    path("accounts/delete/", views.delete, name="delete"),
    # path("test/<int:pk>/", views.test, name="test"),
    # review
    path("create/", views.review_create, name="review-create"),
    path("update/<int:pk>", views.review_update, name="review-update"),
    path("update/<int:pk>", views.review_delete, name="review-delete"),
    path("detail/<int:pk>", views.review_detail, name="review-detail"),
    # comment
    path("<int:pk>/comments/", views.comment_create, name="comment-create"),
    # like
    path("<int:pk>/like/", views.like, name="like"),
    # follow
    path("<int:pk>/follow/", views.follow, name="follow"),
    # search
    path("search_input/", views.search_input, name="search_input"),
    # search_result
    path("search/<str:search_text>", views.search_result, name="search_result"),
    # 아무 결과도 없을 때
    path("no_result", views.no_result, name="no_alert"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
