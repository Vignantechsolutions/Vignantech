import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Course, CourseModule, CourseMaterial


class CourseMaterialInline(admin.TabularInline):
    model = CourseMaterial
    extra = 1
    fields = ['title', 'material_type', 'file', 'url', 'order']


class CourseModuleInline(admin.StackedInline):
    model = CourseModule
    extra = 1
    fields = ['title', 'description', 'duration', 'order']
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'course_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_count=Count('course'))

    @admin.display(description='Courses', ordering='_count')
    def course_count(self, obj):
        return format_html(
            '<span style="background:#EFF6FF;color:#1D4ED8;padding:2px 10px;border-radius:20px;font-weight:700;font-size:.8rem">{}</span>',
            obj._count
        )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'title', 'category', 'instructor', 'fees_display', 'level_badge', 'enrollment_count', 'is_featured', 'is_active']
    list_display_links = ['title']
    list_filter = ['level', 'is_featured', 'is_active', 'category', 'created_at']
    list_editable = ['is_featured', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'instructor', 'description']
    date_hierarchy = 'created_at'
    save_on_top = True
    inlines = [CourseModuleInline]
    actions = ['duplicate_course', 'export_csv']
    fieldsets = [
        ('Basic Info', {'fields': ['title', 'slug', 'category', 'level', 'is_featured', 'is_active']}),
        ('Details', {'fields': ['description', 'duration', 'fees']}),
        ('Instructor', {'fields': ['instructor', 'instructor_bio', 'instructor_photo']}),
        ('Media', {'fields': ['thumbnail'], 'classes': ['collapse']}),
    ]

    def get_queryset(self, request):
        from payments.models import Enrollment
        return super().get_queryset(request).annotate(_enrollments=Count('enrollment'))

    @admin.display(description='Thumbnail')
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="height:36px;width:54px;object-fit:cover;border-radius:4px">', obj.thumbnail.url)
        return format_html('<span style="color:#CBD5E1">—</span>')

    @admin.display(description='Fees')
    def fees_display(self, obj):
        return format_html('<span style="font-weight:600;color:#16A34A">₹{}</span>', obj.fees)

    @admin.display(description='Level')
    def level_badge(self, obj):
        colors = {'beginner': ('#F0FDF4', '#16A34A'), 'intermediate': ('#FFFBEB', '#D97706'), 'advanced': ('#FEF2F2', '#DC2626')}
        bg, fg = colors.get(obj.level, ('#F1F5F9', '#475569'))
        return format_html('<span style="background:{};color:{};padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600">{}</span>', bg, fg, obj.get_level_display())

    @admin.display(description='Enrollments', ordering='_enrollments')
    def enrollment_count(self, obj):
        return format_html(
            '<span style="background:#EFF6FF;color:#1D4ED8;padding:2px 10px;border-radius:20px;font-weight:700;font-size:.8rem">{}</span>',
            obj._enrollments
        )

    def duplicate_course(self, request, queryset):
        for course in queryset:
            course.pk = None
            course.slug = course.slug + '-copy'
            course.title = course.title + ' (Copy)'
            course.is_active = False
            course.save()
        self.message_user(request, f'{queryset.count()} course(s) duplicated as drafts.')
    duplicate_course.short_description = 'Duplicate selected courses'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=courses.csv'
        writer = csv.writer(response)
        writer.writerow(['Title', 'Category', 'Instructor', 'Fees', 'Level', 'Duration', 'Active', 'Featured'])
        for c in queryset:
            writer.writerow([c.title, c.category, c.instructor, c.fees, c.level, c.duration, c.is_active, c.is_featured])
        return response
    export_csv.short_description = 'Export selected to CSV'


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration', 'material_count']
    list_filter = ['course']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']
    inlines = [CourseMaterialInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_mats=Count('materials'))

    @admin.display(description='Materials', ordering='_mats')
    def material_count(self, obj):
        return obj._mats


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'material_type', 'order']
    list_filter = ['material_type', 'module__course']
    search_fields = ['title', 'module__title']
