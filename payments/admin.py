import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Sum
from .models import Enrollment, Payment, Assignment
from certificates.models import Certificate
from certificates.views import generate_certificate_pdf
from django.core.files.base import ContentFile


def issue_certificates(modeladmin, request, queryset):
    count = 0
    skipped = 0
    for enrollment in queryset.filter(status='completed'):
        cert, created = Certificate.objects.get_or_create(
            enrollment=enrollment,
            defaults={'student': enrollment.student}
        )
        if created:
            pdf_buffer = generate_certificate_pdf(cert)
            cert.certificate_file.save(
                f"certificate-{str(cert.certificate_id)[:8]}.pdf",
                ContentFile(pdf_buffer.read()), save=True
            )
            count += 1
        else:
            skipped += 1
    msg = f'{count} certificate(s) issued.'
    if skipped:
        msg += f' {skipped} already had certificates.'
    modeladmin.message_user(request, msg)

issue_certificates.short_description = 'Issue certificates for completed enrollments'


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0
    fields = ['title', 'status', 'submitted_at', 'feedback']
    readonly_fields = ['title', 'submitted_at']
    show_change_link = True


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'program_display', 'enrollment_type', 'status_badge', 'status', 'payment_status', 'enrolled_at', 'completed_at']
    list_filter = ['enrollment_type', 'status', 'enrolled_at']
    list_editable = ['status']
    search_fields = ['student__first_name', 'student__last_name', 'student__email']
    date_hierarchy = 'enrolled_at'
    readonly_fields = ['enrolled_at', 'completed_at']
    actions = [issue_certificates, 'export_enrollments']
    inlines = [AssignmentInline]
    fieldsets = [
        ('Student', {'fields': ['student', 'enrollment_type', 'course', 'internship']}),
        ('Status', {'fields': ['status', 'enrolled_at', 'completed_at']}),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'course', 'internship')

    @admin.display(description='Program')
    def program_display(self, obj):
        item = obj.course or obj.internship
        return str(item) if item else '—'

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'active':    ('#F0FDF4', '#16A34A'),
            'completed': ('#EFF6FF', '#1D4ED8'),
            'pending':   ('#FFFBEB', '#D97706'),
            'cancelled': ('#FEF2F2', '#DC2626'),
        }
        bg, fg = colors.get(obj.status, ('#F1F5F9', '#475569'))
        return format_html('<span style="background:{};color:{};padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">{}</span>', bg, fg, obj.get_status_display())

    @admin.display(description='Payment')
    def payment_status(self, obj):
        try:
            p = obj.payment
            colors = {'paid': ('#F0FDF4', '#16A34A'), 'failed': ('#FEF2F2', '#DC2626'), 'created': ('#FFFBEB', '#D97706'), 'refunded': ('#FAF5FF', '#7C3AED')}
            bg, fg = colors.get(p.status, ('#F1F5F9', '#475569'))
            return format_html('<span style="background:{};color:{};padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">{}</span>', bg, fg, p.get_status_display())
        except Exception:
            return format_html('<span style="color:#CBD5E1">—</span>')

    def save_model(self, request, obj, form, change):
        if obj.status == 'completed' and not obj.completed_at:
            obj.completed_at = timezone.now()
        super().save_model(request, obj, form, change)

    def export_enrollments(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=enrollments.csv'
        writer = csv.writer(response)
        writer.writerow(['Student', 'Email', 'Type', 'Program', 'Status', 'Enrolled At', 'Completed At'])
        for e in queryset.select_related('student', 'course', 'internship'):
            writer.writerow([
                e.student.get_full_name(), e.student.email,
                e.enrollment_type, e.course or e.internship,
                e.status, e.enrolled_at, e.completed_at or ''
            ])
        return response
    export_enrollments.short_description = 'Export selected to CSV'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount_display', 'currency', 'status_badge', 'razorpay_order_id', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['student__first_name', 'student__email', 'razorpay_order_id', 'razorpay_payment_id']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    actions = ['export_payments']
    fieldsets = [
        ('Student & Enrollment', {'fields': ['student', 'enrollment']}),
        ('Payment Info', {'fields': ['amount', 'currency', 'status']}),
        ('Razorpay', {'fields': ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature'], 'classes': ['collapse']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
    ]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        total = Payment.objects.filter(status='paid').aggregate(t=Sum('amount'))['t'] or 0
        extra_context['total_revenue'] = total
        return super().changelist_view(request, extra_context=extra_context)

    @admin.display(description='Amount')
    def amount_display(self, obj):
        return format_html('<span style="font-weight:600;color:#16A34A">₹{}</span>', obj.amount)

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {'paid': ('#F0FDF4', '#16A34A'), 'failed': ('#FEF2F2', '#DC2626'), 'created': ('#FFFBEB', '#D97706'), 'refunded': ('#FAF5FF', '#7C3AED')}
        bg, fg = colors.get(obj.status, ('#F1F5F9', '#475569'))
        return format_html('<span style="background:{};color:{};padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">{}</span>', bg, fg, obj.get_status_display())

    def export_payments(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=payments.csv'
        writer = csv.writer(response)
        writer.writerow(['Student', 'Email', 'Amount', 'Currency', 'Status', 'Order ID', 'Payment ID', 'Date'])
        for p in queryset.select_related('student'):
            writer.writerow([p.student.get_full_name(), p.student.email, p.amount, p.currency, p.status, p.razorpay_order_id, p.razorpay_payment_id, p.created_at])
        return response
    export_payments.short_description = 'Export selected to CSV'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'title', 'program', 'status_badge', 'submitted_at', 'reviewed_at']
    list_filter = ['status', 'submitted_at']
    search_fields = ['enrollment__student__first_name', 'enrollment__student__email', 'title']
    readonly_fields = ['submitted_at']
    date_hierarchy = 'submitted_at'
    actions = ['mark_approved', 'mark_reviewed']
    fieldsets = [
        ('Submission', {'fields': ['enrollment', 'title', 'description', 'file', 'submitted_at']}),
        ('Review', {'fields': ['status', 'feedback', 'reviewed_at']}),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('enrollment__student', 'enrollment__course', 'enrollment__internship')

    @admin.display(description='Student')
    def student_name(self, obj):
        return obj.enrollment.student.get_full_name()

    @admin.display(description='Program')
    def program(self, obj):
        return obj.enrollment.course or obj.enrollment.internship

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {'submitted': ('#FFFBEB', '#D97706'), 'reviewed': ('#EFF6FF', '#1D4ED8'), 'approved': ('#F0FDF4', '#16A34A')}
        bg, fg = colors.get(obj.status, ('#F1F5F9', '#475569'))
        return format_html('<span style="background:{};color:{};padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">{}</span>', bg, fg, obj.get_status_display())

    def save_model(self, request, obj, form, change):
        if obj.status in ('reviewed', 'approved') and not obj.reviewed_at:
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

    def mark_approved(self, request, queryset):
        updated = queryset.update(status='approved', reviewed_at=timezone.now())
        self.message_user(request, f'{updated} assignment(s) approved.')
    mark_approved.short_description = 'Mark selected as approved'

    def mark_reviewed(self, request, queryset):
        updated = queryset.update(status='reviewed', reviewed_at=timezone.now())
        self.message_user(request, f'{updated} assignment(s) marked as reviewed.')
    mark_reviewed.short_description = 'Mark selected as reviewed'
