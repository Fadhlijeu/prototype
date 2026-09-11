lucide.createIcons();

let folderToastTimer = null;
function openFolder(name) {
    const toast = document.getElementById('folderToast');
    const text = document.getElementById('folderToastText');
    if (!toast || !text) return;
    text.textContent = `Membuka berkas: ${name}`;
    toast.classList.add('show');
    clearTimeout(folderToastTimer);
    folderToastTimer = setTimeout(() => {
        toast.classList.remove('show');
    }, 2200);
}