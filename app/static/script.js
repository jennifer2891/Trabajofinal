document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const themeToggle = document.getElementById("theme-toggle");

    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            appendMessage("Tú", message);
            userInput.value = "";

            fetch("/send", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                appendMessage("Chatbot", data.response);
            })
            .catch(error => {
                console.error("Error:", error);
                appendMessage("Sistema", "Error al comunicarse con el servidor.");
            });
        }
    }


    function appendMessage(sender, text) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");
        messageElement.classList.add(sender === "Tú" ? "user-message" : "bot-message");
        
        const formattedText = formatCodeBlocks(text);
        messageElement.innerHTML = `<strong>${sender}:</strong> ${formattedText}`;
        
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;

        Prism.highlightAllUnder(messageElement);
    }

    function formatCodeBlocks(text) {
        const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
        return text.replace(codeBlockRegex, (match, language, code) => {
            language = language || 'plaintext';
            return `<pre><code class="language-${language}">${escapeHtml(code.trim())}</code></pre>`;
        });
    }

    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    sendButton.addEventListener("click", sendMessage);

    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    themeToggle.addEventListener("click", function() {
        document.body.classList.toggle("dark-theme");
    });
});