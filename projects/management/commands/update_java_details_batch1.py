from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "enterprise-learning-management-system-using-spring",
        "problem_statement": "Educational institutions face challenges managing courses, student data, and assessments manually, leading to inefficiencies and errors.",
        "objectives": "Provide a centralized education platform\nManage student and faculty records\nConduct online learning and assessments\nImprove academic performance tracking",
        "features": "Student and faculty login\nCourse management\nAssignment submission\nQuiz and exam system\nGrade tracking\nAdmin dashboard",
        "tech_stack": "Java, Spring Boot, Hibernate, React.js, HTML, CSS, MySQL, Maven, Git",
        "algorithms": "Authentication Algorithm\nCourse Recommendation Algorithm",
        "conclusion": "Improves digital learning and academic management through a centralized, efficient platform.",
        "future_enhancements": "Live video lecture integration\nMobile app support\nAI-based performance analytics",
        "dataset": "Custom academic records dataset",
        "description": "A full-featured LMS with course management, student enrollment, and progress tracking built on Spring Boot and React.js.",
    },
    {
        "slug": "smart-hospital-management-system",
        "problem_statement": "Hospitals struggle to manage patient data, appointments, and billing manually, causing delays and errors in healthcare delivery.",
        "objectives": "Digitize hospital operations\nManage patient records efficiently\nImprove doctor scheduling and appointment management",
        "features": "Patient registration\nDoctor scheduling\nBilling system\nPrescription management",
        "tech_stack": "Java, Spring Boot, Hibernate, Angular, MySQL",
        "algorithms": "Scheduling Algorithm\nBilling Calculation Logic",
        "conclusion": "Improves healthcare service management by digitizing and centralizing hospital operations.",
        "future_enhancements": "Telemedicine module\nLab report integration\nInsurance claim automation",
        "dataset": "Custom hospital records dataset",
        "description": "Manages patient records, doctor schedules, appointments, and billing in a hospital environment using Spring Boot.",
    },
    {
        "slug": "secure-online-banking-system",
        "problem_statement": "Manual banking processes increase transaction delays and risk of errors, while lacking the security required for modern financial operations.",
        "objectives": "Provide secure online transactions\nManage user accounts digitally\nImprove overall banking efficiency",
        "features": "User login and authentication\nFund transfer\nAccount balance inquiry\nTransaction history",
        "tech_stack": "Java, Spring Boot, Spring Security, React.js, MySQL",
        "algorithms": "AES Encryption Algorithm\nJWT Authentication",
        "conclusion": "Enhances digital banking operations with secure, fast, and reliable transaction management.",
        "future_enhancements": "Two-factor authentication\nFraud detection module\nMobile banking app",
        "dataset": "Synthetic banking transaction dataset",
        "description": "Provides secure account management, fund transfers, and transaction history with role-based access using Spring Security.",
    },
    {
        "slug": "inventory-management-system-using-spring-boot",
        "problem_statement": "Businesses struggle to track product stock manually, leading to stock shortages, overstocking, and supply chain inefficiencies.",
        "objectives": "Monitor inventory levels in real time\nTrack product stock movements\nReduce stock shortages and overstocking",
        "features": "Product management\nInventory tracking\nLow-stock alerts\nSupplier management",
        "tech_stack": "Java, Spring Boot, Hibernate, Angular, MySQL",
        "algorithms": "Inventory Optimization Algorithm\nReorder Point Calculation",
        "conclusion": "Improves supply chain efficiency by automating inventory tracking and alerting.",
        "future_enhancements": "Barcode and QR code scanning\nSupplier portal integration\nDemand forecasting with ML",
        "dataset": "Custom product and stock dataset",
        "description": "Tracks stock levels, purchase orders, and supplier details with real-time inventory alerts using Spring Boot.",
    },
    {
        "slug": "online-job-portal-with-resume-upload",
        "problem_statement": "Job seekers face difficulties finding suitable jobs efficiently, while recruiters struggle to manage large volumes of applications.",
        "objectives": "Connect job seekers and recruiters on one platform\nManage job postings and applications\nImprove the overall recruitment process",
        "features": "Resume upload\nJob search and filtering\nApplication tracking\nRecruiter dashboard",
        "tech_stack": "Java, Spring Boot, Hibernate, React.js, MySQL",
        "algorithms": "Resume-Job Matching Algorithm\nKeyword Extraction",
        "conclusion": "Improves job matching efficiency by connecting candidates and employers through an intelligent portal.",
        "future_enhancements": "AI-based resume ranking\nVideo interview integration\nLinkedIn profile import",
        "dataset": "Custom job listings and resume dataset",
        "description": "Connects job seekers and employers with resume upload, job posting, and application tracking using Spring Boot.",
    },
]


class Command(BaseCommand):
    help = 'Update Java projects 16-20 with full detail content'

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
