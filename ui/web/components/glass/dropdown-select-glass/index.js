
function toggleDropdown() {
    document.getElementById('drop').classList.toggle('open');
}

function selectOption(text, el) {
    document.getElementById('selectedLabel').innerText = text;
    document.querySelectorAll('.dropdown-item').forEach(i => i.classList.remove('selected'));
    el.classList.add('selected');
    document.getElementById('drop').classList.remove('open');
}
