from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "house-price-prediction-using-regression-models",
        "problem_statement": "Property buyers and sellers often struggle to estimate accurate house prices due to multiple influencing factors like location, size, and amenities.",
        "objectives": "Predict house prices based on property features\nAnalyze important price-influencing factors\nAssist buyers and sellers in decision-making\nImprove property pricing transparency",
        "features": "Property data input\nPrice prediction output\nVisualization graphs\nFeature importance analysis",
        "tech_stack": "Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Jupyter Notebook",
        "algorithms": "Linear Regression\nRandom Forest Regression",
        "conclusion": "Improves transparency in property pricing and supports informed real estate decision-making.",
        "future_enhancements": "Live market data API integration\nNeighborhood heatmap visualization\nMortgage calculator module",
        "dataset": "Kaggle House Prices Dataset / Boston Housing Dataset",
        "description": "Predicts residential property prices using Linear Regression and Random Forest models based on location, size, and amenities.",
    },
    {
        "slug": "social-media-sentiment-analysis-system",
        "problem_statement": "Organizations struggle to analyze customer opinions from large volumes of social media content, making it difficult to understand public sentiment.",
        "objectives": "Analyze public sentiment from social media text\nClassify opinions as positive, negative, or neutral\nIdentify trending topics and keywords",
        "features": "Text sentiment analysis\nKeyword extraction\nTrend visualization dashboard",
        "tech_stack": "Python, NLTK, TextBlob, Pandas, Scikit-learn, Matplotlib, Jupyter Notebook",
        "algorithms": "Naive Bayes\nLogistic Regression",
        "conclusion": "Improves customer feedback analysis and helps organizations understand public opinion at scale.",
        "future_enhancements": "Real-time Twitter/X stream analysis\nMultilingual sentiment support\nBrand monitoring dashboard",
        "dataset": "Twitter Sentiment Analysis Dataset (Kaggle)",
        "description": "Analyzes sentiment of social media posts using NLP and text classification models to classify opinions and identify trends.",
    },
    {
        "slug": "loan-approval-prediction-system",
        "problem_statement": "Banks struggle to evaluate loan applications quickly and accurately, leading to delays and potential financial risk from bad loans.",
        "objectives": "Predict loan approval status automatically\nReduce financial risk from bad loans\nImprove the speed and accuracy of loan decisions",
        "features": "Loan applicant data analysis\nRisk classification\nApproval prediction output",
        "tech_stack": "Python, Pandas, NumPy, Scikit-learn, Matplotlib, Jupyter Notebook",
        "algorithms": "Decision Tree\nLogistic Regression",
        "conclusion": "Enhances loan risk management by automating approval decisions with high accuracy.",
        "future_enhancements": "Real-time credit score API integration\nExplainable AI for decision transparency\nMobile loan application portal",
        "dataset": "Loan Prediction Dataset (Kaggle / Analytics Vidhya)",
        "description": "Predicts loan approval decisions based on applicant financial and demographic data using Decision Tree and Logistic Regression.",
    },
    {
        "slug": "energy-consumption-forecasting-system",
        "problem_statement": "Energy providers face difficulty predicting power demand accurately, leading to resource wastage and supply-demand imbalances.",
        "objectives": "Predict future energy consumption patterns\nOptimize resource allocation for power grids\nReduce energy waste through accurate forecasting",
        "features": "Consumption trend analysis\nDemand forecasting\nVisualization dashboard",
        "tech_stack": "Python, Pandas, NumPy, Scikit-learn, Statsmodels, Matplotlib, Jupyter Notebook",
        "algorithms": "ARIMA Time Series Forecasting\nLinear Regression",
        "conclusion": "Improves energy distribution efficiency through accurate demand forecasting and resource optimization.",
        "future_enhancements": "Smart meter data integration\nRenewable energy source optimization\nReal-time grid monitoring dashboard",
        "dataset": "UCI Energy Consumption Dataset / Kaggle Energy Dataset",
        "description": "Forecasts building or city energy consumption using time series and ML models to optimize power distribution.",
    },
    {
        "slug": "weather-prediction-using-machine-learning",
        "problem_statement": "Accurate weather prediction is critical for agriculture, disaster management, and daily planning, but traditional models are complex and resource-intensive.",
        "objectives": "Predict weather conditions using historical data\nAnalyze long-term climate trends\nImprove planning decisions for agriculture and disaster management",
        "features": "Weather condition forecasting\nTrend visualization\nClimate pattern monitoring",
        "tech_stack": "Python, Pandas, NumPy, Scikit-learn, Statsmodels, Matplotlib, Jupyter Notebook",
        "algorithms": "Random Forest Regression\nARIMA Time Series Model",
        "conclusion": "Supports climate prediction systems and improves planning accuracy for agriculture and disaster preparedness.",
        "future_enhancements": "Live weather API integration\nSevere weather alert system\nRegional climate change analysis",
        "dataset": "NOAA Weather Dataset / Kaggle Weather Prediction Dataset",
        "description": "Predicts weather conditions using historical meteorological data and ML algorithms including Random Forest and ARIMA.",
    },
]


class Command(BaseCommand):
    help = 'Update Data Science projects 66-70 with full detail content'

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
