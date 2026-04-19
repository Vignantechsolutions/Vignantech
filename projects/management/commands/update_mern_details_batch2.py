from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "multi-vendor-marketplace-system",
        "problem_statement": "Small businesses and individual vendors lack access to scalable platforms that allow them to sell products online efficiently. Managing multiple sellers manually is difficult and error-prone.",
        "objectives": "Create a multi-vendor marketplace platform\nAllow vendors to list and manage products\nManage orders from multiple sellers\nProvide secure payment handling",
        "features": "Vendor registration and login\nProduct listing management\nShopping cart system\nOrder management\nPayment gateway\nAdmin dashboard\nVendor performance analytics",
        "tech_stack": "React.js, Redux, Bootstrap, Node.js, Express.js, MongoDB, Razorpay",
        "algorithms": "Product Recommendation Algorithm\nSorting Algorithm (Price, Popularity, Rating)",
        "conclusion": "Multi-vendor platforms enable scalable digital marketplaces and expand vendor reach to a wider customer base.",
        "future_enhancements": "Vendor mobile app\nAI-based product recommendations\nMulti-currency and multi-language support",
        "dataset": "Custom vendor and product dataset",
        "description": "Marketplace where multiple vendors can list products, manage their storefronts, and process orders with Razorpay integration.",
    },
    {
        "slug": "hospital-management-portal-using-mern",
        "problem_statement": "Hospitals struggle with managing patient records, doctor appointments, and medical reports manually, causing delays and errors in patient care.",
        "objectives": "Digitize hospital operations end-to-end\nStore patient records securely\nAutomate appointment booking and scheduling",
        "features": "Patient registration\nDoctor scheduling\nMedical records storage\nPrescription tracking\nAppointment booking\nBilling management",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, JWT",
        "algorithms": "Doctor Scheduling Algorithm\nAppointment Slot Optimization",
        "conclusion": "Digitized hospital systems improve patient care quality and administrative efficiency.",
        "future_enhancements": "Telemedicine video consultation\nLab report integration\nInsurance claim automation",
        "dataset": "Custom hospital patient and appointment dataset",
        "description": "Manages patient records, doctor appointments, prescriptions, and billing in a hospital environment using MERN stack.",
    },
    {
        "slug": "online-event-booking-and-management-system",
        "problem_statement": "Event organizers face difficulty managing registrations, ticket bookings, and participant tracking manually, leading to errors and poor attendee experience.",
        "objectives": "Manage event registrations digitally\nEnable seamless online ticket booking\nTrack participants and event analytics",
        "features": "Event creation\nTicket booking\nPayment integration\nPush notifications\nEvent analytics dashboard",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Razorpay",
        "algorithms": "Seat Booking Optimization Algorithm\nEvent Capacity Management Logic",
        "conclusion": "Improves event registration and participant management through a seamless digital booking experience.",
        "future_enhancements": "QR code ticket generation\nLive event streaming integration\nSponsor management module",
        "dataset": "Custom event and booking dataset",
        "description": "Allows users to discover, book, and manage event tickets with organizer dashboards and Razorpay payment integration.",
    },
    {
        "slug": "smart-real-estate-listing-platform",
        "problem_statement": "Property buyers face difficulty finding reliable property listings efficiently due to fragmented and unverified information across platforms.",
        "objectives": "Provide searchable and filterable property listings\nEnable location-based property search\nImprove property discovery and transparency",
        "features": "Property listing\nAdvanced search filters\nLocation-based search\nContact property owners\nAdmin approval system",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Redux, Google Maps API",
        "algorithms": "Search Optimization Algorithm\nLocation-Based Filtering",
        "conclusion": "Improves accessibility to property information and enhances transparency in the real estate market.",
        "future_enhancements": "Virtual property tour (360°)\nMortgage calculator\nAI-based price estimation",
        "dataset": "Custom property listing dataset",
        "description": "Property listing platform with advanced search filters, map integration, and agent contact using MERN stack.",
    },
    {
        "slug": "task-management-and-collaboration-system",
        "problem_statement": "Teams struggle to manage projects and tasks manually, leading to missed deadlines, poor coordination, and reduced productivity.",
        "objectives": "Assign and track tasks across team members\nMonitor project progress in real time\nImprove team collaboration and communication",
        "features": "Task creation and assignment\nDeadline tracking\nProgress dashboard\nNotification alerts",
        "tech_stack": "React.js, Node.js, Express.js, MongoDB, Socket.io, JWT, Redux",
        "algorithms": "Task Scheduling Algorithm\nPriority-Based Assignment Logic",
        "conclusion": "Improves workflow management and team productivity through structured task tracking and real-time collaboration.",
        "future_enhancements": "Gantt chart view\nTime tracking module\nSlack and email notification integration",
        "dataset": "Custom project and task dataset",
        "description": "Team task board with drag-and-drop task management, assignments, deadlines, and real-time updates using MERN stack.",
    },
]


class Command(BaseCommand):
    help = 'Update MERN projects 51-55 with full detail content'

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
