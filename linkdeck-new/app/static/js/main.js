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

  // DOM elements
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

  // Weight function for shuffle
  function w(x) {
    var fresh = 1 + Math.max(0, 1 - (now - x.at) / (14 * D));
    var rate = (x.up + 2) / (x.up + x.dn + 4);
    return (MULT[x.p] || 1) * fresh * (0.4 + rate) * (seen[x.id] ? 0.3 : 1);
  }

  // Deal cards
  function deal(n) {
    var pool = codes.filter(function(x) {
      return (cat === 'All' || x.k === cat) &&
             (!query || (x.b + ' ' + x.o).toLowerCase().indexOf(query) > -1);
    });

    if (mode === 'top' || mode === 'new') {
      pool.sort(function(a, b) {
        return mode === 'top' ? b.up - a.up : b.at - a.at;
      });
      var out = pool.slice(0, n);
      out.forEach(function(x) { seen[x.id] = 1; });
      return out;
    }

    // Weighted shuffle with pinned items
    var out = n > 1 ? pool.filter(function(x) { return x.pin; }).slice(0, 1) : [];
    out.forEach(function(x) {
      pool.splice(pool.indexOf(x), 1);
      seen[x.id] = 1;
    });

    while (out.length < n && pool.length) {
      var tot = pool.reduce(function(a, x) { return a + w(x); }, 0);
      var r = Math.random() * tot;
      var i = 0;
      for (; i < pool.length - 1; i++) {
        r -= w(pool[i]);
        if (r <= 0) break;
      }
      out.push(pool.splice(i, 1)[0]);
    }
    out.forEach(function(x) { seen[x.id] = 1; });
    return out;
  }

  // Format time ago
  function ago(t) {
    var h = Math.round((now - t) / 3600000);
    return h < 1 ? 'just now' : h < 24 ? h + 'h ago' : Math.round(h / 24) + 'd ago';
  }

  // Render a card
  function card(x, i) {
    var c = el('article', 'tk' + ((x.p !== 'free' && x.p !== 'plus') ? ' boost' : ''));
    c.style.animationDelay = (i * 70) + 'ms';

    var top = el('div', 'top');
    var r = el('div', 'row');
    r.appendChild(el('span', 'brand', x.b));

    if (x.pin) r.appendChild(el('span', 'tag', '👑 Top referrer'));
    if (x.p === 'boost' || x.p === 'pro') r.appendChild(el('span', 'tag', 'Boosted'));

    top.appendChild(r);
    top.appendChild(el('p', 'offer', x.o));

    var af = el('p', 'hint', 'Affiliate link. The poster may earn a commission.');
    af.style.marginTop = '6px';
    top.appendChild(af);
    c.appendChild(top);

    var st = el('div', 'stub');
    st.appendChild(el('span', 'code', x.c));

    var a = el('div', 'acts');
    var b = el('a', 'btn cp', 'Get the deal →');
    b.href = x.l;
    b.target = '_blank';
    b.rel = 'noopener noreferrer sponsored';
    b.dataset.offerId = x.id;
    a.appendChild(b);

    var sh = el('button', 'btn alt', 'Share');
    sh.type = 'button';
    sh.setAttribute('aria-label', 'Share ' + x.b + ' link');
    sh.onclick = function() { share(x.b + ': ' + x.o + '.', siteUrl()); };
    a.appendChild(sh);

    st.appendChild(a);

    var v = el('div', 'vote');
    var u = el('button', '', '👍 Worked ' + x.up);
    var d = el('button', '', '👎 Didn\'t work ' + x.dn);
    u.type = d.type = 'button';

    var voted = false;
    u.onclick = function() {
      if (voted) return;
      voted = true;
      x.up++;
      u.textContent = '👍 Worked ' + x.up;
    };
    d.onclick = function() {
      if (voted) return;
      voted = true;
      x.dn++;
      d.textContent = '👎 Didn\'t work ' + x.dn;
      toast('Thanks. Low-rated codes show up less.');
    };
    v.appendChild(u);
    v.appendChild(d);
    v.appendChild(el('span', 'age', ago(x.at)));
    st.appendChild(v);
    c.appendChild(st);
    return c;
  }

  // Render all visible cards
  function render() {
    var g = $('#grid');
    if (!g) return;
    g.textContent = '';
    var hand = deal(mode === 'one' ? 1 : 6);

    if (!hand.length) {
      var empty = el('div', 'empty', 'No links match yet. Be the first to add one below.');
      g.appendChild(empty);
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
    var fc = $('#fc');
    if (!ch || !fc) return;

    ['All'].concat(CATS).forEach(function(k) {
      var b = el('button', 'chip', k);
      b.type = 'button';
      b.setAttribute('aria-pressed', k === 'All');
      b.onclick = function() {
        cat = k;
        $$('#chips .chip').forEach(function(c) {
          c.setAttribute('aria-pressed', c === b);
        });
        seen = {};
        render();
      };
      ch.appendChild(b);

      if (k !== 'All') {
        var o = el('option', '', k);
        o.value = k;
        fc.appendChild(o);
      }
    });
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
        seen = {};
        render();
      };
    });
  }

  // Search
  function initSearch() {
    var q = $('#q');
    if (!q) return;
    q.oninput = function() {
      query = this.value.trim().toLowerCase();
      seen = {};
      render();
    };
  }

  // Shuffle button
  function initShuffle() {
    var shuf = $('#shuf');
    if (!shuf) return;
    shuf.onclick = function() {
      mode = 'shuffle';
      seen = {};
      $$('#modes .chip').forEach(function(c) {
        c.setAttribute('aria-pressed', 'false');
      });
      render();
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

  // Odds calculator
  function initOdds() {
    var fp = $('#fp');
    if (!fp) return;
    function calc() {
      var p = fp.value;
      var me = (MULT[p] || 1) * 1.5;
      var tot = codes.reduce(function(a, x) { return a + (MULT[x.p] || 1) * 1.5; }, 0) + me;
      var pc = me / tot * 100;
      var ob = $('#ob');
      var ot = $('#ot');
      if (ob) ob.style.width = Math.min(100, pc * 4) + '%';
      if (ot) ot.textContent = 'Your link gets about ' + (pc).toFixed(1) + '% of all deals (' + (MULT[p] || 1) + '× weight vs. ' + codes.length + ' links in the deck).';
    }
    fp.onchange = calc;
    calc();
  }

  // Form submit
  function initForm() {
    var f = $('#f');
    if (!f) return;
    f.onsubmit = function(ev) {
      ev.preventDefault();
      var v = function(id) { return document.getElementById(id).value.trim(); };
      var er = $('#er');

      if (!v('fb') || !v('fk') || !v('fo')) {
        er.textContent = 'Add a brand, your link, and what it offers.';
        return;
      }
      var link = v('fk');
      if (link && !/^https?:\/\//i.test(link)) {
        er.textContent = 'Start the link with http:// or https://';
        return;
      }
      if (codes.some(function(x) { return x.l.toLowerCase() === link.toLowerCase(); })) {
        er.textContent = 'That link is already in the deck.';
        return;
      }
      er.textContent = '';

      var n = {
        b: v('fb'),
        c: host(link),
        o: v('fo'),
        k: v('fc'),
        p: v('fp'),
        l: link,
        at: Date.now(),
        up: 0,
        dn: 0,
        id: codes.length
      };
      codes.push(n);

      // Persist to localStorage for demo
      try {
        var m = JSON.parse(localStorage.getItem('ld_mine') || '[]');
        m.push(n);
        localStorage.setItem('ld_mine', JSON.stringify(m));
      } catch (e) {}

      f.reset();
      initOdds();
      seen = {};
      cat = 'All';
      $$('#chips .chip').forEach(function(c, i) { c.setAttribute('aria-pressed', i === 0); });
      render();

      toast('Added. Your link is now in the deck.');
      var ok = $('#ok');
      var okt = $('#okt');
      if (ok && okt) {
        okt.textContent = 'You\'re in the deck. ' + ($('#ot')?.textContent || '').replace(/^Your code gets/, 'Your code gets').split(' (')[0] + '.';
        ok.hidden = false;
      }
    };
  }

  // Utilities
  function host(u) {
    try { return new URL(u).hostname.replace(/^www\./, ''); }
    catch (e) { return u; }
  }

  function siteUrl() {
    return location.href.split('#')[0];
  }

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

  // Initialize everything on DOM ready
  function init() {
    // Load seed data (from LinkDeck.html)
    var seed = [
      {b:'DoorDash',c:'doordash.com',o:'$25 off your first order',k:'Food',p:'pro',u:41,d:3,l:'https://doordash.com/',t:2},
      {b:'Uber Eats',c:'ubereats.com',o:'$20 off, orders over $25',k:'Food',p:'free',u:18,d:5,l:'https://ubereats.com/',t:6},
      {b:'Chime',c:'chime.com',o:'$100 when direct deposit hits',k:'Banking',p:'plus',u:33,d:7,l:'https://chime.com/',t:10},
      {b:'SoFi',c:'sofi.com',o:'Up to $300 sign-up bonus',k:'Banking',p:'free',u:12,d:6,l:'https://sofi.com/',t:25},
      {b:'Airbnb',c:'airbnb.com',o:'$40 off your first stay',k:'Travel',p:'boost',u:27,d:4,l:'https://airbnb.com/',t:1},
      {b:'Lyft',c:'lyft.com',o:'15% off your first 3 rides',k:'Travel',p:'free',u:9,d:3,l:'https://lyft.com/',t:40},
      {b:'Mint Mobile',c:'mintmobile.com',o:'First month on us',k:'Phone',p:'plus',u:22,d:5,l:'https://mintmobile.com/',t:14},
      {b:'Visible',c:'visible.com',o:'$20 off your first bill',k:'Phone',p:'free',u:7,d:3,l:'https://visible.com/',t:60},
      {b:'Coinbase',c:'coinbase.com',o:'$10 in crypto after first trade',k:'Crypto',p:'free',u:14,d:6,l:'https://coinbase.com/',t:30},
      {b:'Robinhood',c:'robinhood.com',o:'One free stock on signup',k:'Crypto',p:'plus',u:30,d:4,l:'https://robinhood.com/',t:9},
      {b:'Duolingo',c:'duolingo.com',o:'2 weeks of Super free',k:'Apps',p:'free',u:11,d:2,l:'https://duolingo.com/',t:50},
      {b:'Dropbox',c:'dropbox.com',o:'+500 MB storage for both of us',k:'Apps',p:'free',u:6,d:8,l:'https://dropbox.com/',t:70},
      {b:'Allbirds',c:'allbirds.com',o:'$25 off $100+',k:'Shopping',p:'pro',u:25,d:5,l:'https://allbirds.com/',t:3}
    ].map(function(x, i) {
      x.id = i;
      x.at = now - x.t * 3600000;
      x.up = x.u;
      x.dn = x.d;
      return x;
    });

    // Load user submissions from localStorage
    try {
      var saved = JSON.parse(localStorage.getItem('ld_mine') || '[]');
      saved.forEach(function(x) {
        x.id = codes.length;
        codes.push(x);
      });
    } catch (e) {}

    codes = seed.concat(codes);

    initChips();
    initModes();
    initSearch();
    initShuffle();
    initBuy();
    initOdds();
    initForm();

    // Share button
    var shs = $('#shs');
    if (shs) shs.onclick = function() { share('Affiliate and referral links, shuffled fairly.', siteUrl()); };

    // Invite button
    var inv = $('#inv');
    if (inv) {
      var ME = 'guest';
      try {
        ME = localStorage.getItem('ld_id') || Math.random().toString(36).slice(2, 8);
        localStorage.setItem('ld_id', ME);
        var rm = location.hash.match(/^#r-([\w-]{1,12})/);
        if (rm) localStorage.setItem('ld_ref', rm[1]);
      } catch (e) {}
      inv.onclick = function() { share('Join me on LinkDeck for affiliate and referral links.', siteUrl() + '#r-' + ME); };
    }

    // Sticky CTA hide on submit section
    try {
      var sb = $('#stick');
      var sub = document.getElementById('submit');
      if (sb && sub && 'IntersectionObserver' in window) {
        new IntersectionObserver(function(e) {
          sb.classList.toggle('off', e[0].isIntersecting);
        }, { threshold: .15 }).observe(sub);
      }
    } catch (e) {}

    // Sample leaderboard
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

    // Initial render
    render();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();