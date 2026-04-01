const inputEl = document.getElementById('thought-input');
const chatContainer = document.getElementById('chat-container');

inputEl.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        analyzeThought();
    }
});

async function analyzeThought() {
    const text = inputEl.value.trim();
    if (!text) return;

    // Remove welcome message on first entry
    const welcome = document.querySelector('.welcome-message');
    if (welcome) welcome.remove();

    // 1. Create Layout Block
    const entryId = 'entry-' + Date.now();
    const entryHtml = `
        <div class="entry-card" id="${entryId}">
            <div class="user-text">${escapeHtml(text).replace(/\n/g, '<br>')}</div>
            
            <div class="loader" id="loader-${entryId}" style="display: flex;">
                <span>Психолог анализирует</span>
                <div class="loader-dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
            </div>
            
            <div class="analysis-section" id="analysis-${entryId}" style="display: none;">
                <div class="analysis-row">
                    <div class="label">Insight</div>
                    <div class="insight-text" id="insight-${entryId}"></div>
                </div>
                <div class="analysis-row">
                    <div class="label">Summary</div>
                    <div class="summary-text" id="summary-${entryId}"></div>
                </div>
                <div class="analysis-row" style="margin-top: 6px;">
                    <div class="label">Markers</div>
                    <div class="pills-container" id="markers-${entryId}"></div>
                </div>
            </div>
        </div>
    `;
    
    chatContainer.insertAdjacentHTML('beforeend', entryHtml);
    scrollToBottom();
    
    inputEl.value = '';

    // 2. Fetch Data from Backend
    try {
        const response = await fetch('/entries/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ original_text: text })
        });

        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        // 3. Populate and show analysis
        document.getElementById(`loader-${entryId}`).style.display = 'none';
        document.getElementById(`analysis-${entryId}`).style.display = 'flex';
        
        document.getElementById(`insight-${entryId}`).innerText = data.insight;
        document.getElementById(`summary-${entryId}`).innerText = data.summary;
        
        let markersHtml = `<span class="emotion-pill">🤍 ${data.emotion}</span>`;
        markersHtml += `<span class="intent-pill">🎯 ${data.intent}</span>`;
        data.tags.forEach(tag => {
            markersHtml += `<span class="pill">#${tag}</span>`;
        });
        
        document.getElementById(`markers-${entryId}`).innerHTML = markersHtml;
        scrollToBottom();

    } catch (err) {
        document.getElementById(`loader-${entryId}`).innerHTML = `<span style="color: #ef4444;">Произошла ошибка при получении анализа от агента :(</span>`;
    }
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}
