from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "ai-based-food-delivery-time-prediction-system",
        "problem_statement": "Food delivery companies struggle to estimate delivery time accurately due to varying factors such as distance, traffic, weather, and order volume.",
        "objectives": "Predict food delivery time accurately\nImprove customer satisfaction\nOptimize delivery operations\nReduce delivery delays",
        "features": "Order data input\nDelivery time prediction\nRoute distance calculation\nAdmin dashboard\nVisualization of delivery trends",
        "tech_stack": "Python, Flask, HTML, CSS, JavaScript, Bootstrap, MySQL, Pandas, NumPy, Scikit-learn",
        "algorithms": "Random Forest\nLinear Regression",
        "conclusion": "Enhances operational efficiency in food delivery services through accurate time prediction.",
        "future_enhancements": "Real-time GPS route integration\nWeather API for dynamic prediction\nMobile app support",
        "dataset": "Custom food delivery historical dataset",
        "description": "Predicts food delivery time using ML models based on distance, traffic, and order details to improve customer satisfaction.",
    },
    {
        "slug": "plant-disease-detection-web-application",
        "problem_statement": "Farmers often fail to detect plant diseases early, resulting in significant crop loss and reduced agricultural productivity.",
        "objectives": "Detect plant diseases from leaf images\nProvide treatment recommendations\nImprove agricultural productivity",
        "features": "Leaf image upload\nDisease prediction\nTreatment suggestion\nDisease history logs",
        "tech_stack": "Python, Flask, HTML, CSS, JavaScript, TensorFlow, OpenCV, MySQL",
        "algorithms": "Convolutional Neural Network (CNN)\nImage Preprocessing Pipeline",
        "conclusion": "Improves crop health monitoring by enabling early and automated plant disease detection.",
        "future_enhancements": "Drone-based image capture\nMulti-crop disease support\nFarmer mobile app",
        "dataset": "PlantVillage Dataset — 54,000+ leaf images",
        "description": "Web app that detects plant diseases from uploaded leaf images using a CNN model and provides treatment recommendations.",
    },
    {
        "slug": "secure-online-voting-system-using-flask",
        "problem_statement": "Traditional voting systems face issues such as fraud, vote duplication, and accessibility limitations for remote voters.",
        "objectives": "Enable secure online voting\nPrevent vote duplication\nImprove voting transparency",
        "features": "Voter authentication\nVote casting system\nResult calculation\nAdmin dashboard",
        "tech_stack": "Python, Flask, HTML, CSS, JavaScript, MySQL, OTP Authentication",
        "algorithms": "AES Encryption Algorithm\nOTP-Based Authentication",
        "conclusion": "Improves voting reliability and accessibility through a secure, fraud-resistant digital platform.",
        "future_enhancements": "Blockchain-based vote ledger\nBiometric voter verification\nMulti-election support",
        "dataset": "Synthetic voter registration dataset",
        "description": "A secure digital voting platform with voter authentication, OTP verification, and real-time result display using Flask.",
    },
    {
        "slug": "smart-expense-tracker-and-budget-prediction-system",
        "problem_statement": "Individuals struggle to manage personal finances efficiently, often overspending due to lack of visibility into their spending patterns.",
        "objectives": "Track daily expenses accurately\nPredict future spending patterns\nProvide actionable budgeting insights",
        "features": "Expense logging\nBudget prediction\nMonthly reports\nVisualization dashboard",
        "tech_stack": "Python, Flask, HTML, CSS, JavaScript, SQLite, Pandas, Matplotlib",
        "algorithms": "Linear Regression\nExpense Trend Analysis",
        "conclusion": "Enhances personal financial control through intelligent expense tracking and budget forecasting.",
        "future_enhancements": "Bank account sync via API\nAI-based savings recommendations\nMobile app support",
        "dataset": "Custom personal expense dataset",
        "description": "Tracks personal expenses and predicts future spending using ML regression models with a visualization dashboard.",
    },
    {
        "slug": "online-book-recommendation-web-system",
        "problem_statement": "Users struggle to find books relevant to their interests among large collections, leading to poor reading experience.",
        "objectives": "Provide personalized book recommendations\nImprove user reading experience\nIncrease platform engagement",
        "features": "Book search\nRecommendation engine\nUser preference tracking",
        "tech_stack": "Python, Flask, HTML, CSS, MySQL, Scikit-learn, Pandas",
        "algorithms": "Collaborative Filtering\nContent-Based Filtering",
        "conclusion": "Enhances recommendation capabilities and improves user engagement on digital reading platforms.",
        "future_enhancements": "Integration with Google Books API\nReading progress tracker\nSocial reading features",
        "dataset": "Book-Crossing Dataset / Goodreads Dataset",
        "description": "Recommends books to users based on reading history and preferences using collaborative filtering.",
    },
]


class Command(BaseCommand):
    help = 'Update Python projects 31-35 with full detail content'

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
