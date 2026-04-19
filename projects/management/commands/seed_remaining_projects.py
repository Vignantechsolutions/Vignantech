from django.core.management.base import BaseCommand
from django.utils.text import slugify
from projects.models import Project

PROJECTS = [
    # Java Full Stack
    ("Enterprise Learning Management System Using Spring Boot", "A full-featured LMS with course management, student enrollment, and progress tracking built on Spring Boot.", "Java, Spring Boot, Spring MVC, Hibernate, MySQL, Thymeleaf, Bootstrap", "java"),
    ("Smart Hospital Management System", "Manages patient records, doctor schedules, appointments, and billing in a hospital environment.", "Java, Spring Boot, Hibernate, MySQL, JSP, Bootstrap", "java"),
    ("Secure Online Banking System", "Provides secure account management, fund transfers, and transaction history with role-based access.", "Java, Spring Boot, Spring Security, Hibernate, MySQL, Thymeleaf", "java"),
    ("Inventory Management System Using Spring Boot", "Tracks stock levels, purchase orders, and supplier details with real-time inventory alerts.", "Java, Spring Boot, Hibernate, MySQL, Bootstrap, Thymeleaf", "java"),
    ("Online Job Portal with Resume Upload", "Connects job seekers and employers with resume upload, job posting, and application tracking.", "Java, Spring Boot, Hibernate, MySQL, JSP, Bootstrap", "java"),
    ("E-Commerce Product Management System", "Full-stack e-commerce platform with product catalog, cart, orders, and payment integration.", "Java, Spring Boot, Hibernate, MySQL, Thymeleaf, Bootstrap", "java"),
    ("Face Recognition Attendance Management System", "Automates attendance marking using facial recognition integrated with a Spring Boot backend.", "Java, Spring Boot, OpenCV, Python, MySQL, Bootstrap", "java"),
    ("Online Food Ordering System", "Allows customers to browse menus, place orders, and track delivery status in real time.", "Java, Spring Boot, Hibernate, MySQL, Thymeleaf, Bootstrap", "java"),
    ("Real-Time Chat Application Using WebSockets", "Enables real-time messaging between users using WebSocket protocol and Spring Boot.", "Java, Spring Boot, WebSocket, STOMP, MySQL, Bootstrap", "java"),
    ("Online Examination Management System", "Manages exam creation, scheduling, student attempts, and automated result generation.", "Java, Spring Boot, Hibernate, MySQL, Thymeleaf, Bootstrap", "java"),
    ("Employee Payroll Management System", "Automates salary calculation, payslip generation, and tax deductions for employees.", "Java, Spring Boot, Hibernate, MySQL, Thymeleaf, Bootstrap", "java"),
    ("Smart Library Management System", "Handles book cataloging, member management, issue/return tracking, and fine calculation.", "Java, Spring Boot, Hibernate, MySQL, JSP, Bootstrap", "java"),
    ("Travel and Tourism Booking System", "Allows users to search, book, and manage travel packages, hotels, and transport.", "Java, Spring Boot, Hibernate, MySQL, Thymeleaf, Bootstrap", "java"),
    ("Customer Complaint Management System", "Tracks customer complaints, assigns them to agents, and monitors resolution status.", "Java, Spring Boot, Hibernate, MySQL, Thymeleaf, Bootstrap", "java"),
    ("Vehicle Rental Management System", "Manages vehicle listings, bookings, availability, and rental billing for a rental business.", "Java, Spring Boot, Hibernate, MySQL, Thymeleaf, Bootstrap", "java"),

    # Python Full Stack
    ("AI-Based Food Delivery Time Prediction System", "Predicts food delivery time using ML models based on distance, traffic, and order details.", "Python, Django, Scikit-learn, Pandas, MySQL, Bootstrap", "python"),
    ("Plant Disease Detection Web Application", "Web app that detects plant diseases from uploaded leaf images using a CNN model.", "Python, Django, TensorFlow, Keras, OpenCV, Bootstrap", "python"),
    ("Secure Online Voting System Using Flask", "A secure digital voting platform with voter authentication and real-time result display.", "Python, Flask, SQLAlchemy, MySQL, Bootstrap, Cryptography", "python"),
    ("Smart Expense Tracker and Budget Prediction System", "Tracks personal expenses and predicts future spending using ML regression models.", "Python, Django, Scikit-learn, Pandas, MySQL, Chart.js", "python"),
    ("Online Book Recommendation Web System", "Recommends books to users based on reading history using collaborative filtering.", "Python, Django, Scikit-learn, Pandas, MySQL, Bootstrap", "python"),
    ("AI Resume Screening Web Application", "Web portal that parses and ranks resumes automatically using NLP techniques.", "Python, Django, NLTK, SpaCy, Scikit-learn, MySQL, Bootstrap", "python"),
    ("Multi-Disease Prediction Web Portal", "Predicts multiple diseases from user-entered health parameters using trained ML models.", "Python, Django, Scikit-learn, Pandas, MySQL, Bootstrap", "python"),
    ("Smart Agriculture Advisory Web System", "Provides crop recommendations and disease alerts to farmers based on soil and weather data.", "Python, Django, Scikit-learn, Pandas, MySQL, Bootstrap", "python"),
    ("Student Performance Prediction Portal", "Predicts student academic outcomes using ML models trained on historical performance data.", "Python, Django, Scikit-learn, Pandas, MySQL, Bootstrap", "python"),
    ("Online Shopping Fraud Detection Web App", "Detects fraudulent transactions in real time using anomaly detection ML models.", "Python, Django, Scikit-learn, Pandas, MySQL, Bootstrap", "python"),
    ("AI Chatbot Web Application Using NLP", "A web-based chatbot that answers user queries using NLP intent classification.", "Python, Django, NLTK, TensorFlow, MySQL, Bootstrap", "python"),
    ("Real Estate Price Prediction Web System", "Predicts property prices based on location, size, and amenities using regression models.", "Python, Django, Scikit-learn, Pandas, MySQL, Bootstrap", "python"),
    ("Secure File Sharing and Document Management System", "Allows users to securely upload, share, and manage documents with access control.", "Python, Django, MySQL, Cryptography, Bootstrap, AWS S3", "python"),
    ("AI Image Caption Generator Web Application", "Generates natural language captions for uploaded images using CNN-LSTM architecture.", "Python, Django, TensorFlow, Keras, OpenCV, Bootstrap", "python"),
    ("Automatic Document Classification Web System", "Classifies uploaded documents into categories automatically using NLP and ML models.", "Python, Django, Scikit-learn, NLTK, MySQL, Bootstrap", "python"),

    # MERN Stack
    ("Smart E-Commerce Platform with Recommendation Engine", "Full-stack e-commerce site with AI-powered product recommendations and cart management.", "MongoDB, Express.js, React.js, Node.js, Redux, Stripe", "mern"),
    ("AI-Powered Job Portal with Resume Matching", "Job portal that matches candidates to job listings using NLP-based resume analysis.", "MongoDB, Express.js, React.js, Node.js, Python, NLP", "mern"),
    ("Real-Time Chat Application with Video Calling", "Supports real-time text chat and video calling using WebRTC and Socket.io.", "MongoDB, Express.js, React.js, Node.js, Socket.io, WebRTC", "mern"),
    ("Online Learning Management Platform", "Platform for course creation, video lectures, quizzes, and student progress tracking.", "MongoDB, Express.js, React.js, Node.js, Redux, AWS S3", "mern"),
    ("Expense Tracker with Data Visualization Dashboard", "Tracks income and expenses with interactive charts and budget analytics dashboard.", "MongoDB, Express.js, React.js, Node.js, Chart.js, Redux", "mern"),
    ("Multi-Vendor Marketplace System", "Marketplace where multiple vendors can list products and manage their own storefronts.", "MongoDB, Express.js, React.js, Node.js, Stripe, Redux", "mern"),
    ("Hospital Management Portal Using MERN", "Manages patient records, doctor appointments, and billing in a hospital setting.", "MongoDB, Express.js, React.js, Node.js, Redux, Bootstrap", "mern"),
    ("Online Event Booking and Management System", "Allows users to discover, book, and manage event tickets with organizer dashboards.", "MongoDB, Express.js, React.js, Node.js, Stripe, Redux", "mern"),
    ("Smart Real Estate Listing Platform", "Property listing platform with search filters, map integration, and agent contact.", "MongoDB, Express.js, React.js, Node.js, Google Maps API, Redux", "mern"),
    ("Task Management and Collaboration System", "Team task board with drag-and-drop, assignments, deadlines, and real-time updates.", "MongoDB, Express.js, React.js, Node.js, Socket.io, Redux", "mern"),
    ("Online Movie Streaming Platform", "Streams movies with user authentication, subscription plans, and watchlist management.", "MongoDB, Express.js, React.js, Node.js, AWS S3, Redux", "mern"),
    ("Fitness Tracking Web Application", "Tracks workouts, calories, and fitness goals with progress charts and reminders.", "MongoDB, Express.js, React.js, Node.js, Chart.js, Redux", "mern"),
    ("Donation Management and Fundraising Platform", "Enables NGOs and individuals to create campaigns and accept online donations.", "MongoDB, Express.js, React.js, Node.js, Stripe, Redux", "mern"),
    ("Smart Blogging and Content Management System", "Full-featured CMS with rich text editor, categories, tags, and SEO management.", "MongoDB, Express.js, React.js, Node.js, Redux, AWS S3", "mern"),
    ("Online Quiz and Assessment Platform", "Creates and conducts timed quizzes with auto-grading and performance analytics.", "MongoDB, Express.js, React.js, Node.js, Socket.io, Redux", "mern"),

    # Data Science
    ("Customer Churn Prediction Using Machine Learning", "Predicts which customers are likely to churn using classification models on CRM data.", "Python, Scikit-learn, Pandas, NumPy, Matplotlib, Jupyter", "datascience"),
    ("Retail Sales Forecasting Using Time Series Analysis", "Forecasts future retail sales using ARIMA and Prophet time series models.", "Python, Pandas, Statsmodels, Prophet, Matplotlib, Jupyter", "datascience"),
    ("Student Academic Performance Prediction", "Predicts student grades and dropout risk using regression and classification models.", "Python, Scikit-learn, Pandas, NumPy, Seaborn, Jupyter", "datascience"),
    ("Credit Card Fraud Detection System", "Detects fraudulent credit card transactions using anomaly detection and classification.", "Python, Scikit-learn, Pandas, NumPy, Imbalanced-learn, Jupyter", "datascience"),
    ("Movie Recommendation System Using Collaborative Filtering", "Recommends movies to users based on viewing history using collaborative filtering.", "Python, Scikit-learn, Pandas, Surprise, NumPy, Jupyter", "datascience"),
    ("House Price Prediction Using Regression Models", "Predicts residential property prices using multiple regression and ensemble models.", "Python, Scikit-learn, Pandas, NumPy, Matplotlib, Jupyter", "datascience"),
    ("Social Media Sentiment Analysis System", "Analyzes sentiment of social media posts using NLP and text classification models.", "Python, NLTK, Scikit-learn, Pandas, TextBlob, Jupyter", "datascience"),
    ("Loan Approval Prediction System", "Predicts loan approval decisions based on applicant financial and demographic data.", "Python, Scikit-learn, Pandas, NumPy, Matplotlib, Jupyter", "datascience"),
    ("Energy Consumption Forecasting System", "Forecasts building or city energy consumption using time series and ML models.", "Python, Pandas, Scikit-learn, Statsmodels, Matplotlib, Jupyter", "datascience"),
    ("Weather Prediction Using Machine Learning", "Predicts weather conditions using historical meteorological data and ML algorithms.", "Python, Scikit-learn, Pandas, NumPy, Matplotlib, Jupyter", "datascience"),
    ("Employee Attrition Prediction System", "Identifies employees at risk of leaving using HR data and classification models.", "Python, Scikit-learn, Pandas, NumPy, Seaborn, Jupyter", "datascience"),
    ("Traffic Accident Analysis and Prediction System", "Analyzes traffic accident patterns and predicts high-risk zones using ML models.", "Python, Scikit-learn, Pandas, Folium, Matplotlib, Jupyter", "datascience"),
    ("Disease Prediction Using Patient Health Records", "Predicts disease likelihood from patient records using ensemble ML classifiers.", "Python, Scikit-learn, Pandas, NumPy, Matplotlib, Jupyter", "datascience"),
    ("Customer Segmentation Using Clustering Algorithms", "Segments customers into groups using K-Means and hierarchical clustering algorithms.", "Python, Scikit-learn, Pandas, NumPy, Seaborn, Jupyter", "datascience"),
    ("Stock Market Trend Prediction Using Deep Learning", "Predicts stock market trends using LSTM deep learning on historical price data.", "Python, TensorFlow, Keras, Pandas, NumPy, Matplotlib", "datascience"),
]


class Command(BaseCommand):
    help = 'Seed 60 projects across Java, Python, MERN, and Data Science domains'

    def handle(self, *args, **kwargs):
        created = 0
        for title, description, tech_stack, category in PROJECTS:
            slug = slugify(title)[:50]
            if not Project.objects.filter(slug=slug).exists():
                Project.objects.create(
                    title=title,
                    slug=slug,
                    description=description,
                    tech_stack=tech_stack,
                    category=category,
                    is_active=True,
                )
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created} projects across Java, Python, MERN, and Data Science.'))
