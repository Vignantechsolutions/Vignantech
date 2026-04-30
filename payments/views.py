import razorpay
import hmac
import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.conf import settings
from courses.models import Course
from internships.models import Internship
from .models import Enrollment, Payment


def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def initiate_payment(request, item_type, item_id):
    if request.user.is_staff:
        return redirect('/admin/analytics/')
    if item_type == 'course':
        item = get_object_or_404(Course, id=item_id, is_active=True)
        existing = Enrollment.objects.filter(student=request.user, course=item, status__in=['active', 'completed']).first()
    else:
        item = get_object_or_404(Internship, id=item_id, is_active=True)
        existing = Enrollment.objects.filter(student=request.user, internship=item, status__in=['active', 'completed']).first()

    if existing:
        messages.info(request, 'You are already enrolled.')
        return redirect('accounts:dashboard')

    if not settings.RAZORPAY_KEY_ID or settings.RAZORPAY_KEY_ID.startswith('your_'):
        messages.error(request, 'Payment gateway is not configured. Please contact support.')
        return redirect('accounts:dashboard')

    amount_paise = int(item.fees * 100)
    try:
        client = get_razorpay_client()
        order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': 1,
        })
    except Exception:
        messages.error(request, 'Payment gateway error. Please try again later.')
        return redirect('accounts:dashboard')

    enrollment = Enrollment.objects.create(
        student=request.user,
        enrollment_type=item_type,
        course=item if item_type == 'course' else None,
        internship=item if item_type == 'internship' else None,
        status='pending',
    )
    Payment.objects.create(
        student=request.user,
        enrollment=enrollment,
        razorpay_order_id=order['id'],
        amount=item.fees,
    )

    return render(request, 'payments/checkout.html', {
        'item': item,
        'item_type': item_type,
        'order': order,
        'amount': item.fees,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    })


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)

        # Verify signature
        key_secret = settings.RAZORPAY_KEY_SECRET.encode()
        msg = f"{razorpay_order_id}|{razorpay_payment_id}".encode()
        generated_signature = hmac.new(key_secret, msg, hashlib.sha256).hexdigest()

        if generated_signature == razorpay_signature:
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'paid'
            payment.save()
            payment.enrollment.status = 'active'
            payment.enrollment.save()
            messages.success(request, 'Payment successful! You are now enrolled.')
            return redirect('accounts:dashboard')
        else:
            payment.status = 'failed'
            payment.save()
            messages.error(request, 'Payment verification failed. Please contact support.')
            return redirect('accounts:dashboard')

    return HttpResponse(status=400)


@login_required
def payment_history(request):
    if request.user.is_staff:
        return redirect('/admin/analytics/')
    payments = Payment.objects.filter(student=request.user)
    return render(request, 'payments/history.html', {'payments': payments})
