class ChatApp {
    constructor() {
        this.messageForm = document.getElementById('message-form');
        this.messageInput = document.getElementById('message-input');
        this.messagesContainer = document.getElementById('messages-container');
        this.socket = null;
        this.isSocketConnected = false;
        
        this.init();
    }
    
    init() {
        this.connectWebSocket();
        this.setupEventListeners();
        this.renderMarkdown();
    }
    
    connectWebSocket() {
        const conversationId = document.querySelector('meta[name="conversation-id"]').getAttribute('content');
        this.socket = new WebSocket(`ws://${window.location.host}/ws/chat/${conversationId}/`);

        this.socket.onopen = (e) => {
            console.log("WebSocket connected");
            this.isSocketConnected = true;
        };

        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            this.appendAssistantMessage(data.message, data.message_id);
            this.enableMessageInput();
        };

        this.socket.onclose = (e) => {
            console.log("WebSocket disconnected", e.reason);
            this.isSocketConnected = false;
            setTimeout(() => this.connectWebSocket(), 2000);
        };

        this.socket.onerror = (err) => {
            console.error("WebSocket error", err);
            this.socket.close();
        };
    }
    
    setupEventListeners() {
        this.messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const message = this.messageInput.value.trim();
            if (!message) return;

            this.disableMessageInput();
            
            this.appendUserMessage(message);
            this.messageInput.value = '';
            
            const sent = this.sendMessage(message);
            
            if (!sent) {
                console.log("Using HTMX fallback");
                htmx.ajax('POST', this.messageForm.getAttribute('data-message-url'), {
                    values: { message: message },
                    target: '#messages-container',
                    swap: 'innerHTML'
                });
            }
        });
    }
    
    sendMessage(message) {
        if (this.isSocketConnected) {
            this.socket.send(JSON.stringify({
                'message': message
            }));
            return true;
        } else {
            return false;
        }
    }
    
    appendUserMessage(message) {
        const userMessageElement = document.createElement('div');
        userMessageElement.className = 'user-message';
        userMessageElement.textContent = message;
        this.messagesContainer.appendChild(userMessageElement);
        this.scrollToBottom();
    }
    
    appendAssistantMessage(message, messageId) {
        const messageElement = document.createElement('div');
        messageElement.className = 'assistant-message';
        messageElement.id = `message-${messageId}`;

        const contentElement = document.createElement('div');
        contentElement.className = 'markdown-content';
        contentElement.textContent = message;
        messageElement.appendChild(contentElement);

        this.messagesContainer.appendChild(messageElement);
        
        this.renderMarkdownElement(contentElement);
        this.scrollToBottom();
    }
    
    renderMarkdown() {
        document.querySelectorAll('.markdown-content').forEach(el => {
            this.renderMarkdownElement(el);
        });
    }
    
    renderMarkdownElement(element) {
        const content = element.textContent;
        element.innerHTML = marked.parse(content);
        
        element.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    disableMessageInput() {
        this.messageInput.disabled = true;
        document.getElementById('send-button').disabled = true;
    }
    
    enableMessageInput() {
        this.messageInput.disabled = false;
        document.getElementById('send-button').disabled = false;
        this.messageInput.focus();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('message-form')) {
        new ChatApp();
    }
});
