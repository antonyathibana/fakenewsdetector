/* ==========================================================================
   FAKE NEWS DETECTOR - THEME JAVASCRIPT
   Interactive Components & Animations
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    
    /* =====================
       THEME TOGGLE
       ===================== */
    
    const themeToggle = document.getElementById('themeToggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }
    
    function updateThemeIcon(theme) {
        const icon = themeToggle?.querySelector('i');
        if (icon) {
            if (theme === 'light') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        }
    }
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }
    
    /* =====================
       NAVBAR SCROLL EFFECT
       ===================== */
    
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
        
        lastScroll = currentScroll;
    });
    
    /* =====================
       ACTIVE NAV LINK
       ===================== */
    
    const currentLocation = location.href;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.href === currentLocation) {
            link.classList.add('active');
        }
    });
    
    /* =====================
       INPUT TYPE SWITCHER
       ===================== */
    
    const textInputBtn = document.getElementById('textInputBtn');
    const urlInputBtn = document.getElementById('urlInputBtn');
    const textInputSection = document.getElementById('textInputSection');
    const urlInputSection = document.getElementById('urlInputSection');
    const inputType = document.getElementById('inputType');
    
    if (textInputBtn && urlInputBtn) {
        window.setInputType = function(type) {
            inputType.value = type;
            
            // Update button styles
            textInputBtn.classList.toggle('active', type === 'text');
            urlInputBtn.classList.toggle('active', type === 'url');
            
            // Show/hide appropriate inputs
            if (textInputSection && urlInputSection) {
                textInputSection.style.display = type === 'text' ? 'block' : 'none';
                urlInputSection.style.display = type === 'url' ? 'block' : 'none';
            }
            
            // Update required attribute
            const textArea = document.querySelector('textarea[name="news_text"]');
            const urlInput = document.querySelector('input[name="news_text"]');
            
            if (textArea && urlInput) {
                if (type === 'text') {
                    textArea.required = true;
                    urlInput.required = false;
                } else {
                    textArea.required = false;
                    urlInput.required = true;
                }
            }
        };
    }
    
    /* =====================
       FORM SUBMISSION
       ===================== */
    
    const predictForm = document.getElementById('predictForm');
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    
    if (predictForm) {
        predictForm.addEventListener('submit', function(e) {
            // Only prevent default if it's a new submission (not from result page)
            if (!this.dataset.submitted) {
                this.dataset.submitted = 'true';
                
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin me-2"></i>Analyzing...';
                }
                
                if (loadingIndicator) {
                    loadingIndicator.style.display = 'block';
                }
            }
        });
    }
    
    /* =====================
       SMOOTH SCROLL
       ===================== */
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    /* =====================
       ANIMATE ON SCROLL
       ===================== */
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Apply animation to elements but ensure they're visible by default
    const animatedElements = document.querySelectorAll('.card, .hero-section, .stats-card');
    animatedElements.forEach(el => {
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        // Don't set opacity to 0 - let them be visible initially
        observer.observe(el);
    });
    
    // Add animation class styles dynamically
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
    
    /* =====================
       BUTTON EFFECTS
       ===================== */
    
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function(e) {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = e.clientX - rect.left - size / 2 + 'px';
            ripple.style.top = e.clientY - rect.top - size / 2 + 'px';
            ripple.style.background = 'rgba(255, 255, 255, 0.3)';
            ripple.style.borderRadius = '50%';
            ripple.style.position = 'absolute';
            ripple.style.pointerEvents = 'none';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'rippleEffect 0.6s linear';
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Add ripple keyframes dynamically
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes rippleEffect {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
    
    /* =====================
       PROGRESS BAR ANIMATION
       ===================== */
    
    const progressBars = document.querySelectorAll('.progress-bar');
    
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
                progressObserver.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });
    
    progressBars.forEach(bar => progressObserver.observe(bar));
    
    /* =====================
       CARD HOVER SOUND (Optional)
       ===================== */
    
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });
    
    /* =====================
       GLOW PULSE FOR RESULTS
       ===================== */
    
    const resultHeader = document.querySelector('.result-header');
    if (resultHeader) {
        resultHeader.classList.add('glow-pulse');
    }
    
    /* =====================
       PARALLAX BACKGROUND (Subtle)
       ===================== */
    
    let ticking = false;
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                const body = document.body;
                
                if (scrolled > 0) {
                    body.style.backgroundPosition = `center ${scrolled * 0.1}px`;
                }
                
                ticking = false;
            });
            
            ticking = true;
        }
    });
    
    /* =====================
       LOADING STATE FOR FORMS
       ===================== */
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                submitButton.classList.add('loading');
                
                // Create spinner if not exists
                if (!submitButton.querySelector('.spinner-border')) {
                    const spinner = document.createElement('span');
                    spinner.className = 'spinner-border spinner-border-sm me-2';
                    spinner.setAttribute('role', 'status');
                    spinner.setAttribute('aria-hidden', 'true');
                    submitButton.prepend(spinner);
                }
            }
        });
    });
    
    /* =====================
       ALERT AUTO DISMISS
       ===================== */
    
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    /* =====================
       THEME SWITCH BUTTON
       ===================== */
    
    // Auto-create theme toggle button if not exists
    const navRight = document.querySelector('.navbar-collapse');
    if (navRight && !document.getElementById('themeToggle')) {
        const themeBtn = document.createElement('button');
        themeBtn.id = 'themeToggle';
        themeBtn.className = 'btn btn-icon btn-ghost ms-2';
        themeBtn.setAttribute('aria-label', 'Toggle theme');
        themeBtn.innerHTML = '<i class="fas fa-moon"></i>';
        navRight.appendChild(themeBtn);
        
        // Update icon based on current theme
        const currentTheme = document.documentElement.getAttribute('data-theme');
        updateThemeIcon(currentTheme || 'dark');
    }
    
    /* =====================
       COUNTER ANIMATION
       ===================== */
    
    const counters = document.querySelectorAll('[data-count]');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-count'));
                const duration = 2000;
                const increment = target / (duration / 16);
                
                let current = 0;
                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        counter.textContent = Math.floor(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target;
                    }
                };
                
                updateCounter();
                counterObserver.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => counterObserver.observe(counter));
    
    /* =====================
       COPY TO CLIPBOARD
       ===================== */
    
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-copy');
            const target = document.getElementById(targetId);
            
            if (target) {
                navigator.clipboard.writeText(target.textContent).then(() => {
                    const originalIcon = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => {
                        this.innerHTML = originalIcon;
                    }, 2000);
                });
            }
        });
    });
    
    /* =====================
       COLLAPSE TRANSITIONS
       ===================== */
    
    document.querySelectorAll('.collapse').forEach(collapse => {
        collapse.addEventListener('show.bs.collapse', function() {
            this.style.opacity = '0';
            this.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                this.style.opacity = '1';
                this.style.transform = 'translateY(0)';
                this.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            }, 10);
        });
    });
    
    /* =====================
       KEYBOARD SHORTCUTS
       ===================== */
    
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for theme toggle
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (themeToggle) {
                themeToggle.click();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });
    
    /* =====================
       INITIALIZE
       ===================== */
    
    console.log('%c🎨 Premium Futuristic Theme Loaded', 'color: #6366F1; font-size: 14px; font-weight: bold;');
});

/* =====================
   UTILITY FUNCTIONS
   ===================== */

// Theme ready class
document.documentElement.classList.add('theme-ready');

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Add to window for global access
window.debounce = debounce;
window.throttle = throttle;

