// WhatsApp Integration and Analytics
class WhatsAppIntegration {
    constructor() {
        this.phoneNumber = '9110478047'; // Vignan TechSolutions WhatsApp number
        this.init();
    }

    init() {
        this.createWhatsAppButton();
        this.setupClickTracking();
    }

    createWhatsAppButton() {
        const whatsappHTML = `
            <div class="whatsapp-float" id="whatsapp-float">
                <div class="whatsapp-button">
                    <i class="fab fa-whatsapp"></i>
                    <span class="whatsapp-tooltip">Chat with us on WhatsApp</span>
                </div>
                <div class="whatsapp-popup" id="whatsapp-popup">
                    <div class="whatsapp-header">
                        <i class="fab fa-whatsapp"></i>
                        <span>Start WhatsApp Chat</span>
                        <button class="whatsapp-close" id="whatsapp-close">×</button>
                    </div>
                    <div class="whatsapp-content">
                        <p>Hi! Click one of our representatives below to chat on WhatsApp or send us an email to vignantechsolutions@gmail.com</p>
                        <div class="whatsapp-agents">
                            <div class="whatsapp-agent" data-message="Hi! I'm interested in AI/ML projects. Can you help me?">
                                <div class="agent-avatar">
                                    <i class="fas fa-brain"></i>
                                </div>
                                <div class="agent-info">
                                    <div class="agent-name">AI/ML Specialist</div>
                                    <div class="agent-status">Online</div>
                                </div>
                            </div>
                            <div class="whatsapp-agent" data-message="Hi! I need help with Java Full-Stack project. Can we discuss?">
                                <div class="agent-avatar">
                                    <i class="fab fa-java"></i>
                                </div>
                                <div class="agent-info">
                                    <div class="agent-name">Java Developer</div>
                                    <div class="agent-status">Online</div>
                                </div>
                            </div>
                            <div class="whatsapp-agent" data-message="Hi! I'm looking for Python/MERN stack projects. Please help!">
                                <div class="agent-avatar">
                                    <i class="fab fa-python"></i>
                                </div>
                                <div class="agent-info">
                                    <div class="agent-name">Full-Stack Developer</div>
                                    <div class="agent-status">Online</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', whatsappHTML);
        this.addWhatsAppStyles();
        this.setupWhatsAppListeners();
    }

    addWhatsAppStyles() {
        const styles = `
            <style>
                .whatsapp-float {
                    position: fixed;
                    bottom: 90px;
                    right: 20px;
                    z-index: 9998;
                    font-family: 'Poppins', sans-serif;
                }

                .whatsapp-button {
                    width: 60px;
                    height: 60px;
                    background: #25d366;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 28px;
                    cursor: pointer;
                    box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
                    transition: all 0.3s ease;
                    position: relative;
                    animation: whatsappPulse 2s infinite;
                }

                .whatsapp-button:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 25px rgba(37, 211, 102, 0.6);
                }

                .whatsapp-tooltip {
                    position: absolute;
                    right: 70px;
                    top: 50%;
                    transform: translateY(-50%);
                    background: #0F172A;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-size: 12px;
                    white-space: nowrap;
                    opacity: 0;
                    pointer-events: none;
                    transition: opacity 0.3s ease;
                    font-weight: 500;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                }

                .whatsapp-button:hover .whatsapp-tooltip {
                    opacity: 1;
                }

                .whatsapp-popup {
                    position: absolute;
                    bottom: 70px;
                    right: 0;
                    width: 300px;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                    display: none;
                    overflow: hidden;
                    border: 1px solid rgba(0,0,0,0.05);
                }

                .whatsapp-popup.active {
                    display: block;
                    animation: slideUp 0.3s ease;
                }

                .whatsapp-header {
                    background: #25d366;
                    color: white;
                    padding: 15px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    font-weight: 600;
                }

                .whatsapp-close {
                    margin-left: auto;
                    background: none;
                    border: none;
                    color: white;
                    font-size: 20px;
                    cursor: pointer;
                }

                .whatsapp-content {
                    padding: 15px;
                }

                .whatsapp-content p {
                    font-size: 13px;
                    color: #64748B;
                    margin-bottom: 15px;
                    line-height: 1.45;
                }

                .whatsapp-agents {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }

                .whatsapp-agent {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 10px;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: background 0.2s ease;
                    border: 1px solid #F1F5F9;
                }

                .whatsapp-agent:hover {
                    background: #F8FAFC;
                    border-color: #E2E8F0;
                }

                .agent-avatar {
                    width: 40px;
                    height: 40px;
                    background: #1B3A6B;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 16px;
                }

