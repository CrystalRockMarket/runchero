// LinkDeck client-side logic
(function() {
  'use strict';

  // State
  var CATS = ['Food','Banking','Travel','Phone','Crypto','Apps','Shopping'];
  var MULT = {free:1, plus:3, pro:8, boost:10};
  var D = 86400000;
  var now = Date.now();
  var codes = [];
  var seen = {};
  var cat = 'All';
  var query = '';
  var mode = 'shuffle';

  // DOM helpers
  var $ = function(sel) { return document.querySelector(sel); };
  var $$ = function(sel) { return Array.from(document.querySelectorAll(sel)); };

  // Toast
  function toast(msg) {
    var t = $('#toast');
    if (t) {
      t.textContent = msg;
      t.className = 'on';
      clearTimeout(toast.h);
      toast.h = setTimeout(function() { t.className = ''; }, 2200);
    }
  }

  // DOM helpers
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  // Format time ago
  function ago(t) {
    var h = Math.round((now - t) / 3600000);
    return h < 1 ? 'just now' : h < 24 ? h + 'h ago' : Math.round(h / 24) + 'd ago';
  }

  // Fetch a fresh hand from the API
  function fetchHand() {
    var url = '/api/offers?mode=' + mode;
    if (cat !== 'All') url += '&category=' + encodeURIComponent(cat);
    if (query) url += '&query=' + encodeURIComponent(query);

    return fetch(url).then(function(r) { return r.json(); }).then(function(hand) {
      codes = hand;
      codes.forEach(function(x, i) { x.at = x.at || now; });
      return hand;
    });
  }

  // Render cards
  function card(x, i) {
    var c = el('article', 'tk' + ((x.plan !== 'free' && x.plan !== 'plus') ? ' boost' : ''));
    c.style.animationDelay = (i * 70) + 'ms';

    var top = el('div', 'top');
    var r = el('div', 'row');
    r.appendChild(el('span', 'brand', x.brand));
    if (x.pin) r.appendChild(el('span', 'tag', '👑 Top referrer'));
    if (x.is_boosted || x.plan === 'boost') r.appendChild(el('span', 'tag', 'Boosted'));
    top.appendChild(r);
    top.appendChild(el('p', 'offer', x.offer));
    var af = el('p', 'hint', 'Affiliate link. The poster may earn a commission.');
    af.style.marginTop = '6px';
    top.appendChild(af);
    c.appendChild(top);

    var st = el('div', 'stub');
    var codeText = x.code || x.promo || ('LD-' + x.id);
    var codeRow = el('div', 'code-row');
    var codeEl = el('span', 'code', codeText);
    codeEl.title = 'Click to copy';
    codeEl.style.cursor = 'pointer';
    var copyBtn = el('button', 'copybtn', 'Copy code');
    copyBtn.type = 'button';
    copyBtn.setAttribute('aria-label', 'Copy code ' + codeText + ' for ' + x.brand);
    codeEl.onclick = function() { copyCode(codeText, copyBtn); };
    copyBtn.onclick = function() { copyCode(codeText, copyBtn); };
    codeRow.appendChild(codeEl);
    codeRow.appendChild(copyBtn);
    st.appendChild(codeRow);

    var a = el('div', 'acts');
    var b = el('a', 'btn cp', 'Get the deal →');
    b.href = x.url;
    b.target = '_blank';
    b.rel = 'noopener noreferrer sponsored';
    b.dataset.offerId = x.id;
    b.addEventListener('click', function() {
      // Record the click without blocking navigation.
      try {
        var payload = JSON.stringify({ offer_id: x.id });
        if (navigator.sendBeacon) {
          navigator.sendBeacon('/api/click/' + x.id + '?beacon=1');
        } else {
          fetch('/api/click/' + x.id, { method: 'POST', keepalive: true }).catch(function() {});
        }
      } catch (e) {}
    });
    a.appendChild(b);

    var sh = el('button', 'btn alt', 'Share');
    sh.type = 'button';
    sh.setAttribute('aria-label', 'Share ' + x.brand + ' link');
    sh.onclick = function() { share(x.brand + ': ' + x.offer + '.', siteUrl()); };
    a.appendChild(sh);

    st.appendChild(a);

    var v = el('div', 'vote');
    var u = el('button', '', '👍 Worked ' + (x.upvotes || 0));
    var d = el('button', '', '👎 Didn\'t work ' + (x.downvotes || 0));
    u.type = d.type = 'button';

    var voted = false;
    u.onclick = function() {
      if (voted) return;
      voted = true;
      sendVote(x.id, true).then(function(res) {
        if (res) { x.upvotes = res.upvotes; x.downvotes = res.downvotes; }
        else { x.upvotes = (x.upvotes || 0) + 1; }
        u.textContent = '👍 Worked ' + x.upvotes;
        d.textContent = '👎 Didn\'t work ' + x.downvotes;
      });
      u.textContent = '👍 Worked ' + ((x.upvotes || 0) + 1);
    };
    d.onclick = function() {
      if (voted) return;
      voted = true;
      sendVote(x.id, false).then(function(res) {
        if (res) { x.upvotes = res.upvotes; x.downvotes = res.downvotes; }
        else { x.downvotes = (x.downvotes || 0) + 1; }
        u.textContent = '👍 Worked ' + x.upvotes;
        d.textContent = '👎 Didn\'t work ' + x.downvotes;
      });
      toast('Thanks. Low-rated codes show up less.');
    };
    v.appendChild(u);
    v.appendChild(d);
    v.appendChild(el('span', 'age', ago(x.at || now)));
    st.appendChild(v);
    c.appendChild(st);
    return c;
  }

  // Render the grid
  function render(hand) {
    var g = $('#grid');
    if (!g) return;
    g.textContent = '';
    if (!hand || !hand.length) {
      g.appendChild(el('div', 'empty', 'No links match yet. Be the first to add one below.'));
    } else {
      hand.forEach(function(x, i) { g.appendChild(card(x, i)); });
    }

    var meta = $('#meta');
    if (meta) {
      meta.textContent = ({
        shuffle: 'A new random hand every time.',
        top: 'Top deals: most "Worked" votes.',
        new: 'Newest links first.',
        one: 'One random pick. Tap again for another.'
      })[mode] + ' ' + codes.length + ' links in the deck.';
    }
  }

  // Category chips
  function initChips() {
    var ch = $('#chips');
    if (!ch) return;

    function setAll(active) {
      $$('#chips .chip').forEach(function(c) {
        c.setAttribute('aria-pressed', c === ch.querySelector('.chip[data-c="' + (active || 'All') + '"]') ? 'true' : 'false');
      });
    }

    var chipEls = [];
    ['All'].concat(CATS).forEach(function(k) {
      var b = el('button', 'chip', k);
      b.type = 'button';
      b.dataset.c = k;
      b.setAttribute('aria-pressed', k === 'All');
      b.onclick = function() {
        cat = k;
        setAll(k);
        // Re-fetch with category
        fetchHand().then(render);
      };
      ch.appendChild(b);
      chipEls.push(b);
    });

    // Populate category select from chips
    var fc = $('#fc');
    if (fc) {
      var allChips = chipEls;
      // Rebuild options
      fc.innerHTML = '';
      CATS.forEach(function(k) {
        var o = document.createElement('option');
        o.value = k;
        o.textContent = k;
        fc.appendChild(o);
      });
    }
  }

  // Mode chips
  function initModes() {
    var mb = $('#modes');
    if (!mb) return;
    $$('#modes .chip').forEach(function(b) {
      b.onclick = function() {
        mode = b.getAttribute('data-m');
        $$('#modes .chip').forEach(function(c) {
          c.setAttribute('aria-pressed', c === b);
        });
        fetchHand().then(render);
      };
    });
  }

  // Search
  function initSearch() {
    var q = $('#q');
    if (!q) return;
    q.addEventListener('input', function() {
      query = q.value.trim().toLowerCase();
      // Client-side filtering after fetch
      fetchHand().then(render);
    });
  }

  // Shuffle button
  function initShuffle() {
    var shuf = $('#shuf');
    if (!shuf) return;
    shuf.onclick = function() {
      mode = 'shuffle';
      $$('#modes .chip').forEach(function(c) {
        c.setAttribute('aria-pressed', 'false');
      });
      fetchHand().then(render);
    };
  }

  // Buy buttons (placeholder)
  function initBuy() {
    $$('[data-buy]').forEach(function(b) {
      b.onclick = function() {
        toast(b.getAttribute('data-buy') + ': checkout is not connected in this prototype.');
      };
    });
  }

  // Share
  function share(text, url) {
    try {
      if (navigator.share) {
        navigator.share({ title: 'LinkDeck', text: text, url: url }).catch(function() {});
        return;
      }
    } catch (e) {}
    try {
      navigator.clipboard.writeText(text + ' ' + url).then(
        function() { toast('Copied. Paste it anywhere to share.'); },
        function() { toast('Could not copy the link'); }
      );
    } catch (e) {
      toast('Sharing is not available here');
    }
  }

  function siteUrl() { return location.href.split('#')[0]; }

  function copyCode(text, btn) {
    var label = btn.getAttribute('data-label') || btn.textContent;
    btn.setAttribute('data-label', label);
    var done = function() {
      btn.textContent = 'Copied ✓';
      btn.classList.add('done');
      setTimeout(function() {
        btn.textContent = label;
        btn.classList.remove('done');
      }, 1600);
    };
    var fallback = function() {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'absolute';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); }
      catch (e) { toast('Select the code and copy it by hand'); }
      ta.remove();
    };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else {
        fallback();
      }
    } catch (e) { fallback(); }
  }

  function voterKey() {
    var k = 'ld_voter';
    try {
      var existing = localStorage.getItem(k);
      if (existing) return existing;
      var rnd = 'v_' + Math.random().toString(36).slice(2) + Date.now().toString(36);
      localStorage.setItem(k, rnd);
      return rnd;
    } catch (e) { return 'anon'; }
  }

  function sendVote(id, isUp) {
    var url = '/api/vote/' + id + '?is_up=' + (isUp ? 'true' : 'false') +
      '&voter_key=' + encodeURIComponent(voterKey());
    return fetch(url, { method: 'POST' })
      .then(function(r) { return r.ok ? r.json() : null; })
      .catch(function() { return null; });
  }

  // Init
  function init() {
    fetchHand().then(function(hand) {
      codes = hand;
      render(hand);
    }).catch(function(e) {
      toast('Could not load the deck.');
    });

    initChips();
    initModes();
    initSearch();
    initShuffle();
    initBuy();

    var shs = $('#shs');
    if (shs) shs.onclick = function() { share('Affiliate and referral links, shuffled fairly.', siteUrl()); };

    var inv = $('#inv');
    if (inv) {
      inv.onclick = function() { share('Join me on LinkDeck for affiliate and referral links.', siteUrl() + '#r-' + 'guest'); };
    }

    var sb = $('#stick');
    var sub = document.getElementById('submit');
    if (sb && sub && 'IntersectionObserver' in window) {
      new IntersectionObserver(function(e) { sb.classList.toggle('off', e[0].isIntersecting); }, { threshold: .15 }).observe(sub);
    }

    var b = $('#board');
    if (b) {
      [['@mike_k',62],['@saveswithsam',48],['@dealdana',31],['@refrefs',17],['You',0]].forEach(function(r) {
        var w = el('div', 'rw');
        w.appendChild(el('span', '', r[0]));
        var o = el('div', 'odds'), i = el('i');
        i.style.width = r[1] + '%';
        o.appendChild(i);
        w.appendChild(o);
        w.appendChild(el('span', '', r[1] + '/100'));
        b.appendChild(w);
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
