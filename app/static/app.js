const inputEl = document.getElementById('thought-input');
const chatContainer = document.getElementById('chat-container');

// Загрузка истории при страте
document.addEventListener('DOMContentLoaded', loadHistory);

inputEl.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        analyzeThought();
    }
});

function removeWelcome() {
    const welcome = document.querySelector('.welcome-message');
    if (welcome) welcome.remove();
}

async function loadHistory() {
    try {
        const response = await fetch('/entries');
        if (!response.ok) return;
        const entries = await response.json();
        
        if (entries.length > 0) {
            removeWelcome();
            entries.reverse().forEach(entry => {
                if (entry.summary && entry.tags) {
                    renderEntry(entry);
                }
            });
            scrollToBottom();
        }
    } catch (err) {
        console.error('Failed to load history', err);
    }
}

function renderEntry(data, isLoading = false, tempId = null) {
    const entryId = tempId || 'entry-' + data.id;
    const text = data.original_text;

    let html = `<div class="entry-card" id="${entryId}">
        <div class="user-text">${escapeHtml(text).replace(/\n/g, '<br>')}</div>`;

    if (isLoading) {
        html += `
        <div class="loader" id="loader-${entryId}" style="display: flex;">
            <span>Психолог анализирует</span>
            <div class="loader-dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
        </div>
        <div class="analysis-section" id="analysis-${entryId}" style="display: none;">`;
    } else {
        html += `<div class="analysis-section" id="analysis-${entryId}">`;
    }

    const insight = data.insight || '';
    const summary = data.summary || '';
    
    let markersHtml = '';
    if (data.emotion) markersHtml += `<span class="emotion-pill">🤍 ${data.emotion}</span>`;
    if (data.intent) markersHtml += `<span class="intent-pill">🎯 ${data.intent}</span>`;
    if (data.tags) {
        data.tags.forEach(tag => {
            markersHtml += `<span class="pill">#${tag}</span>`;
        });
    }

    html += `
            <div class="analysis-row">
                <div class="label">Insight</div>
                <div class="insight-text" id="insight-${entryId}">${insight}</div>
            </div>
            <div class="analysis-row">
                <div class="label">Summary</div>
                <div class="summary-text" id="summary-${entryId}">${summary}</div>
            </div>
            <div class="analysis-row" style="margin-top: 6px;">
                <div class="label">Markers</div>
                <div class="pills-container" id="markers-${entryId}">${markersHtml}</div>
            </div>
        </div>
    </div>`;

    chatContainer.insertAdjacentHTML('beforeend', html);
}

async function analyzeThought() {
    const text = inputEl.value.trim();
    if (!text) return;
    removeWelcome();

    const tempId = 'entry-temp-' + Date.now();
    renderEntry({ original_text: text }, true, tempId);
    scrollToBottom();
    inputEl.value = '';

    try {
        const response = await fetch('/entries/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ original_text: text })
        });
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        document.getElementById(`loader-${tempId}`).style.display = 'none';
        document.getElementById(`analysis-${tempId}`).style.display = 'flex';
        
        document.getElementById(`insight-${tempId}`).innerText = data.insight;
        document.getElementById(`summary-${tempId}`).innerText = data.summary;
        
        let markersHtml = `<span class="emotion-pill">🤍 ${data.emotion}</span>`;
        markersHtml += `<span class="intent-pill">🎯 ${data.intent}</span>`;
        data.tags.forEach(tag => {
            markersHtml += `<span class="pill">#${tag}</span>`;
        });
        document.getElementById(`markers-${tempId}`).innerHTML = markersHtml;
        scrollToBottom();

    } catch (err) {
        document.getElementById(`loader-${tempId}`).innerHTML = `<span style="color: #ef4444;">Произошла ошибка при получении анализа :(</span>`;
    }
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function escapeHtml(unsafe) {
    if (!unsafe) return "";
    return String(unsafe)
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}
