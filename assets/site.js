// Language switch shared by every page. Blocks marked data-lang-block="en|pt"
// are shown one language at a time; without JavaScript both stay visible.
// Choice order: #en / #pt in the URL, then the last choice, then the browser.
(function () {
  var langs = ["en", "pt"];
  function stored() {
    try { return localStorage.getItem("lang"); } catch (e) { return null; }
  }
  function remember(lang) {
    try { localStorage.setItem("lang", lang); } catch (e) {}
  }
  function initial() {
    var h = location.hash.slice(1);
    if (langs.indexOf(h) >= 0) { remember(h); return h; }
    var s = stored();
    if (langs.indexOf(s) >= 0) return s;
    return (navigator.language || "").toLowerCase().indexOf("pt") === 0 ? "pt" : "en";
  }
  function show(lang) {
    document.querySelectorAll("[data-lang-block]").forEach(function (el) {
      el.hidden = el.getAttribute("data-lang-block") !== lang;
    });
    document.querySelectorAll("[data-set-lang]").forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-set-lang") === lang ? "true" : "false");
    });
    document.documentElement.lang = lang === "pt" ? "pt-BR" : "en";
  }
  document.querySelectorAll("[data-set-lang]").forEach(function (b) {
    b.addEventListener("click", function () {
      var lang = b.getAttribute("data-set-lang");
      remember(lang);
      show(lang);
      if (langs.indexOf(location.hash.slice(1)) >= 0) history.replaceState(null, "", "#" + lang);
    });
  });
  window.addEventListener("hashchange", function () {
    var h = location.hash.slice(1);
    if (langs.indexOf(h) >= 0) { remember(h); show(h); window.scrollTo(0, 0); }
  });
  show(initial());
  // A #en / #pt link would otherwise land below the header.
  if (langs.indexOf(location.hash.slice(1)) >= 0) {
    window.addEventListener("load", function () { window.scrollTo(0, 0); });
  }
})();
