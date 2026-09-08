const sheet = document.getElementById('sheet');
        const canvas = document.getElementById('fxCanvas');
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        const work = document.createElement('canvas');
        const wctx = work.getContext('2d', { willReadFrequently: true });

        let W = 0, H = 0, raf = 0, active = false, t = 0, last = 0;

        function resize() {
            const d = Math.min(window.devicePixelRatio || 1, 1.5);
            const rect = sheet.getBoundingClientRect();
            W = Math.max(1, Math.floor(rect.width * d));
            H = Math.max(1, Math.floor(rect.height * d));
            canvas.width = W; canvas.height = H;
            work.width = W; work.height = H;
        }

        function drawScene(c) {
            c.clearRect(0, 0, W, H);
            const g = c.createLinearGradient(0, 0, W, H);
            g.addColorStop(0, '#090A0E');
            g.addColorStop(0.5, '#0D1017');
            g.addColorStop(1, '#08090C');
            c.fillStyle = g;
            c.fillRect(0, 0, W, H);

            const rg = c.createRadialGradient(W * 0.1, H * 0.1, 0, W * 0.1, H * 0.1, W * 0.6);
            rg.addColorStop(0, 'rgba(77, 99, 192, 0.3)');
            rg.addColorStop(1, 'transparent');
            c.fillStyle = rg;
            c.fillRect(0, 0, W, H);
        }

        function distort(time) {
            const data = wctx.getImageData(0, 0, W, H);
            const src = data.data;
            const out = ctx.createImageData(W, H);
            const dst = out.data;

            for (let y = 0; y < H; y += 2) {
                for (let x = 0; x < W; x += 2) {
                    const nx = x / W, ny = y / H;
                    const a = Math.sin(ny * 18 + time * 0.9) * 6 + Math.sin(ny * 40 - time * 0.35) * 2;
                    const b = Math.cos(nx * 15 - time * 0.75) * 6 + Math.sin(nx * 32 + time * 0.4) * 1.8;
                    const swirl = Math.sin(nx * 20 + ny * 12 + time * 0.6) * 5;
                    const dx = Math.round(a + swirl * 0.5);
                    const dy = Math.round(b + swirl * 0.3);
                    const sx = Math.max(0, Math.min(W - 1, x + dx));
                    const sy = Math.max(0, Math.min(H - 1, y + dy));
                    const si = (sy * W + sx) * 4;

                    for (let oy = 0; oy < 2; oy++) {
                        for (let ox = 0; ox < 2; ox++) {
                            if (x + ox < W && y + oy < H) {
                                const di = ((y + oy) * W + (x + ox)) * 4;
                                dst[di] = Math.min(255, src[si] * 1.07 + 8);
                                dst[di + 1] = Math.min(255, src[si + 1] * 1.08 + 8);
                                dst[di + 2] = Math.min(255, src[si + 2] * 1.12 + 10);
                                dst[di + 3] = 140;
                            }
                        }
                    }
                }
            }
            ctx.putImageData(out, 0, 0);
        }

        function loop(now) {
            if (!active) return;
            if (!last) last = now;
            if (now - last > 24) {
                t += 0.02;
                last = now;
                wctx.clearRect(0, 0, W, H);
                drawScene(wctx);
                distort(t);
            }
            raf = requestAnimationFrame(loop);
        }

        function openSheet() {
            active = true;
            document.body.classList.add('modal-open');
            resize();
            drawScene(wctx);
            cancelAnimationFrame(raf);
            raf = requestAnimationFrame(loop);
            setTimeout(() => document.getElementById('folderInput').focus(), 350);
        }

        function closeSheet() {
            document.body.classList.remove('modal-open');
            active = false;
            cancelAnimationFrame(raf);
        }

        function updateBtn() {
            const has = document.getElementById('folderInput').value.trim().length > 0;
            document.getElementById('createBtn').disabled = !has;
        }

        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && active) closeSheet();
        });