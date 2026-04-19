from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import ProjectDomain, Project, ProjectScreenshot


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(ProjectDomain)
class ProjectDomainAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'emoji_preview', 'name', 'slug',
        'gradient_preview', 'badge_preview',
        'project_count', 'is_active',
    ]
    list_display_links = ['name']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']
    fieldsets = [
        ('Identity', {
            'fields': ['name', 'slug', 'emoji', 'description', 'order', 'is_active'],
        }),
        ('Colors & Styling', {
            'description': (
                'These control the gradient on project cards and the domain badge color. '
                'Use hex values like #1E3A8A. badge_bg accepts CSS rgba e.g. rgba(59,130,246,.12).'
            ),
            'fields': ['color_from', 'color_to', 'badge_bg', 'badge_color'],
        }),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_count=Count('projects'))

    @admin.display(description='Emoji')
    def emoji_preview(self, obj):
        return format_html('<span style="font-size:1.4rem">{}</span>', obj.emoji)

    @admin.display(description='Gradient')
    def gradient_preview(self, obj):
        return format_html(
            '<div style="width:80px;height:22px;border-radius:6px;'
            'background:linear-gradient(135deg,{},{})"></div>',
            obj.color_from, obj.color_to,
        )

    @admin.display(description='Badge')
    def badge_preview(self, obj):
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:50px;font-size:.75rem;font-weight:700">{}</span>',
            obj.badge_bg, obj.badge_color, obj.name,
        )

    @admin.display(description='Projects', ordering='_count')
    def project_count(self, obj):
        return format_html(
            '<span style="background:#EFF6FF;color:#1D4ED8;padding:2px 10px;'
            'border-radius:50px;font-weight:700;font-size:.8rem">{}</span>',
            obj._count,
        )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'domain_badge', 'is_featured', 'is_active',
        'tech_preview', 'created_at',
    ]
    list_filter = ['domain', 'is_featured', 'is_active', 'created_at']
    list_editable = ['is_featured', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'tech_stack', 'description']
    autocomplete_fields = ['domain']
    date_hierarchy = 'created_at'
    save_on_top = True
    fieldsets = [
        ('Basic Info', {
            'fields': ['title', 'slug', 'domain', 'is_featured', 'is_active'],
        }),
        ('Content', {
            'fields': ['description', 'problem_statement', 'objectives', 'features', 'conclusion'],
        }),
        ('Technical Details', {
            'fields': ['tech_stack', 'algorithms', 'dataset', 'future_enhancements'],
        }),
        ('Media & Links', {
            'fields': ['thumbnail', 'live_url', 'github_url'],
            'classes': ['collapse'],
        }),
    ]
    inlines = [ProjectScreenshotInline]

    @admin.display(description='Domain')
    def domain_badge(self, obj):
        if not obj.domain:
            return format_html('<span style="color:#94A3B8">—</span>')
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:50px;font-size:.75rem;font-weight:700">{} {}</span>',
            obj.domain.badge_bg, obj.domain.badge_color,
            obj.domain.emoji, obj.domain.name,
        )

    @admin.display(description='Tech Stack')
    def tech_preview(self, obj):
        tags = obj.tech_stack.split()[:4]
        html = ''.join(
            f'<span style="background:#F1F5F9;color:#475569;padding:2px 7px;'
            f'border-radius:4px;font-size:.72rem;margin:1px;display:inline-block">{t}</span>'
            for t in tags
        )
        return format_html(html)


@admin.register(ProjectScreenshot)
class ProjectScreenshotAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'order']
    list_editable = ['order']
    search_fields = ['project__title', 'caption']
