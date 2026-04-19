from django.shortcuts import render, get_object_or_404
from .models import Internship


def internship_list(request):
    internships = Internship.objects.filter(is_active=True)
    mode = request.GET.get('mode')
    if mode:
        internships = internships.filter(mode=mode)
    return render(request, 'internships/list.html', {'internships': internships})


def internship_detail(request, slug):
    internship = get_object_or_404(Internship, slug=slug, is_active=True)
    is_enrolled = False
    if request.user.is_authenticated:
        from payments.models import Enrollment
        is_enrolled = Enrollment.objects.filter(
            student=request.user, internship=internship, status__in=['active', 'completed']
        ).exists()
    return render(request, 'internships/detail.html', {
        'internship': internship, 'is_enrolled': is_enrolled
    })
