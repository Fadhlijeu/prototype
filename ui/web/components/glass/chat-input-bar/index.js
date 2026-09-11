/**
 * Chat Input Bar Logic with File Upload & Preview Reset
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const form = document.getElementById('chatForm');
    const input = document.getElementById('chatInput');
    const fileInput = document.getElementById('chatFileInput');
    const attachBtn = document.getElementById('attachBtn');
    const micBtn = document.getElementById('micBtn');
    const previewArea = document.getElementById('uploadPreviewArea');
    const thumbBox = document.getElementById('previewThumbBox');
    const nameEl = document.getElementById('previewFilename');
    const sizeEl = document.getElementById('previewFilesize');
    const removeBtn = document.getElementById('btnRemoveMedia');

    let currentUploadedFile = null;

    if (attachBtn && fileInput) {
        attachBtn.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files && fileInput.files[0]) {
                const file = fileInput.files[0];
                currentUploadedFile = file;

                nameEl.textContent = file.name;
                const sizeKb = (file.size / 1024).toFixed(1);
                sizeEl.textContent = sizeKb > 1024 ? `${(sizeKb / 1024).toFixed(2)} MB` : `${sizeKb} KB`;

                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        thumbBox.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                    };
                    reader.readAsDataURL(file);
                } else {
                    thumbBox.innerHTML = `<i data-lucide="file-text"></i>`;
                    if (window.lucide) window.lucide.createIcons();
                }

                previewArea.classList.add('active');
                attachBtn.classList.add('active');
            }
        });
    }

    function removeMedia() {
        currentUploadedFile = null;
        if (fileInput) fileInput.value = '';
        if (previewArea) previewArea.classList.remove('active');
        if (attachBtn) attachBtn.classList.remove('active');
    }

    if (removeBtn) {
        removeBtn.addEventListener('click', removeMedia);
    }

    let toastTimer = null;
    function showToast(msg, iconName = 'check-circle-2') {
        const toast = document.getElementById('toastBox');
        if (!toast) return;
        const text = document.getElementById('toastText');
        text.textContent = msg;

        toast.querySelector('svg')?.remove();
        const icon = document.createElement('i');
        icon.setAttribute('data-lucide', iconName);
        toast.prepend(icon);
        if (window.lucide) window.lucide.createIcons();

        toast.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    if (micBtn) {
        let isRecording = false;
        micBtn.addEventListener('click', () => {
            isRecording = !isRecording;
            if (isRecording) {
                micBtn.classList.add('active');
                showToast('Mendengarkan suara...', 'mic');
            } else {
                micBtn.classList.remove('active');
                showToast('Perekaman selesai.', 'check');
            }
        });
    }

    if (form && input) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = input.value.trim();

            if (!text && !currentUploadedFile) {
                showToast('Ketik pesan atau lampirkan berkas terlebih dahulu.', 'alert-circle');
                return;
            }

            const sentMsg = currentUploadedFile ? `Terkirim: "${text || currentUploadedFile.name}" dengan 1 berkas` : `Terkirim: "${text}"`;
            showToast(sentMsg, 'check-circle-2');

            // Reset input and uploaded media
            input.value = '';
            removeMedia();
        });
    }
});
