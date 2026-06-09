// ============================================================
// Vignan TechSolutions — Main JS v3.0
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

    // ── AOS Init ──
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 700, once: true, offset: 40,
            easing: 'ease-out-cubic',
            disable: window.innerWidth < 576
        });
    }

    // ── Navbar scroll effect ──
    const nav = document.getElementById('mainNav');
    if (nav) {
        const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 20);
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // ── Mobile nav: close on link click ──
    const navCollapse = document.getElementById('navMenu');
    if (navCollapse) {
        navCollapse.querySelectorAll('.nav-link:not(.dropdown-toggle)').forEach(link => {
            link.addEventListener('click', () => {
                const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                if (bsCollapse) bsCollapse.hide();
            });
        });
    }

    // ── Active nav link ──
    const path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && href !== '/' && path.startsWith(href)) link.classList.add('active');
        if (href === '/' && path === '/') link.classList.add('active');
    });

    // ── Auto-dismiss alerts ──
    document.querySelectorAll('.alert-dismissible').forEach(el => {
        setTimeout(() => bootstrap.Alert.getOrCreateInstance(el)?.close(), 5000);
    });

    // ── Counter animation ──
    const counters = document.querySelectorAll('[data-count]');
    if (counters.length) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                const target = parseInt(el.dataset.count);
                let current = 0;
                const step = Math.ceil(target / 60);
                const timer = setInterval(() => {
                    current = Math.min(current + step, target);
                    el.textContent = current;
                    if (current >= target) clearInterval(timer);
                }, 20);
                observer.unobserve(el);
            });
        }, { threshold: 0.5 });
        counters.forEach(c => observer.observe(c));
    }

    // ── Back to top ──
    const btn = document.getElementById('back-to-top');
    if (btn) {
        window.addEventListener('scroll', () => {
            btn.style.display = window.scrollY > 400 ? 'flex' : 'none';
        }, { passive: true });
        btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // ── Password toggle ──
    document.querySelectorAll('[data-toggle-pass]').forEach(b => {
        b.addEventListener('click', function () {
            const input = document.getElementById(this.dataset.togglePass);
            if (!input) return;
            input.type = input.type === 'password' ? 'text' : 'password';
            this.querySelector('i')?.classList.toggle('bi-eye');
            this.querySelector('i')?.classList.toggle('bi-eye-slash');
        });
    });

    // ── Password strength ──
    const p1 = document.getElementById('password1');
    if (p1) {
        p1.addEventListener('input', function () {
            let bar = document.getElementById('pass-strength-bar');
            if (!bar) {
                const wrap = document.createElement('div');
                wrap.innerHTML = '<div class="progress mt-1" style="height:4px"><div id="pass-strength-bar" class="progress-bar" style="transition:.3s"></div></div><small id="pass-strength-label" class="mt-1 d-block"></small>';
                this.closest('.mb-3, .col-md-6')?.appendChild(wrap);
                bar = document.getElementById('pass-strength-bar');
            }
            const label = document.getElementById('pass-strength-label');
            const v = this.value;
            let score = 0;
            if (v.length >= 8) score++;
            if (/[A-Z]/.test(v)) score++;
            if (/[0-9]/.test(v)) score++;
            if (/[^A-Za-z0-9]/.test(v)) score++;
            const cfg = [
                ['0%','',''],['25%','bg-danger','Weak'],
                ['50%','bg-warning','Fair'],['75%','bg-info','Good'],['100%','bg-success','Strong']
            ];
            bar.style.width = cfg[score][0];
            bar.className = 'progress-bar ' + cfg[score][1];
            if (label) {
                label.textContent = cfg[score][2];
                label.className = 'mt-1 d-block small text-' + (cfg[score][1].replace('bg-','') || 'muted');
            }
        });
    }

    // ── Smooth scroll anchors ──
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const t = document.querySelector(a.getAttribute('href'));
            if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        });
    });

    // ── Form validation ──
    document.querySelectorAll('form[novalidate]').forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!this.checkValidity()) { e.preventDefault(); e.stopPropagation(); }
            this.classList.add('was-validated');
        });
    });

    // ── Tooltip init ──
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));

    // ── Lazy-load images ──
    if ('loading' in HTMLImageElement.prototype) {
        document.querySelectorAll('img:not([loading])').forEach(img => img.setAttribute('loading', 'lazy'));
    }

    // ── Fix 300ms tap delay on mobile ──
    document.querySelectorAll('a, button, .btn, .nav-link').forEach(el => {
        el.style.touchAction = 'manipulation';
    });
});

