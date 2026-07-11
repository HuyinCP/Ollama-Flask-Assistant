document.getElementById('analyze-btn').addEventListener('click', async () => {
    const message = document.getElementById('message').value;
    if (!message.trim()) return;

    const btn = document.getElementById('analyze-btn');
    btn.disabled = true;
    btn.textContent = 'Analyzing...';
    
    document.getElementById('results').classList.remove('hidden');
    const outputs = ['summary', 'sentiment', 'action', 'response', 'duration'];
    outputs.forEach(id => document.getElementById(`out-${id}`).textContent = '...');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) throw new Error('API request failed');
        
        const data = await response.json();
        
        document.getElementById('out-summary').textContent = data.summary || '';
        document.getElementById('out-sentiment').textContent = data.sentiment || '';
        document.getElementById('out-action').textContent = data.action || '';
        document.getElementById('out-response').textContent = data.response || '';
        document.getElementById('out-duration').textContent = data.duration || '';
    } catch (error) {
        alert('An error occurred during analysis.');
        console.error(error);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Analyze';
    }
});
