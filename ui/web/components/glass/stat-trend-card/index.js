const stage = document.getElementById('chartStage');
const point = document.getElementById('cursorPoint');
const tooltip = document.getElementById('chartTooltip');
const revenueText = document.getElementById('statRevenue');

const tfData = {
    '24h': { rev: '148,620', area: 'M0,70 Q40,55 80,60 T160,35 T240,40 T320,15 L320,90 L0,90 Z', line: 'M0,70 Q40,55 80,60 T160,35 T240,40 T320,15' },
    '7d': { rev: '412,890', area: 'M0,80 Q50,60 100,50 T200,45 T280,25 T320,20 L320,90 L0,90 Z', line: 'M0,80 Q50,60 100,50 T200,45 T280,25 T320,20' },
    '30d': { rev: '1,894,300', area: 'M0,65 Q60,40 120,45 T220,30 T300,15 T320,10 L320,90 L0,90 Z', line: 'M0,65 Q60,40 120,45 T220,30 T300,15 T320,10' },
    '1y': { rev: '18,450,200', area: 'M0,85 Q80,70 140,55 T240,30 T300,10 T320,5 L320,90 L0,90 Z', line: 'M0,85 Q80,70 140,55 T240,30 T300,10 T320,5' }
};

document.querySelectorAll('.btn-time').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.btn-time').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const tf = btn.dataset.tf;
        const d = tfData[tf];
        revenueText.textContent = d.rev;
        document.getElementById('sparkArea').setAttribute('d', d.area);
        document.getElementById('sparkLine').setAttribute('d', d.line);
    });
});

stage.addEventListener('mousemove', (e) => {
    const rect = stage.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = Math.max(10, Math.min(80, e.clientY - rect.top));
    
    point.style.display = 'block';
    point.style.left = `${x}px`;
    point.style.top = `${y}px`;

    tooltip.style.display = 'block';
    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
    
    const approxVal = Math.floor(130000 + (x / rect.width) * 35000);
    tooltip.textContent = `$${approxVal.toLocaleString()}`;
});

stage.addEventListener('mouseleave', () => {
    point.style.display = 'none';
    tooltip.style.display = 'none';
});