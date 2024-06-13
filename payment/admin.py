from django.contrib import admin
from payment.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("status", "type", "borrowing", "session_url", "session_id", "user")
    list_filter = ("status", "type", "borrowing", "session_url", "session_id", "user")
    search_fields = ("status", "type", "borrowing", "session_url", "session_id", "user")


admin.site.register(Payment, PaymentAdmin)
