from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "smart-e-commerce-platform-with-recommendation-engi",
        "problem_statement": "Online stores struggle to recommend relevant products to users, leading to reduced engagement and lower sales conversion rates.",
        "objectives": "Build a scalable e-commerce platform\nRecommend personalized products to users\nImprove customer shopping experience\nIncrease sales conversion",
        "features": "User registration and login\nProduct catalog\nShopping cart\nOrder management\nRecommendation system\nPayment gateway\nAdmin dashboard",
        "tech_stack": "React.js, Redux, Node.js, Express.js, MongoDB, Python Recommendation API, Razorpay",
        "algorithms": "Collaborative Filtering\nContent-Based Filtering",
        "conclusion": "Enhances online shopping through intelligent product recommendations and a seamless user experience.",
        "future_enhancements": "AI-based dynamic pricing\nAR product preview\nMulti-vendor marketplace extension",
        "dataset": "Custom product and user behavior dataset",
        "description": "Full-stack e-commerce site with AI-powered product recommendations, cart management, and Razorpay payment integration.",
    },
    {
        "slug": "ai-powered-job-portal-with-resume-matching",
        "problem_statement": "Job seekers struggle to find relevant jobs efficiently while recruiters face difficulty shortlisting suitable candidates from large applicant pools.",
        "objectives": "Match resumes with job postings using AI\nAutomate the recruitment screening process\nImprove overall hiring efficiency",
        "features": "Resume upload\nJob posting management\nAI-based job matching\nApplication tracking",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Python NLP API, SpaCy",
        "algorithms": "Cosine Similarity\nTF-IDF Vectorization",
        "conclusion": "Improves job recruitment processes by intelligently matching candidates to relevant job postings.",
        "future_enhancements": "Video interview integration\nLinkedIn profile import\nAI-based candidate ranking dashboard",
        "dataset": "Custom resume and job description dataset",
        "description": "Job portal that matches candidates to job listings using NLP-based resume analysis and cosine similarity scoring.",
    },
    {
        "slug": "real-time-chat-application-with-video-calling",
        "problem_statement": "Modern communication requires real-time messaging and video interaction that traditional HTTP-based systems cannot support efficiently.",
        "objectives": "Enable real-time bidirectional chat messaging\nProvide integrated video calling\nSupport group communication channels",
        "features": "Real-time messaging\nVideo calls\nFile sharing\nPush notifications",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Socket.io, WebRTC",
        "algorithms": "WebSocket Real-Time Communication Protocol\nWebRTC Peer-to-Peer Connection",
        "conclusion": "Improves digital communication by combining real-time messaging and video calling in a single platform.",
        "future_enhancements": "End-to-end encryption\nScreen sharing support\nMobile app deployment",
        "dataset": "Custom chat message dataset",
        "description": "Supports real-time text chat and video calling using WebRTC and Socket.io on a MERN stack platform.",
    },
    {
        "slug": "online-learning-management-platform",
        "problem_statement": "Educational platforms require scalable systems to manage courses, students, and content delivery efficiently.",
        "objectives": "Provide a digital learning platform\nTrack student performance and progress\nManage courses and content",
        "features": "Course enrollment\nVideo content delivery\nAssignment submission\nStudent dashboard",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Redux, AWS S3",
        "algorithms": "Course Recommendation Algorithm\nProgress Tracking Logic",
        "conclusion": "Improves digital education accessibility and course management for students and instructors.",
        "future_enhancements": "Live class streaming\nAI-based learning path suggestions\nCertificate generation",
        "dataset": "Custom course and student dataset",
        "description": "Platform for course creation, video lectures, assignments, and student progress tracking built on MERN stack.",
    },
    {
        "slug": "expense-tracker-with-data-visualization-dashboard",
        "problem_statement": "People struggle to manage expenses and understand their spending habits, leading to poor financial planning.",
        "objectives": "Track daily income and expenses\nVisualize spending patterns with charts\nImprove personal financial planning",
        "features": "Expense logging\nInteractive graph visualization\nBudget alerts",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Redux, Chart.js",
        "algorithms": "Data Aggregation Algorithm\nBudget Threshold Detection",
        "conclusion": "Enhances financial tracking and awareness through interactive dashboards and budget alerts.",
        "future_enhancements": "Bank account sync via Plaid API\nAI-based savings recommendations\nMobile app support",
        "dataset": "Custom personal expense dataset",
        "description": "Tracks income and expenses with interactive Chart.js visualizations and budget analytics on a MERN stack.",
    },
]


class Command(BaseCommand):
    help = 'Update MERN projects 46-50 with full detail content'

    def handle(self, *args, **kwargs):
        updated = 0
        for data in DETAILS:
            slug = data.pop("slug")
            try:
                project = Project.objects.get(slug=slug)
                for field, value in data.items():
                    setattr(project, field, value)
                project.save()
                updated += 1
                self.stdout.write(f'  Updated: {project.title}')
            except Project.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Not found: {slug}'))
        self.stdout.write(self.style.SUCCESS(f'Done. Updated {updated} projects.'))
