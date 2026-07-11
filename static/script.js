const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message');
const sendBtn = document.getElementById('send-btn');
const status = document.getElementById('status');

function addMessage(text, sender, sources) {
    const div = document.createElement('div');
    div.className = `msg msg-${sender}`;
    div.textContent = text;
    chatMessages.appendChild(div);

    // Hiển thị sources nếu có
    if (sources && sources.length > 0) {
        const srcDiv = document.createElement('div');
        srcDiv.className = 'msg msg-sources';
        srcDiv.innerHTML = '<strong>📎 Nguồn tham khảo:</strong>';
        const list = document.createElement('ul');
        sources.forEach(src => {
            const li = document.createElement('li');
            li.innerHTML = `<span class="src-file">${src.file}</span>
                <span class="src-preview">${src.preview}...</span>`;
            li.title = src.path;
            list.appendChild(li);
        });
        srcDiv.appendChild(list);
        chatMessages.appendChild(srcDiv);
    }

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
        addMessage(data.answer, 'bot', data.sources);
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
