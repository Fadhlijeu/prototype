// Initialize Lucide Icons
if (window.lucide) {
    lucide.createIcons();
}

function slidePills(delta) {
    const track = document.getElementById('pillsTrack');
    if (track) track.scrollBy({ left: delta, behavior: 'smooth' });
}

function triggerPill(action) {
    console.log('Action activated:', action);
}
