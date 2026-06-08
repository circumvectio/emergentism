// Background canvas animation
        const bgCanvas = document.getElementById('bgCanvas');
        const bgCtx = bgCanvas.getContext('2d');
        
        function resizeBg() {
            bgCanvas.width = window.innerWidth;
            bgCanvas.height = window.innerHeight;
        }
        resizeBg();
        window.addEventListener('resize', resizeBg);
        
        // Particle system for background
        const particles = [];
        const particleCount = 60;
        
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3,
                size: Math.random() * 2 + 0.5,
                alpha: Math.random() * 0.3 + 0.1
            });
        }
        
        function drawBackground() {
            bgCtx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            bgCtx.fillRect(0, 0, bgCanvas.width, bgCanvas.height);
            
            particles.forEach((p, i) => {
                p.x += p.vx;
                p.y += p.vy;
                
                if (p.x < 0) p.x = bgCanvas.width;
                if (p.x > bgCanvas.width) p.x = 0;
                if (p.y < 0) p.y = bgCanvas.height;
                if (p.y > bgCanvas.height) p.y = 0;
                
                bgCtx.fillStyle = `rgba(100, 150, 255, ${p.alpha})`;
                bgCtx.beginPath();
                bgCtx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                bgCtx.fill();
            });
            
            // Draw connections
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    
                    if (dist < 150) {
                        bgCtx.strokeStyle = `rgba(100, 150, 255, ${0.05 * (1 - dist / 150)})`;
                        bgCtx.lineWidth = 0.5;
                        bgCtx.beginPath();
                        bgCtx.moveTo(particles[i].x, particles[i].y);
                        bgCtx.lineTo(particles[j].x, particles[j].y);
                        bgCtx.stroke();
                    }
                }
            }
            
            requestAnimationFrame(drawBackground);
        }
        
        drawBackground();
        
        // Mini preview animations
        function createPreview(canvasId, drawFn) {
            const canvas = document.getElementById(canvasId);
            const ctx = canvas.getContext('2d');
            canvas.width = 320;
            canvas.height = 180;
            
            let time = 0;
            
            function animate() {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                time += 0.016;
                drawFn(ctx, canvas.width, canvas.height, time);
                
                requestAnimationFrame(animate);
            }
            
            animate();
        }
        
        // Preview 1: Transcendental Trinity
        createPreview('preview1', (ctx, w, h, t) => {
            const cx = w / 2;
            const cy = h / 2;
            const progress = (Math.sin(t * 0.5) + 1) / 2;
            
            // Dot expanding
            const radius = 5 + progress * 20;
            const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius * 2);
            gradient.addColorStop(0, 'rgba(255, 255, 200, 0.8)');
            gradient.addColorStop(0.5, 'rgba(100, 150, 255, 0.3)');
            gradient.addColorStop(1, 'transparent');
            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(cx, cy, radius * 2, 0, Math.PI * 2);
            ctx.fill();
            
            // Line
            if (progress > 0.3) {
                ctx.strokeStyle = `rgba(255, 204, 0, ${(progress - 0.3) / 0.7})`;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(cx - 80, cy);
                ctx.lineTo(cx + 80, cy);
                ctx.stroke();
            }
            
            // Angle arc
            if (progress > 0.5) {
                const angleProgress = (progress - 0.5) / 0.5;
                ctx.strokeStyle = 'rgba(255, 100, 100, 0.5)';
                ctx.beginPath();
                ctx.arc(cx, cy, 30, 0, -angleProgress * Math.PI / 2, true);
                ctx.stroke();
            }
        });
        
        // Preview 2: Second Dimension
        createPreview('preview2', (ctx, w, h, t) => {
            const cx = w / 2;
            const cy = h / 2;
            const progress = (Math.sin(t * 0.4 + 1) + 1) / 2;
            
            // Circle
            const radius = 40 + progress * 20;
            ctx.strokeStyle = 'rgba(100, 150, 255, 0.4)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.stroke();
            
            // Line both ways
            const lineWidth = 60 + progress * 40;
            ctx.strokeStyle = `rgba(255, 200, 50, ${0.5 + progress * 0.5})`;
            ctx.lineWidth = 2;
            ctx.shadowColor = '#ffcc00';
            ctx.shadowBlur = 8;
            ctx.beginPath();
            ctx.moveTo(cx - lineWidth, cy);
            ctx.lineTo(cx + lineWidth, cy);
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            // Arrows
            ctx.fillStyle = 'rgba(255, 50, 50, 0.8)';
            ctx.beginPath();
            ctx.moveTo(cx + lineWidth, cy);
            ctx.lineTo(cx + lineWidth - 8, cy - 4);
            ctx.lineTo(cx + lineWidth - 8, cy + 4);
            ctx.fill();
            
            ctx.fillStyle = 'rgba(50, 255, 100, 0.8)';
            ctx.beginPath();
            ctx.moveTo(cx - lineWidth, cy);
            ctx.lineTo(cx - lineWidth + 8, cy - 4);
            ctx.lineTo(cx - lineWidth + 8, cy + 4);
            ctx.fill();
        });
        
        // Preview 3: Complete Sphere
        createPreview('preview3', (ctx, w, h, t) => {
            const cx = w / 2;
            const cy = h / 2;
            const progress = (Math.sin(t * 0.3 + 2) + 1) / 2;
            const rotation = t * 0.3;
            
            const radius = 35 + progress * 15;
            const squish = 0.7 + 0.3 * Math.cos(rotation);
            
            ctx.save();
            ctx.translate(cx, cy);
            ctx.scale(1, squish);
            ctx.translate(-cx, -cy);
            
            // Sphere
            const gradient = ctx.createRadialGradient(cx - radius * 0.3, cy - radius * 0.3, 0, cx, cy, radius);
            gradient.addColorStop(0, 'rgba(60, 80, 120, 0.6)');
            gradient.addColorStop(1, 'rgba(20, 30, 50, 0.8)');
            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.strokeStyle = 'rgba(100, 150, 255, 0.6)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.stroke();
            
            // Equator
            ctx.strokeStyle = 'rgba(255, 204, 0, 0.8)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.ellipse(cx, cy, radius, radius * squish, 0, 0, Math.PI * 2);
            ctx.stroke();
            
            ctx.restore();
            
            // Center point
            ctx.fillStyle = 'rgba(255, 255, 100, 0.9)';
            ctx.beginPath();
            ctx.arc(cx, cy, 4, 0, Math.PI * 2);
            ctx.fill();
            
            // Multiplication symbol
            ctx.strokeStyle = 'rgba(255, 204, 0, 0.6)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(cx - 8, cy);
            ctx.lineTo(cx + 8, cy);
            ctx.moveTo(cx, cy - 8);
            ctx.lineTo(cx, cy + 8);
            ctx.stroke();
        });
