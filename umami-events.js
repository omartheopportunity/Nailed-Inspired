/* Umami conversion tracking — loaded after the Umami script on every page.
   Sends custom events when visitors click a call-to-action or submit a form.
   Events (view them under Events in Umami):
     cta-skool, cta-book-call, cta-register-form, cta-register, cta-join,
     cta-checkout, cta-etsy, outbound-click, form-submit,
     cta-<id> (Daily Roast buttons whose link is set by script) */
(function () {
  function track(name, data) {
    try { if (window.umami && typeof window.umami.track === 'function') window.umami.track(name, data || {}); } catch (e) {}
  }
  var page = location.pathname;

  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('a,button') : null;
    if (!el) return;
    var label = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60);
    var data = { page: page, label: label };
    if (el.tagName !== 'A') return;

    var u;
    try { u = new URL(el.href, location.href); } catch (err) { return; }
    var host = u.hostname.replace(/^www\./, '');
    var sameSite = u.hostname === location.hostname;

    // Named buttons / links whose target is filled in by script (e.g. Daily Roast)
    if ((el.id && /btn|shop|preview|cta|join|signup/i.test(el.id)) || /(^|\s)(signup|cal-link)(\s|$)/.test(el.className || '')) {
      data.id = el.id || (/cal-link/.test(el.className) ? 'cal-link' : 'signup');
      return track('cta-' + data.id, data);
    }
    if (sameSite && u.hash && u.pathname === location.pathname) return; // in-page scroll

    if (host.indexOf('skool.com') !== -1) { data.url = u.pathname; return track('cta-skool', data); }
    if (host.indexOf('calendly.com') !== -1) return track('cta-book-call', data);
    if (host === 'docs.google.com' && u.pathname.indexOf('/forms/') !== -1) {
      data.room = u.searchParams.get('entry.1753222212') || '';
      return track('cta-register-form', data);
    }
    if (host.indexOf('stripe.com') !== -1) return track('cta-checkout', data);
    if (host.indexOf('etsy.com') !== -1) { data.url = u.pathname; return track('cta-etsy', data); }
    if (/(^|\/)register[^\/]*\.html$/.test(u.pathname)) { data.target = u.pathname; return track('cta-register', data); }
    if (/(^|\/)join(\.html)?$/.test(u.pathname)) { data.target = u.pathname; return track('cta-join', data); }
    if (!sameSite && u.protocol.indexOf('http') === 0) { data.domain = host; return track('outbound-click', data); }
  }, true);

  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM') return;
    track('form-submit', { page: page, form: f.id || f.getAttribute('data-path') || f.className || 'form' });
  }, true);
})();
