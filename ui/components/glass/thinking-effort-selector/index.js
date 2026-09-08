lucide.createIcons();
        const levels = ['Low', 'Medium', 'High'];
        let idx = 2;
        function cycleEffort() {
            idx = (idx + 1) % levels.length;
            document.getElementById('effortVal').textContent = levels[idx];
        }