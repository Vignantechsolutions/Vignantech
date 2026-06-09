import hmac
import hashlib
import razorpay
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import StudentProfile, Testimonial, OTPVerification, ContactMessage
from courses.models import Course
from internships.models import Internship
from projects.models import Project, ProjectDomain
from payments.models import Enrollment, Payment
from certificates.models import Certificate, CustomCertificate
from .serializers import (
    CourseSerializer, CourseDetailSerializer, InternshipSerializer,
    ProjectSerializer, ProjectDomainSerializer, TestimonialSerializer,
    StudentProfileSerializer, RegisterSerializer, EnrollmentSerializer,
    PaymentSerializer, CertificateSerializer,
)


# ── Auth ─────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    s = RegisterSerializer(data=request.data)
    if not s.is_valid():
        return Response(s.errors, status=400)
    d = s.validated_data
    otp_obj = OTPVerification.generate(d['email'], OTPVerification.PURPOSE_REGISTER)
    # Store pending in a simple way — return token for OTP step
    return Response({'message': f"OTP sent to {d['email']}", 'email': d['email'],
                     'pending': d}, status=200)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_otp_view(request):
    email = request.data.get('email', '').lower()
    otp = request.data.get('otp', '').strip()
    pending = request.data.get('pending', {})

    otp_obj = OTPVerification.objects.filter(
        email=email, purpose=OTPVerification.PURPOSE_REGISTER, is_verified=False
    ).order_by('-created_at').first()

    if not otp_obj:
        return Response({'error': 'No OTP found.'}, status=400)
    if otp_obj.is_expired:
        return Response({'error': 'OTP expired.'}, status=400)
    if otp_obj.otp != otp:
        return Response({'error': 'Incorrect OTP.'}, status=400)

    otp_obj.is_verified = True
    otp_obj.save()

    user = User.objects.create_user(
        username=email, email=email, password=pending['password'],
        first_name=pending['first_name'], last_name=pending['last_name'],
    )
    StudentProfile.objects.create(user=user, phone=pending.get('phone', ''))
    refresh = RefreshToken.for_user(user)
    return Response({'access': str(refresh.access_token), 'refresh': str(refresh)})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    email = request.data.get('email', '').lower()
    password = request.data.get('password', '')
    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({'error': 'Invalid credentials.'}, status=401)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {'id': user.id, 'name': user.get_full_name(),
                 'email': user.email, 'is_staff': user.is_staff},
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def forgot_password_view(request):
    email = request.data.get('email', '').lower()
    if User.objects.filter(email=email, is_active=True).exists():
        otp_obj = OTPVerification.generate(email, OTPVerification.PURPOSE_RESET)
    return Response({'message': f'If {email} is registered, an OTP has been sent.'})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password_view(request):
    email = request.data.get('email', '').lower()
    otp = request.data.get('otp', '').strip()
    password = request.data.get('password', '')

    otp_obj = OTPVerification.objects.filter(
        email=email, purpose=OTPVerification.PURPOSE_RESET, is_verified=False
    ).order_by('-created_at').first()

    if not otp_obj or otp_obj.is_expired or otp_obj.otp != otp:
        return Response({'error': 'Invalid or expired OTP.'}, status=400)
    if len(password) < 8:
        return Response({'error': 'Password too short.'}, status=400)

    user = User.objects.filter(email=email).first()
    if user:
        user.set_password(password)
        user.save()
    otp_obj.is_verified = True
    otp_obj.save()
    return Response({'message': 'Password reset successfully.'})


