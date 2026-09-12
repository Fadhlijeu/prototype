const slider = document.getElementById('batRange');
const fluid = document.getElementById('batFluid');
const pctText = document.getElementById('batPct');
const timeText = document.getElementById('batTime');
const statusText = document.getElementById('batStatus');

slider.addEventListener('input', (e) => {
    const val = parseInt(e.target.value);
    fluid.style.width = `${val}%`;
    pctText.textContent = val;

    // Color shifting
    if (val > 50) {
        fluid.style.background = 'linear-gradient(90deg, #059669 0%, #10B981 60%, #34D399 100%)';
        fluid.style.boxShadow = '0 0 20px rgba(16, 185, 129, 0.5)';
        statusText.style.color = '#10B981';
        statusText.textContent = 'SUPERCHARGING ACTIVE (65W)';
    } else if (val > 20) {
        fluid.style.background = 'linear-gradient(90deg, #D97706 0%, #F59E0B 60%, #FCD34D 100%)';
        fluid.style.boxShadow = '0 0 20px rgba(245, 158, 11, 0.5)';
        statusText.style.color = '#F59E0B';
        statusText.textContent = 'DISCHARGING • NORMAL WORKLOAD';
    } else {
        fluid.style.background = 'linear-gradient(90deg, #DC2626 0%, #EF4444 60%, #FCA5A5 100%)';
        fluid.style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.5)';
        statusText.style.color = '#EF4444';
        statusText.textContent = 'LOW POWER RESERVE • CONNECT DOCK';
    }

    const hours = Math.floor((val / 100) * 18);
    const mins = Math.floor(((val / 100) * 18 - hours) * 60);
    timeText.textContent = `${hours}h ${mins}m`;
});