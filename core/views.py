from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def health_check(request):
    return JsonResponse({'status': 'ok'})
from courses.models import Course
from internships.models import Internship
from projects.models import Project, ProjectDomain
from accounts.models import Testimonial, ContactMessage


SERVICES = [
    {'icon': 'bi-briefcase-fill', 'color': 'icon-blue', 'title': 'Internship Programs',
     'desc': 'Hands-on industry internships with real project experience and mentorship.',
     'url': '/internships/'},
    {'icon': 'bi-book-fill', 'color': 'icon-green', 'title': 'Professional Courses',
     'desc': 'Industry-aligned courses taught by experienced professionals.',
     'url': '/courses/'},
    {'icon': 'bi-kanban-fill', 'color': 'icon-purple', 'title': 'Real-Time Projects',
     'desc': 'Work on live projects and build an impressive portfolio.',
     'url': '/projects/'},
    {'icon': 'bi-building-fill', 'color': 'icon-orange', 'title': 'Corporate Training',
     'desc': 'Customized training programs for colleges and companies.',
     'url': '/corporate-training/'},
    {'icon': 'bi-code-slash', 'color': 'icon-red', 'title': 'Software Development',
     'desc': 'End-to-end software development services for businesses.',
     'url': '/contact/'},
    {'icon': 'bi-award-fill', 'color': 'icon-teal', 'title': 'Certifications',
     'desc': 'Industry-recognized certificates to boost your career prospects.',
     'url': '/certificates/verify/'},
]


WHY_US = [
    {'icon': 'bi-kanban-fill',      'title': 'UG & PG Major Projects',   'desc': 'Complete MCA, BCA, B.Tech & M.Tech projects — code, documentation, demo & mentorship. VTU CPGS aligned.'},
    {'icon': 'bi-building-fill',    'title': 'Corporate Training',        'desc': 'Custom tech training for colleges and companies — Python, Django, React, AWS, and more. On-site or online.'},
    {'icon': 'bi-book-half',        'title': 'Industry Courses',          'desc': 'Structured, mentor-led courses built around what companies actually hire for — not outdated syllabi.'},
    {'icon': 'bi-briefcase-fill',   'title': 'Live Internships',          'desc': 'Real internships with real tasks, real deadlines, and a certificate that proves it — not just a participation letter.'},
    {'icon': 'bi-globe2',           'title': 'Website Development',       'desc': 'Professional websites for businesses, colleges, and startups — fast, mobile-ready, and built to convert.'},
    {'icon': 'bi-award-fill',       'title': 'Verified Certificates',     'desc': 'Every certificate carries a unique ID — scannable, verifiable, and trusted by recruiters.'},
]

TECH_LIST = [
    {'icon': 'bi-filetype-py', 'name': 'Python'}, {'icon': 'bi-filetype-js', 'name': 'JavaScript'},
    {'icon': 'bi-filetype-java', 'name': 'Java'}, {'icon': 'bi-database-fill', 'name': 'MySQL'},
    {'icon': 'bi-phone-fill', 'name': 'React Native'}, {'icon': 'bi-cloud-fill', 'name': 'AWS'},
    {'icon': 'bi-git', 'name': 'Git & GitHub'}, {'icon': 'bi-robot', 'name': 'Machine Learning'},
    {'icon': 'bi-bar-chart-fill', 'name': 'Data Science'}, {'icon': 'bi-shield-fill', 'name': 'Cybersecurity'},
    {'icon': 'bi-layout-text-window', 'name': 'Django'}, {'icon': 'bi-bootstrap-fill', 'name': 'Bootstrap'},
]


def home(request):
    context = {
        'featured_courses': Course.objects.filter(is_featured=True, is_active=True)[:6],
        'featured_internships': Internship.objects.filter(is_featured=True, is_active=True)[:4],
        'featured_projects': Project.objects.filter(is_featured=True, is_active=True).select_related('domain')[:6],
        'project_domains': ProjectDomain.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_approved=True)[:6],
        'services_list': SERVICES,
        'project_total': Project.objects.filter(is_active=True).count(),
        'why_us_home': [
            {'icon': 'bi-kanban-fill',   'title': '75+ MCA Projects',        'desc': 'Across 5 domains for VTU CPGS'},
            {'icon': 'bi-people-fill',   'title': 'Expert Instructors',      'desc': '5+ years industry experience'},
            {'icon': 'bi-laptop-fill',   'title': 'End-to-End Support',      'desc': 'Code, docs, demo & mentorship'},
            {'icon': 'bi-award-fill',    'title': 'Recognized Certificates', 'desc': 'Verified & industry accepted'},
            {'icon': 'bi-briefcase-fill','title': 'Placement Support',       'desc': 'Till you get hired'},
            {'icon': 'bi-headset',       'title': '24/7 Mentor Support',     'desc': 'WhatsApp, email & phone'},
        ],
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html', {'why_us': WHY_US})


def corporate_training(request):
    return render(request, 'core/corporate_training.html', {'tech_list': TECH_LIST})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and subject and message:
            ContactMessage.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)
            try:
                send_mail(
                    f'New Contact: {subject}',
                    f'From: {name} ({email})\nPhone: {phone}\n\n{message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.COMPANY_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Your message has been sent! We will get back to you soon.')
            return redirect('core:contact')
        else:
            messages.error(request, 'Please fill all required fields.')

    return render(request, 'core/contact.html')


def search(request):
    query = request.GET.get('q', '').strip()
    results = {'courses': [], 'internships': [], 'projects': []}
    if query:
        results['courses'] = Course.objects.filter(title__icontains=query, is_active=True)
        results['internships'] = Internship.objects.filter(title__icontains=query, is_active=True)
        results['projects'] = Project.objects.filter(title__icontains=query, is_active=True)
    return render(request, 'core/search.html', {'results': results, 'query': query})


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    import sys
    import traceback
    from django.http import HttpResponse
    if request.GET.get('debug') == '1':
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        return HttpResponse(tb_text, status=500, content_type="text/plain; charset=utf-8")
    return render(request, '500.html', status=500)

