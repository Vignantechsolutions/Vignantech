// Interactive Project Recommender
class ProjectRecommender {
    constructor() {
        this.currentStep = 0;
        this.answers = {};
        this.questions = [
            {
                id: 'interest',
                question: 'What interests you most?',
                options: [
                    { value: 'ai', label: 'Artificial Intelligence & Machine Learning', icon: 'fas fa-brain' },
                    { value: 'web', label: 'Web Development & Full-Stack', icon: 'fas fa-globe' },
                    { value: 'mobile', label: 'Mobile App Development', icon: 'fas fa-mobile-alt' },
                    { value: 'data', label: 'Data Science & Analytics', icon: 'fas fa-chart-bar' }
                ]
            },
            {
                id: 'experience',
                question: 'What\'s your programming experience level?',
                options: [
                    { value: 'beginner', label: 'Beginner (Basic programming knowledge)', icon: 'fas fa-seedling' },
                    { value: 'intermediate', label: 'Intermediate (Some project experience)', icon: 'fas fa-tree' },
                    { value: 'advanced', label: 'Advanced (Strong technical skills)', icon: 'fas fa-rocket' }
                ]
            },
            {
                id: 'domain',
                question: 'Which application domain excites you?',
                options: [
                    { value: 'healthcare', label: 'Healthcare & Medical', icon: 'fas fa-heartbeat' },
                    { value: 'finance', label: 'Finance & Banking', icon: 'fas fa-coins' },
                    { value: 'education', label: 'Education & E-Learning', icon: 'fas fa-graduation-cap' },
                    { value: 'ecommerce', label: 'E-Commerce & Business', icon: 'fas fa-shopping-cart' },
                    { value: 'social', label: 'Social Media & Communication', icon: 'fas fa-users' }
                ]
            },
            {
                id: 'timeline',
                question: 'When do you need the project completed?',
                options: [
                    { value: 'urgent', label: 'Within 2 weeks (Rush delivery)', icon: 'fas fa-clock' },
                    { value: 'normal', label: '2-4 weeks (Standard timeline)', icon: 'fas fa-calendar-alt' },
                    { value: 'flexible', label: '1-2 months (Flexible timeline)', icon: 'fas fa-calendar-check' }
                ]
            },
            {
                id: 'budget',
                question: 'What\'s your budget range?',
                options: [
                    { value: 'low', label: '₹8,000 - ₹15,000 (Budget-friendly)', icon: 'fas fa-rupee-sign' },
                    { value: 'medium', label: '₹15,000 - ₹25,000 (Standard)', icon: 'fas fa-coins' },
                    { value: 'high', label: '₹25,000+ (Premium features)', icon: 'fas fa-gem' }
                ]
            }
        ];
        this.init();
    }

    init() {
        this.createRecommenderWidget();
        this.setupEventListeners();
        this.showQuestion();
    }

