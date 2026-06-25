// Interactive Tech Stack Visualizer
class TechStackVisualizer {
    constructor() {
        this.techStacks = {
            'ai-ml': {
                title: 'AI/ML Stack',
                color: '#2563EB',
                technologies: [
                    { name: 'Python', icon: 'fab fa-python', description: 'Core programming language' },
                    { name: 'TensorFlow', icon: 'fas fa-brain', description: 'Deep learning framework' },
                    { name: 'PyTorch', icon: 'fas fa-fire', description: 'ML research framework' },
                    { name: 'OpenCV', icon: 'fas fa-eye', description: 'Computer vision library' },
                    { name: 'Scikit-learn', icon: 'fas fa-chart-line', description: 'Machine learning toolkit' },
                    { name: 'Flask/FastAPI', icon: 'fas fa-server', description: 'Web framework for APIs' }
                ]
            },
            'java': {
                title: 'Java Full-Stack',
                color: '#D97706',
                technologies: [
                    { name: 'Java 17', icon: 'fab fa-java', description: 'Enterprise programming language' },
                    { name: 'Spring Boot', icon: 'fas fa-leaf', description: 'Backend framework' },
                    { name: 'Spring Security', icon: 'fas fa-shield-alt', description: 'Authentication & authorization' },
                    { name: 'React/Angular', icon: 'fab fa-react', description: 'Frontend framework' },
                    { name: 'MySQL/PostgreSQL', icon: 'fas fa-database', description: 'Relational database' },
                    { name: 'Docker', icon: 'fab fa-docker', description: 'Containerization platform' }
                ]
            },
            'python': {
                title: 'Python Full-Stack',
                color: '#059669',
                technologies: [
                    { name: 'Python 3.9+', icon: 'fab fa-python', description: 'Modern Python version' },
                    { name: 'Django/Flask', icon: 'fas fa-globe', description: 'Web framework' },
                    { name: 'Vue.js/React', icon: 'fab fa-react', description: 'Frontend framework' },
                    { name: 'PostgreSQL', icon: 'fas fa-database', description: 'Advanced SQL database' },
                    { name: 'Redis', icon: 'fas fa-memory', description: 'In-memory data store' },
                    { name: 'Celery', icon: 'fas fa-tasks', description: 'Async task queue' }
                ]
            },
            'mern': {
                title: 'MERN Stack',
                color: '#DC2626',
                technologies: [
                    { name: 'MongoDB', icon: 'fas fa-database', description: 'NoSQL database' },
                    { name: 'Express.js', icon: 'fas fa-server', description: 'Backend framework' },
                    { name: 'React.js', icon: 'fab fa-react', description: 'Frontend library' },
                    { name: 'Node.js', icon: 'fab fa-node-js', description: 'JavaScript runtime' },
                    { name: 'Socket.io', icon: 'fas fa-bolt', description: 'Real-time communication' },
                    { name: 'JWT', icon: 'fas fa-key', description: 'Authentication tokens' }
                ]
            }
        };
        this.init();
    }

    init() {
        this.createVisualizerSection();
        this.setupEventListeners();
    }

