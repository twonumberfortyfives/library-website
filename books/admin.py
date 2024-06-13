from django.contrib import admin

from books.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "cover", "daily_fee", "inventory")
    search_fields = ("title", "author", "cover", "daily_fee", "inventory")
    list_filter = ("title", "author", "cover", "daily_fee", "inventory")


admin.site.register(Book, BookAdmin)
