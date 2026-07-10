from django.contrib import admin
from .models import Payment, Subscription


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['learner', 'course', 'amount', 'currency', 'provider', 'status', 'created_at']
    list_filter = ['status', 'provider', 'currency', 'created_at']
    search_fields = ['learner__email', 'course__title', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['learner', 'course']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['learner', 'plan', 'status', 'starts_at', 'expires_at', 'created_at']
    list_filter = ['plan', 'status']
    search_fields = ['learner__email']
    raw_id_fields = ['learner', 'payment']
    readonly_fields = ['created_at']
