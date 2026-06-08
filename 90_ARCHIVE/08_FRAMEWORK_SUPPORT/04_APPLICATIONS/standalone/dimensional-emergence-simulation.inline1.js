// Three.js Scene Setup
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x000000, 0.03);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.01, 1000);
        camera.position.set(0, 0, 10);
        
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.getElementById('canvas-container').appendChild(renderer.domElement);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 1);
        scene.add(ambientLight);
        
        const light1 = new THREE.PointLight(0x00e5ff, 2, 100);
        light1.position.set(10, 10, 10);
        scene.add(light1);
        
        const light2 = new THREE.PointLight(0xff0000, 2, 100);
        light2.position.set(-10, -10, 10);
        scene.add(light2);
        
        // ==================== DIMENSION 0: THE BINDU ====================
        const dim0Group = new THREE.Group();
        scene.add(dim0Group);
        
        // The singularity (black hole — nothingness)
        const singularityGeo = new THREE.SphereGeometry(0.1, 32, 32);
        const singularityMat = new THREE.MeshBasicMaterial({
            color: 0x000000,
            transparent: true
        });
        const singularity = new THREE.Mesh(singularityGeo, singularityMat);
        dim0Group.add(singularity);
        
        // The event horizon glow (emerging from nothing)
        const horizonGeo = new THREE.SphereGeometry(0.3, 32, 32);
        const horizonMat = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            transparent: true,
            opacity: 0.8
        });
        const horizon = new THREE.Mesh(horizonGeo, horizonMat);
        dim0Group.add(horizon);
        
        // Outer glow
        const glowGeo = new THREE.SphereGeometry(0.6, 32, 32);
        const glowMat = new THREE.MeshBasicMaterial({
            color: 0x00e5ff,
            transparent: true,
            opacity: 0.2
        });
        const glowMesh = new THREE.Mesh(glowGeo, glowMat);
        dim0Group.add(glowMesh);
        
        // ==================== DIMENSION 1: THE LINE ====================
        const dim1Group = new THREE.Group();
        dim1Group.visible = false;
        scene.add(dim1Group);
        
        // The line from 0 to infinity (logarithmic scale)
        const linePoints = [];
        for (let i = 0; i <= 200; i++) {
            const t = i / 200;
            // Logarithmic spacing: starts at 0, goes to "infinity"
            const x = Math.pow(t, 0.3) * 10;
            linePoints.push(new THREE.Vector3(x, 0, 0));
        }
        
        const lineGeo = new THREE.BufferGeometry().setFromPoints(linePoints);
        const lineMat = new THREE.LineBasicMaterial({
            color: 0x00e5ff,
            linewidth: 3,
            transparent: true,
            opacity: 0
        });
        const line = new THREE.Line(lineGeo, lineMat);
        dim1Group.add(line);
        
        // Point at ZERO (the origin)
        const zeroGeo = new THREE.SphereGeometry(0.2, 32, 32);
        const zeroMat = new THREE.MeshBasicMaterial({
            color: 0xff0000,
            emissive: 0xff0000,
            emissiveIntensity: 1
        });
        const zeroPoint = new THREE.Mesh(zeroGeo, zeroMat);
        zeroPoint.position.set(0, 0, 0);
        dim1Group.add(zeroPoint);
        
        // Point at ONE (unity)
        const oneGeo = new THREE.SphereGeometry(0.25, 32, 32);
        const oneMat = new THREE.MeshBasicMaterial({
            color: 0x76ff03,
            emissive: 0x76ff03,
            emissiveIntensity: 0.8
        });
        const onePoint = new THREE.Mesh(oneGeo, oneMat);
        onePoint.position.set(1, 0, 0);
        dim1Group.add(onePoint);
        
        // Point at INFINITY
        const infGeo = new THREE.SphereGeometry(0.2, 32, 32);
        const infMat = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            emissive: 0xffffff,
            emissiveIntensity: 2
        });
        const infPoint = new THREE.Mesh(infGeo, infMat);
        infPoint.position.set(10, 0, 0);
        dim1Group.add(infPoint);
        
        // Ray from 0 through 1 to ∞ (the projection ray)
        const rayGeo = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(15, 0, 0)
        ]);
        const rayMat = new THREE.LineBasicMaterial({
            color: 0xffffff,
            transparent: true,
            opacity: 0,
            linewidth: 2
        });
        const ray = new THREE.Line(rayGeo, rayMat);
        dim1Group.add(ray);
        
        // ==================== DIMENSION 2: THE CIRCLE ====================
        const dim2Group = new THREE.Group();
        dim2Group.visible = false;
        scene.add(dim2Group);
        
        // The circle at infinity (slope 0)
        const circleGeo = new THREE.RingGeometry(4, 4.05, 128);
        const circleMat = new THREE.MeshBasicMaterial({
            color: 0x76ff03,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0
        });
        const circle = new THREE.Mesh(circleGeo, circleMat);
        dim2Group.add(circle);
        
        // Inner circle (unit circle)
        const unitCircleGeo = new THREE.RingGeometry(1, 1.02, 128);
        const unitCircleMat = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0
        });
        const unitCircle = new THREE.Mesh(unitCircleGeo, unitCircleMat);
        dim2Group.add(unitCircle);
        
        // The complex plane grid
        const gridHelper = new THREE.GridHelper(20, 40, 0x00e5ff, 0x002244);
        gridHelper.rotation.x = Math.PI / 2;
        gridHelper.material.opacity = 0;
        gridHelper.material.transparent = true;
        dim2Group.add(gridHelper);
        
        // Points on the circle
        const circlePoints = [];
        for (let i = 0; i < 12; i++) {
            const angle = (i / 12) * Math.PI * 2;
            const point = new THREE.Mesh(
                new THREE.SphereGeometry(0.1, 16, 16),
                new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0 })
            );
            point.position.set(Math.cos(angle) * 4, Math.sin(angle) * 4, 0);
            dim2Group.add(point);
            circlePoints.push(point);
        }
        
        // ==================== DIMENSION 3: THE SPHERE ====================
        const dim3Group = new THREE.Group();
        dim3Group.visible = false;
        scene.add(dim3Group);
        
        // The Riemann sphere
        const sphereGeo = new THREE.SphereGeometry(3, 64, 64);
        const sphereMat = new THREE.MeshPhongMaterial({
            color: 0x00e5ff,
            emissive: 0x001133,
            specular: 0xffffff,
            shininess: 100,
            transparent: true,
            opacity: 0
        });
        const sphere = new THREE.Mesh(sphereGeo, sphereMat);
        dim3Group.add(sphere);
        
        // Wireframe
        const wireGeo = new THREE.SphereGeometry(3.01, 32, 32);
        const wireMat = new THREE.MeshBasicMaterial({
            color: 0x76ff03,
            wireframe: true,
            transparent: true,
            opacity: 0
        });
        const wireSphere = new THREE.Mesh(wireGeo, wireMat);
        dim3Group.add(wireSphere);
        
        // North pole (0)
        const northPole = new THREE.Mesh(
            new THREE.SphereGeometry(0.25, 32, 32),
            new THREE.MeshBasicMaterial({ color: 0xff0000, emissive: 0xff0000, emissiveIntensity: 1 })
        );
        northPole.position.set(0, 3, 0);
        dim3Group.add(northPole);
        
        // South pole (∞)
        const southPole = new THREE.Mesh(
            new THREE.SphereGeometry(0.25, 32, 32),
            new THREE.MeshBasicMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 2 })
        );
        southPole.position.set(0, -3, 0);
        dim3Group.add(southPole);
        
        // Equator (the unity circle)
        const equatorGeo = new THREE.TorusGeometry(3, 0.05, 16, 100);
        const equatorMat = new THREE.MeshBasicMaterial({
            color: 0x76ff03,
            transparent: true,
            opacity: 0
        });
        const equator = new THREE.Mesh(equatorGeo, equatorMat);
        dim3Group.add(equator);
        
        // Projection lines (stereographic)
        const projLines = [];
        for (let i = 0; i < 16; i++) {
            const angle = (i / 16) * Math.PI * 2;
            const lineG = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(0, 3, 0),
                new THREE.Vector3(Math.cos(angle) * 3, 0, Math.sin(angle) * 3)
            ]);
            const lineM = new THREE.LineBasicMaterial({
                color: 0xffffff,
                transparent: true,
                opacity: 0
            });
            const projLine = new THREE.Line(lineG, lineM);
            dim3Group.add(projLine);
            projLines.push(projLine);
        }
        
        // ==================== STATE & ANIMATION ====================
        let sliderValue = 0;
        let currentPhase = 0;
        
        const phases = [
            { 
                eq: "⊙ = •", 
                sub: "Dimension 0: The Bindu — The Non-Manifest Point",
                math: "The singularity. The ground. Nothing (∅).",
                dim: "0D"
            },
            { 
                eq: "0 × ∞ = 1", 
                sub: "Dimension 1: The Line — The Transcendental Trinity",
                math: "1/0 = ∞ | 0×∞ = 1 | The resolution of division by zero",
                dim: "1D"
            },
            { 
                eq: "z = x + iy", 
                sub: "Dimension 2: The Circle — The Complex Plane",
                math: "The line at 90° becomes the circle with infinite diameter",
                dim: "2D"
            },
            { 
                eq: "φ · ν = 1", 
                sub: "Dimension 3: The Sphere — S² Compactification",
                math: "The Riemann sphere: ℂ ∪ {∞} = S²",
                dim: "3D"
            }
        ];
        
        function updateScene() {
            const t = sliderValue / 100;
            
            // Determine phase and local progress
            let phase, localT;
            if (t < 0.25) {
                phase = 0;
                localT = t / 0.25;
            } else if (t < 0.5) {
                phase = 1;
                localT = (t - 0.25) / 0.25;
            } else if (t < 0.75) {
                phase = 2;
                localT = (t - 0.5) / 0.25;
            } else {
                phase = 3;
                localT = (t - 0.75) / 0.25;
            }
            
            // Update visibility
            dim0Group.visible = (phase === 0) || (phase === 1 && localT < 0.3);
            dim1Group.visible = (phase === 1) || (phase === 2 && localT < 0.3);
            dim2Group.visible = (phase === 2) || (phase === 3 && localT < 0.3);
            dim3Group.visible = (phase === 3);
            
            // PHASE 0: The Dot
            if (phase === 0) {
                const pulse = 1 + Math.sin(localT * Math.PI) * 0.3;
                horizon.scale.setScalar(pulse);
                glowMesh.scale.setScalar(pulse * 1.5);
                glowMesh.material.opacity = 0.2 + localT * 0.3;
                
                camera.position.set(0, 0, 10 - localT * 4);
                camera.lookAt(0, 0, 0);
            }
            
            // PHASE 1: The Line
            if (phase === 1) {
                // Fade in line
                line.material.opacity = localT;
                ray.material.opacity = localT * 0.5;
                
                // Animate points
                zeroPoint.scale.setScalar(1 + Math.sin(localT * Math.PI * 2) * 0.3);
                zeroPoint.material.emissiveIntensity = 1 + localT;
                
                onePoint.scale.setScalar(1 + Math.sin(localT * Math.PI * 2 + 1) * 0.2);
                onePoint.material.emissiveIntensity = 0.8 + localT * 0.4;
                
                infPoint.scale.setScalar(1 + localT * 0.5);
                infPoint.material.emissiveIntensity = 2 - localT * 0.5;
                
                // Camera follows the line
                camera.position.x = localT * 3;
                camera.position.y = 2 + localT;
                camera.position.z = 8 - localT * 2;
                camera.lookAt(localT * 5, 0, 0);
                
                // Show trinity box
                if (localT > 0.5) {
                    document.getElementById('trinity-box').style.display = 'block';
                    document.getElementById('trinity-box').style.opacity = (localT - 0.5) * 2;
                }
            } else if (phase > 1) {
                document.getElementById('trinity-box').style.display = 'none';
            }
            
            // PHASE 2: The Circle
            if (phase === 2) {
                // Rotate line up to become circle
                dim1Group.rotation.z = localT * Math.PI / 2;
                
                // Fade out line elements
                line.material.opacity = 1 - localT;
                zeroPoint.material.opacity = 1 - localT;
                onePoint.material.opacity = 1 - localT;
                infPoint.material.opacity = 1 - localT;
                
                // Fade in circle
                circle.material.opacity = localT;
                unitCircle.material.opacity = localT * 0.5;
                gridHelper.material.opacity = localT * 0.3;
                
                circlePoints.forEach(p => {
                    p.material.opacity = localT;
                });
                
                // Camera rises above
                camera.position.x = 0;
                camera.position.y = 2 + localT * 8;
                camera.position.z = 6;
                camera.lookAt(0, 0, 0);
            }
            
            // PHASE 3: The Sphere
            if (phase === 3) {
                // Fade out plane
                circle.material.opacity = 1 - localT * 0.5;
                gridHelper.material.opacity = 0.3 * (1 - localT);
                
                // Fade in sphere
                sphere.material.opacity = localT;
                wireSphere.material.opacity = localT * 0.4;
                equator.material.opacity = localT;
                
                projLines.forEach(l => {
                    l.material.opacity = localT * 0.4;
                });
                
                // Rotate sphere
                sphere.rotation.y = localT * 0.5;
                wireSphere.rotation.y = localT * 0.5;
                equator.rotation.z = localT * 0.2;
                
                // Camera orbits
                const angle = localT * Math.PI;
                camera.position.x = Math.sin(angle) * 10;
                camera.position.z = Math.cos(angle) * 10;
                camera.position.y = 3 + Math.sin(localT * Math.PI) * 3;
                camera.lookAt(0, 0, 0);
            }
            
            // Continuous animations
            glowMesh.scale.setScalar(1 + Math.sin(Date.now() * 0.003) * 0.1);
            
            // Update UI
            if (phase !== currentPhase) {
                currentPhase = phase;
                const p = phases[phase];
                document.getElementById('main-eq').textContent = p.eq;
                document.getElementById('subtitle').textContent = p.sub;
                document.getElementById('math-note').textContent = p.math;
                document.getElementById('dim-label').textContent = p.dim;
                
                document.querySelectorAll('.phase-btn').forEach((btn, i) => {
                    btn.classList.toggle('active', i === phase);
                });
            }
        }
        
        function animate() {
            requestAnimationFrame(animate);
            updateScene();
            renderer.render(scene, camera);
        }
        
        // Event handlers
        document.getElementById('slider').addEventListener('input', (e) => {
            sliderValue = parseFloat(e.target.value);
        });
        
        document.querySelectorAll('.phase-btn').forEach((btn, i) => {
            btn.addEventListener('click', () => {
                const target = i * 25 + 12.5;
                gsap.to({ val: sliderValue }, {
                    val: target,
                    duration: 1.5,
                    ease: "power2.inOut",
                    onUpdate: function() {
                        sliderValue = this.targets()[0].val;
                        document.getElementById('slider').value = sliderValue;
                    }
                });
            });
        });
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        animate();
