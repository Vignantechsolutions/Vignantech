from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "employee-attrition-prediction-system",
        "problem_statement": "Organizations face challenges retaining employees, and unexpected resignations increase recruitment costs and reduce overall productivity.",
        "objectives": "Predict employee attrition risk\nIdentify key attrition risk factors\nImprove employee retention strategies\nSupport HR decision-making with data",
        "features": "Employee data analysis\nAttrition prediction\nRisk scoring dashboard\nEmployee retention insights",
        "tech_stack": "Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Jupyter Notebook",
        "algorithms": "Random Forest\nLogistic Regression",
        "conclusion": "Improves employee retention strategies and supports proactive HR workforce planning.",
        "future_enhancements": "Real-time HR system integration\nPersonalized retention recommendation engine\nDepartment-level attrition heatmap",
        "dataset": "IBM HR Analytics Employee Attrition Dataset (Kaggle)",
        "description": "Identifies employees at risk of leaving using HR data and Random Forest and Logistic Regression classification models.",
    },
    {
        "slug": "traffic-accident-analysis-and-prediction-system",
        "problem_statement": "Traffic accidents cause major safety risks, and identifying accident-prone zones is difficult without proper data analysis tools.",
        "objectives": "Analyze historical traffic accident data\nPredict accident-prone areas and zones\nImprove road safety planning",
        "features": "Accident trend visualization\nRisk zone detection\nSafety insights dashboard",
        "tech_stack": "Python, Pandas, Scikit-learn, Folium, Matplotlib, Seaborn, Jupyter Notebook",
        "algorithms": "K-Means Clustering\nLinear Regression Analysis",
        "conclusion": "Enhances road safety planning by identifying high-risk zones and predicting accident trends.",
        "future_enhancements": "Real-time traffic data integration\nGPS-based risk zone alerts\nGovernment road safety reporting module",
        "dataset": "US Accidents Dataset (Kaggle) — 2.8 million records",
        "description": "Analyzes traffic accident patterns and predicts high-risk zones using K-Means clustering and regression on accident data.",
    },
    {
        "slug": "disease-prediction-using-patient-health-records",
        "problem_statement": "Doctors require predictive tools to assist diagnosis using patient health data, especially in resource-limited healthcare settings.",
        "objectives": "Predict disease risk from patient health records\nSupport and assist medical diagnosis\nImprove healthcare decision-making speed",
        "features": "Patient data input form\nDisease prediction output\nRisk scoring",
        "tech_stack": "Python, Pandas, NumPy, Scikit-learn, Matplotlib, Jupyter Notebook",
        "algorithms": "K-Nearest Neighbors (KNN)\nDecision Tree",
        "conclusion": "Supports healthcare analytics and improves diagnosis speed through data-driven disease risk prediction.",
        "future_enhancements": "Integration with electronic health records (EHR)\nMulti-disease simultaneous prediction\nDoctor recommendation module",
        "dataset": "UCI Machine Learning Repository — Multiple disease datasets",
        "description": "Predicts disease likelihood from patient records using KNN and Decision Tree ensemble ML classifiers.",
    },
    {
        "slug": "customer-segmentation-using-clustering-algorithms",
        "problem_statement": "Businesses struggle to identify distinct customer groups based on purchasing behavior, making targeted marketing campaigns ineffective.",
        "objectives": "Segment customers into meaningful groups\nImprove targeted marketing campaigns\nIncrease sales through personalized offers",
        "features": "Customer grouping\nVisualization dashboard\nMarketing insights report",
        "tech_stack": "Python, Pandas, Scikit-learn, NumPy, Matplotlib, Seaborn, Jupyter Notebook",
        "algorithms": "K-Means Clustering\nHierarchical Clustering",
        "conclusion": "Enhances targeted marketing efficiency by grouping customers based on purchasing patterns and behavior.",
        "future_enhancements": "Real-time customer behavior tracking\nPersonalized product recommendation integration\nCRM system export",
        "dataset": "Mall Customer Segmentation Dataset (Kaggle)",
        "description": "Segments customers into groups using K-Means and hierarchical clustering algorithms based on purchasing behavior.",
    },
    {
        "slug": "stock-market-trend-prediction-using-deep-learning",
        "problem_statement": "Stock market trends are difficult to predict manually due to high volatility and complex sequential dependencies in historical price data.",
        "objectives": "Predict future stock price trends\nAnalyze historical market patterns\nAssist investors in data-driven decisions",
        "features": "Stock data visualization\nTrend prediction\nForecast dashboard",
        "tech_stack": "Python, TensorFlow, Keras, Pandas, NumPy, Matplotlib, Jupyter Notebook",
        "algorithms": "Long Short-Term Memory (LSTM)\nTime Series Forecasting",
        "conclusion": "Supports data-driven investment strategies by accurately forecasting stock market trends using deep learning.",
        "future_enhancements": "Live stock market API integration\nSentiment analysis from financial news\nPortfolio optimization module",
        "dataset": "Yahoo Finance Historical Stock Data",
        "description": "Predicts stock market trends using LSTM deep learning on historical price data for investment decision support.",
    },
]


class Command(BaseCommand):
    help = 'Update Data Science projects 71-75 with full detail content'

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
