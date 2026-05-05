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
      links.classList.toggle('open');
    });
    links.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => links.classList.remove('open'));
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
    document.getElementById('incomeVal').textContent = gross.toLocaleString('en-IN');
    document.getElementById('ded80cVal').textContent = c80.toLocaleString('en-IN');
    document.getElementById('ded80dVal').textContent = d80.toLocaleString('en-IN');
    document.getElementById('hraVal').textContent = hraVal.toLocaleString('en-IN');

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

  function num(id) { return Math.max(0, parseFloat(document.getElementById(id).value) || 0); }

  function fmt(v) {
    return '₹' + Math.round(v).toLocaleString('en-IN');
  }

  /* Old Regime Slabs (FY 25-26) */
  function oldRegime(ti) {
    if (ti <= 500000) return 0; // 87A rebate
    let t = 0;
    // 0-2.5L = 0%, 2.5-5L = 5%, 5-10L = 20%, 10L+ = 30%
    if (ti > 1000000) { t += (ti - 1000000) * 0.30; ti = 1000000; }
    if (ti > 500000)  { t += (ti - 500000)  * 0.20; ti = 500000;  }
    if (ti > 250000)  { t += (ti - 250000)  * 0.05; }
    return t * 1.04; // + 4% cess
  }

  /* New Regime Slabs (FY 25-26 – Budget 2025) */
  function newRegime(income) {
    if (income <= 700000) return 0; // 87A rebate (new regime)

    let ti = income;
    let t = 0;

    // 0-3L = 0%, 3-7L = 5%, 7-10L = 10%, 10-12L = 15%, 12-15L = 20%, 15L+ = 30%
    if (ti > 1500000) { t += (ti - 1500000) * 0.30; ti = 1500000; }
    if (ti > 1200000) { t += (ti - 1200000) * 0.20; ti = 1200000; }
    if (ti > 1000000) { t += (ti - 1000000) * 0.15; ti = 1000000; }
    if (ti > 700000)  { t += (ti - 700000)  * 0.10; ti = 700000;  }
    if (ti > 300000)  { t += (ti - 300000)  * 0.05; }

    // Marginal relief: if income is just above 7L, tax ≤ excess over 7L
    if (income > 700000 && income <= 730000) {
      t = Math.min(t, income - 700000);
    }

    return t * 1.04; // + 4% cess
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
          btn.textContent = 'Oops! Error.';
        }
      } catch (error) {
        btn.textContent = 'Oops! Error.';
      }

      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        btn.style.opacity = '1';
      }, 3000);
    });
  }

  /* ─── 7. Modal Handler ─── */
  const modalTrigger = document.getElementById('journal-modal-trigger');
  const modalOverlay = document.getElementById('journalModal');
  const modalClose = document.getElementById('modalClose');

  if (modalTrigger && modalOverlay && modalClose) {
    modalTrigger.addEventListener('click', () => {
      modalOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    });

    modalClose.addEventListener('click', () => {
      modalOverlay.classList.remove('active');
      document.body.style.overflow = '';
    });

    modalOverlay.addEventListener('click', e => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  }

});
