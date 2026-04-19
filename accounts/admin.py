import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.db.models import Count
from .models import StudentProfile, Testimonial, ContactMessage, OTPVerification


def export_csv(modeladmin, request, queryset):
    """Generic CSV export action."""
    meta = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
    writer = csv.writer(response)
    fields = [f for f in meta.fields]
    writer.writerow([f.verbose_name for f in fields])
    for obj in queryset:
        writer.writerow([getattr(obj, f.name) for f in fields])
    return response
export_csv.short_description = 'Export selected to CSV'


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['email', 'purpose', 'otp', 'is_verified', 'status_badge', 'created_at', 'expires_at']
    list_filter = ['purpose', 'is_verified']
    search_fields = ['email']
    readonly_fields = ['email', 'otp', 'purpose', 'created_at', 'expires_at', 'is_verified']
    date_hierarchy = 'created_at'
    actions = ['delete_expired']

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_verified:
            return format_html('<span style="background:#F0FDF4;color:#16A34A;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">Verified</span>')
        if obj.is_expired:
            return format_html('<span style="background:#FEF2F2;color:#DC2626;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">Expired</span>')
        return format_html('<span style="background:#FFFBEB;color:#D97706;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">Pending</span>')

    def delete_expired(self, request, queryset):
        from django.utils import timezone
        deleted, _ = queryset.filter(expires_at__lt=timezone.now(), is_verified=False).delete()
        self.message_user(request, f'{deleted} expired OTP(s) deleted.')
    delete_expired.short_description = 'Delete expired OTPs'


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'college', 'course_of_study', 'year_of_study', 'profile_complete', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone', 'college']
    list_filter = ['year_of_study', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    actions = [export_csv]
    fieldsets = [
        ('User', {'fields': ['user', 'phone', 'profile_photo']}),
        ('Academic', {'fields': ['college', 'course_of_study', 'year_of_study']}),
        ('Social', {'fields': ['bio', 'linkedin_url', 'github_url']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
    ]

    @admin.display(description='Profile %')
    def profile_complete(self, obj):
        fields = [obj.phone, obj.college, obj.course_of_study, obj.year_of_study, obj.bio, obj.profile_photo]
        pct = int(sum(1 for f in fields if f) / len(fields) * 100)
        color = '#16A34A' if pct >= 80 else '#D97706' if pct >= 40 else '#DC2626'
        return format_html(
            '<div style="display:flex;align-items:center;gap:6px">'
            '<div style="width:60px;height:6px;background:#E5E7EB;border-radius:3px">'
            '<div style="width:{}%;height:100%;background:{};border-radius:3px"></div></div>'
            '<span style="color:{};font-size:.75rem;font-weight:600">{}%</span></div>',
            pct, color, color, pct
        )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'company', 'star_rating', 'is_approved', 'is_active', 'created_at']
    list_filter = ['is_approved', 'is_active', 'rating']
    list_editable = ['is_approved', 'is_active']
    readonly_fields = ['student', 'created_at']
    search_fields = ['name', 'designation', 'company', 'message']
    date_hierarchy = 'created_at'
    actions = ['approve_reviews', 'reject_reviews', export_csv]

    @admin.display(description='Rating')
    def star_rating(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color:#F59E0B;letter-spacing:2px">{}</span>', stars)

    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved.')
    approve_reviews.short_description = 'Approve selected reviews'

    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} review(s) rejected.')
    reject_reviews.short_description = 'Reject selected reviews'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'read_badge', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'
    actions = ['mark_read', 'mark_unread', export_csv]

    @admin.display(description='Status')
    def read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="background:#F0FDF4;color:#16A34A;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">Read</span>')
        return format_html('<span style="background:#FFFBEB;color:#D97706;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">● Unread</span>')

    def mark_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_read.short_description = 'Mark selected as read'

    def mark_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_unread.short_description = 'Mark selected as unread'
