const tagCloud = document.getElementById('tagCloud');
const input = document.getElementById('newTagInput');
const btnAdd = document.getElementById('btnAddTag');
const counter = document.getElementById('activeCount');

function updateCounter() {
    const active = tagCloud.querySelectorAll('.glass-tag.active').length;
    counter.textContent = `${active} Active`;
}

function bindTagEvents(tag) {
    tag.addEventListener('click', (e) => {
        if (e.target.closest('.btn-remove-tag')) {
            tag.remove();
            updateCounter();
            return;
        }
        tag.classList.toggle('active');
        updateCounter();
    });
}

document.querySelectorAll('.glass-tag').forEach(bindTagEvents);

function addTag() {
    const val = input.value.trim();
    if (!val) return;
    const span = document.createElement('span');
    span.className = 'glass-tag active';
    span.dataset.name = val;
    span.innerHTML = `
        <span class="tag-glow-dot cyan"></span>
        <span class="tag-name">${val}</span>
        <button type="button" class="btn-remove-tag"><i data-lucide="x"></i></button>
    `;
    tagCloud.appendChild(span);
    bindTagEvents(span);
    input.value = '';
    if (window.lucide) lucide.createIcons();
    updateCounter();
}

btnAdd.addEventListener('click', addTag);
input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addTag();
});