/* AI Agent Scenery Component Interaction Logic */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        lucide.createIcons();
    }

    let activeModel = "Nexus Core 4.0";
    let activeEffort = "High";
    let currentUploadedFile = null;
    let isMuted = false;
    let isListening = false;
    let toastTimer = null;

    const overlay = document.getElementById('configDrawerOverlay');
    const menuBtn = document.getElementById('menuBtn');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const activeConfigPill = document.getElementById('activeConfigPill');
    const soundBtn = document.getElementById('soundBtn');
    const volumeIcon = document.getElementById('volumeIcon');
    const sceneryThinkingTrigger = document.getElementById('sceneryThinkingTrigger');
    const thinkingOptionsBox = document.getElementById('thinkingOptionsBox');
    const curThinkingLabel = document.getElementById('curThinkingLabel');
    const activeModelTag = document.getElementById('activeModelTag');
    const activeEffortTag = document.getElementById('activeEffortTag');

    const fileInput = document.getElementById('sceneryFileInput');
    const btnAttach = document.getElementById('btnSceneryAttach');
    const uploadChip = document.getElementById('sceneryUploadChip');
    const fileNameSpan = document.getElementById('sceneryFileName');
    const btnChipClose = document.getElementById('btnChipClose');
    const micBtn = document.getElementById('btnSceneryMic');
    const chatForm = document.getElementById('sceneryChatForm');
    const chatInput = document.getElementById('sceneryInput');
    const chatStreamArea = document.getElementById('chatStreamArea');

    function toggleModal() {
        if (overlay) {
            overlay.classList.toggle('open');
        }
    }

    if (menuBtn) menuBtn.addEventListener('click', toggleModal);
    if (modalCloseBtn) modalCloseBtn.addEventListener('click', toggleModal);
    if (activeConfigPill) activeConfigPill.addEventListener('click', toggleModal);
    if (overlay) {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) toggleModal();
        });
    }

    // Model selection
    document.querySelectorAll('.scenery-model-item').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('.scenery-model-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            activeModel = item.dataset.name || "Nexus Core 4.0";
            if (activeModelTag) {
                activeModelTag.innerHTML = `Model: <b>${activeModel}</b>`;
            }
            showToast(`Model dialihkan ke ${activeModel}`);
            toggleModal();
        });
    });

    // Thinking options dropdown
    if (sceneryThinkingTrigger) {
        sceneryThinkingTrigger.addEventListener('click', () => {
            if (thinkingOptionsBox) thinkingOptionsBox.classList.toggle('open');
        });
    }

    document.querySelectorAll('.th-option').forEach(opt => {
        opt.addEventListener('click', (e) => {
            document.querySelectorAll('.th-option').forEach(o => o.classList.remove('active'));
            opt.classList.add('active');
            const label = opt.dataset.val || opt.textContent.trim();
            if (curThinkingLabel) curThinkingLabel.textContent = label;
            activeEffort = label.split(' ')[0];
            if (activeEffortTag) {
                activeEffortTag.innerHTML = `Thinking: <b>${activeEffort}</b>`;
            }
            if (thinkingOptionsBox) thinkingOptionsBox.classList.remove('open');
            showToast(`Thinking level: ${activeEffort}`);
        });
    });

    // Sound toggle
    if (soundBtn) {
        soundBtn.addEventListener('click', () => {
            isMuted = !isMuted;
            if (isMuted) {
                soundBtn.classList.remove('active');
                if (volumeIcon) volumeIcon.setAttribute('data-lucide', 'volume-x');
                showToast('Suara haptik dimatikan', 'volume-x');
            } else {
                soundBtn.classList.add('active');
                if (volumeIcon) volumeIcon.setAttribute('data-lucide', 'volume-2');
                showToast('Suara haptik diaktifkan', 'volume-2');
            }
            if (window.lucide) lucide.createIcons();
        });
    }

    // Quick prompts pills
    document.querySelectorAll('.pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const prompt = pill.dataset.prompt || pill.textContent.trim();
            if (chatInput) {
                chatInput.value = prompt;
                chatInput.focus();
                showToast('Prompt disisipkan ke input', 'sparkles');
            }
        });
    });

    // Attachment
    if (btnAttach && fileInput) {
        btnAttach.addEventListener('click', () => fileInput.click());
    }

    if (fileInput) {
        fileInput.addEventListener('change', () => {
            if (fileInput.files && fileInput.files[0]) {
                currentUploadedFile = fileInput.files[0];
                if (fileNameSpan) fileNameSpan.textContent = currentUploadedFile.name;
                if (uploadChip) uploadChip.classList.add('active');
                if (btnAttach) btnAttach.classList.add('active');
                showToast(`Berkas terlampir: ${currentUploadedFile.name}`, 'file-check');
            }
        });
    }

    function clearAttachment() {
        currentUploadedFile = null;
        if (fileInput) fileInput.value = '';
        if (uploadChip) uploadChip.classList.remove('active');
        if (btnAttach) btnAttach.classList.remove('active');
    }

    if (btnChipClose) {
        btnChipClose.addEventListener('click', clearAttachment);
    }

    // Mic
    if (micBtn) {
        micBtn.addEventListener('click', () => {
            isListening = !isListening;
            if (isListening) {
                micBtn.classList.add('active');
                showToast('Mendengarkan instruksi suara...', 'mic');
            } else {
                micBtn.classList.remove('active');
                showToast('Perekaman audio selesai.', 'check');
            }
        });
    }

    // Submit form
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const textVal = chatInput ? chatInput.value.trim() : '';

            if (!textVal && !currentUploadedFile) {
                showToast('Silakan masukkan instruksi atau lampirkan berkas.', 'alert-circle');
                return;
            }

            if (chatStreamArea) {
                const userBubble = document.createElement('div');
                userBubble.className = 'chat-bubble user';
                userBubble.textContent = currentUploadedFile ? `${textVal || currentUploadedFile.name} (1 file)` : textVal;
                chatStreamArea.appendChild(userBubble);

                if (chatInput) chatInput.value = '';
                clearAttachment();

                setTimeout(() => {
                    const agentBubble = document.createElement('div');
                    agentBubble.className = 'chat-bubble agent';
                    agentBubble.innerHTML = `
                        <div class="agent-header-row">
                            <i data-lucide="bot"></i>
                            <span>${activeModel} • Thinking: ${activeEffort}</span>
                        </div>
                        Menerima permintaan: "<em>${userBubble.textContent}</em>". Sedang mengorkestrasi rencana solusi dan mengeksekusi artefak.
                    `;
                    chatStreamArea.appendChild(agentBubble);
                    if (window.lucide) lucide.createIcons();
                    chatStreamArea.scrollTop = chatStreamArea.scrollHeight;
                }, 600);

                chatStreamArea.scrollTop = chatStreamArea.scrollHeight;
            }
        });
    }

    function showToast(msg, iconName = 'check-circle-2') {
        const toast = document.getElementById('sceneryToast');
        const text = document.getElementById('sceneryToastText');
        if (!toast || !text) return;

        text.textContent = msg;
        const oldSvg = toast.querySelector('svg');
        if (oldSvg) oldSvg.remove();

        const icon = document.createElement('i');
        icon.setAttribute('data-lucide', iconName);
        toast.prepend(icon);
        if (window.lucide) lucide.createIcons();

        toast.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => {
            toast.classList.remove('show');
        }, 2600);
    }
});