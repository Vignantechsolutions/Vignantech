from django.core.management.base import BaseCommand
from django.utils.text import slugify
from projects.models import Project, ProjectDomain

PROJECTS = {
    'aiml': [
        ("AI-Based Multi-Disease Prediction System", "Predicts multiple diseases using patient health data with ML classification algorithms.", "Python, Scikit-learn, Flask, Pandas, NumPy"),
        ("Intelligent Plant Disease Detection Using Deep Learning", "Detects plant diseases from leaf images using CNN-based deep learning models.", "Python, TensorFlow, Keras, OpenCV, Flask"),
        ("AI Resume Screening and Candidate Ranking System", "Automates resume parsing and ranks candidates using NLP and ML techniques.", "Python, NLTK, Scikit-learn, SpaCy, Django"),
        ("Fake News Detection Using Natural Language Processing", "Classifies news articles as real or fake using NLP and text classification models.", "Python, NLTK, Scikit-learn, TF-IDF, Flask"),
        ("Real-Time Emotion Detection from Facial Expressions", "Detects human emotions in real-time from webcam feed using deep learning.", "Python, OpenCV, TensorFlow, Keras, Flask"),
        ("Traffic Sign Recognition Using Convolutional Neural Networks", "Recognizes and classifies traffic signs from images using CNN architecture.", "Python, TensorFlow, Keras, OpenCV, NumPy"),
        ("AI-Based Voice Assistant with NLP", "A voice-controlled assistant that understands and responds to natural language commands.", "Python, SpeechRecognition, NLTK, pyttsx3, Flask"),
        ("Handwritten Digit Recognition Using Deep Learning", "Recognizes handwritten digits using a trained deep neural network on MNIST dataset.", "Python, TensorFlow, Keras, NumPy, Matplotlib"),
        ("Real-Time Object Detection Using YOLO Algorithm", "Detects and labels multiple objects in real-time video streams using YOLO.", "Python, OpenCV, YOLOv5, PyTorch, Flask"),
        ("AI-Based Customer Support Chatbot System", "An intelligent chatbot that handles customer queries using NLP and intent classification.", "Python, NLTK, TensorFlow, Flask, JSON"),
        ("Stock Price Prediction Using LSTM Networks", "Predicts future stock prices using Long Short-Term Memory recurrent neural networks.", "Python, TensorFlow, Keras, Pandas, Matplotlib"),
        ("Personalized Recommendation System Using Machine Learning", "Recommends products or content to users based on collaborative and content-based filtering.", "Python, Scikit-learn, Pandas, NumPy, Flask"),
        ("Fake Social Media Profile Detection Using Machine Learning", "Identifies fake or bot social media profiles using ML classification on profile features.", "Python, Scikit-learn, Pandas, Flask, Matplotlib"),
        ("Automatic Text Summarization Using Transformers", "Generates concise summaries of long documents using transformer-based NLP models.", "Python, HuggingFace Transformers, PyTorch, Flask"),
        ("AI-Based Image Caption Generator Using CNN-LSTM", "Generates descriptive captions for images by combining CNN feature extraction with LSTM.", "Python, TensorFlow, Keras, OpenCV, Flask"),
    ],
    'python': [
        ("Hospital Management System Using Django", "A complete hospital management system with patient records, appointments and billing.", "Python, Django, MySQL, Bootstrap, HTML/CSS"),
        ("Online Examination Portal Using Flask", "An online exam system with timer, auto-grading and result analytics.", "Python, Flask, SQLite, Bootstrap, JavaScript"),
        ("E-Commerce Website Using Django", "A full-featured online store with cart, payments and order management.", "Python, Django, Razorpay, Bootstrap, MySQL"),
        ("Student Result Management System", "Manages student results, generates report cards and provides analytics.", "Python, Django, MySQL, Bootstrap, Chart.js"),
        ("Library Management System Using Flask", "Tracks books, members, issue/return and fine management.", "Python, Flask, SQLite, Bootstrap, Jinja2"),
        ("Job Portal Web Application Using Django", "Connects job seekers with employers, with resume upload and application tracking.", "Python, Django, MySQL, Bootstrap, REST API"),
        ("Online Food Ordering System", "Restaurant ordering platform with menu management and order tracking.", "Python, Django, MySQL, Bootstrap, Razorpay"),
        ("Real Estate Property Listing Platform", "Property listing, search and inquiry management system.", "Python, Django, PostgreSQL, Bootstrap, Google Maps API"),
        ("College Admission Management System", "Automates college admission process with online application and merit list.", "Python, Django, MySQL, Bootstrap, PDF generation"),
        ("Inventory Management System Using Flask", "Tracks stock, manages suppliers and generates inventory reports.", "Python, Flask, SQLite, Bootstrap, Chart.js"),
        ("Bank Management System Using Django", "Handles accounts, transfers, statements and loan management.", "Python, Django, MySQL, Bootstrap, ReportLab"),
        ("Online Voting System Using Flask", "Secure digital voting system with OTP verification and results dashboard.", "Python, Flask, SQLite, Bootstrap, Chart.js"),
        ("Employee Leave Management System", "Manages employee leave requests, approvals and attendance tracking.", "Python, Django, MySQL, Bootstrap, Email"),
        ("Blood Bank Management System", "Manages blood donors, requests, stock and hospital coordination.", "Python, Flask, MySQL, Bootstrap, SMS API"),
        ("Crime Record Management System", "Digital crime record system for police departments with search and analytics.", "Python, Django, PostgreSQL, Bootstrap, Leaflet Maps"),
    ],
    'mern': [
        ("Real-Time Chat Application Using MERN Stack", "A full-featured chat app with rooms, private messaging and file sharing.", "MongoDB, Express.js, React, Node.js, Socket.io"),
        ("Social Media Platform Using MERN Stack", "A social network with posts, likes, comments, follow system and notifications.", "MongoDB, Express.js, React, Node.js, JWT"),
        ("Online Learning Management System", "LMS with course creation, video lectures, quizzes and certificates.", "MongoDB, Express.js, React, Node.js, AWS S3"),
        ("Food Delivery App Using MERN Stack", "Food ordering platform with real-time tracking and payment integration.", "MongoDB, Express.js, React, Node.js, Stripe"),
        ("Project Management Tool Like Trello", "Kanban-style project management with drag-and-drop boards and team collaboration.", "MongoDB, Express.js, React, Node.js, DnD"),
        ("Healthcare Appointment Booking System", "Book doctor appointments, manage prescriptions and health records online.", "MongoDB, Express.js, React, Node.js, JWT"),
        ("E-Commerce Platform Using MERN Stack", "Online shopping platform with product search, cart, wishlist and checkout.", "MongoDB, Express.js, React, Node.js, Razorpay"),
        ("News Aggregator Portal", "Aggregates and categorizes news from multiple sources with personalization.", "MongoDB, Express.js, React, Node.js, News API"),
        ("Freelancer Marketplace Platform", "Connects freelancers with clients, manages projects and payments.", "MongoDB, Express.js, React, Node.js, Stripe"),
        ("Online Code Editor and Compiler", "Browser-based code editor with multi-language support and real-time execution.", "MongoDB, Express.js, React, Node.js, Docker"),
        ("Event Management System", "Create, manage and book events with QR-based ticket generation.", "MongoDB, Express.js, React, Node.js, QR Code"),
        ("Travel Booking Platform", "Book flights, hotels and packages with itinerary management.", "MongoDB, Express.js, React, Node.js, Maps API"),
        ("Expense Tracker with Budget Analytics", "Personal finance tracker with charts, budget goals and expense categories.", "MongoDB, Express.js, React, Node.js, Chart.js"),
        ("Online Auction System", "Real-time bidding platform with countdown timers and payment processing.", "MongoDB, Express.js, React, Node.js, Socket.io"),
        ("Recipe Sharing Social Platform", "Share, discover and review recipes with ingredient-based search.", "MongoDB, Express.js, React, Node.js, Cloudinary"),
    ],
    'java': [
        ("Online Banking System Using Spring Boot", "A secure banking application with accounts, transactions and loan management.", "Java, Spring Boot, Hibernate, MySQL, Bootstrap"),
        ("Hospital Management System Using JSP Servlet", "Hospital information system with patient records, billing and pharmacy.", "Java, JSP, Servlet, MySQL, Bootstrap, JDBC"),
        ("Online Examination System Using Spring Boot", "MCQ-based exam system with timer, auto-evaluation and analytics.", "Java, Spring Boot, Thymeleaf, MySQL, Bootstrap"),
        ("Inventory Management System Using Java", "Manages warehouse stock, purchase orders and supplier management.", "Java, Spring Boot, Hibernate, MySQL, Bootstrap"),
        ("Hotel Booking and Management System", "Hotel reservation system with room management and billing.", "Java, Spring Boot, Hibernate, MySQL, Thymeleaf"),
        ("Employee Payroll Management System", "Automates payroll calculation, salary slips and tax computation.", "Java, Spring Boot, Hibernate, MySQL, iText PDF"),
        ("Online Shopping Cart Using Spring MVC", "E-commerce application with product catalog, cart and order processing.", "Java, Spring MVC, Hibernate, MySQL, Bootstrap"),
        ("Library Management System Using Spring Boot", "Digital library with book catalog, member management and fine tracking.", "Java, Spring Boot, Hibernate, MySQL, Thymeleaf"),
        ("Student Information System", "Comprehensive student data management with marks, attendance and fees.", "Java, Spring Boot, Hibernate, MySQL, Bootstrap"),
        ("Vehicle Rental Management System", "Manages vehicle fleet, bookings, maintenance and billing.", "Java, Spring Boot, Hibernate, MySQL, Bootstrap"),
        ("Courier Tracking System", "Track courier shipments in real-time with delivery management.", "Java, Spring Boot, Hibernate, MySQL, REST API"),
        ("Online Voting System Using Spring Boot", "Secure electronic voting with authentication and real-time results.", "Java, Spring Boot, Hibernate, MySQL, Bootstrap"),
        ("Gym Management System", "Manages gym memberships, attendance, trainers and billing.", "Java, Spring Boot, Hibernate, MySQL, Bootstrap"),
        ("Supply Chain Management System", "Manages suppliers, orders, logistics and delivery tracking.", "Java, Spring Boot, Hibernate, MySQL, Bootstrap"),
        ("College ERP System Using Spring Boot", "Enterprise resource planning for colleges with all departments integrated.", "Java, Spring Boot, Hibernate, MySQL, Bootstrap"),
    ],
    'datascience': [
        ("Customer Churn Prediction System", "Predicts which customers are likely to churn using classification models.", "Python, Scikit-learn, Pandas, Matplotlib, Seaborn"),
        ("Sales Forecasting Using Time Series Analysis", "Forecasts future sales trends using ARIMA and Prophet models.", "Python, Prophet, Statsmodels, Pandas, Matplotlib"),
        ("COVID-19 Data Analysis and Visualization", "Analyzes and visualizes COVID-19 spread patterns using real-world datasets.", "Python, Pandas, Plotly, Seaborn, NumPy"),
        ("Credit Card Fraud Detection System", "Detects fraudulent transactions using anomaly detection and classification.", "Python, Scikit-learn, Pandas, Imbalanced-learn, Flask"),
        ("House Price Prediction Using Regression", "Predicts property prices based on location, size and amenities.", "Python, Scikit-learn, Pandas, Matplotlib, Flask"),
        ("Twitter Sentiment Analysis Dashboard", "Analyzes public sentiment on Twitter topics using NLP and visualization.", "Python, Tweepy, NLTK, Matplotlib, Streamlit"),
        ("Movie Box Office Revenue Prediction", "Predicts movie box office performance using ML regression models.", "Python, Scikit-learn, Pandas, Seaborn, Flask"),
        ("E-Commerce Customer Segmentation", "Segments customers based on purchase behavior using clustering algorithms.", "Python, Scikit-learn, Pandas, Matplotlib, KMeans"),
        ("Air Quality Index Prediction System", "Predicts air quality levels using environmental sensor data and ML.", "Python, Scikit-learn, Pandas, Plotly, Flask"),
        ("Heart Disease Risk Analysis Dashboard", "Analyzes patient data to assess heart disease risk with visualizations.", "Python, Scikit-learn, Pandas, Plotly, Streamlit"),
        ("Student Performance Analytics System", "Analyzes student academic performance patterns and predicts outcomes.", "Python, Pandas, Matplotlib, Seaborn, Scikit-learn"),
        ("Supply Chain Demand Forecasting", "Forecasts product demand for supply chain optimization using ML.", "Python, Prophet, Scikit-learn, Pandas, Plotly"),
        ("Loan Default Prediction System", "Predicts whether a loan applicant will default using classification.", "Python, Scikit-learn, Pandas, Imbalanced-learn, Flask"),
        ("Energy Consumption Prediction", "Predicts building energy consumption using regression and time series.", "Python, Scikit-learn, Pandas, Matplotlib, Flask"),
        ("Sports Performance Analytics Dashboard", "Analyzes athlete and team performance using statistical data science.", "Python, Pandas, Plotly, Scikit-learn, Streamlit"),
    ],
}


class Command(BaseCommand):
    help = 'Seed all 75 projects across 5 domains'

    def handle(self, *args, **kwargs):
        total = 0
        for domain_slug, project_list in PROJECTS.items():
            domain = ProjectDomain.objects.filter(slug=domain_slug).first()
            if not domain:
                self.stdout.write(self.style.WARNING(f'Domain not found: {domain_slug}'))
                continue
            for i, (title, description, tech_stack) in enumerate(project_list):
                slug = slugify(title)[:48]
                # ensure slug uniqueness
                base_slug = slug
                counter = 1
                while Project.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                Project.objects.get_or_create(
                    slug=slug,
                    defaults=dict(
                        title=title,
                        description=description,
                        tech_stack=tech_stack,
                        domain=domain,
                        is_active=True,
                        is_featured=(i < 3),  # first 3 per domain are featured
                    )
                )
                total += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {total} projects across {len(PROJECTS)} domains.'))
