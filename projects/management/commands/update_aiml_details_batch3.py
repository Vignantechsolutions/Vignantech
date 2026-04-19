from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "stock-price-prediction-using-lstm-networks",
        "problem_statement": "Stock markets are highly volatile, making it difficult for investors to predict future trends accurately using manual methods.",
        "objectives": "Predict stock prices using historical data\nAnalyze historical market trends\nAssist investors in decision-making",
        "features": "Historical stock data visualization\nTrend prediction\nPrice forecasting dashboard\nGraph-based outputs",
        "tech_stack": "Python, Pandas, NumPy, TensorFlow, Keras, Matplotlib, Jupyter Notebook",
        "algorithms": "Long Short-Term Memory (LSTM)\nTime-Series Data Normalization",
        "conclusion": "LSTM-based stock prediction systems improve financial decision-making by accurately forecasting market trends.",
        "future_enhancements": "Live stock market API integration\nSentiment analysis from financial news\nPortfolio optimization module",
        "dataset": "Yahoo Finance historical stock data",
        "description": "Predicts future stock prices using Long Short-Term Memory recurrent neural networks trained on historical market data.",
    },
    {
        "slug": "personalized-recommendation-system-using-machine-l",
        "problem_statement": "Users face difficulty finding relevant products or content among large datasets, leading to poor user experience and reduced engagement.",
        "objectives": "Recommend personalized items to users\nImprove overall user experience\nIncrease platform engagement",
        "features": "User preference tracking\nPersonalized suggestions\nRecommendation engine dashboard",
        "tech_stack": "Python, Scikit-learn, Pandas, NumPy, Flask",
        "algorithms": "Collaborative Filtering\nContent-Based Filtering",
        "conclusion": "Recommendation systems enhance personalization in digital platforms, improving user satisfaction and retention.",
        "future_enhancements": "Hybrid filtering approach\nReal-time preference updates\nA/B testing module for recommendations",
        "dataset": "MovieLens Dataset / Amazon Product Reviews Dataset",
        "description": "Recommends products or content to users based on collaborative and content-based filtering techniques.",
    },
    {
        "slug": "fake-social-media-profile-detection-using-machine-",
        "problem_statement": "Social media platforms face serious issues due to fake accounts used for fraud, spam, and misinformation campaigns.",
        "objectives": "Detect fake social media profiles automatically\nImprove platform security\nReduce fraud and spam activity",
        "features": "Profile verification system\nFraud detection\nRisk scoring dashboard",
        "tech_stack": "Python, Scikit-learn, Pandas, Flask, Matplotlib",
        "algorithms": "Random Forest\nSupport Vector Machine (SVM)",
        "conclusion": "Enhances digital platform safety by automatically identifying and flagging fake or bot-operated profiles.",
        "future_enhancements": "Real-time profile monitoring\nGraph-based network analysis\nIntegration with platform moderation APIs",
        "dataset": "Twitter Fake Account Dataset / Kaggle Social Media Dataset",
        "description": "Identifies fake or bot social media profiles using ML classification on profile features and behavioral patterns.",
    },
    {
        "slug": "automatic-text-summarization-using-transformers",
        "problem_statement": "Reading long documents takes significant time, making it difficult to extract key information quickly and efficiently.",
        "objectives": "Generate concise summaries from long documents\nExtract the most important sentences\nImprove information accessibility",
        "features": "Text input interface\nAutomatic summary generation\nKeyword extraction",
        "tech_stack": "Python, HuggingFace Transformers, PyTorch, Flask",
        "algorithms": "BERT (Bidirectional Encoder Representations from Transformers)\nExtractive and Abstractive Summarization",
        "conclusion": "Text summarization enhances information accessibility and saves time in document-heavy workflows.",
        "future_enhancements": "Multi-document summarization\nMultilingual support\nBrowser extension for web page summarization",
        "dataset": "CNN/DailyMail News Summarization Dataset",
        "description": "Generates concise summaries of long documents using transformer-based NLP models including BERT.",
    },
    {
        "slug": "ai-based-image-caption-generator-using-cnn-lstm",
        "problem_statement": "Manual captioning of images is time-consuming and inefficient, especially for large image datasets used in media and accessibility tools.",
        "objectives": "Generate descriptive captions automatically\nImprove accessibility for visually impaired users\nAutomate image labeling workflows",
        "features": "Image upload interface\nAutomatic caption generation\nCaption history tracking",
        "tech_stack": "Python, TensorFlow, Keras, OpenCV, Flask",
        "algorithms": "Convolutional Neural Network (CNN)\nLong Short-Term Memory (LSTM)",
        "conclusion": "Enhances automation in visual content processing and improves accessibility for image-heavy applications.",
        "future_enhancements": "Video captioning support\nMultilingual caption generation\nMobile app deployment",
        "dataset": "MS COCO Image Captioning Dataset — 330,000+ images",
        "description": "Generates descriptive captions for images by combining CNN feature extraction with LSTM sequence generation.",
    },
]


class Command(BaseCommand):
    help = 'Update AIML projects 11-15 with full detail content'

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
