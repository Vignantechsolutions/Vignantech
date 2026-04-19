from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta, date


def analytics_view(request):
    from payments.models import Enrollment, Payment, Assignment
    from courses.models import Course
    from internships.models import Internship
    from certificates.models import Certificate
    from accounts.models import ContactMessage, Testimonial

    today = timezone.now()
    last_30 = today - timedelta(days=30)
    last_7  = today - timedelta(days=7)

    total_revenue = Payment.objects.filter(status='paid').aggregate(t=Sum('amount'))['t'] or 0

    # Top courses by enrollment
    top_courses = (
        Course.objects.filter(is_active=True)
        .annotate(enroll_count=Count('enrollment'))
        .order_by('-enroll_count')[:5]
    )
    # Top internships by enrollment
    top_internships = (
        Internship.objects.filter(is_active=True)
        .annotate(enroll_count=Count('enrollment'))
        .order_by('-enroll_count')[:5]
    )
    # Monthly revenue (last 6 months)
    monthly_revenue = []
    for i in range(5, -1, -1):
        month_start = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        month_end   = (month_start + timedelta(days=32)).replace(day=1)
        rev = Payment.objects.filter(status='paid', created_at__gte=month_start, created_at__lt=month_end).aggregate(t=Sum('amount'))['t'] or 0
        monthly_revenue.append({'month': month_start.strftime('%b %Y'), 'revenue': float(rev)})

    context = {
        'title': 'Analytics Dashboard',
        'kpi_cards': [
            ('Total Students',     User.objects.filter(is_staff=False).count(),          '#1E3A8A'),
            ('Total Enrollments',  Enrollment.objects.count(),                            '#3B82F6'),
            ('Total Revenue',      f'\u20b9{total_revenue:,.0f}',                         '#16A34A'),
            ('Certificates Issued',Certificate.objects.count(),                           '#D97706'),
            ('Active Courses',     Course.objects.filter(is_active=True).count(),         '#7C3AED'),
            ('Active Internships', Internship.objects.filter(is_active=True).count(),     '#0D9488'),
        ],
        'total_revenue': total_revenue,
        'new_students_30d':    User.objects.filter(date_joined__gte=last_30, is_staff=False).count(),
        'new_students_7d':     User.objects.filter(date_joined__gte=last_7,  is_staff=False).count(),
        'new_enrollments_30d': Enrollment.objects.filter(enrolled_at__gte=last_30).count(),
        'revenue_30d':         Payment.objects.filter(status='paid', created_at__gte=last_30).aggregate(t=Sum('amount'))['t'] or 0,
        'revenue_7d':          Payment.objects.filter(status='paid', created_at__gte=last_7).aggregate(t=Sum('amount'))['t'] or 0,
        'enrollments_by_status': Enrollment.objects.values('status').annotate(count=Count('id')),
        'payments_by_status':    Payment.objects.values('status').annotate(count=Count('id')),
        'recent_enrollments':    Enrollment.objects.select_related('student', 'course', 'internship').order_by('-enrolled_at')[:10],
        'recent_payments':       Payment.objects.select_related('student').order_by('-created_at')[:10],
        'unread_messages':       ContactMessage.objects.filter(is_read=False).count(),
        'recent_messages':       ContactMessage.objects.order_by('-created_at')[:5],
        'approved_reviews':      Testimonial.objects.filter(is_approved=True).order_by('-created_at'),
        'pending_reviews':       Testimonial.objects.filter(is_approved=False).order_by('-created_at'),
        'top_courses':           top_courses,
        'top_internships':       top_internships,
        'monthly_revenue':       monthly_revenue,
        'pending_assignments':   Assignment.objects.filter(status='submitted').count(),
        'total_assignments':     Assignment.objects.count(),
        'completed_enrollments': Enrollment.objects.filter(status='completed').count(),
    }
    return render(request, 'admin/analytics.html', context)


