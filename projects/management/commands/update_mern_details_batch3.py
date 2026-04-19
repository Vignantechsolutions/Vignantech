from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "online-movie-streaming-platform",
        "problem_statement": "Users require secure and scalable platforms to stream movies online, but traditional systems lack efficient content management and recommendation features.",
        "objectives": "Provide seamless online movie streaming\nManage user subscriptions and plans\nRecommend movies based on user preferences",
        "features": "Movie browsing\nVideo streaming\nUser subscriptions\nWatch history\nRecommendation system\nAdmin dashboard",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Redux, AWS S3",
        "algorithms": "Collaborative Filtering Recommendation Algorithm\nAdaptive Streaming Buffer Algorithm",
        "conclusion": "Improves content delivery and entertainment accessibility through personalized streaming and subscription management.",
        "future_enhancements": "Offline download support\nMulti-language subtitle support\nAI-based content tagging",
        "dataset": "Custom movie metadata and user viewing history dataset",
        "description": "Streams movies with user authentication, subscription plans, watch history, and AI-based recommendations on MERN stack.",
    },
    {
        "slug": "fitness-tracking-web-application",
        "problem_statement": "People struggle to monitor fitness activities and track health progress effectively without a centralized digital tool.",
        "objectives": "Track daily fitness activities\nMonitor health metrics and progress\nProvide actionable performance insights",
        "features": "Workout tracking\nHealth metrics monitoring\nProgress visualization\nGoal setting",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Redux, Chart.js",
        "algorithms": "Fitness Trend Analysis Algorithm\nGoal Progress Calculation",
        "conclusion": "Improves personal health monitoring and encourages a healthier lifestyle through data-driven insights.",
        "future_enhancements": "Wearable device sync (Fitbit, Apple Watch)\nAI-based workout recommendations\nNutrition tracking module",
        "dataset": "Custom workout and health metrics dataset",
        "description": "Tracks workouts, calories, and fitness goals with interactive Chart.js progress charts and goal reminders.",
    },
    {
        "slug": "donation-management-and-fundraising-platform",
        "problem_statement": "Charitable organizations struggle to track donations efficiently and maintain transparency with donors and stakeholders.",
        "objectives": "Manage and track donations digitally\nMaintain donor records and history\nEnsure full transparency in fund usage",
        "features": "Online donation system\nDonor management\nCampaign creation\nReporting dashboard",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Redux, Razorpay",
        "algorithms": "Payment Tracking Algorithm\nCampaign Progress Calculation",
        "conclusion": "Enhances charity operations by improving donation transparency and simplifying fund management.",
        "future_enhancements": "Recurring donation support\nTax receipt generation\nSocial media campaign sharing",
        "dataset": "Custom donor and campaign dataset",
        "description": "Enables NGOs and individuals to create fundraising campaigns and accept online donations with Razorpay integration.",
    },
    {
        "slug": "smart-blogging-and-content-management-system",
        "problem_statement": "Content creators need flexible and feature-rich platforms to publish, manage, and grow their blog content efficiently.",
        "objectives": "Enable seamless blog content publishing\nManage user posts and categories\nEnable reader interaction through comments",
        "features": "Blog creation with rich text editor\nComment system\nContent management\nSearch functionality",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Redux, AWS S3",
        "algorithms": "Full-Text Search Indexing Algorithm\nContent Ranking by Engagement",
        "conclusion": "Improves content publishing systems by providing creators with a powerful and flexible blogging platform.",
        "future_enhancements": "SEO optimization tools\nNewsletter subscription module\nMonetization via ads integration",
        "dataset": "Custom blog post and user interaction dataset",
        "description": "Full-featured CMS with rich text editor, categories, tags, comment system, and SEO management on MERN stack.",
    },
    {
        "slug": "online-quiz-and-assessment-platform",
        "problem_statement": "Educational institutions need digital tools to conduct assessments efficiently, replacing manual paper-based exams.",
        "objectives": "Conduct timed online quizzes and assessments\nEvaluate results automatically\nProvide detailed performance insights",
        "features": "Quiz creation\nTimer-based tests\nAuto evaluation and grading\nResult dashboard",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Socket.io, Redux",
        "algorithms": "Random Question Generator\nAuto-Grading Logic",
        "conclusion": "Improves digital education by automating assessment creation, delivery, and result evaluation.",
        "future_enhancements": "Anti-cheating proctoring module\nQuestion bank import from CSV\nCertificate generation on completion",
        "dataset": "Custom question bank and student response dataset",
        "description": "Creates and conducts timed quizzes with auto-grading, randomized questions, and performance analytics on MERN stack.",
    },
]


class Command(BaseCommand):
    help = 'Update MERN projects 56-60 with full detail content'

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
