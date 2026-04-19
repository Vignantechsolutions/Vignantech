from django.shortcuts import render, get_object_or_404
from .models import Course, CourseModule


def course_list(request):
    courses = Course.objects.filter(is_active=True)
    category = request.GET.get('category')
    level = request.GET.get('level')
    if category:
        courses = courses.filter(category__slug=category)
    if level:
        courses = courses.filter(level=level)
    return render(request, 'courses/list.html', {'courses': courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    modules = course.modules.prefetch_related('materials').all()
    is_enrolled = False
    if request.user.is_authenticated:
        from payments.models import Enrollment
        is_enrolled = Enrollment.objects.filter(
            student=request.user, course=course, status__in=['active', 'completed']
        ).exists()
    return render(request, 'courses/detail.html', {
        'course': course, 'modules': modules, 'is_enrolled': is_enrolled
    })
