---
---
(function () {
  var PAGE_SIZE = 5; // tweak anytime

  var btns = Array.from(document.querySelectorAll('.tag-btn'));
  var grid = document.getElementById('post-grid');
  var pagerTop = document.getElementById('pagination');
  var pagerBottom = document.getElementById('pagination-bottom');

  if (!grid || !pagerTop || !pagerBottom || !btns.length) return;

  var state = { tag: 'all', page: 1 };
  var posts = [];

  function norm(s){ return (s||'').trim().toLowerCase(); }

  function setActive(btn) {
    btns.forEach(b => b.classList.remove('is-active'));
    btn.classList.add('is-active');
  }

  function filterPosts(tag) {
    if (tag === 'all') return posts;
    var t = norm(tag);
    return posts.filter(p => (p.tags || []).map(norm).includes(t));
  }

  function paginate(arr, page, size) {
    var totalPages = Math.max(1, Math.ceil(arr.length / size));
    var current = Math.min(Math.max(1, page), totalPages);
    var start = (current - 1) * size;
    return {
      totalPages: totalPages,
      current: current,
      items: arr.slice(start, start + size)
    };
  }

  function renderCards(items) {
    grid.innerHTML = items.map(p => `
      <article class="post-card" data-tags="${(p.tags||[]).join(',')}">
        <a class="post-card__link" href="${p.url}">
          <div class="post-card__media">
            ${p.image ? `<img class="post-card__thumb" src="${p.image}" alt="">`
                       : `<div class="post-card__thumb placeholder" aria-hidden="true"></div>`}
          </div>
          <div class="post-card__body">
            <h2 class="post-card__title">${p.title}</h2>
            <p class="post-card__meta">
              <time datetime="${p.date}">${p.display_date}</time>
            </p>
            ${(p.tags && p.tags.length)
              ? `<ul class="post-card__tags">${p.tags.map(t=>`<li class="tag">${t}</li>`).join('')}</ul>`
              : ''
            }
          </div>
        </a>
      </article>
    `).join('');
  }

  function renderPager(container, totalPages, current, onClick) {
    var html = '';
    for (var i = 1; i <= totalPages; i++) {
      if (i === current) {
        html += `<span class="page current" aria-current="page">${i}</span>`;
      } else {
        html += `<button class="page" type="button" data-page="${i}">${i}</button>`;
      }
    }
    container.innerHTML = html;
    container.querySelectorAll('button[data-page]').forEach(btn => {
      btn.addEventListener('click', () => onClick(parseInt(btn.dataset.page,10)));
    });
  }

  function render() {
    var filtered = filterPosts(state.tag);
    var paged = paginate(filtered, state.page, PAGE_SIZE);

    // if filtering shrank results, keep page in range
    if (paged.current !== state.page) state.page = paged.current;

    renderCards(paged.items);
    renderPager(pagerTop, paged.totalPages, paged.current, goToPage);
    renderPager(pagerBottom, paged.totalPages, paged.current, goToPage);
  }

  function goToPage(p) {
    state.page = p;
    render();
    grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
    updateHash();
  }

  function chooseTag(tag) {
    state.tag = tag;
    state.page = 1;
    render();
    updateHash();
  }

  function updateHash() {
    if (history && history.replaceState) {
      var parts = [];
      if (state.tag && state.tag !== 'all') parts.push('t=' + encodeURIComponent(state.tag));
      if (state.page && state.page !== 1) parts.push('p=' + state.page);
      var hash = parts.length ? '#' + parts.join('&') : '#';
      history.replaceState(null, '', hash);
    }
  }

  function initFromHash() {
    var mTag = (location.hash||'').match(/(?:^#|&)t=([^&]+)/i);
    var mPage = (location.hash||'').match(/(?:^#|&)p=(\d+)/i);
    var tag = mTag ? norm(decodeURIComponent(mTag[1])) : 'all';
    var page = mPage ? parseInt(mPage[1],10) : 1;

    // sync UI button
    var btn = btns.find(b => norm(b.getAttribute('data-tag')) === tag);
    if (btn) setActive(btn);

    state = { tag: tag, page: page };
  }

  // Wire tag buttons
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      setActive(btn);
      chooseTag(norm(btn.getAttribute('data-tag')));
    });
  });

  // Load posts and start
  fetch('{{ "/assets/posts.json" | relative_url }}', { credentials: 'same-origin' })
    .then(r => r.json())
    .then(json => {
      posts = json;              // already newest-first from the Liquid we wrote
      initFromHash();
      render();
    })
    .catch(err => {
      console.error('Failed to load posts.json', err);
      grid.innerHTML = '<p>Unable to load posts.</p>';
    });
})();

