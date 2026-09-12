const buttons = document.querySelectorAll('.btn-bill');
const priceEl = document.getElementById('priceAmount');
const subEl = document.getElementById('priceSub');

buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const plan = btn.dataset.plan;
        if (plan === 'monthly') {
            priceEl.textContent = '65';
            subEl.textContent = 'Billed monthly ($65/mo)';
        } else {
            priceEl.textContent = '49';
            subEl.textContent = 'Billed annually ($588/year)';
        }
    });
});