from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Category, Course, CourseModule
from internships.models import Internship
from projects.models import Project
from accounts.models import Testimonial


class Command(BaseCommand):
    help = 'Load sample data for Vignan TechSolutions'

    def handle(self, *args, **kwargs):
        # Categories
        cat_web, _ = Category.objects.get_or_create(name='Web Development', defaults={'slug': 'web-development'})
        cat_py, _ = Category.objects.get_or_create(name='Python', defaults={'slug': 'python'})
        cat_ds, _ = Category.objects.get_or_create(name='Data Science', defaults={'slug': 'data-science'})

        # Courses
        courses_data = [
            {
                'title': 'Full Stack Web Development', 'slug': 'full-stack-web-development',
                'category': cat_web, 'instructor': 'Rajesh Kumar',
                'description': 'Master HTML, CSS, JavaScript, React, Node.js, and Django to build complete web applications from scratch.',
                'duration': '6 Months', 'fees': 15000, 'level': 'beginner', 'is_featured': True,
            },
            {
                'title': 'Python for Data Science', 'slug': 'python-data-science',
                'category': cat_ds, 'instructor': 'Priya Sharma',
                'description': 'Learn Python, Pandas, NumPy, Matplotlib, Scikit-learn and build real data science projects.',
                'duration': '4 Months', 'fees': 12000, 'level': 'intermediate', 'is_featured': True,
            },
            {
                'title': 'Django Backend Development', 'slug': 'django-backend-development',
                'category': cat_py, 'instructor': 'Anil Reddy',
                'description': 'Build scalable backend APIs and web applications using Django and Django REST Framework.',
                'duration': '3 Months', 'fees': 10000, 'level': 'intermediate', 'is_featured': True,
            },
        ]

        for data in courses_data:
            course, created = Course.objects.get_or_create(slug=data['slug'], defaults=data)
            if created:
                CourseModule.objects.create(course=course, title='Introduction & Setup', order=1, duration='1 Week')
                CourseModule.objects.create(course=course, title='Core Concepts', order=2, duration='2 Weeks')
                CourseModule.objects.create(course=course, title='Advanced Topics', order=3, duration='3 Weeks')
                CourseModule.objects.create(course=course, title='Project Work', order=4, duration='2 Weeks')
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))

        # Internships
        internships_data = [
            {
                'title': 'Web Development Internship', 'slug': 'web-development-internship',
                'description': 'Work on real client projects using HTML, CSS, JavaScript, and Django. Build a complete portfolio.',
                'duration': '3 Months', 'fees': 5000, 'mode': 'hybrid', 'is_featured': True,
                'seats_available': 20,
                'topics_covered': 'HTML5 & CSS3\nJavaScript ES6+\nBootstrap 5\nDjango Framework\nMySQL Database\nGit & GitHub\nDeployment',
                'benefits': 'Industry experience certificate\nLetter of recommendation\nPortfolio projects\nPlacement assistance\nMentor support',
                'certificate_info': 'Upon successful completion, students receive an industry-recognized certificate from Vignan TechSolutions, valid for job applications and higher studies.',
            },
            {
                'title': 'Python & Machine Learning Internship', 'slug': 'python-ml-internship',
                'description': 'Hands-on internship covering Python programming, data analysis, and machine learning model building.',
                'duration': '2 Months', 'fees': 4000, 'mode': 'online', 'is_featured': True,
                'seats_available': 15,
                'topics_covered': 'Python Programming\nNumPy & Pandas\nData Visualization\nMachine Learning Basics\nScikit-learn\nProject Implementation',
                'benefits': 'Completion certificate\nReal dataset projects\nMentor guidance\nJob referrals\nLinkedIn recommendation',
                'certificate_info': 'Certificate issued after completing all modules and submitting the final project. Verified online via our portal.',
            },
            {
                'title': 'Android App Development Internship', 'slug': 'android-internship',
                'description': 'Build real Android applications using Java/Kotlin. Learn UI design, APIs, and app deployment.',
                'duration': '2 Months', 'fees': 4500, 'mode': 'online', 'is_featured': True,
                'seats_available': 10,
                'topics_covered': 'Java/Kotlin Basics\nAndroid Studio\nUI/UX Design\nREST API Integration\nFirebase\nApp Deployment',
                'benefits': 'Published app on Play Store\nCompletion certificate\nPortfolio project\nPlacement support',
                'certificate_info': 'Certificate awarded upon app submission and code review by our technical team.',
            },
        ]

        for data in internships_data:
            _, created = Internship.objects.get_or_create(slug=data['slug'], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created internship: {data['title']}"))

        # Projects
        projects_data = [
            {
                'title': 'E-Commerce Platform', 'slug': 'ecommerce-platform',
                'description': 'A full-featured e-commerce platform with product management, cart, payments, and order tracking.',
                'tech_stack': 'Django Python MySQL Bootstrap Razorpay',
                'category': 'web', 'is_featured': True,
            },
            {
                'title': 'Student Management System', 'slug': 'student-management-system',
                'description': 'Complete student management system for colleges with attendance, marks, and fee management.',
                'tech_stack': 'Django Python MySQL JavaScript Bootstrap',
                'category': 'web', 'is_featured': True,
            },
            {
                'title': 'Sales Prediction ML Model', 'slug': 'sales-prediction-ml',
                'description': 'Machine learning model to predict sales using historical data with 92% accuracy.',
                'tech_stack': 'Python Scikit-learn Pandas NumPy Matplotlib',
                'category': 'ml', 'is_featured': True,
            },
        ]

        for data in projects_data:
            _, created = Project.objects.get_or_create(slug=data['slug'], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created project: {data['title']}"))

        # Testimonials
        testimonials_data = [
            {'name': 'Arjun Mehta', 'designation': 'Software Engineer', 'company': 'TCS',
             'message': 'The internship at Vignan TechSolutions was a game-changer for me. The hands-on projects and mentorship helped me land my dream job at TCS.', 'rating': 5},
            {'name': 'Sneha Patel', 'designation': 'Data Analyst', 'company': 'Infosys',
             'message': 'Excellent training quality! The Python and Data Science course was very practical and industry-relevant. Highly recommend to all students.', 'rating': 5},
            {'name': 'Kiran Reddy', 'designation': 'Full Stack Developer', 'company': 'Wipro',
             'message': 'The Full Stack course covered everything from basics to deployment. The instructors are very knowledgeable and supportive.', 'rating': 5},
        ]

        for data in testimonials_data:
            _, created = Testimonial.objects.get_or_create(name=data['name'], defaults={**data, 'is_active': True})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created testimonial: {data['name']}"))

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
        self.stdout.write('Next: python manage.py createsuperuser')
