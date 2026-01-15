/**
 * MONARCH CASTLE TECHNOLOGIES - WEBSITE SCRIPTS
 * Animations, interactions, and dynamic elements
 */

// ============================================
// NAVIGATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Mobile nav toggle
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
            navbar.style.padding = '12px 0';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.8)';
            navbar.style.padding = '20px 0';
        }
        
        lastScroll = currentScroll;
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Close mobile menu if open
                navMenu.classList.remove('active');
            }
        });
    });
});

// ============================================
// COUNTER ANIMATIONS
// ============================================

function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const update = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(update);
        } else {
            element.textContent = target;
        }
    };
    
    update();
}

// Intersection Observer for counter animations
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const element = entry.target;
            const target = parseInt(element.dataset.count);
            if (target && !element.classList.contains('animated')) {
                element.classList.add('animated');
                animateCounter(element, target);
            }
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('[data-count]').forEach(el => {
    counterObserver.observe(el);
});

// ============================================
// SCROLL ANIMATIONS (Simple AOS alternative)
// ============================================

const animateOnScroll = () => {
    const elements = document.querySelectorAll('[data-aos]');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        
        if (elementTop < windowHeight * 0.85) {
            const delay = element.dataset.aosDelay || 0;
            setTimeout(() => {
                element.classList.add('aos-animate');
            }, delay);
        }
    });
};

// Add CSS for AOS
const aosStyles = document.createElement('style');
aosStyles.textContent = `
    [data-aos] {
        opacity: 0;
        transform: translateY(30px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    
    [data-aos].aos-animate {
        opacity: 1;
        transform: translateY(0);
    }
    
    [data-aos="fade-up"] {
        transform: translateY(40px);
    }
    
    [data-aos="fade-in"] {
        transform: translateY(0);
    }
`;
document.head.appendChild(aosStyles);

window.addEventListener('scroll', animateOnScroll);
window.addEventListener('load', animateOnScroll);

// ============================================
// DEMO FORM HANDLING
// ============================================

const demoForm = document.getElementById('demoForm');
if (demoForm) {
    demoForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = demoForm.querySelector('input').value;
        
        // Create success message
        const successHtml = `
            <div style="
                background: rgba(34, 197, 94, 0.1);
                border: 1px solid rgba(34, 197, 94, 0.3);
                border-radius: 8px;
                padding: 20px;
                text-align: center;
            ">
                <div style="font-size: 2rem; margin-bottom: 12px;">✅</div>
                <div style="font-weight: 600; margin-bottom: 8px;">Request Received!</div>
                <div style="color: #a0a0a0; font-size: 0.9rem;">
                    We'll contact you at <strong style="color: #d4af37;">${email}</strong>
                </div>
            </div>
        `;
        
        demoForm.innerHTML = successHtml;
    });
}

// ============================================
// TERMINAL TYPING EFFECT
// ============================================

const typeWriter = (element, text, speed = 50) => {
    let i = 0;
    element.textContent = '';
    
    const type = () => {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    };
    
    type();
};

// ============================================
// PARALLAX EFFECT FOR HERO GLOWS
// ============================================

const glows = document.querySelectorAll('.glow');
let mouseX = 0, mouseY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX / window.innerWidth - 0.5;
    mouseY = e.clientY / window.innerHeight - 0.5;
});

const parallaxGlows = () => {
    glows.forEach((glow, index) => {
        const speed = (index + 1) * 20;
        const x = mouseX * speed;
        const y = mouseY * speed;
        glow.style.transform = `translate(${x}px, ${y}px)`;
    });
    requestAnimationFrame(parallaxGlows);
};

parallaxGlows();

// ============================================
// PRODUCT CARD HOVER EFFECTS
// ============================================

document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-8px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// ============================================
// CONSOLE EASTER EGG
// ============================================

console.log(`
%c🏰 MONARCH CASTLE TECHNOLOGIES
%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  The Palantir of Türkiye
  
  "The chart doesn't lie."
  
  System Status: ONLINE
  AI Director: ACTIVE
  
  Interested in joining our team?
  Contact: careers@monarchcastle.tech

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`, 
'color: #d4af37; font-size: 20px; font-weight: bold;',
'color: #888;'
);
