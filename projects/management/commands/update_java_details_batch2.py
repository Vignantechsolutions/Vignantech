from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    # Projects 21-25 (auto-filled)
    {
        "slug": "e-commerce-product-management-system",
        "problem_statement": "Businesses lack an efficient platform to manage product listings, customer orders, and payments, resulting in poor customer experience and revenue loss.",
        "objectives": "Build a full-stack e-commerce platform\nManage product catalog and inventory\nHandle orders and payment processing",
        "features": "Product catalog\nShopping cart\nOrder management\nPayment integration\nAdmin dashboard",
        "tech_stack": "Java, Spring Boot, Hibernate, Thymeleaf, MySQL, Bootstrap",
        "algorithms": "Cart Total Calculation Algorithm\nOrder Status Workflow",
        "conclusion": "Provides a complete e-commerce solution that improves product management and customer shopping experience.",
        "future_enhancements": "AI-based product recommendations\nMobile app support\nMulti-vendor marketplace extension",
        "dataset": "Custom product and order dataset",
        "description": "Full-stack e-commerce platform with product catalog, cart, orders, and payment integration built on Spring Boot.",
    },
    {
        "slug": "face-recognition-attendance-management-system",
        "problem_statement": "Manual attendance systems are time-consuming and prone to proxy attendance, leading to inaccurate records.",
        "objectives": "Automate attendance using facial recognition\nEliminate proxy attendance\nGenerate accurate attendance reports",
        "features": "Face registration\nReal-time face detection\nAttendance marking\nReport generation",
        "tech_stack": "Java, Spring Boot, Python, OpenCV, MySQL, Bootstrap",
        "algorithms": "Haar Cascade Face Detection\nFace Encoding and Matching",
        "conclusion": "Eliminates manual attendance errors and proxy attendance through automated facial recognition.",
        "future_enhancements": "Multi-camera support\nMobile check-in\nIntegration with HR systems",
        "dataset": "Custom employee/student face image dataset",
        "description": "Automates attendance marking using facial recognition integrated with a Spring Boot backend.",
    },
    {
        "slug": "online-food-ordering-system",
        "problem_statement": "Restaurants lack an efficient digital platform for customers to browse menus, place orders, and track deliveries in real time.",
        "objectives": "Enable online food ordering\nManage restaurant menus and orders\nProvide real-time delivery tracking",
        "features": "Menu browsing\nCart and order placement\nDelivery tracking\nPayment integration\nAdmin order dashboard",
        "tech_stack": "Java, Spring Boot, Hibernate, Thymeleaf, MySQL, Bootstrap",
        "algorithms": "Order Queue Management Algorithm\nDelivery Time Estimation",
        "conclusion": "Improves restaurant operations and customer experience through a seamless digital ordering platform.",
        "future_enhancements": "Real-time GPS delivery tracking\nLoyalty rewards system\nMulti-restaurant support",
        "dataset": "Custom menu and order dataset",
        "description": "Allows customers to browse menus, place orders, and track delivery status in real time using Spring Boot.",
    },
    {
        "slug": "real-time-chat-application-using-websockets",
        "problem_statement": "Traditional HTTP-based communication cannot support real-time messaging, causing delays and poor user experience in chat applications.",
        "objectives": "Enable real-time bidirectional messaging\nSupport group and private chats\nEnsure message delivery reliability",
        "features": "Real-time messaging\nGroup chat rooms\nPrivate messaging\nOnline status indicator\nMessage history",
        "tech_stack": "Java, Spring Boot, WebSocket, STOMP, MySQL, Bootstrap",
        "algorithms": "WebSocket Handshake Protocol\nMessage Routing Algorithm",
        "conclusion": "Delivers a reliable real-time communication platform using WebSocket technology.",
        "future_enhancements": "File and media sharing\nEnd-to-end encryption\nMobile app integration",
        "dataset": "Custom chat message dataset",
        "description": "Enables real-time messaging between users using WebSocket protocol and Spring Boot with STOMP messaging.",
    },
    {
        "slug": "online-examination-management-system",
        "problem_statement": "Conducting exams manually is resource-intensive and prone to errors in question distribution, timing, and result calculation.",
        "objectives": "Automate exam creation and scheduling\nConduct timed online examinations\nGenerate results automatically",
        "features": "Exam creation\nTimed question paper\nAuto-grading\nResult dashboard\nStudent performance reports",
        "tech_stack": "Java, Spring Boot, Hibernate, Thymeleaf, MySQL, Bootstrap",
        "algorithms": "Random Question Selection Algorithm\nAuto-Grading Logic",
        "conclusion": "Automates the entire examination lifecycle from creation to result generation, reducing manual effort.",
        "future_enhancements": "Anti-cheating proctoring module\nQuestion bank import\nCertificate generation",
        "dataset": "Custom question bank dataset",
        "description": "Manages exam creation, scheduling, student attempts, and automated result generation using Spring Boot.",
    },
    # Projects 26-30 (user provided)
    {
        "slug": "employee-payroll-management-system",
        "problem_statement": "Organizations face difficulties calculating salaries, managing employee records, and generating payroll reports manually, which leads to calculation errors and delays.",
        "objectives": "Automate salary calculation\nManage employee records\nGenerate payslips automatically\nImprove payroll accuracy",
        "features": "Employee registration\nSalary calculation\nLeave tracking\nTax calculation\nPayslip generation\nAdmin dashboard",
        "tech_stack": "Java, Spring Boot, Hibernate, JSP, React.js, MySQL",
        "algorithms": "Payroll Calculation Algorithm\nTax Deduction Formula",
        "conclusion": "Automates salary processing and improves financial accuracy across HR departments.",
        "future_enhancements": "Automated tax filing integration\nEmployee self-service portal\nMulti-currency payroll support",
        "dataset": "Custom employee salary and HR dataset",
        "description": "Automates salary calculation, payslip generation, and tax deductions for employees using Spring Boot.",
    },
    {
        "slug": "smart-library-management-system",
        "problem_statement": "Libraries face challenges managing book records and user transactions manually, leading to misplaced books and untracked fines.",
        "objectives": "Manage book inventory digitally\nTrack book issue and return\nCalculate fines automatically",
        "features": "Book catalog\nIssue and return system\nFine calculation\nUser management",
        "tech_stack": "Java, Spring Boot, Hibernate, React.js, MySQL",
        "algorithms": "Binary Search Algorithm\nFine Calculation Logic",
        "conclusion": "Improves library resource management by digitizing book tracking and fine collection.",
        "future_enhancements": "QR code-based book scanning\nOnline book reservation\nDigital e-book integration",
        "dataset": "Custom library book and member dataset",
        "description": "Handles book cataloging, member management, issue/return tracking, and fine calculation using Spring Boot.",
    },
    {
        "slug": "travel-and-tourism-booking-system",
        "problem_statement": "Travel agencies face difficulties managing bookings, tour packages, and customer records manually, causing errors and poor customer experience.",
        "objectives": "Manage travel packages digitally\nTrack reservations and bookings\nProvide seamless online booking",
        "features": "Tour package management\nBooking system\nPayment integration\nCustomer management",
        "tech_stack": "Java, Spring Boot, Hibernate, Angular, MySQL",
        "algorithms": "Booking Optimization Algorithm\nAvailability Check Logic",
        "conclusion": "Improves booking efficiency and customer service for travel agencies through digital management.",
        "future_enhancements": "Third-party hotel and flight API integration\nMulti-language support\nMobile booking app",
        "dataset": "Custom travel package and booking dataset",
        "description": "Allows users to search, book, and manage travel packages, hotels, and transport using Spring Boot.",
    },
    {
        "slug": "customer-complaint-management-system",
        "problem_statement": "Organizations struggle to track and resolve customer complaints manually, leading to poor customer satisfaction and unresolved issues.",
        "objectives": "Register and track customer complaints\nMonitor complaint resolution status\nImprove overall customer satisfaction",
        "features": "Complaint submission\nStatus tracking\nResolution dashboard",
        "tech_stack": "Java, Spring Boot, Hibernate, React.js, MySQL",
        "algorithms": "Priority Assignment Algorithm\nEscalation Workflow Logic",
        "conclusion": "Improves complaint handling efficiency and customer satisfaction through structured tracking.",
        "future_enhancements": "Email and SMS notification alerts\nSentiment analysis on complaints\nSLA breach detection",
        "dataset": "Custom complaint and resolution dataset",
        "description": "Tracks customer complaints, assigns them to agents, and monitors resolution status using Spring Boot.",
    },
    {
        "slug": "vehicle-rental-management-system",
        "problem_statement": "Vehicle rental services face difficulties managing bookings and vehicle availability manually, causing double bookings and billing errors.",
        "objectives": "Track vehicle availability in real time\nManage rental bookings efficiently\nAutomate billing and invoicing",
        "features": "Vehicle booking\nRental tracking\nPayment system\nCustomer records",
        "tech_stack": "Java, Spring Boot, Hibernate, React.js, MySQL",
        "algorithms": "Vehicle Scheduling Algorithm\nRental Billing Calculation",
        "conclusion": "Enhances rental management efficiency by automating bookings, availability tracking, and billing.",
        "future_enhancements": "GPS vehicle tracking integration\nMobile booking app\nDamage assessment module",
        "dataset": "Custom vehicle and rental booking dataset",
        "description": "Manages vehicle listings, bookings, availability, and rental billing for a rental business using Spring Boot.",
    },
]


class Command(BaseCommand):
    help = 'Update Java projects 21-30 with full detail content'

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
