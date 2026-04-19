from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "customer-churn-prediction-using-machine-learning",
        "problem_statement": "Businesses lose customers without knowing the reasons beforehand. Identifying customers likely to leave helps organizations take preventive actions.",
        "objectives": "Predict customer churn probability\nIdentify key churn factors\nImprove customer retention strategies\nReduce revenue loss",
        "features": "Customer data analysis\nChurn prediction\nRisk scoring\nVisualization dashboards\nRetention recommendations",
        "tech_stack": "Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Jupyter Notebook",
        "algorithms": "Logistic Regression\nRandom Forest",
        "conclusion": "Customer churn prediction improves retention strategies and helps businesses proactively reduce revenue loss.",
        "future_enhancements": "Real-time churn monitoring dashboard\nCRM system integration\nPersonalized retention campaign automation",
        "dataset": "Telco Customer Churn Dataset (Kaggle)",
        "description": "Predicts which customers are likely to churn using classification models on CRM data to improve retention strategies.",
    },
    {
        "slug": "retail-sales-forecasting-using-time-series-analysi",
        "problem_statement": "Businesses face difficulty predicting future sales accurately, leading to overstocking or stock shortages and poor inventory planning.",
        "objectives": "Predict future retail sales accurately\nIdentify seasonal demand trends\nImprove inventory and supply chain planning",
        "features": "Sales trend visualization\nDemand forecasting\nSeasonal pattern analysis",
        "tech_stack": "Python, Pandas, NumPy, Statsmodels, Prophet, Matplotlib, Jupyter Notebook",
        "algorithms": "ARIMA (AutoRegressive Integrated Moving Average)\nFacebook Prophet",
        "conclusion": "Improves business planning efficiency through accurate sales forecasting and seasonal trend identification.",
        "future_enhancements": "Live POS data integration\nMulti-store forecasting\nAutomated reorder alert system",
        "dataset": "Rossmann Store Sales Dataset (Kaggle)",
        "description": "Forecasts future retail sales using ARIMA and Prophet time series models to optimize inventory planning.",
    },
    {
        "slug": "student-academic-performance-prediction",
        "problem_statement": "Educational institutions struggle to identify students at risk of poor academic performance before it is too late to provide support.",
        "objectives": "Predict student academic results\nIdentify at-risk students early\nImprove academic outcomes through timely intervention",
        "features": "Student data analysis\nPerformance prediction\nRisk classification",
        "tech_stack": "Python, Pandas, Scikit-learn, NumPy, Matplotlib, Seaborn, Jupyter Notebook",
        "algorithms": "Random Forest\nK-Nearest Neighbors (KNN)",
        "conclusion": "Enhances student monitoring and enables timely academic intervention to improve overall outcomes.",
        "future_enhancements": "Parent and teacher notification system\nPersonalized study plan generator\nLMS platform integration",
        "dataset": "UCI Student Performance Dataset",
        "description": "Predicts student grades and dropout risk using Random Forest and KNN classifiers on historical academic data.",
    },
    {
        "slug": "credit-card-fraud-detection-system",
        "problem_statement": "Online transactions are increasingly vulnerable to fraudulent activities, causing significant financial losses to banks and customers.",
        "objectives": "Detect fraudulent transactions accurately\nReduce financial losses from fraud\nImprove overall transaction security",
        "features": "Transaction monitoring\nFraud alerts\nRisk scoring\nFraud pattern visualization",
        "tech_stack": "Python, Pandas, Scikit-learn, NumPy, Imbalanced-learn, Matplotlib, Jupyter Notebook",
        "algorithms": "Isolation Forest\nRandom Forest",
        "conclusion": "Enhances transaction safety by detecting fraud patterns with high accuracy using anomaly detection and classification.",
        "future_enhancements": "Real-time streaming fraud detection\nGraph-based fraud network analysis\nMobile alert notifications",
        "dataset": "Kaggle Credit Card Fraud Detection Dataset — 284,807 transactions",
        "description": "Detects fraudulent credit card transactions using Isolation Forest anomaly detection and Random Forest classification.",
    },
    {
        "slug": "movie-recommendation-system-using-collaborative-fi",
        "problem_statement": "Users struggle to find relevant movies among large collections, leading to poor content discovery and reduced platform engagement.",
        "objectives": "Recommend personalized movies to users\nImprove content discovery experience\nIncrease platform engagement",
        "features": "User preference tracking\nPersonalized movie recommendations\nSimilar movie suggestions",
        "tech_stack": "Python, Pandas, Scikit-learn, Surprise, NumPy, Matplotlib, Jupyter Notebook",
        "algorithms": "Collaborative Filtering\nContent-Based Filtering",
        "conclusion": "Improves content discovery and user engagement through personalized movie recommendations.",
        "future_enhancements": "Hybrid filtering approach\nReal-time preference updates\nIntegration with streaming platform APIs",
        "dataset": "MovieLens Dataset — 100,000+ ratings",
        "description": "Recommends movies to users based on viewing history using collaborative and content-based filtering techniques.",
    },
]


class Command(BaseCommand):
    help = 'Update Data Science projects 61-65 with full detail content'

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
