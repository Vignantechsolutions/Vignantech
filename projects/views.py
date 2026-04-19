from django.shortcuts import render, get_object_or_404
from .models import Project, ProjectDomain


def project_list(request):
    domains = ProjectDomain.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True).select_related('domain')
    domain_slug = request.GET.get('category')
    active_domain = None
    if domain_slug:
        active_domain = domains.filter(slug=domain_slug).first()
        if active_domain:
            projects = projects.filter(domain=active_domain)
    return render(request, 'projects/list.html', {
        'projects': projects,
        'domains': domains,
        'active_domain': active_domain,
        'active_cat': domain_slug,  # kept for backward-compat with template links
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_active=True)
    screenshots = project.screenshots.all()
    objectives = [o.strip() for o in project.objectives.splitlines() if o.strip()]
    features = [f.strip() for f in project.features.splitlines() if f.strip()]
    algorithms = [a.strip() for a in project.algorithms.splitlines() if a.strip()]
    enhancements = [e.strip() for e in project.future_enhancements.splitlines() if e.strip()]
    related = Project.objects.filter(domain=project.domain, is_active=True).exclude(id=project.id)[:3]
    return render(request, 'projects/detail.html', {
        'project': project,
        'screenshots': screenshots,
        'objectives': objectives,
        'features': features,
        'algorithms': algorithms,
        'enhancements': enhancements,
        'related': related,
    })
