from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['learner', 'course', 'amount', 'currency', 'provider', 'status', 'created_at']
    list_filter = ['status', 'provider', 'currency', 'created_at']
    search_fields = ['learner__email', 'course__title', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['learner', 'course']
