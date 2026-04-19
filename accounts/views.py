from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import StudentProfile, Testimonial, OTPVerification
from payments.models import Enrollment, Assignment, Payment
from certificates.models import Certificate


# ─── helpers ────────────────────────────────────────────────────────────────

def _send_otp_email(email, otp, purpose):
    subject = f'[Vignan TechSolutions] Your verification code: {otp}'
    action = 'verify your email address' if purpose == OTPVerification.PURPOSE_REGISTER else 'reset your password'

    import base64, os
    logo_b64 = ''
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    try:
        with open(logo_path, 'rb') as f:
            logo_b64 = base64.b64encode(f.read()).decode()
    except Exception:
        pass

    html = render_to_string('accounts/emails/otp_email.html', {
        'otp': otp,
        'action': action,
        'expiry': settings.OTP_EXPIRY_MINUTES,
        'logo_b64': logo_b64,
        'year': __import__('datetime').date.today().year,
    })
    from django.core.mail import EmailMultiAlternatives
    msg = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(html),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        headers={
            'X-Priority': '1',
            'X-Mailer': 'Vignan TechSolutions Mailer',
            'List-Unsubscribe': f'<mailto:{settings.COMPANY_EMAIL}>',
        }
    )
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)


# ─── registration ────────────────────────────────────────────────────────────

def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip().lower()
        phone      = request.POST.get('phone', '').strip()
        password1  = request.POST.get('password1', '')
        password2  = request.POST.get('password2', '')

        if not all([first_name, last_name, email, phone, password1]):
            messages.error(request, 'All fields are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
        else:
            # Store pending data in session, send OTP
            request.session['pending_registration'] = {
                'first_name': first_name, 'last_name': last_name,
                'email': email, 'phone': phone, 'password': password1,
            }
            otp_obj = OTPVerification.generate(email, OTPVerification.PURPOSE_REGISTER)
            try:
                _send_otp_email(email, otp_obj.otp, OTPVerification.PURPOSE_REGISTER)
                messages.success(request, f'OTP sent to {email}. Please verify to complete registration.')
                return redirect('accounts:verify_otp')
            except Exception as e:
                otp_obj.delete()
                messages.error(request, f'Email error: {e}' if settings.DEBUG else 'Failed to send OTP. Please try again.')

    return render(request, 'accounts/register.html')


def verify_otp(request):
    pending = request.session.get('pending_registration')
    if not pending:
        return redirect('accounts:register')

    email = pending['email']

    if request.method == 'POST':
        action = request.POST.get('action', 'verify')

        if action == 'resend':
            otp_obj = OTPVerification.generate(email, OTPVerification.PURPOSE_REGISTER)
            try:
                _send_otp_email(email, otp_obj.otp, OTPVerification.PURPOSE_REGISTER)
                messages.success(request, 'A new OTP has been sent to your email.')
            except Exception:
                messages.error(request, 'Failed to resend OTP. Please try again.')
            return redirect('accounts:verify_otp')

        entered = request.POST.get('otp', '').strip()
        otp_obj = OTPVerification.objects.filter(
            email=email, purpose=OTPVerification.PURPOSE_REGISTER,
            is_verified=False
        ).order_by('-created_at').first()

        if not otp_obj:
            messages.error(request, 'No OTP found. Please register again.')
            return redirect('accounts:register')
        if otp_obj.is_expired:
            messages.error(request, 'OTP has expired. Please request a new one.')
            return redirect('accounts:verify_otp')
        if otp_obj.otp != entered:
            messages.error(request, 'Incorrect OTP. Please try again.')
            return render(request, 'accounts/verify_otp.html', {'email': email, 'purpose': 'register'})

        # OTP correct — create account
        otp_obj.is_verified = True
        otp_obj.save()

        user = User.objects.create_user(
            username=pending['email'], email=pending['email'],
            password=pending['password'],
            first_name=pending['first_name'], last_name=pending['last_name'],
        )
        StudentProfile.objects.create(user=user, phone=pending['phone'])
        del request.session['pending_registration']

        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}! Your account is verified and ready.')
        return redirect('accounts:dashboard')

    return render(request, 'accounts/verify_otp.html', {'email': email, 'purpose': 'register'})


# ─── login / logout ──────────────────────────────────────────────────────────

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/admin/analytics/' if request.user.is_staff else 'accounts:dashboard')
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/analytics/')
            return redirect(request.GET.get('next', '/accounts/dashboard/'))
        messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')


# ─── forgot / reset password ─────────────────────────────────────────────────

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if not User.objects.filter(email=email, is_active=True).exists():
            # Don't reveal whether email exists — show same message
            messages.success(request, f'If {email} is registered, an OTP has been sent.')
            return redirect('accounts:forgot_password')
        otp_obj = OTPVerification.generate(email, OTPVerification.PURPOSE_RESET)
        try:
            _send_otp_email(email, otp_obj.otp, OTPVerification.PURPOSE_RESET)
            request.session['reset_email'] = email
            messages.success(request, f'OTP sent to {email}.')
            return redirect('accounts:verify_reset_otp')
        except Exception as e:
            otp_obj.delete()
            messages.error(request, f'Email error: {e}' if settings.DEBUG else 'Failed to send OTP. Please try again.')
    return render(request, 'accounts/forgot_password.html')


