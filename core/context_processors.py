from django.conf import settings


def site_settings(request):
    return {
        'COMPANY_NAME': settings.COMPANY_NAME,
        'COMPANY_EMAIL': settings.COMPANY_EMAIL,
        'COMPANY_PHONE': settings.COMPANY_PHONE,
        'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
        'RAZORPAY_KEY_ID': settings.RAZORPAY_KEY_ID,
    }