# ── Profile ───────────────────────────────────────────────────────────────────

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        return Response(StudentProfileSerializer(profile).data)

    def patch(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()
        for field in ['phone', 'college', 'course_of_study', 'year_of_study', 'bio', 'linkedin_url', 'github_url']:
            if field in request.data:
                setattr(profile, field, request.data[field])
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
        profile.save()
        return Response(StudentProfileSerializer(profile).data)


# ── Dashboard ─────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_view(request):
    user = request.user
    enrollments = Enrollment.objects.filter(student=user).select_related('course', 'internship')
    certificates = Certificate.objects.filter(student=user)
    payments = Payment.objects.filter(student=user).order_by('-created_at')
    paid_total = sum(p.amount for p in payments.filter(status='paid'))

    return Response({
        'enrollments': EnrollmentSerializer(enrollments, many=True).data,
        'certificates': CertificateSerializer(certificates, many=True).data,
        'payments': PaymentSerializer(payments[:5], many=True).data,
        'stats': {
            'active': enrollments.filter(status='active').count(),
            'completed': enrollments.filter(status='completed').count(),
            'certificates': certificates.count(),
            'total_spent': float(paid_total),
        },
    })


# ── Courses ───────────────────────────────────────────────────────────────────

class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Course.objects.filter(is_active=True)
        if cat := self.request.query_params.get('category'):
            qs = qs.filter(category__slug=cat)
        if level := self.request.query_params.get('level'):
            qs = qs.filter(level=level)
        if featured := self.request.query_params.get('featured'):
            qs = qs.filter(is_featured=True)
        return qs


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Course.objects.filter(is_active=True)
    lookup_field = 'slug'


# ── Internships ───────────────────────────────────────────────────────────────

class InternshipListView(generics.ListAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Internship.objects.filter(is_active=True)
        if mode := self.request.query_params.get('mode'):
            qs = qs.filter(mode=mode)
        if self.request.query_params.get('featured'):
            qs = qs.filter(is_featured=True)
        return qs


class InternshipDetailView(generics.RetrieveAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Internship.objects.filter(is_active=True)
    lookup_field = 'slug'


# ── Projects ──────────────────────────────────────────────────────────────────

class ProjectDomainListView(generics.ListAPIView):
    serializer_class = ProjectDomainSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ProjectDomain.objects.filter(is_active=True)


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Project.objects.filter(is_active=True).select_related('domain')
        if cat := self.request.query_params.get('category'):
            qs = qs.filter(domain__slug=cat)
        if self.request.query_params.get('featured'):
            qs = qs.filter(is_featured=True)
        if q := self.request.query_params.get('q'):
            qs = qs.filter(title__icontains=q)
        return qs


class ProjectDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.filter(is_active=True)
    lookup_field = 'slug'


# ── Testimonials ──────────────────────────────────────────────────────────────

class TestimonialListView(generics.ListAPIView):
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Testimonial.objects.filter(is_approved=True, is_active=True)[:12]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_review_view(request):
    rating = int(request.data.get('rating', 5))
    message = request.data.get('message', '').strip()
    designation = request.data.get('designation', '').strip()
    if not message or not designation:
        return Response({'error': 'All fields required.'}, status=400)
    existing = Testimonial.objects.filter(student=request.user).first()
    name = request.user.get_full_name() or request.user.email
    if existing:
        existing.rating = rating; existing.message = message
        existing.designation = designation; existing.is_approved = False
        existing.save()
    else:
        Testimonial.objects.create(
            student=request.user, name=name,
            designation=designation, rating=rating,
            message=message, is_approved=False,
        )
    return Response({'message': 'Review submitted, pending approval.'})


# ── Payments ──────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initiate_payment_view(request):
    item_type = request.data.get('type')   # 'course' or 'internship'
    item_id = request.data.get('id')

    if item_type == 'course':
        item = Course.objects.get(id=item_id, is_active=True)
        existing = Enrollment.objects.filter(student=request.user, course=item, status__in=['active', 'completed']).first()
    else:
        item = Internship.objects.get(id=item_id, is_active=True)
        existing = Enrollment.objects.filter(student=request.user, internship=item, status__in=['active', 'completed']).first()

    if existing:
        return Response({'error': 'Already enrolled.'}, status=400)

    if not settings.RAZORPAY_KEY_ID or settings.RAZORPAY_KEY_ID.startswith('your_'):
        return Response({'error': 'Payment not configured.'}, status=400)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({'amount': int(item.fees * 100), 'currency': 'INR', 'payment_capture': 1})

    enrollment = Enrollment.objects.create(
        student=request.user, enrollment_type=item_type,
        course=item if item_type == 'course' else None,
        internship=item if item_type == 'internship' else None,
        status='pending',
    )
    Payment.objects.create(student=request.user, enrollment=enrollment,
                           razorpay_order_id=order['id'], amount=item.fees)

    return Response({'order_id': order['id'], 'amount': item.fees,
                     'key': settings.RAZORPAY_KEY_ID, 'name': item.title})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def payment_callback_view(request):
    order_id = request.data.get('razorpay_order_id')
    payment_id = request.data.get('razorpay_payment_id')
    signature = request.data.get('razorpay_signature')

    try:
        payment = Payment.objects.get(razorpay_order_id=order_id)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found.'}, status=404)

    key_secret = settings.RAZORPAY_KEY_SECRET.encode()
    msg = f'{order_id}|{payment_id}'.encode()
    generated = hmac.new(key_secret, msg, hashlib.sha256).hexdigest()

    if generated == signature:
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = 'paid'
        payment.save()
        payment.enrollment.status = 'active'
        payment.enrollment.save()
        return Response({'message': 'Payment verified. Enrollment active.'})
    else:
        payment.status = 'failed'
        payment.save()
        return Response({'error': 'Signature mismatch.'}, status=400)


# ── Certificates ──────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_certificate_view(request, cert_id):
    try:
        cert = Certificate.objects.select_related(
            'student', 'enrollment__course', 'enrollment__internship'
        ).get(certificate_id=cert_id, is_valid=True)
        return Response(CertificateSerializer(cert).data)
    except Certificate.DoesNotExist:
        return Response({'error': 'Invalid certificate.'}, status=404)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_certificate_view(request, cert_id):
    from certificates.views import generate_certificate_pdf
    try:
        cert = Certificate.objects.get(certificate_id=cert_id, student=request.user, is_valid=True)
    except Certificate.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)
    buffer = generate_certificate_pdf(cert)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate-{str(cert_id)[:8]}.pdf"'
    return response


# ── Contact ───────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def contact_view(request):
    name = request.data.get('name', '').strip()
    email = request.data.get('email', '').strip()
    phone = request.data.get('phone', '').strip()
    subject = request.data.get('subject', '').strip()
    message = request.data.get('message', '').strip()
    if not all([name, email, subject, message]):
        return Response({'error': 'All fields required.'}, status=400)
    ContactMessage.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)
    return Response({'message': 'Message sent successfully.'})


# ── Home data ─────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def home_data_view(request):
    from courses.models import Course
    return Response({
        'featured_courses': CourseSerializer(
            Course.objects.filter(is_featured=True, is_active=True)[:6], many=True).data,
        'featured_internships': InternshipSerializer(
            Internship.objects.filter(is_featured=True, is_active=True)[:4], many=True).data,
        'featured_projects': ProjectSerializer(
            Project.objects.filter(is_featured=True, is_active=True).select_related('domain')[:6], many=True).data,
        'project_domains': ProjectDomainSerializer(
            ProjectDomain.objects.filter(is_active=True), many=True).data,
        'testimonials': TestimonialSerializer(
            Testimonial.objects.filter(is_approved=True)[:6], many=True).data,
        'project_total': Project.objects.filter(is_active=True).count(),
    })
