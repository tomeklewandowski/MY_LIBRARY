from django.contrib import admin
from .models import BookRate, Book, BookStatus


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(BookRate)
class BookRateAdmin(admin.ModelAdmin):
    pass


@admin.register(BookStatus)
class BookStatusAdmin(admin.ModelAdmin):
    pass

