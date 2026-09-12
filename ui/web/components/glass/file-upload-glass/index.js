const dropzone = document.getElementById('dropzone');
const btnBrowse = document.getElementById('btnBrowse');
const fileInput = document.getElementById('realFileInput');
const btnAddDemo = document.getElementById('btnAddDemo');
const fileQueue = document.getElementById('fileQueue');

btnBrowse.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
});

dropzone.addEventListener('click', () => {
    fileInput.click();
});

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        addFileItem(e.dataTransfer.files[0].name, '1.2 GB');
    }
});

document.getElementById('btnCancelFile').addEventListener('click', () => {
    const item = document.getElementById('demoFileItem');
    if (item) item.remove();
});

btnAddDemo.addEventListener('click', () => {
    addFileItem('instruct_dataset_v4.parquet', '420 MB');
});

function addFileItem(name, size) {
    const div = document.createElement('div');
    div.className = 'queue-item';
    div.innerHTML = `
        <div class="file-type-icon" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3); color: #10B981;">
            <i data-lucide="check-circle-2"></i>
        </div>
        <div class="file-info-col">
            <div class="file-name-row">
                <span class="file-name">${name}</span>
                <span class="file-progress-pct" style="color: #10B981;">100%</span>
            </div>
            <div class="progress-bar-track">
                <div class="progress-bar-fill" style="width: 100%; background: #10B981;"></div>
            </div>
            <div class="file-meta-row">
                <span>${size} • Verified SHA-256</span>
                <span style="color: #10B981;">Complete</span>
            </div>
        </div>
        <button type="button" class="btn-cancel-file" onclick="this.parentElement.remove()" title="Remove">
            <i data-lucide="x"></i>
        </button>
    `;
    fileQueue.appendChild(div);
    if (window.lucide) lucide.createIcons();
}