/**
 * Glass Avatar with Status Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    // Autonomous Status Randomizer (Zero dummy buttons!)
    const agentStates = [
        { name: "Online", color: "#10B981", label: "Online — Siap Menerima Instruksi" },
        { name: "Berpikir", color: "#38BDF8", label: "Berpikir — Proses Penalaran Mendalam" },
        { name: "Mensintesis", color: "#8B5CF6", label: "Mensintesis — Merancang Solusi Artefak" },
        { name: "Siaga", color: "#F59E0B", label: "Siaga — Memantau Event Pipeline" }
    ];

    let stateIndex = 0;

    function applyAgentState(state) {
        const dot = document.getElementById('mainStatusDot');
        const dotText = document.getElementById('liveDotText');
        const label = document.getElementById('statusLabel');

        if (dot) {
            dot.style.background = state.color;
            dot.style.boxShadow = `0 0 12px ${state.color}`;
        }
        if (dotText) {
            dotText.style.background = state.color;
            dotText.style.boxShadow = `0 0 6px ${state.color}`;
        }
        if (label) {
            label.textContent = state.label;
        }
    }

    // Cycle through states organically
    setInterval(() => {
        stateIndex = (stateIndex + 1) % agentStates.length;
        applyAgentState(agentStates[stateIndex]);
    }, 3400);
});
