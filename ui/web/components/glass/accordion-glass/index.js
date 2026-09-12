function toggleAccordion(id) {
    const card = document.getElementById(id);
    if (!card) return;
    card.classList.toggle('open');
}

const btnToggleAll = document.getElementById('btnToggleAll');
let allExpanded = false;

btnToggleAll.addEventListener('click', () => {
    allExpanded = !allExpanded;
    document.querySelectorAll('.accordion-card').forEach(card => {
        card.classList.toggle('open', allExpanded);
    });
    btnToggleAll.innerHTML = allExpanded 
        ? '<i data-lucide="chevrons-down-up"></i> Collapse All' 
        : '<i data-lucide="chevrons-up-down"></i> Expand All';
    if (window.lucide) lucide.createIcons();
});