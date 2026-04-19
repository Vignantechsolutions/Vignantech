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
