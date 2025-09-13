// document.addEventListener('DOMContentLoaded', () => {
//     const chatMessages = document.getElementById('chat-messages');
//     const messageInput = document.getElementById('message-input');
//     const sendBtn = document.getElementById('send-btn');

//     const appendMessage = (message, sender) => {
//         const messageElement = document.createElement('div');
//         messageElement.classList.add('message', sender);
//         messageElement.textContent = message;
//         chatMessages.appendChild(messageElement);
//         chatMessages.scrollTop = chatMessages.scrollHeight;
//     };

//     const handleSendMessage = () => {
//         const message = messageInput.value.trim();
//         if (message) {
//             appendMessage(message, 'user');
//             messageInput.value = '';

//             setTimeout(() => {
//                 appendMessage("This is an AI-generated response to your query.", 'ai');
//             }, 1000);
//         }
//     };

//     sendBtn.addEventListener('click', handleSendMessage);

//     messageInput.addEventListener('keypress', (e) => {
//         if (e.key === 'Enter') {
//             handleSendMessage();
//         }
//     });

//     appendMessage("Hello! I'm your AI assistant. How can I help you today?", 'ai');
// });

// // Chatbot 

// document.addEventListener('DOMContentLoaded', () => {
//     const userInput = document.getElementById('user-input');
//     const sendBtn = document.getElementById('send-btn');
//     const chatLog = document.querySelector('.chat-log');

//     // Function to add a new message to the chat log
//     function addMessage(message, isUser = false) {
//         const messageDiv = document.createElement('div');
//         messageDiv.classList.add('chat-message');
        
//         if (isUser) {
//             messageDiv.classList.add('user-message');
//         } else {
//             messageDiv.classList.add('bot-message');
//         }

//         const contentDiv = document.createElement('div');
//         contentDiv.classList.add('message-content');
//         contentDiv.innerHTML = `<p>${message}</p>`; // Use innerHTML with <p> tag

//         messageDiv.appendChild(contentDiv);
//         chatLog.appendChild(messageDiv);

//         // Scroll to the bottom to show the new message
//         chatLog.scrollTop = chatLog.scrollHeight;
//     }

//     // Function to handle sending a message
//     function sendMessage() {
//         const message = userInput.value.trim();
//         if (message === '' && (!fileInput || fileInput.files.length === 0)) return;

//         // Add user's message to chat log
//         if (message !== '') {
//             addMessage(message, true);
//         }

//         // Prepare data for backend (query + file if uploaded)
//         const formData = new FormData();
//         formData.append("user_message", message);
//         if (fileInput && fileInput.files.length > 0) {
//             formData.append("file", fileInput.files[0]);
//         }

//         // Clear the input field
//         userInput.value = '';

//         // Send to Flask backend
//         fetch('/chat', {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => response.json())
//         .then(data => {
//             addMessage(data.reply, false);  // Add AI reply to chat
//         })
//         .catch(error => {
//             console.error("Error:", error);
//             addMessage(" Error contacting server.", false);
//         });
//     }

//     // Event listeners
//     if (sendBtn) {
//         sendBtn.addEventListener('click', sendMessage);
//     }

//     if (userInput) {
//         userInput.addEventListener('keypress', (event) => {
//             if (event.key === 'Enter') {
//                 sendMessage();
//             }
//         });
//     }

//     // File upload logic
//     const fileInput = document.getElementById('file-upload');

//     // Add an event listener to the file input
//     if (fileInput) {
//         fileInput.addEventListener('change', (event) => {
//             const files = event.target.files;
//             if (files.length > 0) {
//                 // You can now access the selected files
//                 console.log("Files selected:", files);
//                 // For example, display the name of the first file in the chat
//                 const fileName = files[0].name;
//                 addMessage(`File selected: ${fileName}`, true);

//                 // TODO: Here you would typically upload the file to your Flask backend
//                 // using a FormData object with a fetch() request.
//             }
//         });
//     }

//     // ... (existing functions and event listeners)
// });

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatLog = document.querySelector('.chat-log');
    const fileInput = document.getElementById('file-upload');

    // Function to add messages to chat log
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', isUser ? 'user-message' : 'bot-message');

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.innerHTML = `<p>${message}</p>`;

        messageDiv.appendChild(contentDiv);
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // Send message to Flask backend
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '' && (!fileInput || fileInput.files.length === 0)) return;

        if (message !== '') addMessage(message, true);

        const formData = new FormData();
        formData.append("user_message", message);
        if (fileInput && fileInput.files.length > 0) {
            formData.append("file", fileInput.files[0]);
        }

        userInput.value = '';

        try {
            const response = await fetch('/chatbot', { method: 'POST', body: formData });
            const data = await response.json();
            addMessage(data.reply, false);
        } catch (error) {
            console.error("Error:", error);
            addMessage("⚠️ Error contacting server.", false);
        }
    }

    // Event listeners
    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    if (userInput) {
        userInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') sendMessage();
        });
    }

    // File upload preview
    if (fileInput) {
        fileInput.addEventListener('change', (event) => {
            const files = event.target.files;
            if (files.length > 0) {
                const fileName = files[0].name;
                addMessage(`📄 File selected: ${fileName}`, true);
            }
        });
    }

    // Optional greeting
    addMessage("👋 Hello! I'm your AI Legal Assistant. How can I help you today?", false);
});
