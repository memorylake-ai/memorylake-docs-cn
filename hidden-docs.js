// Hidden API docs: click the "API reference" tab in the top bar 5 times within 3 seconds to show
// or hide every sidebar group tagged "Preview" / "预览". hidden-docs.css does the hiding; this
// script only flips an attribute on <html> and remembers the choice. Desktop only: on narrow
// screens the tabs collapse into a menu with no stable hook. Conventions: CLAUDE.md "Hidden API docs".
(function () {
  var REQUIRED_CLICKS = 5;
  var WINDOW_MS = 3000;
  var STORAGE_KEY = 'memorylake-docs:show-hidden';
  var ATTR = 'data-show-hidden-docs';
  // The tab links to the first page of the API reference tab, in either language.
  var TRIGGER = 'a.nav-tabs-item[href*="/api-reference/"]';
  var shown = false;
  var clicks = [];

  // localStorage can throw (private windows, blocked storage); the toggle still works for the visit.
  try { shown = localStorage.getItem(STORAGE_KEY) === '1'; } catch (e) {}

  function apply() {
    if (shown) document.documentElement.setAttribute(ATTR, '');
    else document.documentElement.removeAttribute(ATTR);
  }

  apply();
  window.addEventListener('mintlify:navigate', apply);

  document.addEventListener('click', function (event) {
    if (!event.target.closest || !event.target.closest(TRIGGER)) return;
    var now = Date.now();
    clicks = clicks.filter(function (t) { return now - t < WINDOW_MS; });
    clicks.push(now);
    if (clicks.length < REQUIRED_CLICKS) return;
    clicks = [];
    shown = !shown;
    try {
      if (shown) localStorage.setItem(STORAGE_KEY, '1');
      else localStorage.removeItem(STORAGE_KEY);
    } catch (e) {}
    apply();
  });
})();
