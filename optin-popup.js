/* Nailed & Inspired — optin-popup.js
   Email opt-in popup for the "Become Her" list. Loaded by tracking.js on every page.
   - Shows on content pages (blog posts, community, home). Skipped on product/shop
     pages and on pages that already capture email (join, quiz, era-quiz).
   - Opens after ~7s or ~45% scroll (whichever is first), or on desktop exit-intent.
   - Shows once per visitor per 14 days once closed or submitted. Force it with ?optin=1.
   - Sends to the same Google Form the quiz and join page use. Keeps the pin's utm
     source so you can see which pin or board produced the signup. */
(function () {
  var path = location.pathname.split('/').pop() || 'index.html';
  var skip = /^(join|quiz|era-quiz|products|bundle-next-chapter|gift-wrap-coffee)(\.html)?$/;
  var force = /[?&]optin=1/.test(location.search);
  if (skip.test(path) && !force) return;

  var KEY = 'ni_optin_state';
  function get() { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } }
  function set(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }
  var st = get();
  var DAY = 864e5;
  if (!force && st.t && Date.now() - st.t < (st.done ? 90 : 14) * DAY) return;

  var shown = false;
  function open() {
    if (shown) return; shown = true;
    var css = document.createElement('style');
    css.textContent =
      '.nio-bg{position:fixed;inset:0;background:rgba(36,19,24,.62);z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px;opacity:0;transition:opacity .25s}' +
      '.nio-bg.on{opacity:1}' +
      '.nio-card{position:relative;background:#FBF3EC;color:#241318;max-width:420px;width:100%;border-radius:4px;padding:34px 28px 26px;text-align:center;font-family:Jost,"Helvetica Neue",Arial,sans-serif;box-shadow:0 18px 60px rgba(0,0,0,.35);border-top:4px solid #B98B4E}' +
      '.nio-x{position:absolute;top:8px;right:12px;background:none;border:0;font-size:26px;line-height:1;color:#3B1F2B;cursor:pointer;padding:6px}' +
      '.nio-eyebrow{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#B98B4E;margin:0 0 8px}' +
      '.nio-h{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;font-size:30px;line-height:1.1;color:#3B1F2B;margin:0 0 10px}' +
      '.nio-p{font-size:15px;line-height:1.5;margin:0 0 18px;color:#3B1F2B}' +
      '.nio-in{width:100%;box-sizing:border-box;padding:13px 14px;border:1px solid rgba(59,31,43,.3);border-radius:2px;font:inherit;font-size:16px;background:#fff;margin-bottom:10px}' +
      '.nio-btn{width:100%;padding:14px;border:0;border-radius:2px;background:#3B1F2B;color:#FBF3EC;font:inherit;font-weight:500;letter-spacing:.06em;cursor:pointer}' +
      '.nio-btn:hover{background:#241318}' +
      '.nio-err{color:#a3303c;font-size:13px;min-height:18px;margin:0 0 6px}' +
      '.nio-note{font-size:12px;color:#6b5560;margin:12px 0 0}' +
      '.nio-skip{background:none;border:0;color:#6b5560;font:inherit;font-size:13px;text-decoration:underline;cursor:pointer;margin-top:10px}';
    document.head.appendChild(css);

    var bg = document.createElement('div');
    bg.className = 'nio-bg';
    bg.setAttribute('role', 'dialog'); bg.setAttribute('aria-modal', 'true'); bg.setAttribute('aria-labelledby', 'nio-h');
    bg.innerHTML =
      '<div class="nio-card">' +
      '<button class="nio-x" type="button" aria-label="Close">&times;</button>' +
      '<div class="nio-body">' +
      '<p class="nio-eyebrow">Nailing your look is step one</p>' +
      '<h2 class="nio-h" id="nio-h">Become Her &mdash; join the list</h2>' +
      '<p class="nio-p">Weekly reset texts, confidence tips &amp; women-only events for the woman you&rsquo;re becoming. Takes ten seconds.</p>' +
      '<form novalidate><input class="nio-in" type="email" name="email" placeholder="you@email.com" autocomplete="email" aria-label="Email address" required>' +
      '<p class="nio-err" role="alert"></p>' +
      '<button class="nio-btn" type="submit">Join the list</button></form>' +
      '<button class="nio-skip" type="button">No thanks</button>' +
      '<p class="nio-note">No spam. Unsubscribe anytime.</p>' +
      '</div></div>';
    document.body.appendChild(bg);
    requestAnimationFrame(function () { bg.classList.add('on'); });

    var input = bg.querySelector('input'), err = bg.querySelector('.nio-err');
    function close(done) {
      set({ t: Date.now(), done: !!done });
      bg.classList.remove('on');
      setTimeout(function () { bg.remove(); }, 250);
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e) { if (e.key === 'Escape') close(false); }
    document.addEventListener('keydown', onKey);
    bg.querySelector('.nio-x').onclick = bg.querySelector('.nio-skip').onclick = function () { close(false); };
    bg.addEventListener('click', function (e) { if (e.target === bg) close(false); });

    bg.querySelector('form').addEventListener('submit', function (e) {
      e.preventDefault();
      var email = (input.value || '').trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { err.textContent = 'Please enter a valid email address.'; input.focus(); return; }
      var src = '';
      try {
        var u = JSON.parse(sessionStorage.getItem('ni_utm') || '{}');
        src = ' | from: ' + (u.utm_source || 'direct') + ' ' + (u.utm_campaign || '') + ' ' + (u.utm_content || '') + ' @' + path;
      } catch (x) { src = ' | from: direct @' + path; }
      try {
        var body = new URLSearchParams();
        body.append('entry.1825262067', email);
        body.append('entry.866244110', 'Popup' + src);
        fetch('https://docs.google.com/forms/d/e/1FAIpQLScBecL9eSqa8flRzst3Z_YT2gsx0buz-Aaisvs7qgEKj3TOPA/formResponse', {
          method: 'POST', mode: 'no-cors',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body.toString()
        });
      } catch (x) {}
      try { if (window.pintrk) window.pintrk('track', 'lead', { lead_type: 'popup', property: location.pathname }); } catch (x) {}
      bg.querySelector('.nio-body').innerHTML =
        '<p class="nio-eyebrow">You&rsquo;re in</p><h2 class="nio-h">Welcome to the room.</h2>' +
        '<p class="nio-p">Watch your inbox. Your first reset is on the way.</p>' +
        '<button class="nio-btn" type="button">Keep exploring</button>';
      bg.querySelector('.nio-btn').onclick = function () { close(true); };
      set({ t: Date.now(), done: true });
    });
  }

  /* Triggers: scroll depth, timer, desktop exit-intent */
  var timer = setTimeout(open, 7000);
  function onScroll() {
    var h = document.documentElement;
    var pct = (h.scrollTop + window.innerHeight) / Math.max(h.scrollHeight, 1);
    if (pct > 0.45) { clearTimeout(timer); window.removeEventListener('scroll', onScroll); open(); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  document.addEventListener('mouseout', function (e) { if (!e.relatedTarget && e.clientY < 8) { clearTimeout(timer); open(); } });
})();
