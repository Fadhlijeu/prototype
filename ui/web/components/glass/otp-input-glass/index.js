const boxes = document.querySelectorAll('.otp-box');
const feedback = document.getElementById('otpFeedback');
const btnVerify = document.getElementById('btnVerify');

boxes.forEach((box, idx) => {
    box.addEventListener('input', (e) => {
        if (e.target.value.length === 1 && idx < boxes.length - 1) {
            boxes[idx + 1].focus();
        }
    });

    box.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && !box.value && idx > 0) {
            boxes[idx - 1].focus();
        }
    });

    box.addEventListener('paste', (e) => {
        e.preventDefault();
        const text = (e.clipboardData || window.clipboardData).getData('text').trim();
        if (/^\d{6}$/.test(text)) {
            text.split('').forEach((ch, i) => {
                if (boxes[i]) boxes[i].value = ch;
            });
            boxes[boxes.length - 1].focus();
        }
    });
});

btnVerify.addEventListener('click', () => {
    const code = Array.from(boxes).map(b => b.value).join('');
    if (code.length === 6) {
        feedback.style.color = '#10B981';
        feedback.textContent = 'Token Validated: Enclave Access Granted!';
    } else {
        feedback.style.color = '#EF4444';
        feedback.textContent = 'Please enter complete 6-digit code.';
    }
});