    createVisualizerSection() {
        const visualizerHTML = `
            <section class="tech-visualizer-section" id="tech-visualizer">
                <div class="container">
                    <div class="text-center mb-5">
                        <span class="section-badge" style="background:rgba(255,255,255,0.15);color:#fff;border:1px solid rgba(255,255,255,0.2)">Interactive Stack Explorer</span>
                        <h2 class="section-title text-white">🛠️ Advanced Tech Stack Explorer</h2>
                        <p class="section-subtitle text-white-50">Hover over each stack card to explore the specific technologies we teach and build with</p>
                    </div>
                    
                    <div class="tech-stacks-grid">
                        ${Object.entries(this.techStacks).map(([key, stack]) => `
                            <div class="tech-stack-card" data-stack="${key}">
                                <div class="stack-header">
                                    <div class="stack-icon" style="background: ${stack.color}">
                                        <i class="fas fa-code"></i>
                                    </div>
                                    <h3>${stack.title}</h3>
                                </div>
                                <div class="stack-preview">
                                    <div class="tech-icons">
                                        ${stack.technologies.slice(0, 4).map(tech => `
                                            <div class="tech-icon-mini">
                                                <i class="${tech.icon}"></i>
                                            </div>
                                        `).join('')}
                                        ${stack.technologies.length > 4 ? '<div class="tech-more">+' + (stack.technologies.length - 4) + '</div>' : ''}
                                    </div>
                                </div>
                                <div class="stack-overlay">
                                    <div class="tech-details">
                                        ${stack.technologies.map(tech => `
                                            <div class="tech-item">
                                                <div class="tech-icon">
                                                    <i class="${tech.icon}"></i>
                                                </div>
                                                <div class="tech-info">
                                                    <div class="tech-name">${tech.name}</div>
                                                    <div class="tech-desc">${tech.description}</div>
                                                </div>
                                            </div>
                                        `).join('')}
                                    </div>
                                    <div class="stack-actions">
                                        <button class="stack-btn" onclick="window.location.href='/corporate-training/'">
                                            Learn More
                                        </button>
                                        <button class="stack-btn secondary" onclick="window.location.href='/contact/'">
                                            Get Quote
                                        </button>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>

                    <div class="tech-comparison">
                        <h3>🔍 Technology Stack Matrix</h3>
                        <div class="comparison-table">
                            <div class="comparison-header">
                                <div class="comparison-cell">Feature</div>
                                <div class="comparison-cell">AI/ML</div>
                                <div class="comparison-cell">Java</div>
                                <div class="comparison-cell">Python</div>
                                <div class="comparison-cell">MERN</div>
                            </div>
                            <div class="comparison-row">
                                <div class="comparison-cell feature">Best For</div>
                                <div class="comparison-cell">Data Science &amp; Intelligence</div>
                                <div class="comparison-cell">Enterprise Backend Systems</div>
                                <div class="comparison-cell">Scalable Web Apps &amp; APIs</div>
                                <div class="comparison-cell">Modern Responsive SPA Web Apps</div>
                            </div>
                            <div class="comparison-row">
                                <div class="comparison-cell feature">Difficulty</div>
                                <div class="comparison-cell">Advanced</div>
                                <div class="comparison-cell">Intermediate</div>
                                <div class="comparison-cell">Beginner-Friendly</div>
                                <div class="comparison-cell">Intermediate</div>
                            </div>
                            <div class="comparison-row">
                                <div class="comparison-cell feature">Timeline</div>
                                <div class="comparison-cell">3-4 weeks</div>
                                <div class="comparison-cell">2-3 weeks</div>
                                <div class="comparison-cell">2-3 weeks</div>
                                <div class="comparison-cell">1-2 weeks</div>
                            </div>
                            <div class="comparison-row">
                                <div class="comparison-cell feature">Price Range</div>
                                <div class="comparison-cell">₹15K - 35K</div>
                                <div class="comparison-cell">₹12K - 28K</div>
                                <div class="comparison-cell">₹10K - 25K</div>
                                <div class="comparison-cell">₹8K - 22K</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        `;

        // Insert after services section or append to body
        const servicesSection = document.getElementById('services');
        if (servicesSection) {
            servicesSection.insertAdjacentHTML('afterend', visualizerHTML);
        } else {
            document.body.insertAdjacentHTML('beforeend', visualizerHTML);
        }

        this.addVisualizerStyles();
    }

    addVisualizerStyles() {
        const styles = `
            <style>
                .tech-visualizer-section {
                    padding: 80px 0;
                    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #0F172A 100%);
                    color: white;
                    position: relative;
                    overflow: hidden;
                    font-family: 'Poppins', sans-serif;
                }

                .tech-visualizer-section::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
                    opacity: 0.8;
                }

                .tech-visualizer-section .container {
                    position: relative;
                    z-index: 2;
                }

                .tech-visualizer-section .section-title {
                    color: white;
                    text-align: center;
                    margin-bottom: 0.5rem;
                    font-weight: 800;
                    font-size: 2rem;
                }

                .tech-visualizer-section .section-subtitle {
                    text-align: center;
                    font-size: 1rem;
                    opacity: 0.8;
                    margin-bottom: 3rem;
                }