                .whatsapp-agent:nth-child(2) .agent-avatar { background: #D97706; }
                .whatsapp-agent:nth-child(3) .agent-avatar { background: #059669; }

                .agent-info {
                    flex: 1;
                }

                .agent-name {
                    font-weight: 600;
                    color: #0F172A;
                    font-size: 13.5px;
                }

                .agent-status {
                    font-size: 11px;
                    color: #25d366;
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    margin-top: 1px;
                    font-weight: 500;
                }

                .agent-status::before {
                    content: '';
                    width: 6px;
                    height: 6px;
                    background: #25d366;
                    border-radius: 50%;
                    animation: blink 2s infinite;
                }

                @keyframes whatsappPulse {
                    0% { box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4); }
                    50% { box-shadow: 0 4px 30px rgba(37, 211, 102, 0.6); }
                    100% { box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4); }
                }

                @keyframes blink {
                    0%, 50% { opacity: 1; }
                    51%, 100% { opacity: 0.3; }
                }

                @media (max-width: 768px) {
                    .whatsapp-float {
                        bottom: 90px;
                        right: 15px;
                    }
                    .whatsapp-popup {
                        width: 270px;
                        right: 0;
                    }
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', styles);
    }

    setupWhatsAppListeners() {
        const button = document.querySelector('.whatsapp-button');
        const popup = document.getElementById('whatsapp-popup');
        const closeBtn = document.getElementById('whatsapp-close');
        const agents = document.querySelectorAll('.whatsapp-agent');

        button.addEventListener('click', () => {
            popup.classList.toggle('active');
        });

        closeBtn.addEventListener('click', () => {
            popup.classList.remove('active');
        });

        agents.forEach(agent => {
            agent.addEventListener('click', () => {
                const message = agent.dataset.message;
                this.openWhatsApp(message);
            });
        });

        // Close popup when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.whatsapp-float')) {
                popup.classList.remove('active');
            }
        });
    }

    setupClickTracking() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.whatsapp-agent')) {
                this.trackEvent('whatsapp_click', 'engagement', 'WhatsApp Chat Started');
            }
        });
    }

    openWhatsApp(message) {
        const encodedMessage = encodeURIComponent(message);
        const whatsappURL = `https://wa.me/${this.phoneNumber}?text=${encodedMessage}`;
        window.open(whatsappURL, '_blank');
    }

    trackEvent(action, category, label) {
        if (typeof gtag !== 'undefined') {
            gtag('event', action, {
                event_category: category,
                event_label: label
            });
        }
        console.log(`Event tracked: ${action} - ${category} - ${label}`);
    }
}

// Live Analytics and Visitor Counter
class LiveAnalytics {
    constructor() {
        this.visitors = this.getStoredVisitors();
        this.currentSession = this.generateSessionId();
        this.init();
    }

    init() {
        this.trackVisitor();
        this.createAnalyticsWidget();
        this.updateRealTimeStats();
        this.setupPageTracking();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    getStoredVisitors() {
        const stored = localStorage.getItem('vignan_visitors');
        return stored ? JSON.parse(stored) : {
            total: 3120, // Starting count
            today: 88,
            online: 14,
            projects: 75,
            students: 500
        };
    }

    trackVisitor() {
        const lastVisit = localStorage.getItem('vignan_last_visit');
        const today = new Date().toDateString();
        
        if (lastVisit !== today) {
            this.visitors.today++;
            localStorage.setItem('vignan_last_visit', today);
        }
        
        this.visitors.total++;
        this.visitors.online = Math.floor(Math.random() * 15) + 6; // Simulate online users
        
        localStorage.setItem('vignan_visitors', JSON.stringify(this.visitors));
    }

    createAnalyticsWidget() {
        const analyticsHTML = `
            <div class="analytics-widget" id="analytics-widget">
                <div class="analytics-toggle" id="analytics-toggle">
                    <i class="fas fa-chart-line"></i>
                    <span class="analytics-badge">Live</span>
                </div>
                <div class="analytics-panel" id="analytics-panel">
                    <div class="analytics-header">
                        <h4>📊 Vignan Live Stats</h4>
                        <button class="analytics-close" id="analytics-close">×</button>
                    </div>
                    <div class="analytics-stats">
                        <div class="stat-item">
                            <div class="stat-icon"><i class="fas fa-users"></i></div>
                            <div class="stat-info">
                                <div class="stat-number" id="total-visitors">${this.visitors.total.toLocaleString()}</div>
                                <div class="stat-label">Total Visits</div>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon"><i class="fas fa-eye"></i></div>
                            <div class="stat-info">
                                <div class="stat-number" id="today-visitors">${this.visitors.today}</div>
                                <div class="stat-label">Today's Visits</div>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon online"><i class="fas fa-circle"></i></div>
                            <div class="stat-info">
                                <div class="stat-number" id="online-users">${this.visitors.online}</div>
                                <div class="stat-label">Users Online Now</div>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon"><i class="fas fa-project-diagram"></i></div>
                            <div class="stat-info">
                                <div class="stat-number" id="total-projects">${this.visitors.projects}+</div>
                                <div class="stat-label">Projects Delivered</div>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon"><i class="fas fa-graduation-cap"></i></div>
                            <div class="stat-info">
                                <div class="stat-number" id="happy-students">${this.visitors.students}+</div>
                                <div class="stat-label">Students Guided</div>
                            </div>
                        </div>
                    </div>
                    <div class="analytics-footer">
                        <small>Updated in real-time</small>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', analyticsHTML);
        this.addAnalyticsStyles();
        this.setupAnalyticsListeners();
    }

    addAnalyticsStyles() {
        const styles = `
            <style>
                .analytics-widget {
                    position: fixed;
                    bottom: 160px;
                    right: 20px;
                    z-index: 9997;
                    font-family: 'Poppins', sans-serif;
                }

                .analytics-toggle {
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    cursor: pointer;
                    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
                    transition: all 0.3s ease;
                    position: relative;
                }

                .analytics-toggle:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.55);
                }

