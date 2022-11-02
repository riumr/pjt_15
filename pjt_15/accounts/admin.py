from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Review,Comment
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'review')

admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)