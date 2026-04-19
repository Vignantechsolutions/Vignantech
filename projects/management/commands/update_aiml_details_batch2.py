from django.core.management.base import BaseCommand
from projects.models import Project

DETAILS = [
    {
        "slug": "traffic-sign-recognition-using-convolutional-neura",
        "problem_statement": "Road accidents frequently occur due to drivers missing or misinterpreting traffic signs. Manual monitoring systems are inefficient in recognizing signs in real time.",
        "objectives": "Detect traffic signs automatically\nClassify sign types accurately\nImprove road safety systems\nSupport autonomous driving technologies",
        "features": "Real-time sign detection\nImage classification\nTraffic sign alerts\nAccuracy visualization\nData logging",
        "tech_stack": "HTML, CSS, Python, Flask, TensorFlow, OpenCV, NumPy",
        "algorithms": "Convolutional Neural Network (CNN)\nImage Preprocessing Pipeline",
        "conclusion": "This system enhances transportation safety and supports intelligent driving solutions.",
        "future_enhancements": "Integration with GPS navigation systems\nNight-vision camera support\nReal-time driver alert notifications",
        "dataset": "German Traffic Sign Recognition Benchmark (GTSRB) — 50,000+ images",
        "description": "Recognizes and classifies traffic signs from images using CNN architecture to improve road safety and support autonomous driving.",
    },
    {
        "slug": "ai-based-voice-assistant-with-nlp",
        "problem_statement": "Many applications require hands-free control, but traditional input systems depend on manual interaction, limiting accessibility and efficiency.",
        "objectives": "Develop a voice-controlled system\nConvert speech into actionable commands\nAutomate task execution through voice",
        "features": "Voice recognition\nCommand processing\nTask execution\nSpeech response output",
        "tech_stack": "Python, SpeechRecognition, NLTK, pyttsx3, PyAudio",
        "algorithms": "Natural Language Processing (NLP)\nSpeech-to-Text Model",
        "conclusion": "Voice assistants enhance automation and improve usability for hands-free environments.",
        "future_enhancements": "Multi-language voice support\nSmart home device integration\nPersonalized voice profile learning",
        "dataset": "Custom voice command dataset",
        "description": "A voice-controlled assistant that understands and responds to natural language commands using NLP and speech recognition.",
    },
    {
        "slug": "handwritten-digit-recognition-using-deep-learning",
        "problem_statement": "Manual reading of handwritten digits is prone to errors, especially in postal, banking, and document processing systems.",
        "objectives": "Recognize handwritten digits accurately\nImprove digit classification accuracy\nAutomate data entry processes",
        "features": "Digit recognition from images\nImage preprocessing\nPrediction visualization",
        "tech_stack": "Python, TensorFlow, Keras, OpenCV, NumPy, Matplotlib",
        "algorithms": "Convolutional Neural Network (CNN)\nSoftmax Classification",
        "conclusion": "Automates digit recognition tasks effectively, reducing manual errors in data entry systems.",
        "future_enhancements": "Full handwritten text recognition\nMobile app integration\nMulti-language character support",
        "dataset": "MNIST Dataset — 70,000 handwritten digit images",
        "description": "Recognizes handwritten digits using a trained deep neural network on the MNIST dataset with high classification accuracy.",
    },
    {
        "slug": "real-time-object-detection-using-yolo-algorithm",
        "problem_statement": "Manual object detection is slow and inefficient in surveillance and automation systems, leading to delayed responses.",
        "objectives": "Detect objects in real time\nTrack multiple objects simultaneously\nImprove surveillance accuracy",
        "features": "Real-time object detection\nBounding box display\nMulti-object tracking",
        "tech_stack": "Python, OpenCV, YOLOv5, PyTorch, Flask",
        "algorithms": "YOLO (You Only Look Once)\nNon-Maximum Suppression (NMS)",
        "conclusion": "YOLO-based detection improves automation and monitoring systems with high-speed real-time performance.",
        "future_enhancements": "Edge device deployment\nCustom object class training\nIntegration with CCTV systems",
        "dataset": "COCO Dataset — 330,000+ images with 80 object categories",
        "description": "Detects and labels multiple objects in real-time video streams using the YOLO algorithm for surveillance and automation.",
    },
    {
        "slug": "ai-based-customer-support-chatbot-system",
        "problem_statement": "Customer support centers face high workloads due to repeated user queries, leading to slow response times and increased operational costs.",
        "objectives": "Provide automated customer responses\nReduce human workload\nImprove response time and availability",
        "features": "Chat interface\nQuery classification\nAutomated responses\nChat history storage",
        "tech_stack": "Python, Flask, NLTK, TensorFlow, MongoDB",
        "algorithms": "Natural Language Processing (NLP)\nTransformer-based Response Generation",
        "conclusion": "Chatbots enhance customer service efficiency and reduce operational costs with 24/7 availability.",
        "future_enhancements": "Multilingual support\nSentiment-aware responses\nCRM system integration",
        "dataset": "Custom FAQ and customer query dataset",
        "description": "An intelligent chatbot that handles customer queries using NLP and intent classification for automated support.",
    },
]


class Command(BaseCommand):
    help = 'Update AIML projects 6-10 with full detail content'

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
