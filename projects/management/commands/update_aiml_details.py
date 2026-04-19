from django.core.management.base import BaseCommand
from django.utils.text import slugify
from projects.models import Project

DETAILS = [
    {
        "slug": "ai-based-multi-disease-prediction-system",
        "problem_statement": "Healthcare systems often face delays in diagnosing diseases due to manual medical analysis. Patients in remote areas lack access to specialists, resulting in delayed treatment.",
        "objectives": "Predict multiple diseases using patient input\nProvide early-stage diagnosis\nReduce dependency on manual diagnosis\nImprove healthcare accessibility",
        "features": "Multi-disease prediction\nPatient input form\nPrediction accuracy display\nMedical history tracking\nReport generation",
        "tech_stack": "HTML, CSS, JavaScript, Python, Flask, MySQL, Pandas, NumPy, Scikit-learn",
        "algorithms": "Logistic Regression\nDecision Tree",
        "conclusion": "The system improves early disease detection and supports better healthcare decision-making.",
        "future_enhancements": "Integration with wearable health devices\nMobile application support\nReal-time doctor consultation feature",
        "dataset": "UCI Machine Learning Repository — Disease datasets",
        "description": "Predicts multiple diseases using patient health data with ML classification algorithms. Provides early-stage diagnosis to improve healthcare accessibility.",
    },
    {
        "slug": "intelligent-plant-disease-detection-using-deep-lea",
        "problem_statement": "Farmers often fail to detect crop diseases early, leading to significant crop loss.",
        "objectives": "Detect plant diseases from leaf images\nProvide disease classification\nImprove agricultural productivity",
        "features": "Leaf image upload\nDisease detection\nTreatment suggestions\nHistory tracking",
        "tech_stack": "HTML, CSS, Python, Flask, TensorFlow, OpenCV, MySQL",
        "algorithms": "Convolutional Neural Network (CNN)\nImage Preprocessing Pipeline",
        "conclusion": "This project significantly improves agricultural productivity by enabling early and automated disease recognition.",
        "future_enhancements": "Mobile app for field use\nMulti-language support\nDrone-based image capture integration",
        "dataset": "PlantVillage Dataset — 54,000+ leaf images",
        "description": "Detects plant diseases from leaf images using CNN-based deep learning models to improve agricultural productivity.",
    },
    {
        "slug": "ai-resume-screening-and-candidate-ranking-system",
        "problem_statement": "Recruiters spend large amounts of time manually screening resumes, leading to inefficiency and potential bias in the hiring process.",
        "objectives": "Automate resume filtering\nRank candidates based on job requirements\nMatch skills with job roles",
        "features": "Resume upload\nSkill extraction\nRanking system\nRecruiter dashboard",
        "tech_stack": "Python, Flask, SpaCy, Scikit-learn, MongoDB",
        "algorithms": "TF-IDF (Term Frequency-Inverse Document Frequency)\nCosine Similarity",
        "conclusion": "Improves hiring process automation by reducing manual effort and improving candidate-job matching accuracy.",
        "future_enhancements": "Integration with LinkedIn API\nBias detection module\nMulti-language resume support",
        "dataset": "Custom HR resume dataset",
        "description": "Automates resume parsing and ranks candidates using NLP and ML techniques to streamline the recruitment process.",
    },
    {
        "slug": "fake-news-detection-using-natural-language-process",
        "problem_statement": "Fake news spreads rapidly through online platforms, causing widespread misinformation and public harm.",
        "objectives": "Detect fake news articles automatically\nImprove information reliability\nReduce spread of misinformation",
        "features": "News article classification\nText analysis\nCredibility score display",
        "tech_stack": "Python, Flask, NLTK, Scikit-learn",
        "algorithms": "Naive Bayes\nLogistic Regression",
        "conclusion": "Helps maintain trustworthy information flow by automatically classifying news articles as real or fake.",
        "future_enhancements": "Browser extension integration\nMultilingual support\nReal-time social media feed analysis",
        "dataset": "LIAR Dataset / Kaggle Fake News Dataset",
        "description": "Classifies news articles as real or fake using NLP and text classification models to combat misinformation.",
    },
    {
        "slug": "real-time-emotion-detection-from-facial-expression",
        "problem_statement": "Understanding human emotions automatically is challenging but essential for improving human-computer interaction and security systems.",
        "objectives": "Detect facial emotions in real time\nImprove human-computer interaction\nSupport security and surveillance applications",
        "features": "Real-time face detection\nEmotion classification\nLive webcam analysis",
        "tech_stack": "Python, OpenCV, TensorFlow, Keras",
        "algorithms": "Convolutional Neural Network (CNN)\nHaar Cascade Classifier",
        "conclusion": "Enhances interaction between humans and machines by enabling real-time emotion-aware systems.",
        "future_enhancements": "Multi-face simultaneous detection\nMobile deployment\nEmotion trend analytics dashboard",
        "dataset": "FER-2013 Facial Expression Dataset",
        "description": "Detects human emotions in real-time from webcam feed using deep learning and OpenCV.",
    },
]


class Command(BaseCommand):
    help = 'Update 5 AIML projects with full detail content'

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