// ── Creative UI v5.0 ──

// ── Magnetic CTA buttons ──
document.querySelectorAll('.vt-btn-primary, .vt-btn-white, .vt-btn-ghost').forEach(btn => {
    btn.addEventListener('mousemove', e => {
        const rect = btn.getBoundingClientRect();
        const x = (e.clientX - rect.left - rect.width / 2) * 0.25;
        const y = (e.clientY - rect.top - rect.height / 2) * 0.25;
        btn.style.transform = `translate(${x}px, ${y}px) translateY(-3px)`;
    });
    btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
});

// ── Spotlight cursor on dark hero sections ──
(function() {
    const heroes = document.querySelectorAll('.vt-hero, .proj-hero, .intern-hero, .contact-hero, .about-hero, .vt-impact-section');
    heroes.forEach(hero => {
        const spotlight = document.createElement('div');
        spotlight.style.cssText = 'position:absolute;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,rgba(124,58,237,.08) 0%,transparent 70%);pointer-events:none;transform:translate(-50%,-50%);transition:left .12s ease,top .12s ease;z-index:1;opacity:0;';
        hero.style.position = 'relative';
        hero.appendChild(spotlight);
        hero.addEventListener('mousemove', e => {
            const rect = hero.getBoundingClientRect();
            spotlight.style.left = (e.clientX - rect.left) + 'px';
            spotlight.style.top  = (e.clientY - rect.top)  + 'px';
            spotlight.style.opacity = '1';
        });
        hero.addEventListener('mouseleave', () => { spotlight.style.opacity = '0'; });
    });
})();

// ── Social proof toast ──
setTimeout(() => {
    const msgs = [
        '🔥 3 students enrolled today',
        '✅ New MCA project delivered!',
        '🎓 Certificate issued to a student',
        '⭐ New 5-star review received',
    ];
    const msg = msgs[Math.floor(Math.random() * msgs.length)];
    const toast = document.createElement('div');
    toast.style.cssText = 'position:fixed;bottom:100px;left:20px;background:#0F172A;border:1px solid rgba(124,58,237,.4);color:#fff;padding:12px 18px;border-radius:14px;font-size:.82rem;font-weight:600;z-index:9997;box-shadow:0 8px 32px rgba(0,0,0,.4);display:flex;align-items:center;gap:10px;animation:toastIn .4s ease forwards;max-width:260px;';
    const emoji = msg.split(' ')[0];
    const text  = msg.slice(msg.indexOf(' ') + 1);
    toast.innerHTML = `<span style="font-size:1rem">${emoji}</span><span>${text}</span>`;
    const style = document.createElement('style');
    style.textContent = '@keyframes toastIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}@keyframes toastOut{from{opacity:1}to{opacity:0;transform:translateX(-20px)}}';
    document.head.appendChild(style);
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'toastOut .4s ease forwards';
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}, 8000);

// ── Ripple on buttons ──
document.querySelectorAll('.vt-btn-primary, .vt-btn-white, .btn-primary').forEach(btn => {
    btn.addEventListener('click', function(e) {
        const r = document.createElement('span');
        r.className = 'ripple';
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        r.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX-rect.left-size/2}px;top:${e.clientY-rect.top-size/2}px;position:absolute;`;
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(r);
        setTimeout(() => r.remove(), 700);
    });
});

// 3D tilt on project/program cards
document.querySelectorAll('.vt-project-card, .vt-program-card, .vt-step').forEach(card => {
    card.classList.add('tilt-card');
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width  - .5;
        const y = (e.clientY - rect.top)  / rect.height - .5;
        card.style.transform = `perspective(600px) rotateY(${x*10}deg) rotateX(${-y*10}deg) translateY(-6px)`;
    });
    card.addEventListener('mouseleave', () => { card.style.transform = ''; });
});

// Scroll reveal
const revealEls = document.querySelectorAll('[data-aos]');
if (revealEls.length === 0) {
    document.querySelectorAll('.vt-service-card,.vt-step,.vt-why-card,.vt-testimonial').forEach((el,i) => {
        el.classList.add('reveal');
        el.style.transitionDelay = (i % 4) * 0.1 + 's';
    });
    const ro = new IntersectionObserver(entries => {
        entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); ro.unobserve(e.target); } });
    }, { threshold: 0.15 });
    document.querySelectorAll('.reveal').forEach(el => ro.observe(el));
}