def verify_reset_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('accounts:forgot_password')

    if request.method == 'POST':
        action = request.POST.get('action', 'verify')

        if action == 'resend':
            otp_obj = OTPVerification.generate(email, OTPVerification.PURPOSE_RESET)
            try:
                _send_otp_email(email, otp_obj.otp, OTPVerification.PURPOSE_RESET)
                messages.success(request, 'A new OTP has been sent.')
            except Exception:
                messages.error(request, 'Failed to resend OTP.')
            return redirect('accounts:verify_reset_otp')

        entered = request.POST.get('otp', '').strip()
        otp_obj = OTPVerification.objects.filter(
            email=email, purpose=OTPVerification.PURPOSE_RESET,
            is_verified=False
        ).order_by('-created_at').first()

        if not otp_obj:
            messages.error(request, 'No OTP found. Please try again.')
            return redirect('accounts:forgot_password')
        if otp_obj.is_expired:
            messages.error(request, 'OTP expired. Request a new one.')
            return redirect('accounts:verify_reset_otp')
        if otp_obj.otp != entered:
            messages.error(request, 'Incorrect OTP.')
            return render(request, 'accounts/verify_otp.html', {'email': email, 'purpose': 'reset'})

        otp_obj.is_verified = True
        otp_obj.save()
        request.session['reset_verified'] = True
        return redirect('accounts:reset_password')

    return render(request, 'accounts/verify_otp.html', {'email': email, 'purpose': 'reset'})


def reset_password(request):
    email = request.session.get('reset_email')
    verified = request.session.get('reset_verified')
    if not email or not verified:
        return redirect('accounts:forgot_password')

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        else:
            user = User.objects.filter(email=email).first()
            if user:
                user.set_password(password1)
                user.save()
            del request.session['reset_email']
            del request.session['reset_verified']
            messages.success(request, 'Password reset successfully. Please log in.')
            return redirect('accounts:login')

    return render(request, 'accounts/reset_password.html', {'email': email})


# ─── dashboard & profile ─────────────────────────────────────────────────────

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('/admin/analytics/')
    profile_obj, _ = StudentProfile.objects.get_or_create(user=request.user)
    enrollments  = Enrollment.objects.filter(student=request.user).select_related('course', 'internship')
    certificates = Certificate.objects.filter(student=request.user).select_related('enrollment__course', 'enrollment__internship')
    payments     = Payment.objects.filter(student=request.user).order_by('-created_at')
    user_review  = Testimonial.objects.filter(student=request.user).first()
    paid_payments = payments.filter(status='paid')
    total_spent  = sum(p.amount for p in paid_payments)
    active_enrollments    = enrollments.filter(status='active')
    completed_enrollments = enrollments.filter(status='completed')
    pending_enrollments   = enrollments.filter(status='pending')
    # Profile completion score
    fields = [profile_obj.phone, profile_obj.college, profile_obj.course_of_study,
              profile_obj.year_of_study, profile_obj.bio, profile_obj.profile_photo,
              request.user.first_name, request.user.last_name]
    profile_pct = int(sum(1 for f in fields if f) / len(fields) * 100)
    context = {
        'profile': profile_obj,
        'enrollments': enrollments,
        'active_enrollments': active_enrollments,
        'completed_enrollments': completed_enrollments,
        'pending_enrollments': pending_enrollments,
        'certificates': certificates,
        'payments': payments,
        'recent_payments': payments[:5],
        'active_count': active_enrollments.count(),
        'completed_count': completed_enrollments.count(),
        'pending_count': pending_enrollments.count(),
        'total_spent': total_spent,
        'user_review': user_review,
        'profile_pct': profile_pct,
        'cert_count': certificates.count(),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    if request.user.is_staff:
        return redirect('/admin/analytics/')
    profile_obj, _ = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.last_name  = request.POST.get('last_name', user.last_name).strip()
        user.save()
        profile_obj.phone          = request.POST.get('phone', profile_obj.phone).strip()
        profile_obj.college        = request.POST.get('college', '').strip()
        profile_obj.course_of_study = request.POST.get('course_of_study', '').strip()
        profile_obj.year_of_study  = request.POST.get('year_of_study', '').strip()
        profile_obj.bio            = request.POST.get('bio', '').strip()
        profile_obj.linkedin_url   = request.POST.get('linkedin_url', '').strip()
        profile_obj.github_url     = request.POST.get('github_url', '').strip()
        if 'profile_photo' in request.FILES:
            profile_obj.profile_photo = request.FILES['profile_photo']
        profile_obj.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'profile': profile_obj})


@login_required
def submit_assignment(request, enrollment_id):
    if request.user.is_staff:
        return redirect('/admin/analytics/')
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user, status='active')
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        file        = request.FILES.get('file')
        if title and file:
            Assignment.objects.create(enrollment=enrollment, title=title, description=description, file=file)
            messages.success(request, 'Assignment submitted successfully.')
            return redirect('accounts:dashboard')
        messages.error(request, 'Title and file are required.')
    return render(request, 'accounts/submit_assignment.html', {'enrollment': enrollment})


@login_required
def submit_review(request):
    existing = Testimonial.objects.filter(student=request.user).first()
    if request.method == 'POST':
        rating      = int(request.POST.get('rating', 5))
        message     = request.POST.get('message', '').strip()
        designation = request.POST.get('designation', '').strip()
        next_url    = request.POST.get('next', '/accounts/dashboard/')
        if not message or not designation:
            messages.error(request, 'Please fill all required fields.')
        else:
            name = request.user.get_full_name() or request.user.email
            if existing:
                existing.rating = rating; existing.message = message
                existing.designation = designation; existing.is_approved = False
                existing.save()
                messages.success(request, 'Review updated and pending approval.')
            else:
                Testimonial.objects.create(
                    student=request.user, name=name,
                    designation=designation, rating=rating,
                    message=message, is_approved=False,
                )
                messages.success(request, 'Thank you! Your review is pending admin approval.')
        return redirect(next_url)
    return redirect('accounts:dashboard')
