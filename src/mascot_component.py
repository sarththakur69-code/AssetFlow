def get_mascot_html():
    """
    Returns HTML/CSS/JS for an interactive mini-game mascot.
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: transparent;
            height: 400px;
            position: relative;
            cursor: crosshair;
        }
        
        /* Character */
        .mascot {
            position: absolute;
            width: 70px;
            height: 85px;
            transition: transform 0.2s ease-out;
            filter: drop-shadow(0 0 12px rgba(0, 243, 255, 0.5));
            cursor: pointer;
        }
        
        .character {
            position: relative;
            width: 100%;
            height: 100%;
        }
        
        /* Head */
        .head {
            width: 45px;
            height: 55px;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            border-radius: 22px 22px 18px 18px;
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            border: 2px solid #00f3ff;
            box-shadow: 0 0 8px rgba(0, 243, 255, 0.3);
        }
        
        .eyes {
            position: absolute;
            width: 28px;
            height: 10px;
            top: 18px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            justify-content: space-between;
        }
        
        .eye {
            width: 8px;
            height: 8px;
            background: #00f3ff;
            border-radius: 50%;
            box-shadow: 0 0 5px rgba(0, 243, 255, 0.8);
        }
        
        .mouth {
            position: absolute;
            width: 18px;
            height: 9px;
            border: 2px solid #00f3ff;
            border-top: none;
            border-radius: 0 0 9px 9px;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
            transition: width 0.2s;
        }
        
        .mascot.happy .mouth {
            width: 24px;
        }
        
        .body {
            position: absolute;
            width: 32px;
            height: 28px;
            background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
            border-radius: 10px;
            top: 52px;
            left: 50%;
            transform: translateX(-50%);
            border: 2px solid #00f3ff;
        }
        
        /* Data Orbs */
        .orb {
            position: absolute;
            width: 20px;
            height: 20px;
            background: radial-gradient(circle, #00f3ff 0%, rgba(0, 243, 255, 0.3) 100%);
            border-radius: 50%;
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.6);
            animation: orbFloat 2s ease-in-out infinite;
            cursor: pointer;
        }
        
        @keyframes orbFloat {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-8px) scale(1.1); }
        }
        
        /* Score counter */
        .score {
            position: absolute;
            top: 10px;
            left: 10px;
            font-family: monospace;
            font-size: 16px;
            color: #00f3ff;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.8);
            z-index: 100;
        }
        
        /* Particle effect */
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00f3ff;
            border-radius: 50%;
            pointer-events: none;
            animation: particleFade 0.8s ease-out forwards;
        }
        
        @keyframes particleFade {
            0% { opacity: 1; transform: translateY(0) scale(1); }
            100% { opacity: 0; transform: translateY(-30px) scale(0.3); }
        }
        
        /* Chase mode */
        .mascot.chasing {
            animation: wiggle 0.3s ease-in-out infinite;
        }
        
        @keyframes wiggle {
            0%, 100% { transform: rotate(-3deg); }
            50% { transform: rotate(3deg); }
        }
        
        /* Collecting */
        @keyframes collect {
            0% { transform: scale(1); }
            50% { transform: scale(1.3); }
            100% { transform: scale(0); opacity: 0; }
        }
        
        .orb.collecting {
            animation: collect 0.4s ease-out forwards;
        }
        
        /* Petting hearts */
        .heart {
            position: absolute;
            font-size: 20px;
            pointer-events: none;
            animation: heartFloat 1s ease-out forwards;
        }
        
        @keyframes heartFloat {
            0% { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-50px); }
        }
    </style>
    </head>
    <body>
        <div class="score" id="score">Orbs: 0</div>
        <div class="mascot" id="mascot">
            <div class="character">
                <div class="head">
                    <div class="eyes">
                        <div class="eye"></div>
                        <div class="eye"></div>
                    </div>
                    <div class="mouth"></div>
                </div>
                <div class="body"></div>
            </div>
        </div>
        
        <script>
            const mascot = document.getElementById('mascot');
            const scoreEl = document.getElementById('score');
            let mascotX = 150;
            let mascotY = 150;
            let targetX = mascotX;
            let targetY = mascotY;
            let score = 0;
            let orbs = [];
            
            // Initialize position
            mascot.style.left = mascotX + 'px';
            mascot.style.top = mascotY + 'px';
            
            // Spawn orbs periodically
            function spawnOrb() {
                const orb = document.createElement('div');
                orb.className = 'orb';
                orb.style.left = Math.random() * (window.innerWidth - 40) + 'px';
                orb.style.top = Math.random() * (window.innerHeight - 40) + 'px';
                document.body.appendChild(orb);
                orbs.push(orb);
                
                orb.addEventListener('click', () => collectOrb(orb));
            }
            
            // Collect orb
            function collectOrb(orb) {
                orb.classList.add('collecting');
                score++;
                scoreEl.textContent = 'Orbs: ' + score;
                
                // Particles
                for (let i = 0; i < 8; i++) {
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    particle.style.left = orb.offsetLeft + 10 + 'px';
                    particle.style.top = orb.offsetTop + 10 + 'px';
                    particle.style.transform = `rotate(${i * 45}deg) translateX(20px)`;
                    document.body.appendChild(particle);
                    setTimeout(() => particle.remove(), 800);
                }
                
                setTimeout(() => {
                    orb.remove();
                    orbs = orbs.filter(o => o !== orb);
                }, 400);
            }
            
            // Pet mascot
            mascot.addEventListener('click', (e) => {
                e.stopPropagation();
                mascot.classList.add('happy');
                
                // Spawn hearts
                for (let i = 0; i < 3; i++) {
                    setTimeout(() => {
                        const heart = document.createElement('div');
                        heart.className = 'heart';
                        heart.textContent = '💙';
                        heart.style.left = mascotX + 20 + (Math.random() - 0.5) * 30 + 'px';
                        heart.style.top = mascotY + 'px';
                        document.body.appendChild(heart);
                        setTimeout(() => heart.remove(), 1000);
                    }, i * 100);
                }
                
                setTimeout(() => mascot.classList.remove('happy'), 500);
            });
            
            // Chase cursor
            let isChasing = false;
            document.addEventListener('mousemove', (e) => {
                targetX = e.clientX - 35;
                targetY = e.clientY - 42;
                
                // Check distance to trigger chase
                const dx = targetX - mascotX;
                const dy = targetY - mascotY;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist > 100) {
                    isChasing = true;
                    mascot.classList.add('chasing');
                } else {
                    isChasing = false;
                    mascot.classList.remove('chasing');
                }
            });
            
            // Animation loop
            function animate() {
                if (isChasing) {
                    const dx = targetX - mascotX;
                    const dy = targetY - mascotY;
                    
                    mascotX += dx * 0.03;
                    mascotY += dy * 0.03;
                    
                    mascot.style.left = mascotX + 'px';
                    mascot.style.top = mascotY + 'px';
                    
                    // Check orb collisions
                    orbs.forEach(orb => {
                        const orbX = parseFloat(orb.style.left);
                        const orbY = parseFloat(orb.style.top);
                        const dist = Math.sqrt((mascotX - orbX) ** 2 + (mascotY - orbY) ** 2);
                        
                        if (dist < 40 && !orb.classList.contains('collecting')) {
                            collectOrb(orb);
                        }
                    });
                }
                
                requestAnimationFrame(animate);
            }
            
            // Start game
            setInterval(spawnOrb, 2000);
            spawnOrb();
            animate();
        </script>
    </body>
    </html>
    """
    return html
