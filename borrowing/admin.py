from django.contrib import admin

from borrowing.models import Borrowing


class BorrowingAdmin(admin.ModelAdmin):
    list_display = ("borrow_date", "expected_return_date", "actual_return_date", "book", "user")
    list_filter = ("borrow_date", "expected_return_date", "actual_return_date", "book", "user")
    search_fields = ("borrow_date", "expected_return_date", "actual_return_date", "book", "user")


admin.site.register(Borrowing, BorrowingAdmin)
