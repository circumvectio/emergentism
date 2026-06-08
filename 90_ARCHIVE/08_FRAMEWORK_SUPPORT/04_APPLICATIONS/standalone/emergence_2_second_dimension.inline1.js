const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        let width, height, centerX, centerY;
        let animationId;
        let isPlaying = true;
        let speed = 1.0;
        let elapsedTime = 0;
        
        // Animation phases (in seconds)
        const PHASES = {
            INITIAL_LINE: 2.0,
            NEGATIVE_EXTEND: 2.5,
            CIRCLE_EMERGE: 2.5,
            FULL_SECOND_D: 2.5,
            REVEAL: 2.5
        };
        const TOTAL_DURATION = Object.values(PHASES).reduce((a, b) => a + b, 0);
        
        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            centerX = width / 2;
            centerY = height / 2;
        }
        
        resize();
        window.addEventListener('resize', resize);
        
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
        
        function drawRiemannSphere(progress) {
            const maxRadius = Math.min(width, height) * 0.35;
            const sphereRadius = maxRadius * Math.min(progress * 1.5, 1);
            
            if (sphereRadius > 5) {
                // Outer glow
                drawGlow(centerX, centerY, sphereRadius * 1.5, 'rgba(100, 150, 255, 0.3)', progress);
                
                // Sphere outline
                ctx.strokeStyle = `rgba(100, 150, 255, ${0.3 + progress * 0.4})`;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.arc(centerX, centerY, sphereRadius, 0, Math.PI * 2);
                ctx.stroke();
            }
            
            return sphereRadius;
        }
        
        function drawInfinityLineOneDirection(progress, sphereRadius) {
            const lineAlpha = Math.min(progress * 2, 1);
            
            // Line going RIGHT (positive direction)
            ctx.strokeStyle = `rgba(255, 50, 50, ${lineAlpha * 0.7})`;
            ctx.lineWidth = 3;
            ctx.shadowColor = '#ff3333';
            ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(centerX + Math.min(progress * 2, 1) * width * 0.5, centerY);
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            // Arrow head
            if (progress > 0.5) {
                const arrowX = centerX + Math.min((progress - 0.5) * 4, 1) * width * 0.5;
                ctx.fillStyle = `rgba(255, 50, 50, ${lineAlpha})`;
                ctx.beginPath();
                ctx.moveTo(arrowX, centerY);
                ctx.lineTo(arrowX - 12, centerY - 6);
                ctx.lineTo(arrowX - 12, centerY + 6);
                ctx.closePath();
                ctx.fill();
                
                ctx.fillStyle = `rgba(255, 255, 255, ${lineAlpha * 0.8})`;
                ctx.font = '14px Courier New';
                ctx.fillText('+∞', arrowX + 5, centerY - 10);
            }
            
            // Infinity symbol at north pole
            if (progress > 0.3 && sphereRadius) {
                drawGlow(centerX, centerY - sphereRadius, 10, 'rgba(255, 100, 100, 1)', progress);
                ctx.fillStyle = `rgba(255, 255, 255, ${progress})`;
                ctx.font = '12px Courier New';
                ctx.fillText('∞', centerX - 6, centerY - sphereRadius + 4);
            }
        }
        
        function drawInfinityLineBothDirections(progress, sphereRadius) {
            const lineAlpha = Math.min(progress * 2, 1);
            const extendProgress = Math.min(progress * 2, 1);
            
            // Line going BOTH directions
            ctx.strokeStyle = `rgba(255, 200, 50, ${lineAlpha * 0.9})`;
            ctx.lineWidth = 4;
            ctx.shadowColor = '#ffcc00';
            ctx.shadowBlur = 15;
            ctx.beginPath();
            ctx.moveTo(centerX - extendProgress * width * 0.4, centerY);
            ctx.lineTo(centerX + extendProgress * width * 0.4, centerY);
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            // Left arrow (-∞)
            const leftX = centerX - extendProgress * width * 0.4;
            ctx.fillStyle = `rgba(50, 255, 100, ${lineAlpha})`;
            ctx.beginPath();
            ctx.moveTo(leftX, centerY);
            ctx.lineTo(leftX + 12, centerY - 6);
            ctx.lineTo(leftX + 12, centerY + 6);
            ctx.closePath();
            ctx.fill();
            
            ctx.fillStyle = `rgba(255, 255, 255, ${lineAlpha * 0.8})`;
            ctx.font = '14px Courier New';
            ctx.fillText('-∞', leftX - 25, centerY - 10);
            
            // Right arrow (+∞)
            const rightX = centerX + extendProgress * width * 0.4;
            ctx.fillStyle = `rgba(255, 50, 50, ${lineAlpha})`;
            ctx.beginPath();
            ctx.moveTo(rightX, centerY);
            ctx.lineTo(rightX - 12, centerY - 6);
            ctx.lineTo(rightX - 12, centerY + 6);
            ctx.closePath();
            ctx.fill();
            
            ctx.fillStyle = `rgba(255, 255, 255, ${lineAlpha * 0.8})`;
            ctx.fillText('+∞', rightX + 5, centerY - 10);
            
            // Central point (1)
            drawGlow(centerX, centerY, 20, 'rgba(255, 255, 100, 1)', lineAlpha);
            ctx.fillStyle = `rgba(0, 0, 0, ${lineAlpha})`;
            ctx.font = 'bold 14px Courier New';
            ctx.fillText('1', centerX - 2, centerY + 4);
        }
        
        function drawEmergentCircle(progress, sphereRadius) {
            const circleAlpha = Math.min(progress * 3, 1);
            const circleRadius = sphereRadius * (0.3 + progress * 0.7);
            
            // The emergent circle appears at the equator
            // It's a circle with infinite diameter (straight line on the sphere)
            // But viewed from "above" it appears as a circle
            
            // Draw the circle with dashed style to show it emerges from the line
            ctx.strokeStyle = `rgba(0, 255, 170, ${circleAlpha * 0.8})`;
            ctx.lineWidth = 2;
            ctx.setLineDash([8, 4]);
            ctx.shadowColor = '#00ffaa';
            ctx.shadowBlur = 10 * circleAlpha;
            ctx.beginPath();
            ctx.arc(centerX, centerY, circleRadius, 0, Math.PI * 2);
            ctx.stroke();
            ctx.shadowBlur = 0;
            ctx.setLineDash([]);
            
            // Label
            if (progress > 0.5) {
                const labelAlpha = Math.min((progress - 0.5) * 2, 1);
                ctx.fillStyle = `rgba(0, 255, 170, ${labelAlpha * 0.8})`;
                ctx.font = '12px Courier New';
                ctx.fillText('ν-axis', centerX + circleRadius * 0.7, centerY + circleRadius * 0.7);
            }
        }
        
        function drawCompleteSecondDimension(progress) {
            const alpha = Math.min(progress * 2, 1);
            const maxRadius = Math.min(width, height) * 0.35;
            
            // Horizontal line (φ-axis)
            ctx.strokeStyle = `rgba(255, 200, 50, ${alpha * 0.9})`;
            ctx.lineWidth = 4;
            ctx.shadowColor = '#ffcc00';
            ctx.shadowBlur = 15;
            ctx.beginPath();
            ctx.moveTo(centerX - width * 0.4, centerY);
            ctx.lineTo(centerX + width * 0.4, centerY);
            ctx.stroke();
            
            // Arrow left
            ctx.fillStyle = `rgba(50, 255, 100, ${alpha})`;
            ctx.beginPath();
            ctx.moveTo(centerX - width * 0.4, centerY);
            ctx.lineTo(centerX - width * 0.4 + 12, centerY - 6);
            ctx.lineTo(centerX - width * 0.4 + 12, centerY + 6);
            ctx.closePath();
            ctx.fill();
            
            // Arrow right
            ctx.fillStyle = `rgba(255, 50, 50, ${alpha})`;
            ctx.beginPath();
            ctx.moveTo(centerX + width * 0.4, centerY);
            ctx.lineTo(centerX + width * 0.4 - 12, centerY - 6);
            ctx.lineTo(centerX + width * 0.4 - 12, centerY + 6);
            ctx.closePath();
            ctx.fill();
            ctx.shadowBlur = 0;
            
            // Labels
            ctx.fillStyle = `rgba(255, 255, 255, ${alpha * 0.8})`;
            ctx.font = '14px Courier New';
            ctx.fillText('-∞', centerX - width * 0.4 - 20, centerY - 10);
            ctx.fillText('+∞', centerX + width * 0.4 + 5, centerY - 10);
            ctx.fillStyle = `rgba(255, 255, 100, ${alpha})`;
            ctx.font = 'bold 14px Courier New';
            ctx.fillText('1', centerX - 4, centerY - 10);
            ctx.font = '12px Courier New';
            ctx.fillStyle = `rgba(100, 150, 255, ${alpha * 0.8})`;
            ctx.fillText('φ-axis', centerX + 15, centerY + 20);
            
            // Vertical circle (ν-axis emerging)
            const circleRadius = maxRadius * (0.5 + progress * 0.5);
            
            ctx.strokeStyle = `rgba(0, 255, 170, ${alpha * 0.6})`;
            ctx.lineWidth = 2;
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.arc(centerX, centerY, circleRadius, 0, Math.PI * 2);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // Vertical line through center
            ctx.strokeStyle = `rgba(0, 255, 170, ${alpha * 0.5})`;
            ctx.lineWidth = 2;
            ctx.setLineDash([3, 3]);
            ctx.beginPath();
            ctx.moveTo(centerX, centerY - height * 0.4);
            ctx.lineTo(centerX, centerY + height * 0.4);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // Central 1
            drawGlow(centerX, centerY, 25, 'rgba(255, 255, 100, 1)', alpha);
            ctx.fillStyle = `rgba(0, 0, 0, ${alpha})`;
            ctx.font = 'bold 14px Courier New';
            ctx.fillText('1', centerX - 2, centerY + 4);
            
            // Pole labels
            if (progress > 0.5) {
                ctx.fillStyle = `rgba(255, 100, 100, ${alpha * 0.8})`;
                ctx.font = '12px Courier New';
                ctx.fillText('∞', centerX - 4, centerY - maxRadius * 1.2);
                ctx.fillStyle = `rgba(100, 255, 100, ${alpha * 0.8})`;
                ctx.fillText('0', centerX - 3, centerY + maxRadius * 1.2 + 15);
                
                ctx.fillStyle = `rgba(0, 255, 170, ${alpha * 0.6})`;
                ctx.font = '10px Courier New';
                ctx.fillText('ν-axis', centerX + circleRadius * 0.7, centerY + 10);
            }
        }
        
        function drawParticles(progress){
            const particleCount = 50;
            const time = Date.now() / 1000;
            
            for (let i = 0; i < particleCount; i++) {
                const angle = (i / particleCount) * Math.PI * 2 + time * 0.5;
                const radius = Math.min(width, height) * 0.4 * (0.3 + Math.sin(time + i) * 0.2);
                const x = centerX + Math.cos(angle) * radius;
                const y = centerY + Math.sin(angle) * radius * 0.3;
                
                const alpha = 0.3 + Math.sin(time * 2 + i) * 0.2;
                const size = 1 + Math.sin(time + i * 0.5) * 0.5;
                
                ctx.fillStyle = `rgba(100, 150, 255, ${alpha * progress})`;
                ctx.beginPath();
                ctx.arc(x, y, size, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        
        function getAnimationProgress() {
            let time = elapsedTime;
            let accumulated = 0;
            
            const phases = {
                initialLine: getPhaseProgress(time, PHASES.INITIAL_LINE, accumulated),
                negativeExtend: getPhaseProgress(time, PHASES.NEGATIVE_EXTEND, accumulated += PHASES.INITIAL_LINE),
                circleEmerge: getPhaseProgress(time, PHASES.CIRCLE_EMERGE, accumulated += PHASES.NEGATIVE_EXTEND),
                fullSecondD: getPhaseProgress(time, PHASES.FULL_SECOND_D, accumulated += PHASES.CIRCLE_EMERGE),
                reveal: getPhaseProgress(time, PHASES.REVEAL, accumulated += PHASES.FULL_SECOND_D)
            };
            
            return phases;
        }
        
        function getPhaseProgress(currentTime, duration, start) {
            if (currentTime < start) return 0;
            if (currentTime >= start + duration) return 1;
            return (currentTime - start) / duration;
        }
        
        function render() {
            // Clear with fade effect
            ctx.fillStyle = 'rgba(0, 0, 0, 0.12)';
            ctx.fillRect(0, 0, width, height);
            
            const phases = getAnimationProgress();
            const totalProgress = elapsedTime / TOTAL_DURATION / 1000;
            
            // Update phase indicator
            let phaseNum = 0;
            if (phases.initialLine < 1) phaseNum = 1;
            else if (phases.negativeExtend < 1) phaseNum = 2;
            else if (phases.circleEmerge < 1) phaseNum = 3;
            else if (phases.fullSecondD < 1) phaseNum = 4;
            else phaseNum = 5;
            document.getElementById('phase').textContent = `PHASE: ${phaseNum} / 5`;
            
            // Draw Riemann sphere base
            const sphereRadius = Math.min(width, height) * 0.35;
            drawRiemannSphere(Math.min(phases.initialLine + phases.negativeExtend * 0.5, 1.5));
            
            // Draw particles
            drawParticles(Math.min(phases.circleEmerge + phases.fullSecondD * 0.5, 1));
            
            // Phase 1: Line going one direction
            if (phases.initialLine > 0 && phases.initialLine < 1) {
                drawInfinityLineOneDirection(phases.initialLine, sphereRadius);
            }
            
            // Phase 2: Line extends to negative
            if (phases.negativeExtend > 0 && phases.negativeExtend < 1) {
                drawInfinityLineBothDirections(phases.negativeExtend, sphereRadius);
            }
            
            // Phase 3: Circle emerges
            if (phases.circleEmerge > 0) {
                drawEmergentCircle(phases.circleEmerge, sphereRadius);
            }
            
            // Phase 4: Full second dimension
            if (phases.fullSecondD > 0) {
                drawCompleteSecondDimension(phases.fullSecondD);
            }
            
            // Show equation at the end
            const equation = document.getElementById('equation');
            if (phases.reveal > 0.1) {
                equation.classList.add('visible');
            } else {
                equation.classList.remove('visible');
            }
            
            // Loop
            if (isPlaying) {
                elapsedTime += 16 * speed;
                if (elapsedTime > TOTAL_DURATION * 1000 + 2000) {
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
