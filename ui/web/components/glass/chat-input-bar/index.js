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
    const filesList = document.getElementById('previewFilesList');
    const countBadge = document.getElementById('previewCountBadge');
    const clearAllBtn = document.getElementById('btnClearAll');

    let uploadedFiles = [];

    if (attachBtn && fileInput) {
        attachBtn.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files && fileInput.files.length > 0) {
                for (let i = 0; i < fileInput.files.length; i++) {
                    uploadedFiles.push(fileInput.files[i]);
                }
                renderFilesList();
                fileInput.value = '';
            }
        });
    }

    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', () => {
            uploadedFiles = [];
            renderFilesList();
        });
    }

    function removeFile(index) {
        uploadedFiles.splice(index, 1);
        renderFilesList();
    }

    function getFileIcon(name) {
        const ext = name.split('.').pop().toLowerCase();
        if (['jpg', 'jpeg', 'png', 'webp', 'gif', 'svg'].includes(ext)) return 'image';
        if (['pdf'].includes(ext)) return 'file-text';
        if (['doc', 'docx', 'txt', 'md'].includes(ext)) return 'file-text';
        if (['zip', 'rar', 'tar', 'gz'].includes(ext)) return 'archive';
        return 'file';
    }

    function renderFilesList() {
        if (!previewArea || !filesList) return;

        if (uploadedFiles.length === 0) {
            previewArea.classList.remove('active');
            if (attachBtn) attachBtn.classList.remove('active');
            filesList.innerHTML = '';
            return;
        }

        previewArea.classList.add('active');
        if (attachBtn) attachBtn.classList.add('active');
        if (countBadge) countBadge.textContent = `Lampiran (${uploadedFiles.length})`;
        filesList.innerHTML = '';

        uploadedFiles.forEach((file, index) => {
            const chip = document.createElement('div');
            chip.className = 'file-chip';

            const thumb = document.createElement('div');
            thumb.className = 'chip-thumb';

            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                const reader = new FileReader();
                reader.onload = (e) => { img.src = e.target.result; };
                reader.readAsDataURL(file);
                thumb.appendChild(img);
            } else {
                thumb.innerHTML = `<i data-lucide="${getFileIcon(file.name)}"></i>`;
            }

            const sizeKb = (file.size / 1024).toFixed(1);
            const sizeStr = sizeKb > 1024 ? `${(sizeKb / 1024).toFixed(2)} MB` : `${sizeKb} KB`;

            const meta = document.createElement('div');
            meta.className = 'chip-meta';
            meta.innerHTML = `
                <span class="chip-name" title="${file.name}">${file.name}</span>
                <span class="chip-size">${sizeStr}</span>
            `;

            const removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.className = 'chip-btn-remove';
            removeBtn.title = 'Hapus berkas ini';
            removeBtn.innerHTML = '<i data-lucide="x"></i>';
            removeBtn.addEventListener('click', () => removeFile(index));

            chip.appendChild(thumb);
            chip.appendChild(meta);
            chip.appendChild(removeBtn);
            filesList.appendChild(chip);
        });

        if (window.lucide) window.lucide.createIcons();
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

            if (!text && uploadedFiles.length === 0) {
                showToast('Ketik pesan atau lampirkan berkas terlebih dahulu.', 'alert-circle');
                return;
            }

            const count = uploadedFiles.length;
            const sentMsg = count > 0 ? `Terkirim: "${text || 'Berkas'}" dengan ${count} lampiran` : `Terkirim: "${text}"`;
            showToast(sentMsg, 'check-circle-2');

            // Reset input and clear uploaded media
            input.value = '';
            uploadedFiles = [];
            renderFilesList();
        });
    }
});
