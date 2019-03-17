from django.contrib import admin
from .models import BookRate, Review, Author, Book, BookComments


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(BookComments)
class BookCommentsAdmin(admin.ModelAdmin):
    pass


@admin.register(BookRate)
class BookRateAdmin(admin.ModelAdmin):
    pass

