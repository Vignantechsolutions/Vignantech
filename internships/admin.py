import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.db.models import Count
from .models import Internship


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'title', 'mode_badge', 'duration', 'fees_display', 'seats_display', 'enrollment_count', 'is_featured', 'is_active']
    list_display_links = ['title']
    list_filter = ['mode', 'is_featured', 'is_active', 'start_date']
    list_editable = ['is_featured', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    save_on_top = True
    actions = ['export_csv']
    fieldsets = [
        ('Basic Info', {'fields': ['title', 'slug', 'mode', 'duration', 'fees', 'seats_available', 'start_date', 'is_featured', 'is_active']}),
        ('Content', {'fields': ['description', 'topics_covered', 'benefits', 'certificate_info']}),
        ('Media', {'fields': ['thumbnail'], 'classes': ['collapse']}),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_enrollments=Count('enrollment'))

    @admin.display(description='Thumbnail')
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="height:36px;width:54px;object-fit:cover;border-radius:4px">', obj.thumbnail.url)
        return format_html('<span style="color:#CBD5E1">—</span>')

    @admin.display(description='Mode')
    def mode_badge(self, obj):
        colors = {'online': ('#EFF6FF', '#1D4ED8'), 'offline': ('#F0FDF4', '#16A34A'), 'hybrid': ('#FAF5FF', '#7C3AED')}
        bg, fg = colors.get(obj.mode, ('#F1F5F9', '#475569'))
        return format_html('<span style="background:{};color:{};padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">{}</span>', bg, fg, obj.get_mode_display())

    @admin.display(description='Fees')
    def fees_display(self, obj):
        return format_html('<span style="font-weight:600;color:#16A34A">₹{}</span>', obj.fees)

    @admin.display(description='Seats')
    def seats_display(self, obj):
        color = '#DC2626' if obj.seats_available <= 5 else '#D97706' if obj.seats_available <= 15 else '#16A34A'
        return format_html('<span style="color:{};font-weight:600">{}</span>', color, obj.seats_available)

    @admin.display(description='Enrollments', ordering='_enrollments')
    def enrollment_count(self, obj):
        return format_html(
            '<span style="background:#EFF6FF;color:#1D4ED8;padding:2px 10px;border-radius:20px;font-weight:700;font-size:.8rem">{}</span>',
            obj._enrollments
        )

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=internships.csv'
        writer = csv.writer(response)
        writer.writerow(['Title', 'Mode', 'Duration', 'Fees', 'Seats Available', 'Start Date', 'Active', 'Featured'])
        for i in queryset:
            writer.writerow([i.title, i.mode, i.duration, i.fees, i.seats_available, i.start_date, i.is_active, i.is_featured])
        return response
    export_csv.short_description = 'Export selected to CSV'