@require_POST
def review_action(request, pk):
    from accounts.models import Testimonial
    if not request.user.is_staff:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    action = request.POST.get('action')
    try:
        review = Testimonial.objects.get(pk=pk)
        if action == 'delete':
            review.delete()
            return JsonResponse({'status': 'deleted'})
        elif action == 'approve':
            review.is_approved = True
            review.save()
            return JsonResponse({
                'status': 'approved', 'name': review.name,
                'designation': review.designation, 'rating': review.rating,
                'message': review.message,
                'created_at': review.created_at.strftime('%d %b %Y'),
            })
        elif action == 'reject':
            review.is_approved = False
            review.save()
            return JsonResponse({'status': 'rejected'})
        return JsonResponse({'error': 'Invalid action'}, status=400)
    except Testimonial.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


# Customize default admin site
admin.site.site_header = 'Vignan TechSolutions Admin'
admin.site.site_title = 'Vignan TechSolutions'
admin.site.index_title = 'Administration Dashboard'


def certificate_generator_view(request):
    from certificates.models import CustomCertificate
    from certificates.views import generate_custom_certificate_pdf

    cert_types = CustomCertificate.CERT_TYPE_CHOICES
    recent = CustomCertificate.objects.order_by('-created_at')[:10]
    success_cert = None
    errors = {}

    if request.method == 'POST':
        recipient_name   = request.POST.get('recipient_name', '').strip()
        cert_type        = request.POST.get('cert_type', 'completion')
        program_name     = request.POST.get('program_name', '').strip()
        project_domain   = request.POST.get('project_domain', '').strip()
        start_date_str   = request.POST.get('start_date', '').strip()
        end_date_str     = request.POST.get('end_date', '').strip()
        issued_date_str  = request.POST.get('issued_date', '').strip()
        signatory_name   = request.POST.get('signatory_name', '').strip()
        signatory_title  = request.POST.get('signatory_title', '').strip()
        signatory_org    = request.POST.get('signatory_org', '').strip()
        extra_note       = request.POST.get('extra_note', '').strip()

        if not recipient_name:
            errors['recipient_name'] = 'Recipient name is required.'
        if not program_name:
            errors['program_name'] = 'Program name is required.'
        if not issued_date_str:
            errors['issued_date'] = 'Issue date is required.'

        issued_date = start_date = end_date = None
        if issued_date_str:
            try:
                issued_date = date.fromisoformat(issued_date_str)
            except ValueError:
                errors['issued_date'] = 'Invalid date format.'
        if start_date_str:
            try:
                start_date = date.fromisoformat(start_date_str)
            except ValueError:
                pass
        if end_date_str:
            try:
                end_date = date.fromisoformat(end_date_str)
            except ValueError:
                pass

        if not errors:
            cert = CustomCertificate.objects.create(
                recipient_name  = recipient_name,
                cert_type       = cert_type,
                program_name    = program_name,
                project_domain  = project_domain,
                start_date      = start_date,
                end_date        = end_date,
                issued_date     = issued_date,
                signatory_name  = signatory_name or 'Suresh Tammali',
                signatory_title = signatory_title or 'Director',
                signatory_org   = signatory_org or 'Vignan Tech Solutions',
                extra_note      = extra_note,
                created_by      = request.user,
            )
            success_cert = cert
            recent = CustomCertificate.objects.order_by('-created_at')[:10]

    return render(request, 'admin/certificate_generator.html', {
        'cert_types':    cert_types,
        'recent':        recent,
        'success_cert':  success_cert,
        'errors':        errors,
        'today':         date.today().isoformat(),
        'post_data':     request.POST if errors else {},
    })


def certificate_generator_download(request, pk):
    from certificates.models import CustomCertificate
    from certificates.views import generate_custom_certificate_pdf
    cert = get_object_or_404(CustomCertificate, pk=pk)
    buffer = generate_custom_certificate_pdf(cert)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cert.cert_number}.pdf"'
    return response


# Inject custom URLs into default admin site
_original_get_urls = admin.site.__class__.get_urls

def _custom_get_urls(self):
    custom = [
        path('analytics/', self.admin_view(analytics_view), name='analytics'),
        path('reviews/<int:pk>/action/', self.admin_view(review_action), name='review_action'),
        path('certificate-generator/', self.admin_view(certificate_generator_view), name='certificate_generator'),
        path('certificate-generator/<int:pk>/download/', self.admin_view(certificate_generator_download), name='certificate_generator_download'),
    ]
    return custom + _original_get_urls(self)

admin.site.__class__.get_urls = _custom_get_urls

# /admin/ shows real Django admin — analytics is at /admin/analytics/
