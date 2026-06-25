// VignAI Chatbot Implementation
class VignAI {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.init();
    }

    init() {
        this.createChatWidget();
        this.setupEventListeners();
        this.addWelcomeMessage();
    }

    createChatWidget() {
        const chatHTML = `
            <div id="vignai-chat" class="chat-widget">
                <div class="chat-toggle" id="chat-toggle">
                    <i class="fas fa-robot"></i>
                    <span class="chat-badge">VignAI</span>
                </div>
                <div class="chat-container" id="chat-container">
                    <div class="chat-header">
                        <div class="chat-title">
                            <i class="fas fa-robot"></i>
                            <span>VignAI Assistant</span>
                        </div>
                        <button class="chat-close" id="chat-close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="chat-messages" id="chat-messages"></div>
                    <div class="chat-input-container">
                        <input type="text" id="chat-input" placeholder="Ask about projects, pricing, timeline..." />
                        <button id="chat-send"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', chatHTML);
        this.addChatStyles();
    }

    addChatStyles() {
        const styles = `
            <style>
                .chat-widget {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 10000;
                    font-family: 'Poppins', sans-serif;
                }
                .chat-toggle {
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #1B3A6B 0%, #2563EB 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    cursor: pointer;
                    box-shadow: 0 4px 20px rgba(27,58,107,0.3);
                    transition: all 0.3s ease;
                    position: relative;
                }
                .chat-toggle:hover {
                    transform: scale(1.1);
                    box-shadow: 0 8px 30px rgba(27,58,107,0.5);
                }
                .chat-badge {
                    position: absolute;
                    top: -8px;
                    right: -8px;
                    background: #DC2626;
                    color: white;
                    font-size: 10px;
                    padding: 2px 6px;
                    border-radius: 10px;
                    font-weight: bold;
                }
                .chat-container {
                    position: absolute;
                    bottom: 70px;
                    right: 0;
                    width: 350px;
                    height: 500px;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                    display: none;
                    flex-direction: column;
                    overflow: hidden;
                    border: 1px solid rgba(0,0,0,0.05);
                }
                .chat-container.open {
                    display: flex;
                    animation: slideUp 0.3s ease;
                }
                .chat-header {
                    background: linear-gradient(135deg, #1B3A6B 0%, #2563EB 100%);
                    color: white;
                    padding: 15px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .chat-title {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-weight: 600;
                }
                .chat-close {
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                    font-size: 16px;
                }
                .chat-messages {
                    flex: 1;
                    padding: 15px;
                    overflow-y: auto;
                    background: #f8f9fa;
                }
                .message {
                    margin-bottom: 15px;
                    display: flex;
                    align-items: flex-start;
                    gap: 8px;
                }
                .message.user {
                    flex-direction: row-reverse;
                }
                .message-content {
                    max-width: 80%;
                    padding: 10px 15px;
                    border-radius: 15px;
                    font-size: 13.5px;
                    line-height: 1.45;
                }
                .message.bot .message-content {
                    background: white;
                    color: #333;
                    border: 1px solid #e9ecef;
                }
                .message.user .message-content {
                    background: #2563EB;
                    color: white;
                }
                .message-avatar {
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    flex-shrink: 0;
                }
                .message.bot .message-avatar {
                    background: #1B3A6B;
                    color: white;
                }
                .message.user .message-avatar {
                    background: #2563EB;
                    color: white;
                }
                .chat-input-container {
                    padding: 15px;
                    background: white;
                    border-top: 1px solid #e9ecef;
                    display: flex;
                    gap: 10px;
                }
                #chat-input {
                    flex: 1;
                    padding: 10px 15px;
                    border: 1px solid #e9ecef;
                    border-radius: 25px;
                    outline: none;
                    font-size: 14px;
                    font-family: 'Poppins', sans-serif;
                }
                #chat-send {
                    width: 40px;
                    height: 40px;
                    background: #2563EB;
                    color: white;
                    border: none;
                    border-radius: 50%;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: background 0.2s;
                }
                #chat-send:hover {
                    background: #1D4ED8;
                }
                .quick-replies {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-top: 10px;
                }
                .quick-reply {
                    background: #EFF6FF;
                    color: #2563EB;
                    padding: 5px 12px;
                    border-radius: 15px;
                    font-size: 12px;
                    cursor: pointer;
                    border: 1px solid rgba(37,99,235,0.15);
                    transition: all 0.2s ease;
                    font-weight: 500;
                }
                .quick-reply:hover {
                    background: #2563EB;
                    color: white;
                }
                @keyframes slideUp {
                    from { transform: translateY(20px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                @media (max-width: 480px) {
                    .chat-container {
                        width: 300px;
                        height: 400px;
                    }
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', styles);
    }

    setupEventListeners() {
        document.getElementById('chat-toggle').addEventListener('click', () => this.toggleChat());
        document.getElementById('chat-close').addEventListener('click', () => this.closeChat());
        document.getElementById('chat-send').addEventListener('click', () => this.sendMessage());
        document.getElementById('chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const container = document.getElementById('chat-container');
        if (this.isOpen) {
            container.classList.add('open');
        } else {
            container.classList.remove('open');
        }
    }

    closeChat() {
        this.isOpen = false;
        document.getElementById('chat-container').classList.remove('open');
    }

    addWelcomeMessage() {
        const welcomeMsg = {
            type: 'bot',
            content: 'Hi! I\'m VignAI, your project assistant. I can help you with:',
            quickReplies: ['Project Pricing', 'Tech Stacks', 'Timeline', 'Support']
        };
        this.addMessage(welcomeMsg);
    }

    addMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.type}`;
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-${message.type === 'bot' ? 'robot' : 'user'}"></i>
            </div>
            <div class="message-content">
                ${message.content}
                ${message.quickReplies ? this.createQuickReplies(message.quickReplies) : ''}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    createQuickReplies(replies) {
        return `
            <div class="quick-replies">
                ${replies.map(reply => `<button class="quick-reply" onclick="vignAI.handleQuickReply('${reply}')">${reply}</button>`).join('')}
            </div>
        `;
    }

    sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (!message) return;

        this.addMessage({ type: 'user', content: message });
        input.value = '';
        
        setTimeout(() => {
            const response = this.generateResponse(message);
            this.addMessage({ type: 'bot', content: response });
        }, 1000);
    }

    handleQuickReply(reply) {
        this.addMessage({ type: 'user', content: reply });
        setTimeout(() => {
            const response = this.generateResponse(reply);
            this.addMessage({ type: 'bot', content: response });
        }, 500);
    }

    generateResponse(message) {
        const msg = message.toLowerCase();
        
        if (msg.includes('pricing') || msg.includes('cost') || msg.includes('price')) {
            return 'Our project development pricing ranges from ₹8,000 to ₹35,000 based on complexity:<br>• MERN Stack: ₹8,000-₹22,000<br>• Python Full-Stack: ₹10,000-₹25,000<br>• Java Full-Stack: ₹12,000-₹28,000<br>• AI/ML Projects: ₹15,000-₹35,000<br><br>Would you like to discuss a custom quote with a counsellor?';
        }
        
        if (msg.includes('timeline') || msg.includes('time') || msg.includes('delivery')) {
            return 'Project development typically takes 2-4 weeks depending on the stack and specifications:<br>• Basic / Minor projects: 1-2 weeks<br>• Standard major projects: 2-3 weeks<br>• Advanced AI/ML projects: 3-4 weeks<br><br>We deliver on-time, including full source code and IEEE documentation!';
        }
        
        if (msg.includes('tech') || msg.includes('stack') || msg.includes('technology')) {
            return 'We specialize in modern engineering stacks:<br>• <strong>AI & ML:</strong> Python, TensorFlow, PyTorch, OpenCV<br>• <strong>Java:</strong> Spring Boot, Hibernate, React, MySQL<br>• <strong>Python:</strong> Django, Flask, React, PostgreSQL<br>• <strong>MERN Stack:</strong> MongoDB, Express, React, Node.js<br><br>Which stack are you planning to use?';
        }
        
        if (msg.includes('support') || msg.includes('help') || msg.includes('maintenance')) {
            return 'We support students end-to-end:<br>• Complete source code & setup<br>• IEEE project documentation (all chapters)<br>• Mock viva and Q&A sessions<br>• Plagiarism report verification<br>• 1-on-1 mentor guidance sessions till submission<br><br>We stay with you until your project is cleared!';
        }
        
        if (msg.includes('ai') || msg.includes('ml') || msg.includes('machine learning')) {
            return 'Our AI/ML projects feature:<br>• Healthcare analysis & predictions<br>• Face recognition attendance systems<br>• NLP sentiment models<br>• Deep Learning image classifers<br><br>We provide working source code, fully trained weights, and PPTs!';
        }
        
        if (msg.includes('contact') || msg.includes('call') || msg.includes('phone') || msg.includes('email') || msg.includes('where')) {
            return 'You can contact Vignan TechSolutions directly at:<br>📧 <strong>vignantechsolutions@gmail.com</strong><br>📱 <strong>+91-9110478047 / +91-9148215446</strong><br>📍 Kalaburagi, Karnataka, India<br><br>Let us know how we can help you today!';
        }
        
        return 'I\'d be happy to assist you! You can ask me about:<br>• Project pricing and packages<br>• Technology stacks we offer<br>• Project development timelines<br>• Student mentorship and support<br>• Specific project categories<br><br>What would you like to know?';
    }
}

// Initialize VignAI when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.vignAI = new VignAI();
});
