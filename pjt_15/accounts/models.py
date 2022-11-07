from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    image_thumbnail = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(160, 90)],
        format="JPEG",
        options={"quality": 95},
    )


class Review(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 95},
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="", null=True
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_reviews"
    )
    location = models.CharField(max_length=40)
    NorthAmerica = "북아메리카"
    SouthAmerica = "남아메리카"
    Europe = "유럽"
    Oceania = "오세아니아"
    Africa = "아프리카"
    Asia = "아시아"
    Domestic = "국내"

    continental = [
        (NorthAmerica, "북아메리카"),
        (SouthAmerica, "남아메리카"),
        (Europe, "유럽"),
        (Africa, "아프리카"),
        (Asia, "아시아"),
        (Domestic, "국내"),
    ]
    category = models.CharField(max_length=5, choices=continental, default=None)

    def rate():
        review = Review.objects.get(pk=pk)
        rate = 0
        for query in review.comment_set.all():
            rate += query.grade


class Comment(models.Model):
    content = models.TextField(max_length=300, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    RATING = [
        (1, "★"),
        (2, "★★"),
        (3, "★★★"),
        (4, "★★★★"),
        (5, "★★★★★"),
    ]
    grade = models.IntegerField(choices=RATING, default=None)
