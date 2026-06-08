const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        let width, height, centerX, centerY;
        let animationId;
        let isPlaying = true;
        let speed = 1.0;
        let startTime = Date.now();
        let elapsedTime = 0;
        let pausedTime = 0;
        
        // Animation phases (in seconds)
        const PHASES = {
            DOT_HOLD: 1.5,
            DOT_EXPAND: 2.5,
            LINE_GLOW: 2.0,
            ANGLE_SWEEP: 2.5,
            REVEAL: 3.0
        };
        const TOTAL_DURATION = PHASES.DOT_HOLD + PHASES.DOT_EXPAND + PHASES.LINE_GLOW + PHASES.ANGLE_SWEEP + PHASES.REVEAL;
        
        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            centerX = width / 2;
            centerY = height / 2;
        }
        
        resize();
        window.addEventListener('resize', resize);
        
        // Glow effect helper
        function drawGlow(x, y, radius, color, intensity = 1) {
            const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
            gradient.addColorStop(0, color);
            gradient.addColorStop(0.3, color.replace('1)', `${0.6 * intensity})`).replace('rgb', 'rgba'));
            gradient.addColorStop(1, 'transparent');
            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fill();
        }
        
        function drawRiemannSphere(progress, angleProgress) {
            const maxRadius = Math.min(width, height) * 0.35;
            const sphereRadius = maxRadius * Math.min(progress * 2, 1);
            
            // Draw the Riemann sphere (circle)
            if (sphereRadius > 5) {
                // Outer glow
                drawGlow(centerX, centerY, sphereRadius * 1.5, 'rgba(100, 150, 255, 0.3)', progress);
                
                // Sphere outline
                ctx.strokeStyle = `rgba(100, 150, 255, ${0.3 + progress * 0.4})`;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.arc(centerX, centerY, sphereRadius, 0, Math.PI * 2);
                ctx.stroke();
                
                // Equator line (the complex plane)
                const equatorY = centerY;
                const lineHalfWidth = sphereRadius * Math.min(angleProgress * 2, 1);
                
                if (lineHalfWidth > 0) {
                    // Glow for the line
                    ctx.shadowColor = '#ffcc00';
                    ctx.shadowBlur = 15 * progress;
                    ctx.strokeStyle = `rgba(255, 204, 0, ${0.5 + progress * 0.5})`;
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.moveTo(centerX - lineHalfWidth, equatorY);
                    ctx.lineTo(centerX + lineHalfWidth, equatorY);
                    ctx.stroke();
                    ctx.shadowBlur = 0;
                }
                
                // Sweeping angle indicator
                if (angleProgress > 0 && angleProgress <= 1) {
                    const angle = angleProgress * Math.PI / 2;
                    const arrowLen = sphereRadius * 0.7;
                    const endX = centerX + Math.cos(angle) * arrowLen;
                    const endY = equatorY - Math.sin(angle) * arrowLen;
                    
                    ctx.strokeStyle = `rgba(255, 100, 100, ${0.5 + Math.sin(angleProgress * Math.PI * 10) * 0.3})`;
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(centerX, equatorY);
                    ctx.lineTo(endX, endY);
                    ctx.stroke();
                    
                    // Angle arc
                    ctx.strokeStyle = `rgba(255, 100, 100, 0.5)`;
                    ctx.beginPath();
                    ctx.arc(centerX, equatorY, sphereRadius * 0.3, 0, -angle, true);
                    ctx.stroke();
                    
                    // Angle label
                    if (angleProgress > 0.3) {
                        ctx.fillStyle = `rgba(255, 100, 100, ${(angleProgress - 0.3) / 0.7})`;
                        ctx.font = '14px Courier New';
                        ctx.fillText(`${Math.round(angleProgress * 90)}°`, centerX + sphereRadius * 0.35, equatorY - sphereRadius * 0.15);
                    }
                }
            }
            
            // North pole indicator (infinity)
            if (progress > 0.3) {
                const poleAlpha = Math.min((progress - 0.3) / 0.3, 1);
                const poleY = centerY - sphereRadius;
                drawGlow(centerX, poleY, 15, 'rgba(255, 50, 50, 1)', poleAlpha);
                ctx.fillStyle = `rgba(255, 255, 255, ${poleAlpha})`;
                ctx.font = '12px Courier New';
                ctx.fillText('∞', centerX - 8, poleY + 4);
            }
            
            // South pole indicator (zero)
            if (progress > 0.4) {
                const poleAlpha = Math.min((progress - 0.4) / 0.3, 1);
                const poleY = centerY + sphereRadius;
                drawGlow(centerX, poleY, 15, 'rgba(50, 255, 50, 1)', poleAlpha);
                ctx.fillStyle = `rgba(255, 255, 255, ${poleAlpha})`;
                ctx.font = '12px Courier New';
                ctx.fillText('0', centerX - 3, poleY + 4);
            }
        }
        
        function drawBindu(progress) {
            const maxRadius = Math.min(width, height) * 0.02;
            const radius = maxRadius * Math.min(progress * 3, 1);
            const alpha = Math.min(progress * 2, 1);
            
            // Pulsing glow
            const pulse = 1 + Math.sin(Date.now() / 200) * 0.1;
            
            drawGlow(centerX, centerY, radius * 3 * pulse, 'rgba(255, 255, 200, 1)', alpha);
            drawGlow(centerX, centerY, radius * 1.5, 'rgba(255, 255, 255, 1)', alpha);
            
            // Core dot
            ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
            ctx.fill();
            
            // Label
            if (progress > 0.5) {
                const labelAlpha = Math.min((progress - 0.5) / 0.5, 1);
                ctx.fillStyle = `rgba(255, 255, 200, ${labelAlpha})`;
                ctx.font = '16px Courier New';
                ctx.fillText('BINDU', centerX + radius + 10, centerY + 5);
                ctx.font = '12px Courier New';
                ctx.fillText('(The Dot)', centerX + radius + 10, centerY + 20);
            }
        }
        
        function drawInfinityLines(progress) {
            const lineLength = Math.min(width, height) * 0.4 * progress;
            const alpha = Math.min(progress, 1);
            
            // Vertical line going up (to infinity)
            ctx.strokeStyle = `rgba(255, 50, 50, ${alpha * 0.5})`;
            ctx.lineWidth = 1;
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(centerX, centerY - lineLength);
            ctx.stroke();
            
            // Arrow head
            if (progress > 0.3) {
                const arrowAlpha = Math.min((progress - 0.3) / 0.7, 1);
                ctx.setLineDash([]);
                ctx.fillStyle = `rgba(255, 50, 50, ${arrowAlpha * 0.7})`;
                ctx.beginPath();
                ctx.moveTo(centerX, centerY - lineLength);
                ctx.lineTo(centerX - 6, centerY - lineLength + 10);
                ctx.lineTo(centerX + 6, centerY - lineLength + 10);
                ctx.closePath();
                ctx.fill();
                
                ctx.fillStyle = `rgba(255, 255, 255, ${arrowAlpha * 0.5})`;
                ctx.font = '12px Courier New';
                ctx.fillText('∞', centerX - 4, centerY - lineLength - 10);
            }
            
            ctx.setLineDash([]);
        }
        
        function drawComplexPlane(progress) {
            // Draw extending plane lines
            const lineAlpha = Math.min(progress * 2, 1);
            
            // Horizontal axis
            ctx.strokeStyle = `rgba(100, 150, 255, ${lineAlpha * 0.3})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(0, centerY);
            ctx.lineTo(width, centerY);
            ctx.stroke();
            
            // Vertical axis
            ctx.beginPath();
            ctx.moveTo(centerX, 0);
            ctx.lineTo(centerX, height);
            ctx.stroke();
            
            // Grid lines
            const gridSpacing = 50;
            for (let x = centerX % gridSpacing; x < width; x += gridSpacing) {
                ctx.strokeStyle = `rgba(100, 150, 255, ${lineAlpha * 0.1})`;
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, height);
                ctx.stroke();
            }
            for (let y = centerY % gridSpacing; y < height; y += gridSpacing) {
                ctx.strokeStyle = `rgba(100, 150, 255, ${lineAlpha * 0.1})`;
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(width, y);
                ctx.stroke();
            }
        }
        
        function drawWavePattern(progress) {
            const waveAlpha = Math.min(progress * 2, 1);
            const amplitude = Math.min(height * 0.15 * progress, 30);
            const frequency = 0.02;
            
            ctx.strokeStyle = `rgba(200, 100, 255, ${waveAlpha * 0.6})`;
            ctx.lineWidth = 2;
            ctx.beginPath();
            
            for (let x = 0; x < width; x++) {
                const y = centerY + Math.sin((x - centerX) * frequency + Date.now() / 500) * amplitude;
                if (x === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();
        }
        
        function getAnimationProgress() {
            let time = elapsedTime;
            const phase = {
                dotHold: Math.min(time / PHASES.DOT_HOLD, 1),
                dotExpand: Math.min(Math.max(time - PHASES.DOT_HOLD, 0) / PHASES.DOT_EXPAND, 1),
                lineGlow: Math.min(Math.max(time - PHASES.DOT_HOLD - PHASES.DOT_EXPAND, 0) / PHASES.LINE_GLOW, 1),
                angleSweep: Math.min(Math.max(time - PHASES.DOT_HOLD - PHASES.DOT_EXPAND - PHASES.LINE_GLOW, 0) / PHASES.ANGLE_SWEEP, 1),
                reveal: Math.min(Math.max(time - PHASES.DOT_HOLD - PHASES.DOT_EXPAND - PHASES.LINE_GLOW - PHASES.ANGLE_SWEEP, 0) / PHASES.REVEAL, 1)
            };
            
            return phase;
        }
        
        function render() {
            // Clear with fade effect
            ctx.fillStyle = 'rgba(0, 0, 0, 0.15)';
            ctx.fillRect(0, 0, width, height);
            
            const phases = getAnimationProgress();
            const totalProgress = elapsedTime / TOTAL_DURATION;
            
            // Update phase indicator
            let phaseNum = 0;
            if (phases.dotHold < 1) phaseNum = 1;
            else if (phases.dotExpand < 1) phaseNum = 2;
            else if (phases.lineGlow < 1) phaseNum = 3;
            else if (phases.angleSweep < 1) phaseNum = 4;
            else phaseNum = 5;
            document.getElementById('phase').textContent = `PHASE: ${phaseNum} / 5`;
            
            // Draw subtle background pattern
            drawComplexPlane(Math.min(totalProgress * 1.5, 1));
            
            // Draw the bindu (dot) - expanding into Riemann sphere
            drawBindu(phases.dotHold);
            
            // Draw Riemann sphere with line
            drawRiemannSphere(phases.dotExpand + phases.lineGlow * 0.3, phases.angleSweep);
            
            // Draw infinity indicator
            drawInfinityLines(phases.lineGlow + phases.angleSweep * 0.3);
            
            // Draw wave pattern
            drawWavePattern(phases.reveal);
            
            // Show equation at the end
            const equation = document.getElementById('equation');
            if (phases.reveal > 0.1) {
                equation.classList.add('visible');
            } else {
                equation.classList.remove('visible');
            }
            
            // Loop or stop
            if (isPlaying) {
                elapsedTime += 16 * speed;
                if (elapsedTime > TOTAL_DURATION * 1000 + 2000) {
                    // Reset for loop
                    elapsedTime = 0;
                }
            }
            
            animationId = requestAnimationFrame(render);
        }
        
        // Controls
        const playPauseBtn = document.getElementById('playPauseBtn');
        playPauseBtn.addEventListener('click', () => {
            isPlaying = !isPlaying;
            playPauseBtn.textContent = isPlaying ? 'PAUSE' : 'PLAY';
            playPauseBtn.classList.toggle('active', !isPlaying);
        });
        
        document.getElementById('resetBtn').addEventListener('click', () => {
            elapsedTime = 0;
        });
        
        document.getElementById('speedSlider').addEventListener('input', (e) => {
            speed = parseFloat(e.target.value);
            document.getElementById('speedValue').textContent = speed.toFixed(1);
        });
        
        // Start animation
        render();
