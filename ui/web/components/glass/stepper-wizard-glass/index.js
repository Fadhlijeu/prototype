let curStep = 1;
const totalSteps = 4;

const stepsData = {
    1: {
        heading: 'Select Regional Compute Cluster',
        desc: 'Choose the low-latency GPU edge datacenter closest to your primary inference pipeline.',
        pills: ['ap-southeast-1 (Singapore)', 'ap-northeast-1 (Tokyo)']
    },
    2: {
        heading: 'Configure Enclave Security Parameters',
        desc: 'Enable hardware cryptographic memory encryption and zero-knowledge TLS attestation.',
        pills: ['AMD SEV-SNP Isolation (Strict)', 'Intel TDX Confidential VM']
    },
    3: {
        heading: 'Deploy Quantized Foundation Models',
        desc: 'Mount optimized neural weights onto PagedAttention high-throughput memory buffers.',
        pills: ['Llama-3-8B-Instruct (FP8)', 'Qwen-2.5-Coder-32B (Q4_K_M)']
    },
    4: {
        heading: 'Final Confirmation & Instant Spin-up',
        desc: 'Review pipeline architecture topology and launch autonomous agent execution.',
        pills: ['Execute Cluster Provisioning', 'Export Terraform Config']
    }
};

function updateWizard() {
    document.getElementById('stepCounter').textContent = `Step ${curStep} of ${totalSteps}`;
    const fillPct = ((curStep - 1) / (totalSteps - 1)) * 100;
    document.getElementById('stepperLineFill').style.width = `${fillPct}%`;

    document.querySelectorAll('.step-node').forEach((node, idx) => {
        const stepNum = idx + 1;
        node.classList.remove('active', 'completed');
        if (stepNum === curStep) {
            node.classList.add('active');
        } else if (stepNum < curStep) {
            node.classList.add('completed');
        }
    });

    const data = stepsData[curStep];
    document.getElementById('stepHeading').textContent = data.heading;
    document.getElementById('stepDesc').textContent = data.desc;
    
    const pillsWrap = document.querySelector('.step-sample-select');
    pillsWrap.innerHTML = data.pills.map((p, i) => `
        <div class="radio-pill ${i === 0 ? 'active' : ''}">
            <i data-lucide="server"></i> ${p}
        </div>
    `).join('');
    if (window.lucide) lucide.createIcons();

    document.getElementById('btnPrevStep').disabled = (curStep === 1);
    document.getElementById('btnNextStep').innerHTML = (curStep === totalSteps)
        ? 'Deploy Pipeline <i data-lucide="rocket"></i>'
        : 'Continue Step <i data-lucide="arrow-right"></i>';
    if (window.lucide) lucide.createIcons();
}

document.getElementById('btnNextStep').addEventListener('click', () => {
    if (curStep < totalSteps) {
        curStep++;
        updateWizard();
    } else {
        alert('Enclave Provisioning Initiated Successfully!');
    }
});

document.getElementById('btnPrevStep').addEventListener('click', () => {
    if (curStep > 1) {
        curStep--;
        updateWizard();
    }
});