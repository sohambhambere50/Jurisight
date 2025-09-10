document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');

    const appendMessage = (message, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const handleSendMessage = () => {
        const message = messageInput.value.trim();
        if (message) {
            appendMessage(message, 'user');
            messageInput.value = '';

            setTimeout(() => {
                appendMessage("This is an AI-generated response to your query.", 'ai');
            }, 1000);
        }
    };

    sendBtn.addEventListener('click', handleSendMessage);

    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });

    appendMessage("Hello! I'm your AI assistant. How can I help you today?", 'ai');
});