    createRecommenderWidget() {
        const recommenderHTML = `
            <div id="project-recommender" class="recommender-widget">
                <div class="recommender-trigger" id="recommender-trigger">
                    <i class="fas fa-magic"></i>
                    <span>Find Your Perfect Project</span>
                </div>
                <div class="recommender-modal" id="recommender-modal">
                    <div class="recommender-content">
                        <div class="recommender-header">
                            <h3>🎯 Find Your Perfect Final-Year Project</h3>
                            <button class="recommender-close" id="recommender-close">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="progress-fill"></div>
                        </div>
                        <div class="question-container" id="question-container">
                            <!-- Questions will be inserted here -->
                        </div>
                        <div class="navigation-buttons">
                            <button id="prev-btn" class="nav-btn" disabled>Previous</button>
                            <button id="next-btn" class="nav-btn">Next</button>
                        </div>
                        <div class="recommendation-result" id="recommendation-result" style="display: none;">
                            <!-- Results will be shown here -->
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', recommenderHTML);
        this.addRecommenderStyles();
    }

    addRecommenderStyles() {
        const styles = `
            <style>
                .recommender-widget {
                    position: fixed;
                    top: 50%;
                    right: 20px;
                    transform: translateY(-50%);
                    z-index: 9999;
                    font-family: 'Poppins', sans-serif;
                }
                .recommender-trigger {
                    background: linear-gradient(135deg, #1B3A6B 0%, #2563EB 100%);
                    color: white;
                    padding: 12px 20px;
                    border-radius: 25px;
                    cursor: pointer;
                    box-shadow: 0 4px 15px rgba(27, 58, 107, 0.3);
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    animation: pulse-widget 2.5s infinite;
                }
                .recommender-trigger:hover {
                    transform: scale(1.05);
                    box-shadow: 0 6px 20px rgba(27, 58, 107, 0.5);
                }
                .recommender-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(15, 23, 42, 0.75);
                    backdrop-filter: blur(4px);
                    display: none;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                }
                .recommender-modal.active {
                    display: flex;
                }
                .recommender-content {
                    background: white;
                    border-radius: 20px;
                    padding: 30px;
                    max-width: 600px;
                    width: 90%;
                    max-height: 85vh;
                    overflow-y: auto;
                    position: relative;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.15);
                    border: 1px solid rgba(0,0,0,0.05);
                }
                .recommender-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }
                .recommender-header h3 {
                    color: #0F172A;
                    margin: 0;
                    font-size: 1.25rem;
                    font-weight: 700;
                }
                .recommender-close {
                    background: none;
                    border: none;
                    font-size: 20px;
                    cursor: pointer;
                    color: #64748B;
                    transition: color 0.2s;
                }
                .recommender-close:hover {
                    color: #0F172A;
                }
                .progress-bar {
                    width: 100%;
                    height: 6px;
                    background: #F1F5F9;
                    border-radius: 3px;
                    margin-bottom: 30px;
                    overflow: hidden;
                }
                .progress-fill {
                    height: 100%;
                    background: linear-gradient(135deg, #1B3A6B 0%, #2563EB 100%);
                    width: 0%;
                    transition: width 0.3s ease;
                }
                .question-container {
                    margin-bottom: 30px;
                }
                .question-title {
                    font-size: 1.1rem;
                    color: #0F172A;
                    margin-bottom: 20px;
                    font-weight: 700;
                }
                .options-grid {
                    display: grid;
                    gap: 12px;
                }
                .option-card {
                    border: 1.5px solid #E2E8F0;
                    border-radius: 12px;
                    padding: 14px 18px;
                    cursor: pointer;
                    transition: all 0.25s ease;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                .option-card:hover {
                    border-color: #2563EB;
                    background: #F8FAFC;
                    transform: translateX(4px);
                }
                .option-card.selected {
                    border-color: #2563EB;
                    background: #EFF6FF;
                    box-shadow: 0 0 0 1px #2563EB;
                }
                .option-icon {
                    font-size: 1.3rem;
                    color: #2563EB;
                    width: 30px;
                    text-align: center;
                }
                .option-text {
                    flex: 1;
                    color: #1E293B;
                    font-weight: 600;
                    font-size: 0.92rem;
                }
                .navigation-buttons {
                    display: flex;
                    justify-content: space-between;
                    gap: 15px;
                }
                .nav-btn {
                    padding: 12px 24px;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: 700;
                    font-size: 0.9rem;
                    transition: all 0.3s ease;
                    flex: 1;
                }
                .nav-btn:disabled {
                    background: #E2E8F0;
                    color: #94A3B8;
                    cursor: not-allowed;
                }
                #prev-btn {
                    background: #64748B;
                    color: white;
                }
                #prev-btn:not(:disabled):hover {
                    background: #475569;
                }
                #next-btn {
                    background: #2563EB;
                    color: white;
                }
                #next-btn:not(:disabled):hover {
                    background: #1D4ED8;
                }
                .recommendation-result {
                    text-align: center;
                }
                .result-card {
                    background: linear-gradient(135deg, #1B3A6B 0%, #2563EB 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 18px;
                    margin-bottom: 20px;
                    box-shadow: 0 10px 24px rgba(27,58,107,0.3);
                }
                .result-title {
                    font-size: 1.35rem;
                    font-weight: 800;
                    margin-bottom: 12px;
                }
                .result-description {
                    font-size: 0.95rem;
                    margin-bottom: 20px;
                    opacity: 0.9;
                    line-height: 1.6;
                }
                .result-features {
                    text-align: left;
                    margin-bottom: 24px;
                    background: rgba(255,255,255,0.06);
                    padding: 18px;
                    border-radius: 10px;
                    border: 1px solid rgba(255,255,255,0.1);
                }
                .result-features ul {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }
                .result-features li {
                    padding: 6px 0;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    font-size: 0.88rem;
                    font-weight: 500;
                }
                .result-features i {
                    color: #4ADE80;
                }
                .result-actions {
                    display: flex;
                    gap: 12px;
                    justify-content: center;
                    flex-wrap: wrap;
                }
                .result-btn {
                    padding: 10px 20px;
                    border: 2px solid white;
                    background: transparent;
                    color: white;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: 700;
                    font-size: 0.85rem;
                    text-decoration: none;
                    transition: all 0.3s ease;
                }
                .result-btn:hover {
                    background: white;
                    color: #1B3A6B;
                }
                @keyframes pulse-widget {
                    0% { box-shadow: 0 4px 15px rgba(27, 58, 107, 0.35); }
                    50% { box-shadow: 0 4px 25px rgba(27, 58, 107, 0.65); transform: translateY(-50%) scale(1.03); }
                    100% { box-shadow: 0 4px 15px rgba(27, 58, 107, 0.35); }
                }
                @media (max-width: 768px) {
                    .recommender-widget {
                        position: relative;
                        right: auto;
                        top: auto;
                        transform: none;
                        margin: 20px auto;
                        display: flex;
                        justify-content: center;
                        z-index: 100;
                    }
                    .recommender-trigger {
                        animation: none;
                        transform: none;
                    }
                    .recommender-trigger:hover {
                        transform: scale(1.02);
                    }
                    .recommender-content {
                        padding: 20px;
                        margin: 20px;
                    }
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', styles);
    }

    setupEventListeners() {
        document.getElementById('recommender-trigger').addEventListener('click', () => this.openModal());
        document.getElementById('recommender-close').addEventListener('click', () => this.closeModal());
        document.getElementById('prev-btn').addEventListener('click', () => this.previousQuestion());
        document.getElementById('next-btn').addEventListener('click', () => this.nextQuestion());
        
        document.getElementById('recommender-modal').addEventListener('click', (e) => {
            if (e.target.id === 'recommender-modal') this.closeModal();
        });
    }

    openModal() {
        document.getElementById('recommender-modal').classList.add('active');
        document.body.style.overflow = 'hidden';
        this.restart();
    }

    closeModal() {
        document.getElementById('recommender-modal').classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    showQuestion() {
        if (this.currentStep >= this.questions.length) {
            this.showRecommendation();
            return;
        }

        const question = this.questions[this.currentStep];
        const container = document.getElementById('question-container');
        
        container.innerHTML = `
            <div class="question-title">${question.question}</div>
            <div class="options-grid">
                ${question.options.map(option => `
                    <div class="option-card" data-value="${option.value}">
                        <div class="option-icon">
                            <i class="${option.icon}"></i>
                        </div>
                        <div class="option-text">${option.label}</div>
                    </div>
                `).join('')}
            </div>
        `;

        // Add click listeners to options
        container.querySelectorAll('.option-card').forEach(card => {
            card.addEventListener('click', () => this.selectOption(card));
        });

        this.updateProgress();
        this.updateNavigation();
    }

    selectOption(selectedCard) {
        const container = document.getElementById('question-container');
        container.querySelectorAll('.option-card').forEach(card => {
            card.classList.remove('selected');
        });
        selectedCard.classList.add('selected');
        
        const question = this.questions[this.currentStep];
        this.answers[question.id] = selectedCard.dataset.value;
        
        document.getElementById('next-btn').disabled = false;
    }

    nextQuestion() {
        if (this.currentStep < this.questions.length) {
            this.currentStep++;
            this.showQuestion();
        }
    }

    previousQuestion() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.showQuestion();
        }
    }

    updateProgress() {
        const progress = ((this.currentStep + 1) / this.questions.length) * 100;
        document.getElementById('progress-fill').style.width = `${progress}%`;
    }

    updateNavigation() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        
        prevBtn.disabled = this.currentStep === 0;
        nextBtn.disabled = !this.answers[this.questions[this.currentStep]?.id];
        
        if (this.currentStep === this.questions.length - 1) {
            nextBtn.textContent = 'Get Recommendation';
        } else {
            nextBtn.textContent = 'Next';
        }
    }

    showRecommendation() {
        const recommendation = this.generateRecommendation();
        
        document.getElementById('question-container').style.display = 'none';
        document.querySelector('.navigation-buttons').style.display = 'none';
        
        const resultContainer = document.getElementById('recommendation-result');
        resultContainer.style.display = 'block';
        resultContainer.innerHTML = `
            <div class="result-card">
                <div class="result-title">${recommendation.title}</div>
                <div class="result-description">${recommendation.description}</div>
                <div class="result-features">
                    <ul>
                        ${recommendation.features.map(feature => `
                            <li><i class="fas fa-check"></i> ${feature}</li>
                        `).join('')}
                    </ul>
                </div>
                <div class="result-actions">
                    <a href="/contact/" class="result-btn">Get Quote</a>
                    <a href="/corporate-training/" class="result-btn">View Services</a>
                    <button class="result-btn" onclick="projectRecommender.restart()">Try Again</button>
                </div>
            </div>
        `;
    }

    generateRecommendation() {
        const { interest, experience, domain, timeline, budget } = this.answers;
        
        // AI/ML Recommendations
        if (interest === 'ai') {
            if (domain === 'healthcare') {
                return {
                    title: '🏥 AI Healthcare Diagnosis System',
                    description: 'Build an intelligent medical diagnosis system using computer vision and machine learning to analyze medical images and provide preliminary diagnosis.',
                    features: [
                        'Medical image analysis using CNN',
                        'Disease prediction algorithms',
                        'Patient data management',
                        'Doctor dashboard with analytics',
                        'Complete documentation & deployment'
                    ]
                };
            }
            return {
                title: '🤖 Smart AI Recommendation Engine',
                description: 'Create an intelligent recommendation system using collaborative filtering and deep learning to provide personalized suggestions.',
                features: [
                    'Advanced ML algorithms',
                    'Real-time recommendations',
                    'User behavior analysis',
                    'Scalable architecture',
                    'Performance optimization'
                ]
            };
        }
        
        // Web Development Recommendations
        if (interest === 'web') {
            if (domain === 'education') {
                return {
                    title: '📚 Complete E-Learning Platform',
                    description: 'Build a comprehensive online learning management system with course creation, student tracking, and interactive features.',
                    features: [
                        'Course management system',
                        'Video streaming integration',
                        'Interactive quizzes & assessments',
                        'Progress tracking dashboard',
                        'Payment gateway integration'
                    ]
                };
            }
            return {
                title: '🛒 Modern E-Commerce Platform',
                description: 'Develop a full-featured online shopping platform with advanced features like real-time inventory and payment processing.',
                features: [
                    'Product catalog management',
                    'Shopping cart & checkout',
                    'Payment gateway integration',
                    'Order tracking system',
                    'Admin dashboard'
                ]
            };
        }
        
        // Default recommendation
        return {
            title: '🚀 Custom Full-Stack Application',
            description: 'A tailored web application built with modern technologies to meet your specific requirements and academic goals.',
            features: [
                'Modern responsive design',
                'Secure user authentication',
                'Database integration',
                'API development',
                'Complete documentation'
            ]
        };
    }

    restart() {
        this.currentStep = 0;
        this.answers = {};
        document.getElementById('question-container').style.display = 'block';
        document.querySelector('.navigation-buttons').style.display = 'flex';
        document.getElementById('recommendation-result').style.display = 'none';
        this.showQuestion();
    }
}

// Initialize Project Recommender
document.addEventListener('DOMContentLoaded', () => {
    window.projectRecommender = new ProjectRecommender();
});
