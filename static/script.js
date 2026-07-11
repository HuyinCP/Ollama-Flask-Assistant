const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message');
const sendBtn = document.getElementById('send-btn');
const status = document.getElementById('status');

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `msg msg-${sender}`;
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const question = messageInput.value.trim();
    if (!question) return;

    addMessage(question, 'user');
    messageInput.value = '';

    sendBtn.disabled = true;
    sendBtn.textContent = 'Đang xử lý...';
    status.classList.remove('hidden');
    status.textContent = 'Đang tìm kiếm và phân tích tài liệu...';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: question })
        });

        if (!response.ok) throw new Error('API request failed');

        const data = await response.json();
        addMessage(data.answer, 'bot');
        status.textContent = `Hoàn thành trong ${data.duration}s`;
    } catch (error) {
        addMessage('Đã xảy ra lỗi. Vui lòng thử lại.', 'bot');
        status.textContent = '';
        console.error(error);
    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = 'Gửi';
        setTimeout(() => status.classList.add('hidden'), 3000);
    }
}

sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
