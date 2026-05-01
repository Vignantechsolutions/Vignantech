import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vignan_tech.settings'
django.setup()

from internships.models import Internship

# Clear all existing
Internship.objects.all().delete()

CERT = "Upon successful completion, students receive an industry-recognized certificate from Vignan TechSolutions, valid for job applications and higher studies."
BENEFITS = "Industry experience certificate\nLetter of recommendation\nPortfolio projects\nPlacement assistance\nMentor support\nLinkedIn recommendation"

internships = [
    {
        "title": "Python Full Stack Internship",
        "slug": "python-full-stack-internship",
        "description": "Build complete web applications using Python, Django, Flask, HTML, CSS, JavaScript, and MySQL. Work on real client projects and build a strong portfolio.",
        "duration": "3 Months",
        "fees": 1,
        "topics_covered": "Python Programming\nDjango Framework\nFlask Basics\nHTML5 & CSS3\nJavaScript ES6+\nBootstrap 5\nMySQL Database\nREST APIs\nGit & GitHub\nDeployment",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "hybrid",
        "seats_available": 20,
        "is_featured": True,
    },
    {
        "title": "AI & Machine Learning Internship",
        "slug": "ai-machine-learning-internship",
        "description": "Explore deep learning, computer vision, and NLP using TensorFlow and PyTorch. Build real AI projects with hands-on mentorship from industry experts.",
        "duration": "3 Months",
        "fees": 1,
        "topics_covered": "Python for AI/ML\nNumPy & Pandas\nScikit-learn\nDeep Learning Fundamentals\nTensorFlow & Keras\nConvolutional Neural Networks\nNatural Language Processing\nModel Deployment\nCapstone AI Project",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "online",
        "seats_available": 15,
        "is_featured": True,
    },
    {
        "title": "Java Full Stack Internship",
        "slug": "java-full-stack-internship",
        "description": "Learn enterprise-level Java development using Spring Boot, Hibernate, and React.js to build scalable, production-ready web applications.",
        "duration": "3 Months",
        "fees": 1,
        "topics_covered": "Core Java & OOPs\nSpring Boot\nHibernate & JPA\nREST API Development\nReact.js Frontend\nMySQL Database\nMaven & Git\nProject Deployment",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "hybrid",
        "seats_available": 15,
        "is_featured": True,
    },
    {
        "title": "Data Science Internship",
        "slug": "data-science-internship",
        "description": "Gain hands-on experience in data analysis, visualization, and predictive modeling using Python and real-world datasets from various industries.",
        "duration": "2 Months",
        "fees": 1,
        "topics_covered": "Python for Data Science\nPandas & NumPy\nMatplotlib & Seaborn\nExploratory Data Analysis\nStatistical Analysis\nMachine Learning Models\nModel Evaluation\nCapstone Project",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "online",
        "seats_available": 15,
        "is_featured": True,
    },
]

for data in internships:
    Internship.objects.create(**data)
    print(f"Created: {data['title']}")

print(f"\nTotal internships: {Internship.objects.count()}")
