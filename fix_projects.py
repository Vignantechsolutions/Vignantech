import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vignan_tech.settings'
django.setup()

from projects.models import Project, ProjectDomain

aiml       = ProjectDomain.objects.get(slug='aiml')
python     = ProjectDomain.objects.get(slug='python')
mern       = ProjectDomain.objects.get(slug='mern')
java       = ProjectDomain.objects.get(slug='java')
datascience= ProjectDomain.objects.get(slug='datascience')

# Map: project title keywords → domain
DOMAIN_MAP = {
    # AI & ML
    'Deep Learning': aiml,
    'Machine Learning': aiml,
    'Neural Network': aiml,
    'YOLO': aiml,
    'CNN': aiml,
    'LSTM': aiml,
    'NLP': aiml,
    'Natural Language': aiml,
    'Emotion Detection': aiml,
    'Fake News': aiml,
    'Chatbot': aiml,
    'Voice Assistant': aiml,
    'Traffic Sign': aiml,
    'Handwritten Digit': aiml,
    'Object Detection': aiml,
    'Image Caption': aiml,
    'Text Summarization': aiml,
    'Fake Social Media': aiml,
    'Recommendation System Using Machine Learning': aiml,
    'Stock Price Prediction Using LSTM': aiml,
    'AI-Based Customer Support': aiml,
    'AI Resume Screening and Candidate': aiml,
    'Intelligent Plant Disease': aiml,
    'AI-Based Multi-Disease': aiml,
    'AI-Based Voice': aiml,

    # Data Science
    'Stock Market Trend': datascience,
    'Customer Segmentation': datascience,
    'Disease Prediction Using Patient Health Records': datascience,
    'Traffic Accident Analysis': datascience,
    'Employee Attrition': datascience,
    'Weather Prediction': datascience,
    'Energy Consumption': datascience,
    'Loan Approval': datascience,
    'Sentiment Analysis': datascience,
    'House Price Prediction': datascience,
    'Movie Recommendation System Using Collaborative': datascience,
    'Credit Card Fraud': datascience,
    'Student Academic Performance': datascience,
    'Retail Sales Forecasting': datascience,
    'Customer Churn': datascience,

    # Python Full Stack
    'Online Quiz': python,
    'Blogging': python,
    'Donation Management': python,
    'Fitness Tracking': python,
    'Flask': python,
    'Secure Online Voting': python,
    'Plant Disease Detection Web': python,
    'Food Delivery Time Prediction': python,
    'Vehicle Rental': python,
    'Customer Complaint': python,
    'Travel and Tourism': python,
    'Smart Library': python,
    'Employee Payroll': python,
    'Online Examination': python,
    'Online Food Ordering': python,
    'Face Recognition Attendance': python,
    'E-Commerce Product Management': python,
    'Online Job Portal': python,
    'Smart Expense Tracker and Budget': python,
    'Real Estate Price Prediction Web': python,
    'AI Chatbot Web': python,
    'Online Shopping Fraud': python,
    'Student Performance Prediction Portal': python,
    'Smart Agriculture Advisory': python,
    'Multi-Disease Prediction Web Portal': python,
    'AI Resume Screening Web': python,
    'Online Book Recommendation Web': python,
    'Automatic Document Classification': python,
    'AI Image Caption Generator Web': python,
    'Secure File Sharing': python,

    # MERN Stack
    'Online Movie Streaming': mern,
    'Task Management and Collaboration': mern,
    'Smart Real Estate Listing': mern,
    'Online Event Booking': mern,
    'Hospital Management Portal Using MERN': mern,
    'Multi-Vendor Marketplace': mern,
    'Expense Tracker with Data Visualization': mern,
    'Online Learning Management Platform': mern,
    'Real-Time Chat Application with Video': mern,
    'AI-Powered Job Portal': mern,
    'Smart E-Commerce Platform': mern,

    # Java Full Stack
    'Real-Time Chat Application Using WebSockets': java,
    'Inventory Management System Using Spring Boot': java,
    'Secure Online Banking': java,
    'Smart Hospital Management System': java,
    'Enterprise Learning Management System Using Spring Boot': java,
}

updated = 0
skipped = []

for project in Project.objects.all():
    assigned = False
    for keyword, domain in DOMAIN_MAP.items():
        if keyword.lower() in project.title.lower():
            project.domain = domain
            project.save()
            updated += 1
            assigned = True
            break
    if not assigned:
        skipped.append(project.title)

print(f"Updated: {updated}")
if skipped:
    print(f"Skipped ({len(skipped)}):")
    for t in skipped:
        print(" -", t)
