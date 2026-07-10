from django.urls import path
from .views import InitiatePaymentView, PaymentHistoryView, PaymentDetailView, MpesaCallbackView

urlpatterns = [
    path('initiate/', InitiatePaymentView.as_view(), name='payment-initiate'),
    path('history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('mpesa/callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]
