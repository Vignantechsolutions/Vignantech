import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vignan_tech.settings'
django.setup()

from internships.models import Internship

CERT = "Upon successful completion, students receive an industry-recognized certificate from Vignan TechSolutions, valid for job applications and higher studies."
BENEFITS = "Industry experience certificate\nLetter of recommendation\nPortfolio projects\nPlacement assistance\nMentor support\nLinkedIn recommendation"

internships = [
    {
        "title": "Full Stack Web Development Internship",
        "slug": "full-stack-web-development-internship",
        "description": "Build complete web applications using HTML, CSS, JavaScript, React, Node.js, and Django. Work on real client projects and build a strong portfolio.",
        "duration": "3 Months",
        "fees": 5000,
        "topics_covered": "HTML5 & CSS3\nJavaScript ES6+\nReact.js\nNode.js & Express\nDjango Framework\nMySQL & MongoDB\nREST APIs\nGit & GitHub\nDeployment",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "hybrid",
        "seats_available": 20,
        "is_featured": True,
    },
    {
        "title": "Python & Machine Learning Internship",
        "slug": "python-ml-internship",
        "description": "Hands-on internship covering Python programming, data analysis, and machine learning model building with real datasets.",
        "duration": "2 Months",
        "fees": 4000,
        "topics_covered": "Python Programming\nNumPy & Pandas\nData Visualization\nMachine Learning Basics\nScikit-learn\nModel Evaluation\nProject Implementation",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "online",
        "seats_available": 15,
        "is_featured": True,
    },
    {
        "title": "Android App Development Internship",
        "slug": "android-internship",
        "description": "Build real Android applications using Java/Kotlin. Learn UI design, REST APIs, Firebase, and app deployment on Play Store.",
        "duration": "2 Months",
        "fees": 4500,
        "topics_covered": "Java/Kotlin Basics\nAndroid Studio\nUI/UX Design\nREST API Integration\nFirebase\nApp Deployment",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "online",
        "seats_available": 10,
        "is_featured": True,
    },
    {
        "title": "Data Science & Analytics Internship",
        "slug": "data-science-analytics-internship",
        "description": "Gain hands-on experience in data analysis, visualization, and predictive modeling using Python and real-world datasets.",
        "duration": "2 Months",
        "fees": 4500,
        "topics_covered": "Python for Data Science\nPandas & NumPy\nMatplotlib & Seaborn\nExploratory Data Analysis\nStatistical Analysis\nMachine Learning Models\nTableau Basics\nCapstone Project",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "online",
        "seats_available": 15,
        "is_featured": True,
    },
    {
        "title": "MERN Stack Development Internship",
        "slug": "mern-stack-internship",
        "description": "Build full-stack web applications using MongoDB, Express.js, React.js, and Node.js with real project experience.",
        "duration": "3 Months",
        "fees": 5500,
        "topics_covered": "React.js & Redux\nNode.js & Express.js\nMongoDB & Mongoose\nREST API Development\nJWT Authentication\nSocket.io\nDeployment on Render/Vercel",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "hybrid",
        "seats_available": 15,
        "is_featured": True,
    },
    {
        "title": "Java Full Stack Internship",
        "slug": "java-full-stack-internship",
        "description": "Learn enterprise-level Java development using Spring Boot, Hibernate, and React.js to build scalable web applications.",
        "duration": "3 Months",
        "fees": 5500,
        "topics_covered": "Core Java & OOPs\nSpring Boot\nHibernate & JPA\nREST API Development\nReact.js Frontend\nMySQL Database\nMaven & Git\nProject Deployment",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "hybrid",
        "seats_available": 15,
        "is_featured": False,
    },
    {
        "title": "UI/UX Design Internship",
        "slug": "ui-ux-design-internship",
        "description": "Learn user interface and experience design using Figma, Adobe XD, and design principles to create stunning digital products.",
        "duration": "1 Month",
        "fees": 2500,
        "topics_covered": "Design Principles\nFigma & Adobe XD\nWireframing & Prototyping\nUser Research\nResponsive Design\nDesign Systems\nPortfolio Project",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "online",
        "seats_available": 20,
        "is_featured": False,
    },
    {
        "title": "Cybersecurity Internship",
        "slug": "cybersecurity-internship",
        "description": "Learn ethical hacking, network security, and penetration testing fundamentals with hands-on labs and real-world scenarios.",
        "duration": "2 Months",
        "fees": 5000,
        "topics_covered": "Network Security Basics\nEthical Hacking\nPenetration Testing\nKali Linux\nVulnerability Assessment\nOWASP Top 10\nCTF Challenges",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "online",
        "seats_available": 10,
        "is_featured": False,
    },
    {
        "title": "Cloud Computing Internship",
        "slug": "cloud-computing-internship",
        "description": "Get hands-on experience with AWS cloud services including EC2, S3, RDS, Lambda, and deployment of real applications.",
        "duration": "2 Months",
        "fees": 5000,
        "topics_covered": "Cloud Computing Basics\nAWS EC2 & S3\nAWS RDS & Lambda\nDocker & Containers\nCI/CD Pipelines\nCloud Security\nCapstone Deployment Project",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "online",
        "seats_available": 10,
        "is_featured": False,
    },
    {
        "title": "AI & Deep Learning Internship",
        "slug": "ai-deep-learning-internship",
        "description": "Explore deep learning, computer vision, and NLP using TensorFlow and PyTorch with real AI project implementation.",
        "duration": "3 Months",
        "fees": 6000,
        "topics_covered": "Deep Learning Fundamentals\nTensorFlow & Keras\nPyTorch Basics\nConvolutional Neural Networks\nNatural Language Processing\nTransfer Learning\nModel Deployment\nCapstone AI Project",
        "benefits": BENEFITS,
        "certificate_info": CERT,
        "mode": "online",
        "seats_available": 10,
        "is_featured": True,
    },
]

created = 0
skipped = 0
for data in internships:
    if not Internship.objects.filter(slug=data['slug']).exists():
        Internship.objects.create(**data)
        created += 1
        print(f"Created: {data['title']}")
    else:
        skipped += 1
        print(f"Skipped (exists): {data['title']}")

print(f"\nDone — Created: {created}, Skipped: {skipped}")
print(f"Total internships: {Internship.objects.count()}")
