/* ==========================================
   NAIRU — Interactive Scripts
   Particles, Animations, Lightbox, Counters
   ========================================== */

document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initNavbar();
    initScrollReveal();
    initCounters();
    initGalleryLightbox();
    initMobileNav();
    initVipPassword();
});

/* ---- Particle System ---- */
function initParticles() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let particles = [];
    const PARTICLE_COUNT = 60;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    class Particle {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.speedY = (Math.random() - 0.5) * 0.5;
            this.opacity = Math.random() * 0.5 + 0.1;
            this.color = Math.random() > 0.5
                ? `rgba(168, 85, 247, ${this.opacity})`
                : `rgba(236, 72, 153, ${this.opacity})`;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
            if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
    }

    function initParticleArray() {
        particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            particles.push(new Particle());
        }
    }

    function connectParticles() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 120) {
                    const opacity = (1 - distance / 120) * 0.15;
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(168, 85, 247, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        connectParticles();
        requestAnimationFrame(animate);
    }

    resize();
    initParticleArray();
    animate();

    window.addEventListener('resize', () => {
        resize();
        initParticleArray();
    });
}

/* ---- Navbar Scroll Effect ---- */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Close mobile nav
                const navLinks = document.getElementById('nav-links');
                if (navLinks) navLinks.classList.remove('active');
            }
        });
    });
}

/* ---- Mobile Nav Toggle ---- */
function initMobileNav() {
    const toggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');
    if (!toggle || !navLinks) return;

    toggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        toggle.classList.toggle('active');
    });
}

/* ---- Scroll Reveal Animations ---- */
function initScrollReveal() {
    const revealElements = document.querySelectorAll(
        '.section-header, .about-image, .about-content, .gallery-item, ' +
        '.pricing-card, .link-card, .feature'
    );

    revealElements.forEach(el => el.classList.add('reveal'));

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, index * 80);
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );

    revealElements.forEach(el => observer.observe(el));
}

/* ---- Animated Counters ---- */
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    if (!counters.length) return;

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.5 }
    );

    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-count'));
    const duration = 2000;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Ease out quad
        const eased = 1 - (1 - progress) * (1 - progress);
        const current = Math.round(eased * target);

        element.textContent = current.toLocaleString('pt-BR');

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

/* ---- Gallery Lightbox ---- */
function initGalleryLightbox() {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const closeBtn = document.getElementById('lightbox-close');
    const prevBtn = document.getElementById('lightbox-prev');
    const nextBtn = document.getElementById('lightbox-next');

    if (!lightbox) return;

    const galleryItems = document.querySelectorAll('.gallery-item:not(.gallery-item-cta)');
    let currentIndex = 0;
    const images = [];

    galleryItems.forEach((item, idx) => {
        const img = item.querySelector('img');
        if (img) {
            images.push(img.src);
            item.addEventListener('click', () => {
                currentIndex = idx;
                openLightbox(images[currentIndex]);
            });
        }
    });

    function openLightbox(src) {
        lightboxImg.src = src;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }

    function showPrev() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        lightboxImg.src = images[currentIndex];
    }

    function showNext() {
        currentIndex = (currentIndex + 1) % images.length;
        lightboxImg.src = images[currentIndex];
    }

    closeBtn.addEventListener('click', closeLightbox);
    prevBtn.addEventListener('click', showPrev);
    nextBtn.addEventListener('click', showNext);

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
    });

    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') showPrev();
        if (e.key === 'ArrowRight') showNext();
    });
}

/* ---- VIP Password System ---- */
function initVipPassword() {
    const VIP_PASSWORD = 'nairu2024';
    const STORAGE_KEY = 'nairu_vip_unlocked';

    const modal = document.getElementById('password-modal');
    const backdrop = document.getElementById('password-modal-backdrop');
    const closeBtn = document.getElementById('password-modal-close');
    const unlockBtn = document.getElementById('btn-unlock-vip');
    const submitBtn = document.getElementById('btn-submit-password');
    const passwordInput = document.getElementById('vip-password-input');
    const passwordToggle = document.getElementById('password-toggle');
    const passwordError = document.getElementById('password-error');
    const lockedDiv = document.getElementById('vip-locked');
    const unlockedDiv = document.getElementById('vip-unlocked');

    if (!modal || !unlockBtn) return;

    // Check if already unlocked
    if (localStorage.getItem(STORAGE_KEY) === 'true') {
        showUnlocked();
    }

    // Open modal
    unlockBtn.addEventListener('click', () => {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        setTimeout(() => passwordInput.focus(), 300);
    });

    // Close modal
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        passwordInput.value = '';
        passwordError.classList.add('hidden');
    }

    closeBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', closeModal);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // Toggle password visibility
    passwordToggle.addEventListener('click', () => {
        const icon = passwordToggle.querySelector('i');
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });

    // Submit password
    function tryUnlock() {
        const value = passwordInput.value.trim();
        if (value === VIP_PASSWORD) {
            localStorage.setItem(STORAGE_KEY, 'true');
            closeModal();
            showUnlocked();
        } else {
            passwordError.classList.remove('hidden');
            passwordInput.classList.add('error');
            // Re-trigger shake animation
            passwordError.style.animation = 'none';
            void passwordError.offsetHeight;
            passwordError.style.animation = '';

            setTimeout(() => {
                passwordInput.classList.remove('error');
            }, 1000);
        }
    }

    submitBtn.addEventListener('click', tryUnlock);
    passwordInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') tryUnlock();
        // Hide error when typing
        if (!passwordError.classList.contains('hidden')) {
            passwordError.classList.add('hidden');
        }
    });

    function showUnlocked() {
        lockedDiv.classList.add('hidden');
        unlockedDiv.classList.remove('hidden');

        // Init lightbox for VIP gallery items
        const lightbox = document.getElementById('lightbox');
        const lightboxImg = document.getElementById('lightbox-img');
        const closeBtn = document.getElementById('lightbox-close');
        const prevBtn = document.getElementById('lightbox-prev');
        const nextBtn = document.getElementById('lightbox-next');

        const vipItems = document.querySelectorAll('.vip-gallery-item');
        const vipImages = [];

        vipItems.forEach((item, idx) => {
            const img = item.querySelector('img');
            if (img) {
                vipImages.push(img.src);
                item.addEventListener('click', () => {
                    let currentVipIndex = idx;
                    lightboxImg.src = vipImages[currentVipIndex];
                    lightbox.classList.add('active');
                    document.body.style.overflow = 'hidden';
                });
            }
        });

        // VIP Video interactions — play on hover, click to fullscreen
        const vipVideoItems = document.querySelectorAll('.vip-video-item');
        vipVideoItems.forEach(item => {
            const video = item.querySelector('video');
            if (!video) return;

            item.addEventListener('mouseenter', () => {
                video.play().catch(() => { });
            });
            item.addEventListener('mouseleave', () => {
                video.pause();
                video.currentTime = 0;
            });
            item.addEventListener('click', () => {
                if (video.requestFullscreen) {
                    video.muted = false;
                    video.requestFullscreen();
                } else if (video.webkitRequestFullscreen) {
                    video.muted = false;
                    video.webkitRequestFullscreen();
                }
            });
        });
    }
}