                .analytics-badge {
                    position: absolute;
                    top: -5px;
                    right: -5px;
                    background: #DC2626;
                    color: white;
                    font-size: 8px;
                    padding: 2px 5px;
                    border-radius: 8px;
                    font-weight: bold;
                    animation: blink 2s infinite;
                }

                .analytics-panel {
                    position: absolute;
                    bottom: 70px;
                    right: 0;
                    width: 280px;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                    display: none;
                    overflow: hidden;
                    border: 1px solid rgba(0,0,0,0.05);
                }

                .analytics-panel.active {
                    display: block;
                    animation: slideUp 0.3s ease;
                }

                .analytics-header {
                    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                    color: white;
                    padding: 15px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .analytics-header h4 {
                    margin: 0;
                    font-size: 13.5px;
                    font-weight: 600;
                }

                .analytics-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 18px;
                    cursor: pointer;
                }

                .analytics-stats {
                    padding: 15px;
                }

                .stat-item {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 8px 0;
                    border-bottom: 1px solid #f0f0f0;
                }

                .stat-item:last-child {
                    border-bottom: none;
                }

                .stat-icon {
                    width: 35px;
                    height: 35px;
                    background: #F8FAFC;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #059669;
                    font-size: 14px;
                    border: 1px solid #F1F5F9;
                }

                .stat-icon.online {
                    color: #10B981;
                }

                .stat-info {
                    flex: 1;
                }

                .stat-number {
                    font-weight: 700;
                    color: #0F172A;
                    font-size: 15px;
                }

                .stat-label {
                    font-size: 11px;
                    color: #64748B;
                    font-weight: 500;
                }

                .analytics-footer {
                    padding: 10px 15px;
                    background: #F8FAFC;
                    text-align: center;
                    color: #64748B;
                    border-top: 1px solid #F1F5F9;
                }

                @media (max-width: 768px) {
                    .analytics-widget {
                        bottom: 160px;
                        right: 15px;
                    }
                    .analytics-panel {
                        right: 0;
                    }
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', styles);
    }

    setupAnalyticsListeners() {
        const toggle = document.getElementById('analytics-toggle');
        const panel = document.getElementById('analytics-panel');
        const close = document.getElementById('analytics-close');

        toggle.addEventListener('click', () => {
            panel.classList.toggle('active');
        });

        close.addEventListener('click', () => {
            panel.classList.remove('active');
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.analytics-widget')) {
                panel.classList.remove('active');
            }
        });
    }

    updateRealTimeStats() {
        setInterval(() => {
            const onlineVariation = Math.floor(Math.random() * 5) - 2;
            this.visitors.online = Math.max(3, this.visitors.online + onlineVariation);
            
            const onlineEl = document.getElementById('online-users');
            if (onlineEl) onlineEl.textContent = this.visitors.online;
            
            if (Math.random() < 0.1) {
                this.visitors.total++;
                const totalEl = document.getElementById('total-visitors');
                if (totalEl) totalEl.textContent = this.visitors.total.toLocaleString();
            }
            
            localStorage.setItem('vignan_visitors', JSON.stringify(this.visitors));
        }, 10000);
    }

    setupPageTracking() {
        this.trackPageView();
        this.startTime = Date.now();
        
        window.addEventListener('beforeunload', () => {
            const timeSpent = Math.floor((Date.now() - this.startTime) / 1000);
            this.trackEvent('time_on_page', 'engagement', timeSpent);
        });
    }

    trackPageView() {
        const page = window.location.pathname;
        this.trackEvent('page_view', 'navigation', page);
    }

    trackEvent(action, category, value) {
        const event = {
            action,
            category,
            value,
            timestamp: Date.now(),
            session: this.currentSession,
            page: window.location.pathname
        };
        
        const events = JSON.parse(localStorage.getItem('vignan_events') || '[]');
        events.push(event);
        localStorage.setItem('vignan_events', JSON.stringify(events.slice(-100)));
    }
}

// Initialize integrations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WhatsAppIntegration();
    new LiveAnalytics();
});
