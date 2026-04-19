from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "ai-resume-screening-web-application",
        "problem_statement": "Recruiters spend large amounts of time manually reviewing resumes, making the hiring process slow and inefficient.",
        "objectives": "Automate resume screening process\nExtract candidate skills automatically\nRank candidates based on relevance\nImprove overall hiring efficiency",
        "features": "Resume upload system\nSkill extraction\nResume ranking\nJob-role matching\nRecruiter dashboard",
        "tech_stack": "Python, Flask, HTML, CSS, JavaScript, MongoDB, SpaCy, NLTK, Scikit-learn",
        "algorithms": "TF-IDF (Term Frequency-Inverse Document Frequency)\nCosine Similarity",
        "conclusion": "Improves hiring efficiency through automation by reducing manual resume screening effort.",
        "future_enhancements": "LinkedIn profile import\nBias detection module\nMulti-language resume support",
        "dataset": "Custom HR resume and job description dataset",
        "description": "Web portal that parses and ranks resumes automatically using NLP techniques including TF-IDF and cosine similarity.",
    },
    {
        "slug": "multi-disease-prediction-web-portal",
        "problem_statement": "Early disease detection is difficult due to lack of accessible diagnostic tools, especially in remote areas.",
        "objectives": "Predict multiple diseases from patient data\nProvide risk analysis scores\nAssist in early medical diagnosis",
        "features": "Patient data entry form\nDisease prediction\nRisk score display\nMedical history storage",
        "tech_stack": "Python, Flask, HTML, CSS, JavaScript, MySQL, Scikit-learn, Pandas",
        "algorithms": "Logistic Regression\nDecision Tree",
        "conclusion": "Supports early disease detection and improves healthcare accessibility for patients in remote areas.",
        "future_enhancements": "Integration with wearable health devices\nDoctor consultation module\nMobile app support",
        "dataset": "UCI Machine Learning Repository — Disease datasets",
        "description": "Predicts multiple diseases from user-entered health parameters using trained ML models on a Flask web portal.",
    },
    {
        "slug": "smart-agriculture-advisory-web-system",
        "problem_statement": "Farmers lack guidance on selecting suitable crops and fertilizers based on soil and environmental conditions.",
        "objectives": "Recommend suitable crops based on soil data\nSuggest appropriate fertilizers\nImprove agricultural productivity",
        "features": "Soil input analysis\nCrop recommendation\nFertilizer suggestions",
        "tech_stack": "Python, Flask, HTML, CSS, MySQL, Scikit-learn, Pandas",
        "algorithms": "Random Forest\nDecision Tree",
        "conclusion": "Enhances crop planning and agricultural productivity through data-driven advisory recommendations.",
        "future_enhancements": "Weather API integration\nPest detection module\nFarmer mobile app",
        "dataset": "Crop Recommendation Dataset / Fertilizer Prediction Dataset",
        "description": "Provides crop recommendations and fertilizer suggestions to farmers based on soil and weather data using ML.",
    },
    {
        "slug": "student-performance-prediction-portal",
        "problem_statement": "Educational institutions struggle to identify students at risk of poor academic performance before it is too late to intervene.",
        "objectives": "Predict student academic performance\nIdentify at-risk students early\nImprove academic outcomes through intervention",
        "features": "Student data input\nPerformance prediction\nPerformance visualization dashboard",
        "tech_stack": "Python, Flask, HTML, CSS, MySQL, Pandas, Scikit-learn",
        "algorithms": "Random Forest\nGradient Boosting",
        "conclusion": "Improves student performance tracking and enables timely academic intervention.",
        "future_enhancements": "Parent notification system\nPersonalized study plan generator\nIntegration with LMS platforms",
        "dataset": "UCI Student Performance Dataset",
        "description": "Predicts student academic outcomes using ML models trained on historical performance and demographic data.",
    },
    {
        "slug": "online-shopping-fraud-detection-web-app",
        "problem_statement": "Online transactions are increasingly vulnerable to fraudulent activities, causing significant financial losses to businesses and customers.",
        "objectives": "Detect fraudulent transactions in real time\nImprove platform security\nReduce financial losses from fraud",
        "features": "Transaction monitoring\nFraud detection alerts\nRisk scoring dashboard",
        "tech_stack": "Python, Flask, HTML, CSS, MySQL, Scikit-learn, XGBoost",
        "algorithms": "XGBoost\nAnomaly Detection",
        "conclusion": "Enhances financial transaction security by detecting fraud patterns with high accuracy.",
        "future_enhancements": "Real-time streaming fraud detection\nGraph-based fraud network analysis\nMobile alert notifications",
        "dataset": "Kaggle Credit Card Fraud Detection Dataset",
        "description": "Detects fraudulent transactions in real time using anomaly detection and XGBoost classification models.",
    },
]


class Command(BaseCommand):
    help = 'Update Python projects 36-40 with full detail content'

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
