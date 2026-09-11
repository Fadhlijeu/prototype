document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    let currentModel = "Instant";
    let currentThinking = "High";
    let attachedFiles = [];
    let isMuted = false;
    let isRecording = false;

    const menuBtn = document.getElementById('menuBtn');
    const sceneryDropdownMenu = document.getElementById('sceneryDropdownMenu');
    const activeConfigTrigger = document.getElementById('activeConfigTrigger');
    const badgeChevron = document.getElementById('badgeChevron');
    const soundBtn = document.getElementById('soundBtn');
    const volumeIcon = document.getElementById('volumeIcon');
    const sceneryChatForm = document.getElementById('sceneryChatForm');
    const sceneryChatInput = document.getElementById('sceneryChatInput');
    const sceneryFileInput = document.getElementById('sceneryFileInput');
    const btnAttach = document.getElementById('btnAttach');
    const btnMic = document.getElementById('btnMic');
    const btnClearAll = document.getElementById('btnClearAll');
    const uploadPreviewArea = document.getElementById('uploadPreviewArea');
    const previewChipsList = document.getElementById('previewChipsList');
    const previewCountText = document.getElementById('previewCountText');
    const displayModelTag = document.getElementById('displayModelTag');
    const displayEffortTag = document.getElementById('displayEffortTag');
    const sceneryToast = document.getElementById('sceneryToast');
    const sceneryToastText = document.getElementById('sceneryToastText');

    function toggleMenu() {
        if (!sceneryDropdownMenu) return;
        const isOpen = sceneryDropdownMenu.classList.toggle('open');
        if (menuBtn) menuBtn.classList.toggle('active', isOpen);
        if (badgeChevron) {
            badgeChevron.style.transform = isOpen ? 'rotate(180deg)' : 'rotate(0deg)';
        }
    }

    if (menuBtn) {
        menuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleMenu();
        });
    }

    if (activeConfigTrigger) {
        activeConfigTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleMenu();
        });
    }

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!sceneryDropdownMenu || !sceneryDropdownMenu.classList.contains('open')) return;
        if (!sceneryDropdownMenu.contains(e.target) && (!menuBtn || !menuBtn.contains(e.target)) && (!activeConfigTrigger || !activeConfigTrigger.contains(e.target))) {
            sceneryDropdownMenu.classList.remove('open');
            if (menuBtn) menuBtn.classList.remove('active');
            if (badgeChevron) badgeChevron.style.transform = 'rotate(0deg)';
        }
    });

    // Model selection
    document.querySelectorAll('.model-item').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('.model-item').forEach(m => m.classList.remove('active'));
            item.classList.add('active');
            currentModel = item.getAttribute('data-model') || "Instant";
            if (displayModelTag) displayModelTag.innerHTML = `Model: <b>${currentModel}</b>`;
            showToast(`Model diubah ke ${currentModel}`);
            toggleMenu();
        });
    });

    // Thinking effort selection
    document.querySelectorAll('.th-level-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.th-level-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentThinking = btn.getAttribute('data-level') || "High";
            if (displayEffortTag) displayEffortTag.innerHTML = `Reasoning: <b>${currentThinking}</b>`;
            showToast(`Thinking Level: ${currentThinking}`);
            toggleMenu();
        });
    });

    // Sound toggle
    if (soundBtn) {
        soundBtn.addEventListener('click', () => {
            isMuted = !isMuted;
            if (isMuted) {
                soundBtn.classList.remove('active');
                if (volumeIcon) volumeIcon.setAttribute('data-lucide', 'volume-x');
                showToast('Haptic suara dinonaktifkan', 'volume-x');
            } else {
                soundBtn.classList.add('active');
                if (volumeIcon) volumeIcon.setAttribute('data-lucide', 'volume-2');
                showToast('Haptic suara diaktifkan', 'volume-2');
            }
            if (window.lucide) window.lucide.createIcons();
        });
    }

    // Pills prompt click
    document.querySelectorAll('.pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const prompt = pill.getAttribute('data-prompt');
            if (prompt && sceneryChatInput) {
                sceneryChatInput.value = prompt;
                sceneryChatInput.focus();
                showToast('Prompt disisipkan ke input', 'sparkles');
            }
        });
    });

    // Attachment triggers
    if (btnAttach && sceneryFileInput) {
        btnAttach.addEventListener('click', () => {
            sceneryFileInput.click();
        });
    }

    if (sceneryFileInput) {
        sceneryFileInput.addEventListener('change', () => {
            if (sceneryFileInput.files && sceneryFileInput.files.length > 0) {
                for (let i = 0; i < sceneryFileInput.files.length; i++) {
                    attachedFiles.push(sceneryFileInput.files[i]);
                }
                renderFiles();
                sceneryFileInput.value = '';
            }
        });
    }

    if (btnClearAll) {
        btnClearAll.addEventListener('click', () => {
            attachedFiles = [];
            renderFiles();
        });
    }

    function removeFile(index) {
        attachedFiles.splice(index, 1);
        renderFiles();
    }

    function renderFiles() {
        if (!uploadPreviewArea || !previewChipsList || !previewCountText) return;

        if (attachedFiles.length === 0) {
            uploadPreviewArea.classList.remove('active');
            if (btnAttach) btnAttach.classList.remove('active');
            previewChipsList.innerHTML = '';
            return;
        }

        uploadPreviewArea.classList.add('active');
        if (btnAttach) btnAttach.classList.add('active');
        previewCountText.innerHTML = `<i data-lucide="paperclip"></i><span>Lampiran Berkas (${attachedFiles.length})</span>`;
        previewChipsList.innerHTML = '';

        attachedFiles.forEach((file, idx) => {
            const chip = document.createElement('div');
            chip.className = 'file-chip';
            chip.innerHTML = `
                <i data-lucide="file-text"></i>
                <span>${file.name}</span>
                <button type="button" class="btn-remove-chip" title="Hapus"><i data-lucide="x"></i></button>
            `;
            chip.querySelector('.btn-remove-chip').addEventListener('click', () => removeFile(idx));
            previewChipsList.appendChild(chip);
        });

        if (window.lucide) window.lucide.createIcons();
    }

    // Mic toggle
    if (btnMic) {
        btnMic.addEventListener('click', () => {
            isRecording = !isRecording;
            if (isRecording) {
                btnMic.classList.add('active');
                showToast('Mendengarkan instruksi suara...', 'mic');
            } else {
                btnMic.classList.remove('active');
                showToast('Perekaman audio selesai.', 'check');
            }
        });
    }

    // Chat submit
    if (sceneryChatForm) {
        sceneryChatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const val = sceneryChatInput ? sceneryChatInput.value.trim() : '';

            if (!val && attachedFiles.length === 0) {
                showToast('Silakan ketik instruksi atau lampirkan berkas.', 'alert-circle');
                return;
            }

            const count = attachedFiles.length;
            const msg = count > 0 
                ? `Instruksi dikirim ke ${currentModel} (${currentThinking} reasoning) dengan ${count} berkas` 
                : `Instruksi dikirim ke ${currentModel} (${currentThinking} reasoning)`;

            showToast(msg, 'check-circle-2');

            if (sceneryChatInput) sceneryChatInput.value = '';
            attachedFiles = [];
            renderFiles();
        });
    }

    let toastTimer = null;
    function showToast(msg, iconName = 'check-circle-2') {
        if (!sceneryToast || !sceneryToastText) return;
        sceneryToastText.textContent = msg;

        sceneryToast.querySelector('svg')?.remove();
        const icon = document.createElement('i');
        icon.setAttribute('data-lucide', iconName);
        sceneryToast.prepend(icon);
        if (window.lucide) window.lucide.createIcons();

        sceneryToast.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => {
            sceneryToast.classList.remove('show');
        }, 2600);
    }
});