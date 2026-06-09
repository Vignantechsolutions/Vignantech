from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import StudentProfile, Testimonial
from courses.models import Course, CourseModule, Category
from internships.models import Internship
from projects.models import Project, ProjectDomain
from payments.models import Enrollment, Payment
from certificates.models import Certificate, CustomCertificate


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class CourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModule
        fields = ['id', 'title', 'description', 'order', 'duration']


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'category', 'description',
            'instructor', 'instructor_bio', 'thumbnail', 'duration',
            'fees', 'level', 'level_display', 'is_featured', 'created_at',
        ]


class CourseDetailSerializer(CourseSerializer):
    modules = CourseModuleSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['modules', 'instructor_photo']


class InternshipSerializer(serializers.ModelSerializer):
    mode_display = serializers.CharField(source='get_mode_display', read_only=True)
    topics_list = serializers.ListField(source='get_topics_list', read_only=True)
    benefits_list = serializers.ListField(source='get_benefits_list', read_only=True)

    class Meta:
        model = Internship
        fields = [
            'id', 'title', 'slug', 'description', 'duration', 'fees',
            'mode', 'mode_display', 'thumbnail', 'seats_available',
            'is_featured', 'start_date', 'topics_list', 'benefits_list',
            'certificate_info', 'created_at',
        ]


class ProjectDomainSerializer(serializers.ModelSerializer):
    gradient = serializers.CharField(read_only=True)

    class Meta:
        model = ProjectDomain
        fields = [
            'id', 'name', 'slug', 'emoji', 'color_from', 'color_to',
            'badge_bg', 'badge_color', 'description', 'gradient',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    domain = ProjectDomainSerializer(read_only=True)
    tech_stack_list = serializers.SerializerMethodField()

    def get_tech_stack_list(self, obj):
        return [t.strip() for t in obj.tech_stack.split(',') if t.strip()]

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'domain', 'description',
            'problem_statement', 'objectives', 'tech_stack', 'tech_stack_list',
            'features', 'algorithms', 'dataset', 'conclusion',
            'future_enhancements', 'thumbnail', 'live_url', 'github_url',
            'is_featured', 'created_at',
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'designation', 'company', 'message', 'photo', 'rating']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_staff']


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'user', 'phone', 'college', 'course_of_study',
            'year_of_study', 'profile_photo', 'bio',
            'linkedin_url', 'github_url',
        ]


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField(min_length=8)

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('Email already registered.')
        return value.lower()


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    internship = InternshipSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'enrollment_type', 'course', 'internship', 'status', 'enrolled_at']


class PaymentSerializer(serializers.ModelSerializer):
    enrollment = EnrollmentSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'enrollment', 'razorpay_order_id', 'amount', 'currency', 'status', 'created_at']


class CertificateSerializer(serializers.ModelSerializer):
    enrollment = EnrollmentSerializer(read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'certificate_id', 'enrollment', 'issued_date', 'is_valid']
