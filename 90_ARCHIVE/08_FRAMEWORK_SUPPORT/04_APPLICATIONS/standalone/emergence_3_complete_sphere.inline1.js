const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        let width, height, centerX, centerY;
        let animationId;
        let isPlaying = true;
        let speed = 1.0;
        let elapsedTime = 0;
        
        // Animation phases (in seconds)
        const PHASES = {
            DOT_EMERGENCE: 1.5,
            SPHERE_FORMATION: 2.5,
            AXIS_REVELATION: 2.5,
            FULL_3D_UNDERSTANDING: 3.0,
            FINAL_STATE: 3.0
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
        
        function drawBindu(progress) {
            const maxRadius = Math.min(width, height) * 0.015;
            const radius = maxRadius * Math.min(progress * 4, 1);
            const alpha = Math.min(progress * 2, 1);
            const pulse = 1 + Math.sin(Date.now() / 150) * 0.15;
            
            drawGlow(centerX, centerY, radius * 4 * pulse, 'rgba(255, 255, 200, 1)', alpha);
            drawGlow(centerX, centerY, radius * 2, 'rgba(255, 255, 255, 1)', alpha);
            
            ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
            ctx.fill();
            
            if (progress > 0.5) {
                ctx.fillStyle = `rgba(255, 255, 200, ${(progress - 0.5) * 2})`;
                ctx.font = '14px Courier New';
                ctx.fillText('BINDU', centerX + radius + 8, centerY + 4);
            }
        }
        
        function drawSphere(progress, rotation) {
            const maxRadius = Math.min(width, height) * 0.35;
            const sphereRadius = maxRadius * Math.min(progress * 1.5, 1);
            
            // 3D rotation effect
            const rotX = rotation * 0.3;
            const perspectiveFactor = Math.cos(rotX);
            const verticalSquash = 0.7 + 0.3 * perspectiveFactor;
            
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.scale(1, verticalSquash);
            ctx.translate(-centerX, -centerY);
            
            // Outer glow
            drawGlow(centerX, centerY, sphereRadius * 1.8, 'rgba(50, 100, 200, 0.2)', progress);
            
            // Sphere gradient
            const sphereGradient = ctx.createRadialGradient(
                centerX - sphereRadius * 0.3,
                centerY - sphereRadius * 0.3,
                0,
                centerX,
                centerY,
                sphereRadius
            );
            sphereGradient.addColorStop(0, `rgba(60, 80, 120, ${0.4 * progress})`);
            sphereGradient.addColorStop(0.5, `rgba(30, 50, 80, ${0.3 * progress})`);
            sphereGradient.addColorStop(1, `rgba(10, 20, 40, ${0.5 * progress})`);
            
            ctx.fillStyle = sphereGradient;
            ctx.beginPath();
            ctx.arc(centerX, centerY, sphereRadius, 0, Math.PI * 2);
            ctx.fill();
            
            // Sphere outline
            ctx.strokeStyle = `rgba(100, 150, 255, ${0.4 + progress * 0.4})`;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(centerX, centerY, sphereRadius, 0, Math.PI * 2);
            ctx.stroke();
            
            ctx.restore();
            
            return sphereRadius;
        }
        
        function drawEquator(progress, sphereRadius, rotation) {
            const rotX = rotation * 0.3;
            const perspectiveFactor = Math.cos(rotX);
            const verticalSquash = 0.7 + 0.3 * perspectiveFactor;
            
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.scale(1, verticalSquash);
            ctx.translate(-centerX, -centerY);
            
            // Equator line (the complex plane)
            const equatorAlpha = Math.min(progress * 2, 1);
            
            ctx.strokeStyle = `rgba(255, 204, 0, ${0.6 + equatorAlpha * 0.4})`;
            ctx.lineWidth = 3;
            ctx.shadowColor = '#ffcc00';
            ctx.shadowBlur = 12;
            ctx.beginPath();
            ctx.ellipse(centerX, centerY, sphereRadius, sphereRadius * verticalSquash, 0, 0, Math.PI * 2);
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            // Horizontal line through equator
            ctx.strokeStyle = `rgba(255, 204, 0, ${equatorAlpha * 0.7})`;
            ctx.lineWidth = 2;
            ctx.setLineDash([8, 4]);
            ctx.beginPath();
            ctx.moveTo(centerX - sphereRadius * 1.5, centerY);
            ctx.lineTo(centerX + sphereRadius * 1.5, centerY);
            ctx.stroke();
            ctx.setLineDash([]);
            
            ctx.restore();
        }
        
        function drawAxis(progress, sphereRadius, rotation, axisType) {
            const rotX = rotation * 0.3;
            const perspectiveFactor = Math.cos(rotX);
            const verticalSquash = 0.7 + 0.3 * perspectiveFactor;
            
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.scale(1, verticalSquash);
            ctx.translate(-centerX, -centerY);
            
            const axisAlpha = Math.min(progress * 2, 1);
            
            if (axisType === 'phi' || axisType === 'both') {
                // φ-axis (horizontal, through poles)
                ctx.strokeStyle = `rgba(255, 102, 0, ${axisAlpha * 0.8})`;
                ctx.lineWidth = 3;
                ctx.shadowColor = '#ff6600';
                ctx.shadowBlur = 8;
                ctx.beginPath();
                ctx.moveTo(centerX - sphereRadius * 1.3, centerY);
                ctx.lineTo(centerX + sphereRadius * 1.3, centerY);
                ctx.stroke();
                
                // Pole markers
                drawGlow(centerX, centerY - sphereRadius, 8, 'rgba(255, 50, 50, 1)', axisAlpha);
                drawGlow(centerX, centerY + sphereRadius, 8, 'rgba(50, 255, 50, 1)', axisAlpha);
                
                ctx.fillStyle = `rgba(255, 255, 255, ${axisAlpha * 0.9})`;
                ctx.font = '11px Courier New';
                ctx.fillText('∞', centerX - 4, centerY - sphereRadius - 8);
                ctx.fillText('0', centerX - 3, centerY + sphereRadius + 15);
                
                ctx.fillStyle = `rgba(255, 102, 0, ${axisAlpha})`;
                ctx.font = '10px Courier New';
                ctx.fillText('φ', centerX + sphereRadius + 10, centerY + 4);
            }
            
            if (axisType === 'nu' || axisType === 'both') {
                // ν-axis (vertical, through equator center)
                ctx.strokeStyle = `rgba(0, 255, 170, ${axisAlpha * 0.8})`;
                ctx.lineWidth = 3;
                ctx.shadowColor = '#00ffaa';
                ctx.shadowBlur = 8;
                ctx.beginPath();
                ctx.moveTo(centerX, centerY - sphereRadius * 1.3);
                ctx.lineTo(centerX, centerY + sphereRadius * 1.3);
                ctx.stroke();
                
                // Labels
                ctx.fillStyle = `rgba(0, 255, 170, ${axisAlpha})`;
                ctx.font = '10px Courier New';
                ctx.fillText('ν', centerX + 10, centerY);
            }
            
            ctx.shadowBlur = 0;
            ctx.restore();
        }
        
        function drawNorthSouthPoles(progress, sphereRadius) {
            const poleAlpha = Math.min(progress * 2, 1);
            
            // North pole (∞)
            drawGlow(centerX, centerY - sphereRadius, 12, 'rgba(255, 50, 50, 1)', poleAlpha);
            ctx.fillStyle = `rgba(255, 50, 50, ${poleAlpha})`;
            ctx.font = 'bold 14px Courier New';
            ctx.fillText('∞', centerX - 5, centerY - sphereRadius + 5);
            
            // South pole (0)
            drawGlow(centerX, centerY + sphereRadius, 12, 'rgba(50, 255, 50, 1)', poleAlpha);
            ctx.fillStyle = `rgba(50, 255, 50, ${poleAlpha})`;
            ctx.fillText('0', centerX - 3, centerY + sphereRadius + 5);
        }
        
        function drawCentralOne(progress) {
            const oneAlpha = Math.min(progress * 2, 1);
            drawGlow(centerX, centerY, 25, 'rgba(255, 255, 100, 1)', oneAlpha);
            ctx.fillStyle = `rgba(0, 0, 0, ${oneAlpha})`;
            ctx.font = 'bold 16px Courier New';
            ctx.fillText('1', centerX - 4, centerY + 5);
        }
        
        function drawMultiplicationSymbol(progress) {
            const symAlpha = Math.min(progress * 2, 1);
            const time = Date.now() / 1000;
            const pulse = 1 + Math.sin(time * 2) * 0.1;
            const size = 30 * pulse;
            
            // Big circle (representing the sphere/object)
            ctx.strokeStyle = `rgba(100, 150, 255, ${symAlpha * 0.8})`;
            ctx.lineWidth = 3;
            ctx.shadowColor = '#6699ff';
            ctx.shadowBlur = 15;
            ctx.beginPath();
            ctx.arc(centerX - 80, centerY, size, 0, Math.PI * 2);
            ctx.stroke();
            
            // Small dot (representing the bindu/quantum)
            drawGlow(centerX + 60, centerY, size * 0.4, 'rgba(255, 255, 200, 1)', symAlpha);
            
            // Multiplication sign
            ctx.strokeStyle = `rgba(255, 204, 0, ${symAlpha})`;
            ctx.lineWidth = 4;
            ctx.shadowColor = '#ffcc00';
            ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.moveTo(centerX - 15, centerY);
            ctx.lineTo(centerX + 15, centerY);
            ctx.moveTo(centerX, centerY - 15);
            ctx.lineTo(centerX, centerY + 15);
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            // Equals sign
            ctx.strokeStyle = `rgba(255, 255, 255, ${symAlpha * 0.7})`;
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(centerX + 35, centerY - 8);
            ctx.lineTo(centerX + 55, centerY - 8);
            ctx.moveTo(centerX + 35, centerY + 8);
            ctx.lineTo(centerX + 55, centerY + 8);
            ctx.stroke();
            
            // Result symbol
            ctx.strokeStyle = `rgba(255, 204, 0, ${symAlpha})`;
            ctx.lineWidth = 3;
            ctx.shadowColor = '#ffcc00';
            ctx.shadowBlur = 15;
            ctx.beginPath();
            ctx.arc(centerX + 90, centerY, size * 0.8, 0, Math.PI * 2);
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            // Labels
            ctx.fillStyle = `rgba(255, 255, 255, ${symAlpha * 0.6})`;
            ctx.font = '10px Courier New';
            ctx.fillText('○', centerX - 85, centerY + size + 15);
            ctx.fillText('•', centerX + 55, centerY + 15);
            ctx.fillText('⊙', centerX + 85, centerY + size * 0.8 + 15);
        }
        
        function drawParticles(progress, rotation) {
            const particleCount = 80;
            const time = Date.now() / 1000;
            const rotX = rotation * 0.3;
            const perspectiveFactor = Math.cos(rotX);
            
            for (let i = 0; i < particleCount; i++) {
                const layer = Math.floor(i / 20);
                const angle = (i % 20) / 20 * Math.PI * 2 + time * (0.3 + layer * 0.1);
                const baseRadius = Math.min(width, height) * (0.2 + layer * 0.15);
                const radiusVariation = Math.sin(time + i * 0.3) * 20;
                const radius = (baseRadius + radiusVariation) * perspectiveFactor;
                
                const x = centerX + Math.cos(angle) * radius;
                const y = centerY + Math.sin(angle) * radius * (0.7 + 0.3 * perspectiveFactor);
                
                const alpha = (0.2 + Math.sin(time * 2 + i) * 0.15) * progress;
                const size = 1 + Math.sin(time + i * 0.5) * 0.5 + layer * 0.3;
                
                const colors = [
                    `rgba(100, 150, 255, ${alpha})`,
                    `rgba(255, 200, 100, ${alpha})`,
                    `rgba(0, 255, 170, ${alpha})`
                ];
                
                ctx.fillStyle = colors[i % 3];
                ctx.beginPath();
                ctx.arc(x, y, size, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        
        function getAnimationProgress() {
            let time = elapsedTime;
            let accumulated = 0;
            
            const phases = {
                dotEmerge: getPhaseProgress(time, PHASES.DOT_EMERGENCE, accumulated),
                sphereForm: getPhaseProgress(time, PHASES.SPHERE_FORMATION, accumulated += PHASES.DOT_EMERGENCE),
                axisReveal: getPhaseProgress(time, PHASES.AXIS_REVELATION, accumulated += PHASES.SPHERE_FORMATION),
                full3D: getPhaseProgress(time, PHASES.FULL_3D_UNDERSTANDING, accumulated += PHASES.AXIS_REVELATION),
                final: getPhaseProgress(time, PHASES.FINAL_STATE, accumulated += PHASES.FULL_3D_UNDERSTANDING)
            };
            
            return phases;
        }
        
        function getPhaseProgress(currentTime, duration, start) {
            if (currentTime < start) return 0;
            if (currentTime >= start + duration) return 1;
            return (currentTime - start) / duration;
        }
        
        function render() {
            // Clear with fade
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, width, height);
            
            const phases = getAnimationProgress();
            const rotation = elapsedTime / 3000;
            const totalProgress = elapsedTime / TOTAL_DURATION / 1000;
            
            // Update phase indicator
            let phaseNum = 0;
            if (phases.dotEmerge < 1) phaseNum = 1;
            else if (phases.sphereForm < 1) phaseNum = 2;
            else if (phases.axisReveal < 1) phaseNum = 3;
            else if (phases.full3D < 1) phaseNum = 4;
            else phaseNum = 5;
            document.getElementById('phase').textContent = `PHASE: ${phaseNum} / 5`;
            
            // Update depth indicator
            const depthIndicator = document.getElementById('depth');
            if (phases.full3D > 0.3) {
                depthIndicator.textContent = 'PERSPECTIVE: 3D';
                depthIndicator.style.color = 'rgba(0, 255, 170, 0.6)';
            }
            
            // Draw elements in order
            drawParticles(Math.min(phases.sphereForm + phases.axisReveal * 0.5, 1), rotation);
            drawBindu(phases.dotEmerge);
            
            const sphereRadius = drawSphere(phases.sphereForm, rotation);
            
            drawEquator(Math.min(phases.sphereForm + phases.axisReveal * 0.5, 1), sphereRadius, rotation);
            
            if (phases.axisReveal > 0) {
                drawAxis(phases.axisReveal, sphereRadius, rotation, 'phi');
            }
            if (phases.axisReveal > 0.3) {
                drawAxis(Math.min((phases.axisReveal - 0.3) / 0.7, 1), sphereRadius, rotation, 'nu');
            }
            
            drawNorthSouthPoles(Math.min(phases.axisReveal + phases.full3D * 0.3, 1), sphereRadius);
            drawCentralOne(Math.min(phases.full3D, 1));
            
            if (phases.final > 0) {
                drawMultiplicationSymbol(phases.final);
            }
            
            // Show equation
            const equation = document.getElementById('equation');
            if (phases.final > 0.2) {
                equation.classList.add('visible');
            } else {
                equation.classList.remove('visible');
            }
            
            // Show legend
            const legend = document.getElementById('legend');
            if (phases.axisReveal > 0.5) {
                legend.classList.add('visible');
            } else {
                legend.classList.remove('visible');
            }
            
            // Loop
            if (isPlaying) {
                elapsedTime += 16 * speed;
                if (elapsedTime > TOTAL_DURATION * 1000 + 3000) {
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
