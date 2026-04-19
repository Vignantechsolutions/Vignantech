from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Certificate, CustomCertificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['cert_id_display', 'student', 'program', 'issued_date', 'validity_badge', 'download_link', 'is_valid']
    list_filter = ['is_valid', 'issued_date']
    list_editable = ['is_valid']
    search_fields = ['student__first_name', 'student__last_name', 'student__email', 'certificate_id']
    readonly_fields = ['certificate_id', 'issued_date', 'student', 'enrollment']
    date_hierarchy = 'issued_date'
    actions = ['revoke_certificates', 'reissue_certificates']
    fieldsets = [
        ('Certificate', {'fields': ['certificate_id', 'student', 'enrollment', 'certificate_file', 'issued_date']}),
        ('Status', {'fields': ['is_valid']}),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'enrollment__course', 'enrollment__internship')

    @admin.display(description='Certificate ID')
    def cert_id_display(self, obj):
        short = str(obj.certificate_id)[:8].upper()
        return format_html('<span style="font-family:monospace;font-weight:600;color:#1D4ED8">CERT-{}</span>', short)

    @admin.display(description='Program')
    def program(self, obj):
        return obj.enrollment.course or obj.enrollment.internship

    @admin.display(description='Valid')
    def validity_badge(self, obj):
        if obj.is_valid:
            return format_html('<span style="background:#F0FDF4;color:#16A34A;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">✓ Valid</span>')
        return format_html('<span style="background:#FEF2F2;color:#DC2626;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">✕ Revoked</span>')

    @admin.display(description='Download')
    def download_link(self, obj):
        if obj.certificate_file:
            return format_html('<a href="{}" target="_blank" style="color:#1D4ED8;font-weight:600;font-size:.8rem">↓ PDF</a>', obj.certificate_file.url)
        return format_html('<span style="color:#CBD5E1">No file</span>')

    def revoke_certificates(self, request, queryset):
        updated = queryset.update(is_valid=False)
        self.message_user(request, f'{updated} certificate(s) revoked.')
    revoke_certificates.short_description = 'Revoke selected certificates'

    def reissue_certificates(self, request, queryset):
        from certificates.views import generate_certificate_pdf
        from django.core.files.base import ContentFile
        count = 0
        for cert in queryset:
            pdf_buffer = generate_certificate_pdf(cert)
            cert.certificate_file.save(
                f"certificate-{str(cert.certificate_id)[:8]}.pdf",
                ContentFile(pdf_buffer.read()), save=False
            )
            cert.is_valid = True
            cert.save()
            count += 1
        self.message_user(request, f'{count} certificate(s) reissued.')
    reissue_certificates.short_description = 'Reissue (regenerate PDF) for selected'


@admin.register(CustomCertificate)
class CustomCertificateAdmin(admin.ModelAdmin):
    list_display = ['cert_number', 'recipient_name', 'cert_type_badge', 'program_name', 'issued_date', 'created_by', 'download_link']
    list_filter  = ['cert_type', 'issued_date']
    search_fields = ['cert_number', 'recipient_name', 'program_name']
    readonly_fields = ['cert_number', 'created_at', 'created_by']
    date_hierarchy = 'issued_date'
    fieldsets = [
        ('Certificate', {'fields': ['cert_number', 'cert_type', 'recipient_name', 'program_name', 'project_domain', 'issued_date', 'start_date', 'end_date', 'extra_note']}),
        ('Signatory',   {'fields': ['signatory_name', 'signatory_title', 'signatory_org']}),
        ('Meta',        {'fields': ['created_by', 'created_at'], 'classes': ['collapse']}),
    ]

    @admin.display(description='Type')
    def cert_type_badge(self, obj):
        colors_map = {
            'completion':    ('#EFF6FF', '#1D4ED8'),
            'internship':    ('#F0FDF4', '#16A34A'),
            'participation': ('#FAF5FF', '#7C3AED'),
            'excellence':    ('#FFFBEB', '#D97706'),
            'appreciation':  ('#FFF1F2', '#E11D48'),
            'training':      ('#F0FDFA', '#0D9488'),
        }
        bg, fg = colors_map.get(obj.cert_type, ('#F1F5F9', '#475569'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">{}</span>',
            bg, fg, obj.get_cert_type_display().replace('Certificate of ', '')
        )

    @admin.display(description='Download')
    def download_link(self, obj):
        return format_html(
            '<a href="/admin/certificate-generator/{}/download/" '
            'style="background:linear-gradient(135deg,#C9A84C,#A07830);color:#fff;'
            'padding:3px 12px;border-radius:6px;font-size:.75rem;font-weight:700;text-decoration:none">'
            '⬇ PDF</a>', obj.pk
        )
