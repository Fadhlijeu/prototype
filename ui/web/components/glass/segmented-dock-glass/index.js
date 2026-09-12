const items = document.querySelectorAll('.dock-item');
const indicator = document.getElementById('dockIndicator');

const tabsData = {
    overview: {
        title: 'Cluster Overview',
        desc: 'Real-time status of active instances, health probes, and edge telemetry.',
        icon: 'layout-dashboard'
    },
    analytics: {
        title: 'High-Throughput Analytics',
        desc: 'Live streaming metrics: 82.4k req/sec with sub-5ms P99 latency.',
        icon: 'bar-chart-2'
    },
    workflows: {
        title: 'Autonomous Workflows',
        desc: '3 agent pipelines currently executing tasks across Singapore and Tokyo.',
        icon: 'git-branch'
    },
    security: {
        title: 'Enclave Security Shield',
        desc: 'Zero-knowledge verification active. Zero unauthorized attempts detected.',
        icon: 'shield-check'
    },
    settings: {
        title: 'System Preferences',
        desc: 'Configure environment variables, API key rotation, and rate quotas.',
        icon: 'sliders'
    }
};

function updateIndicator(el) {
    indicator.style.left = el.offsetLeft + 'px';
    indicator.style.width = el.offsetWidth + 'px';
}

// Initial position
const activeItem = document.querySelector('.dock-item.active');
if (activeItem) {
    setTimeout(() => updateIndicator(activeItem), 50);
}

items.forEach(item => {
    item.addEventListener('click', () => {
        items.forEach(i => i.classList.remove('active'));
        item.classList.add('active');
        updateIndicator(item);

        const tabKey = item.dataset.tab;
        const data = tabsData[tabKey];
        if (data) {
            document.getElementById('fbTitle').textContent = data.title;
            document.getElementById('fbDesc').textContent = data.desc;
            const iconWrap = document.getElementById('fbIcon');
            iconWrap.innerHTML = `<i data-lucide="${data.icon}"></i>`;
            if (window.lucide) lucide.createIcons();
        }
    });
});

window.addEventListener('resize', () => {
    const cur = document.querySelector('.dock-item.active');
    if (cur) updateIndicator(cur);
});