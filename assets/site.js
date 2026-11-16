// Language switch shared by every page. Blocks marked data-lang-block="en|pt"
// are shown one language at a time; without JavaScript both stay visible.
// Choice order: #en / #pt in the URL, then the last choice, then where the
// visitor is, read from the device's time zone (no request, nothing leaves
// the browser), then the browser language if the time zone is unavailable.
(function () {
  var langs = ["en", "pt"];
  // Time zones of the Portuguese-speaking countries: Brazil, Portugal,
  // Angola, Mozambique, Cape Verde, Guinea-Bissau, São Tomé and East Timor.
  var ptZones = [
    "America/Sao_Paulo", "America/Araguaina", "America/Bahia", "America/Belem",
    "America/Boa_Vista", "America/Campo_Grande", "America/Cuiaba", "America/Eirunepe",
    "America/Fortaleza", "America/Maceio", "America/Manaus", "America/Noronha",
    "America/Porto_Velho", "America/Recife", "America/Rio_Branco", "America/Santarem",
    "America/Porto_Acre", "Brazil/East", "Brazil/West", "Brazil/Acre", "Brazil/DeNoronha",
    "Europe/Lisbon", "Portugal", "Atlantic/Azores", "Atlantic/Madeira",
    "Africa/Luanda", "Africa/Maputo", "Atlantic/Cape_Verde", "Africa/Bissau",
    "Africa/Sao_Tome", "Asia/Dili"
  ];
  function fromTimeZone() {
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      if (!tz) return null;
      return ptZones.indexOf(tz) >= 0 ? "pt" : "en";
    } catch (e) { return null; }
  }
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
    var z = fromTimeZone();
    if (z) return z;
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
