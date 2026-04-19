from django.core.management.base import BaseCommand
from django.utils.text import slugify
from projects.models import Project

AIML_PROJECTS = [
    ("AI-Based Multi-Disease Prediction System", "Predicts multiple diseases using patient health data with ML classification algorithms.", "Python, Scikit-learn, Flask, Pandas, NumPy"),
    ("Intelligent Plant Disease Detection Using Deep Learning", "Detects plant diseases from leaf images using CNN-based deep learning models.", "Python, TensorFlow, Keras, OpenCV, Flask"),
    ("AI Resume Screening and Candidate Ranking System", "Automates resume parsing and ranks candidates using NLP and ML techniques.", "Python, NLTK, Scikit-learn, SpaCy, Django"),
    ("Fake News Detection Using Natural Language Processing", "Classifies news articles as real or fake using NLP and text classification models.", "Python, NLTK, Scikit-learn, TF-IDF, Flask"),
    ("Real-Time Emotion Detection from Facial Expressions", "Detects human emotions in real-time from webcam feed using deep learning.", "Python, OpenCV, TensorFlow, Keras, Flask"),
    ("Traffic Sign Recognition Using Convolutional Neural Networks", "Recognizes and classifies traffic signs from images using CNN architecture.", "Python, TensorFlow, Keras, OpenCV, NumPy"),
    ("AI-Based Voice Assistant with NLP", "A voice-controlled assistant that understands and responds to natural language commands.", "Python, SpeechRecognition, NLTK, pyttsx3, Flask"),
    ("Handwritten Digit Recognition Using Deep Learning", "Recognizes handwritten digits using a trained deep neural network on MNIST dataset.", "Python, TensorFlow, Keras, NumPy, Matplotlib"),
    ("Real-Time Object Detection Using YOLO Algorithm", "Detects and labels multiple objects in real-time video streams using YOLO.", "Python, OpenCV, YOLOv5, PyTorch, Flask"),
    ("AI-Based Customer Support Chatbot System", "An intelligent chatbot that handles customer queries using NLP and intent classification.", "Python, NLTK, TensorFlow, Flask, JSON"),
    ("Stock Price Prediction Using LSTM Networks", "Predicts future stock prices using Long Short-Term Memory recurrent neural networks.", "Python, TensorFlow, Keras, Pandas, Matplotlib"),
    ("Personalized Recommendation System Using Machine Learning", "Recommends products or content to users based on collaborative and content-based filtering.", "Python, Scikit-learn, Pandas, NumPy, Flask"),
    ("Fake Social Media Profile Detection Using Machine Learning", "Identifies fake or bot social media profiles using ML classification on profile features.", "Python, Scikit-learn, Pandas, Flask, Matplotlib"),
    ("Automatic Text Summarization Using Transformers", "Generates concise summaries of long documents using transformer-based NLP models.", "Python, HuggingFace Transformers, PyTorch, Flask"),
    ("AI-Based Image Caption Generator Using CNN-LSTM", "Generates descriptive captions for images by combining CNN feature extraction with LSTM.", "Python, TensorFlow, Keras, OpenCV, Flask"),
]


class Command(BaseCommand):
    help = 'Seed 15 AIML projects'

    def handle(self, *args, **kwargs):
        created = 0
        for title, description, tech_stack in AIML_PROJECTS:
            slug = slugify(title)[:50]
            if not Project.objects.filter(slug=slug).exists():
                Project.objects.create(
                    title=title,
                    slug=slug,
                    description=description,
                    tech_stack=tech_stack,
                    category='aiml',
                    is_active=True,
                )
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created} AIML projects.'))
