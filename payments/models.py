from datetime import timedelta
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PROVIDER_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('stripe', 'Stripe'),
        ('manual', 'Manual'),
    ]

    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments'
    )
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, related_name='payments',
        null=True, blank=True, help_text='Blank for subscription payments',
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=10, default='KES')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='manual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=200, blank=True)
    provider_reference = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, help_text='For M-Pesa payments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        target = self.course.title if self.course else 'subscription'
        return f'{self.learner} — {target} — {self.status}'


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('daily', '1 Day'),
        ('monthly', '30 Days'),
        ('yearly', '12 Months'),
    ]
    PLAN_DURATIONS = {
        'daily': timedelta(days=1),
        'monthly': timedelta(days=30),
        'yearly': timedelta(days=365),
    }
    PLAN_PRICES = {
        'daily': Decimal('50'),
        'monthly': Decimal('500'),
        'yearly': Decimal('4000'),
    }

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('failed', 'Failed'),
    ]

    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions'
    )
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    starts_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    payment = models.OneToOneField(
        Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscription'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.learner} — {self.get_plan_display()} — {self.status}'

    @property
    def is_active(self):
        return self.status == 'active' and self.expires_at is not None and self.expires_at > timezone.now()

    def activate(self):
        self.status = 'active'
        self.starts_at = timezone.now()
        self.expires_at = self.starts_at + self.PLAN_DURATIONS[self.plan]
        self.save(update_fields=['status', 'starts_at', 'expires_at'])
