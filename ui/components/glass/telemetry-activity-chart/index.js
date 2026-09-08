const container = document.getElementById('bars');
        const heights = [45, 62, 50, 78, 58, 88, 68, 94, 72, 60, 80, 92];
        heights.forEach((h, i) => {
            const b = document.createElement('div');
            b.className = 'bar-col';
            b.style.height = h + '%';
            b.title = `Hour ${i + 1}: ${h}% activity load`;
            b.onclick = () => alert(`Telemetry at hour ${i + 1}: ${h}%`);
            container.appendChild(b);
        });