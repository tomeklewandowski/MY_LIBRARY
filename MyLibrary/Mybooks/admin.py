from django.contrib import admin
from .models import Rate, Comments, Review, Author, Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    pass

