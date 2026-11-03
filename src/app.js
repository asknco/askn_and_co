/* ══════════════════════════════════════════════════════════════
   ASKN & Co. LLP — App Logic
   ══════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  /* ─── 1. Sticky Nav ─── */
  const navbar = document.getElementById('navbar');
  const onScroll = () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ─── 2. Mobile Menu Toggle ─── */
  const toggle = document.getElementById('navToggle');
  const links  = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const isOpen = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen);
    });
    links.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ─── 3. Smooth Scroll with Offset ─── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id === '#') return;
      const el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      const top = el.getBoundingClientRect().top + window.pageYOffset - 80;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  /* ─── 4. Scroll-Reveal Animations ─── */
  const faders = document.querySelectorAll('.fade-up');
  if (faders.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      entries => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } }),
      { threshold: 0.15 }
    );
    faders.forEach(el => io.observe(el));
  }

  // Auto-tag elements for fade-up
  document.querySelectorAll('.svc-card, .lit-card, .j-card, .team-card, .process-step, .stat').forEach(el => {
    el.classList.add('fade-up');
  });
  // Re-init observer for the dynamically tagged elements
  const allFaders = document.querySelectorAll('.fade-up:not(.visible)');
  if (allFaders.length && 'IntersectionObserver' in window) {
    const io2 = new IntersectionObserver(
      entries => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io2.unobserve(e.target); } }),
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    allFaders.forEach(el => io2.observe(el));
  }


  /* ─── 5. Tax Regime Simulator (FY 25-26) ─── */
  const calcInputs = ['income', 'ded80c', 'ded80d', 'hra'];
  calcInputs.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', runCalc);
    }
  });
  
  if (document.getElementById('income')) {
    runCalc(); // initial
  }

  function runCalc() {
    const gross   = num('income');
    const c80     = Math.min(num('ded80c'), 150000);
    const d80     = num('ded80d');
    const hraVal  = num('hra');

    // Update UI spans
    const incomeValEl = document.getElementById('incomeVal');
    const ded80cValEl = document.getElementById('ded80cVal');
    const ded80dValEl = document.getElementById('ded80dVal');
    const hraValEl = document.getElementById('hraVal');
    if (incomeValEl) incomeValEl.textContent = gross.toLocaleString('en-IN');
    if (ded80cValEl) ded80cValEl.textContent = c80.toLocaleString('en-IN');
    if (ded80dValEl) ded80dValEl.textContent = d80.toLocaleString('en-IN');
    if (hraValEl) hraValEl.textContent = hraVal.toLocaleString('en-IN');

    // ── Old Regime ──
    const oldSD  = 50000; // standard deduction
    const oldDed = c80 + d80 + hraVal + oldSD;
    const oldTI  = Math.max(0, gross - oldDed);
    const oldTax = oldRegime(oldTI);

    // ── New Regime (FY 25-26) ──
    const newSD  = 75000; // enhanced standard deduction
    const newTI  = Math.max(0, gross - newSD);
    const newTax = newRegime(newTI);

    // UI
    document.getElementById('oldTax').textContent = fmt(oldTax);
    document.getElementById('newTax').textContent = fmt(newTax);

    const badge = document.getElementById('resBadge');
    badge.style.display = 'block';
    
    const cardOld = document.getElementById('cardOldTax');
    const cardNew = document.getElementById('cardNewTax');
    
    if (cardOld) cardOld.classList.remove('is-better');
    if (cardNew) cardNew.classList.remove('is-better');

    if (newTax < oldTax) {
      badge.innerHTML = '<strong>New Regime is BETTER</strong> — Save ' + fmt(oldTax - newTax);
      if (cardNew) cardNew.classList.add('is-better');
    } else if (oldTax < newTax) {
      badge.innerHTML = '<strong>Old Regime is BETTER</strong> — Save ' + fmt(newTax - oldTax);
      if (cardOld) cardOld.classList.add('is-better');
    } else {
      badge.innerHTML = '<strong>Both regimes result in the same tax.</strong>';
    }
  }

  function num(id) {
    const el = document.getElementById(id);
    return el ? Math.max(0, parseFloat(el.value) || 0) : 0;
  }

  function fmt(v) {
    return '₹' + Math.round(v).toLocaleString('en-IN');
  }

  /* Surcharge on income-tax (marginal relief on surcharge not modelled) */
  function surchargeRate(income, cap) {
    if (income > 50000000) return cap;   // above 5 Cr: 37% old, 25% new
    if (income > 20000000) return 0.25;
    if (income > 10000000) return 0.15;
    if (income > 5000000)  return 0.10;
    return 0;
  }

  /* Old Regime Slabs (FY 25-26) */
  function oldRegime(income) {
    if (income <= 500000) return 0; // 87A rebate
    let ti = income;
    let t = 0;
    // 0-2.5L = 0%, 2.5-5L = 5%, 5-10L = 20%, 10L+ = 30%
    if (ti > 1000000) { t += (ti - 1000000) * 0.30; ti = 1000000; }
    if (ti > 500000)  { t += (ti - 500000)  * 0.20; ti = 500000;  }
    if (ti > 250000)  { t += (ti - 250000)  * 0.05; }
    return t * (1 + surchargeRate(income, 0.37)) * 1.04; // + surcharge + 4% cess
  }

  /* New Regime Slabs (FY 25-26 – Budget 2025) */
  function newRegime(income) {
    if (income <= 1200000) return 0; // 87A rebate (new regime)

    let ti = income;
    let t = 0;

    // 0-4L = 0%, 4-8L = 5%, 8-12L = 10%, 12-16L = 15%, 16-20L = 20%, 20-24L = 25%, 24L+ = 30%
    if (ti > 2400000) { t += (ti - 2400000) * 0.30; ti = 2400000; }
    if (ti > 2000000) { t += (ti - 2000000) * 0.25; ti = 2000000; }
    if (ti > 1600000) { t += (ti - 1600000) * 0.20; ti = 1600000; }
    if (ti > 1200000) { t += (ti - 1200000) * 0.15; ti = 1200000; }
    if (ti > 800000)  { t += (ti - 800000)  * 0.10; ti = 800000;  }
    if (ti > 400000)  { t += (ti - 400000)  * 0.05; }

    // Marginal relief: just above 12L, tax ≤ excess over 12L
    t = Math.min(t, income - 1200000);

    return t * (1 + surchargeRate(income, 0.25)) * 1.04; // + surcharge + 4% cess
  }


  /* ─── 6. Contact Form Handler ─── */
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const originalText = btn.innerHTML;
      btn.textContent = 'Sending...';
      btn.disabled = true;
      btn.style.opacity = '.6';

      try {
        const response = await fetch(form.action, {
          method: form.method,
          body: new FormData(form),
          headers: {
            'Accept': 'application/json'
          }
        });
        
        if (response.ok) {
          btn.textContent = 'Sent — Thank You!';
          form.reset();
        } else {
          btn.textContent = 'Could not send. Please try again.';
        }
      } catch (error) {
        btn.textContent = 'Network error. Please check your connection.';
      }

      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        btn.style.opacity = '1';
      }, 3500);
    });
  }

  /* ─── 7. Dynamic Copyright Year ─── */
  const yearEl = document.getElementById('copyrightYear');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

});