                .tech-stacks-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                    gap: 30px;
                    margin-bottom: 60px;
                }

                .tech-stack-card {
                    background: rgba(255, 255, 255, 0.03);
                    backdrop-filter: blur(12px);
                    border-radius: 20px;
                    padding: 25px;
                    position: relative;
                    cursor: pointer;
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    overflow: hidden;
                }

                .tech-stack-card:hover {
                    transform: translateY(-10px);
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
                    border-color: rgba(255,255,255,0.15);
                }

                .stack-header {
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    margin-bottom: 20px;
                }

                .stack-icon {
                    width: 46px;
                    height: 46px;
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 18px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                }

                .stack-header h3 {
                    margin: 0;
                    font-size: 1.15rem;
                    font-weight: 700;
                }

                .stack-preview {
                    margin-bottom: 10px;
                }

                .tech-icons {
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }

                .tech-icon-mini {
                    width: 35px;
                    height: 35px;
                    background: rgba(255, 255, 255, 0.08);
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 14px;
                    transition: all 0.3s ease;
                    border: 1px solid rgba(255, 255, 255, 0.05);
                }

                .tech-icon-mini:hover {
                    background: rgba(255, 255, 255, 0.2);
                    transform: scale(1.1);
                }

                .tech-more {
                    width: 35px;
                    height: 35px;
                    background: rgba(255, 255, 255, 0.12);
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    font-weight: 600;
                }

                .stack-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(15, 23, 42, 0.96);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 25px;
                    opacity: 0;
                    transform: translateY(20px);
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                }

                .tech-stack-card:hover .stack-overlay {
                    opacity: 1;
                    transform: translateY(0);
                }

                .tech-details {
                    flex: 1;
                    overflow-y: auto;
                    scrollbar-width: none;
                }
                .tech-details::-webkit-scrollbar { display: none; }

                .tech-item {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    margin-bottom: 12px;
                    padding: 6px;
                    border-radius: 8px;
                    transition: background 0.3s ease;
                }

                .tech-item:hover {
                    background: rgba(255, 255, 255, 0.06);
                }

                .tech-item .tech-icon {
                    width: 28px;
                    height: 28px;
                    background: rgba(255, 255, 255, 0.08);
                    border-radius: 6px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 13px;
                }

                .tech-info {
                    flex: 1;
                }

                .tech-name {
                    font-weight: 600;
                    margin-bottom: 1px;
                    font-size: 0.88rem;
                }

                .tech-desc {
                    font-size: 11px;
                    opacity: 0.65;
                    line-height: 1.3;
                }

                .stack-actions {
                    display: flex;
                    gap: 10px;
                    margin-top: 15px;
                }

                .stack-btn {
                    flex: 1;
                    padding: 8px 12px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 700;
                    font-size: 0.8rem;
                    transition: all 0.3s ease;
                    background: white;
                    color: #0F172A;
                }

                .stack-btn.secondary {
                    background: transparent;
                    color: white;
                    border: 1.5px solid white;
                }

                .stack-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(255,255,255,0.15);
                }

                .stack-btn.secondary:hover {
                    background: white;
                    color: #0F172A;
                }

                .tech-comparison {
                    background: rgba(255, 255, 255, 0.02);
                    backdrop-filter: blur(12px);
                    border-radius: 20px;
                    padding: 30px;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                }

                .tech-comparison h3 {
                    text-align: center;
                    margin-bottom: 25px;
                    font-size: 1.25rem;
                    font-weight: 700;
                }

                .comparison-table {
                    display: grid;
                    grid-template-columns: 1.2fr 1fr 1fr 1fr 1fr;
                    gap: 1px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    overflow: hidden;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                }

                .comparison-header {
                    display: contents;
                }

                .comparison-header .comparison-cell {
                    background: rgba(255, 255, 255, 0.08);
                    font-weight: 700;
                    text-align: center;
                    color: white;
                }

                .comparison-row {
                    display: contents;
                }

                .comparison-cell {
                    padding: 14px 10px;
                    background: rgba(255, 255, 255, 0.03);
                    text-align: center;
                    font-size: 13px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: rgba(255,255,255,0.8);
                }

                .comparison-cell.feature {
                    font-weight: 700;
                    justify-content: flex-start;
                    background: rgba(255, 255, 255, 0.06);
                    color: white;
                }

                @media (max-width: 768px) {
                    .tech-stacks-grid {
                        grid-template-columns: 1fr;
                        gap: 20px;
                    }

                    .comparison-table {
                        grid-template-columns: 1fr;
                        gap: 10px;
                        background: transparent;
                        border: none;
                    }

                    .comparison-header {
                        display: none;
                    }

                    .comparison-row {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 1px;
                        margin-bottom: 12px;
                        border-radius: 8px;
                        overflow: hidden;
                        border: 1px solid rgba(255,255,255,0.08);
                        background: rgba(255,255,255,0.05);
                    }

                    .comparison-cell {
                        padding: 10px;
                    }

                    .comparison-cell.feature {
                        grid-column: 1 / -1;
                        text-align: center;
                        justify-content: center;
                        font-weight: 700;
                        background: rgba(255, 255, 255, 0.12);
                    }
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', styles);
    }

    setupEventListeners() {
        // Add click tracking for analytics
        document.querySelectorAll('.tech-stack-card').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('.stack-btn')) {
                    const stack = card.dataset.stack;
                    this.trackStackInteraction(stack);
                }
            });
        });
    }

    trackStackInteraction(stack) {
        console.log(`User interacted with ${stack} stack`);
        const interactions = JSON.parse(localStorage.getItem('stack_interactions') || '{}');
        interactions[stack] = (interactions[stack] || 0) + 1;
        localStorage.setItem('stack_interactions', JSON.stringify(interactions));
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TechStackVisualizer();
});
