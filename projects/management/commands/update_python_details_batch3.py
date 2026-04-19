from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "ai-chatbot-web-application-using-nlp",
        "problem_statement": "Businesses receive repetitive customer queries, leading to high workload for support teams and delayed responses.",
        "objectives": "Automate customer support responses\nUnderstand and classify user queries\nProvide instant automated responses\nReduce human support workload",
        "features": "Chat interface\nQuery recognition\nAutomated responses\nChat history storage\nMulti-language support",
        "tech_stack": "Python, Flask, HTML, CSS, JavaScript, MongoDB, NLTK, HuggingFace Transformers",
        "algorithms": "Natural Language Processing (NLP)\nTransformer-based Response Generation",
        "conclusion": "Improves customer support efficiency with 24/7 availability and reduced operational costs.",
        "future_enhancements": "Sentiment-aware responses\nCRM system integration\nVoice input support",
        "dataset": "Custom FAQ and customer query dataset",
        "description": "A web-based chatbot that answers user queries using NLP intent classification and transformer models.",
    },
    {
        "slug": "real-estate-price-prediction-web-system",
        "problem_statement": "Buyers and sellers face difficulty estimating property prices accurately due to complex and dynamic market factors.",
        "objectives": "Predict property prices based on features\nAnalyze real estate market trends\nAssist buyers and sellers in decision-making",
        "features": "Property data input form\nPrice prediction output\nVisualization dashboard",
        "tech_stack": "Python, Flask, HTML, CSS, MySQL, Scikit-learn, Pandas, Matplotlib",
        "algorithms": "Linear Regression\nRandom Forest Regression",
        "conclusion": "Improves property pricing accuracy and supports informed real estate decision-making.",
        "future_enhancements": "Live market data API integration\nNeighborhood heatmap visualization\nMortgage calculator module",
        "dataset": "Kaggle House Prices Dataset / Custom real estate dataset",
        "description": "Predicts property prices based on location, size, and amenities using regression models on a Flask web system.",
    },
    {
        "slug": "secure-file-sharing-and-document-management-system",
        "problem_statement": "Organizations require secure file sharing systems to protect confidential information from unauthorized access.",
        "objectives": "Enable secure file upload and download\nManage document access with role-based control\nProtect sensitive files using encryption",
        "features": "File upload and download\nAccess control\nUser authentication",
        "tech_stack": "Python, Flask, HTML, CSS, MySQL, Cryptography, Bootstrap",
        "algorithms": "AES Encryption Algorithm\nRole-Based Access Control (RBAC)",
        "conclusion": "Enhances document security and ensures confidential files are accessible only to authorized users.",
        "future_enhancements": "Cloud storage integration (AWS S3)\nAudit trail and activity logs\nDigital signature support",
        "dataset": "Custom document and user access dataset",
        "description": "Allows users to securely upload, share, and manage documents with encryption and role-based access control.",
    },
    {
        "slug": "ai-image-caption-generator-web-application",
        "problem_statement": "Manual image captioning is time-consuming and impractical for large image datasets used in media and accessibility tools.",
        "objectives": "Generate descriptive captions automatically\nImprove accessibility for visually impaired users\nAutomate image labeling workflows",
        "features": "Image upload interface\nAutomatic caption generation\nCaption history tracking",
        "tech_stack": "Python, Flask, HTML, CSS, MongoDB, TensorFlow, Keras, OpenCV",
        "algorithms": "Convolutional Neural Network (CNN)\nLong Short-Term Memory (LSTM)",
        "conclusion": "Improves automation in visual content processing and enhances accessibility for image-heavy applications.",
        "future_enhancements": "Video captioning support\nMultilingual caption generation\nMobile app deployment",
        "dataset": "MS COCO Image Captioning Dataset — 330,000+ images",
        "description": "Generates natural language captions for uploaded images using CNN feature extraction and LSTM sequence generation.",
    },
    {
        "slug": "automatic-document-classification-web-system",
        "problem_statement": "Organizations manage large volumes of documents that require manual classification, leading to inefficiency and misorganization.",
        "objectives": "Classify documents automatically into categories\nImprove document organization and retrieval\nReduce manual classification effort",
        "features": "Document upload\nAutomatic classification\nSearch functionality",
        "tech_stack": "Python, Flask, HTML, CSS, MongoDB, NLTK, Scikit-learn",
        "algorithms": "TF-IDF Text Classification\nNaive Bayes Classifier",
        "conclusion": "Improves document management efficiency by automating classification across large document repositories.",
        "future_enhancements": "Multi-label document classification\nOCR for scanned document support\nEnterprise DMS integration",
        "dataset": "Reuters News Dataset / Custom document dataset",
        "description": "Classifies uploaded documents into categories automatically using NLP and ML text classification models.",
    },
]


class Command(BaseCommand):
    help = 'Update Python projects 41-45 with full detail content'

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
