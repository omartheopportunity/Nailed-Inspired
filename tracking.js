/* Nailed & Inspired — tracking.js
   One file, loaded on every page: <script src="tracking.js" defer></script>
   - Pinterest tag (ID 2613377588756): pagevisit on every page, lead on quiz submit,
     checkout-click on product/bundle buttons
   - Saves utm_* params from the pin link so you know which pin sent the visitor
   - Logs quiz funnel steps (start -> answered -> email shown -> email submitted)
     to Pinterest custom events so you can see where people drop off */
(function () {
  var TAG_ID = '2613377588756';

  /* ---- Pinterest base code ---- */
  !function (e) { if (!window.pintrk) { window.pintrk = function () { window.pintrk.queue.push(Array.prototype.slice.call(arguments)); }; var n = window.pintrk; n.queue = []; n.version = '3.0'; var t = document.createElement('script'); t.async = !0; t.src = e; var r = document.getElementsByTagName('script')[0]; r.parentNode.insertBefore(t, r); } }('https://s.pinimg.com/ct/core.js');

  /* ---- Keep UTM params from the first landing (survives page-to-page clicks) ---- */
  var utm = {};
  try {
    var qs = new URLSearchParams(location.search);
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
      if (qs.get(k)) utm[k] = qs.get(k);
    });
    if (Object.keys(utm).length) sessionStorage.setItem('ni_utm', JSON.stringify(utm));
    else utm = JSON.parse(sessionStorage.getItem('ni_utm') || '{}');
  } catch (e) {}

  pintrk('load', TAG_ID);
  pintrk('page', { page_name: document.title, page_category: location.pathname });
  pintrk('track', 'pagevisit', { property: location.pathname });

  function track(evt, data) {
    try { pintrk('track', evt, Object.assign({}, data || {}, utm)); } catch (e) {}
    try { if (window.console) console.log('[ni-track]', evt, data || '', utm); } catch (e) {}
  }

  /* ---- Quiz funnel (only runs on pages with the quiz form) ---- */
  document.addEventListener('DOMContentLoaded', function () {
    var started = false;
    document.addEventListener('click', function (ev) {
      var t = ev.target.closest && ev.target.closest('.quiz-option, .quiz-answer, [data-quiz-option], .quiz-start, #quiz-start');
      if (!t) return;
      if (!started) { started = true; track('custom', { event_name: 'quiz_start' }); }
      track('custom', { event_name: 'quiz_answer' });
    });

    var form = document.getElementById('quiz-email-form');
    if (form) {
      var shown = false, seen = new IntersectionObserver(function (entries) {
        if (!shown && entries[0].isIntersecting) { shown = true; track('custom', { event_name: 'quiz_email_gate_seen' }); }
      });
      seen.observe(form);

      form.addEventListener('submit', function () {
        var email = (document.getElementById('quiz-email-input') || {}).value || '';
        track('lead', { lead_type: 'quiz', em: email });
        try { pintrk('set', { np: 'ni_quiz' }); } catch (e) {}
      });
    }

    /* ---- Buy / bundle buttons ---- */
    document.addEventListener('click', function (ev) {
      var a = ev.target.closest && ev.target.closest('a');
      if (!a || !a.href) return;
      if (/bundle-|\/products\/|etsy\.com|shop\.tiktok\.com|skool\.com|checkout/i.test(a.href)) {
        track('checkout', { value: 0, order_quantity: 1, line_items: [{ product_name: (a.textContent || '').trim().slice(0, 60) }] });
      }
    });
  });
})();
