/* Page « Mes cartes » : carrousels et hauteur des cartes Datawrapper */
(function () {
  /* ---------- Carrousels ---------- */
  document.querySelectorAll(".carrousel").forEach(function (carrousel) {
    var piste = carrousel.querySelector(".carrousel-piste");
    var prec = carrousel.querySelector(".prec");
    var suiv = carrousel.querySelector(".suiv");
    var compte = carrousel.querySelector(".carrousel-compte");

    function diapos() {
      return Array.prototype.filter.call(piste.children, function (f) {
        return !f.classList.contains("manquante");
      });
    }
    function indexCourant() {
      return Math.round(piste.scrollLeft / piste.clientWidth);
    }
    function maj() {
      var n = diapos().length, i = Math.min(indexCourant(), n - 1);
      compte.textContent = (i + 1) + " / " + n;
      prec.disabled = i <= 0;
      suiv.disabled = i >= n - 1;
      carrousel.classList.toggle("seule", n <= 1);
    }
    function aller(i) {
      piste.scrollTo({ left: i * piste.clientWidth, behavior: "smooth" });
    }

    prec.addEventListener("click", function () { aller(indexCourant() - 1); });
    suiv.addEventListener("click", function () { aller(indexCourant() + 1); });
    piste.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { e.preventDefault(); aller(indexCourant() - 1); }
      if (e.key === "ArrowRight") { e.preventDefault(); aller(indexCourant() + 1); }
    });
    var attente;
    piste.addEventListener("scroll", function () {
      clearTimeout(attente);
      attente = setTimeout(maj, 80);
    });
    window.addEventListener("resize", maj);
    /* Une image manquante disparaît : on recompte */
    piste.querySelectorAll("img").forEach(function (img) {
      img.addEventListener("error", function () { setTimeout(maj, 0); });
    });
    maj();
  });

  /* ---------- Plein écran au clic sur une carte ---------- */
  var langue = (document.documentElement.lang || "fr").slice(0, 2);
  var textes = {
    fr: { fermer: "Fermer", agrandir: "Afficher la carte en plein écran" },
    en: { fermer: "Close", agrandir: "View the map full screen" },
    it: { fermer: "Chiudi", agrandir: "Visualizza la mappa a schermo intero" }
  }[langue] || { fermer: "Fermer", agrandir: "Afficher la carte en plein écran" };

  var voile = document.createElement("div");
  voile.className = "plein-ecran";
  voile.setAttribute("role", "dialog");
  voile.setAttribute("aria-modal", "true");
  voile.hidden = true;
  voile.innerHTML = '<button type="button" class="plein-ecran-fermer">×</button><img alt="">';
  var boutonFermer = voile.querySelector("button");
  var grande = voile.querySelector("img");
  boutonFermer.setAttribute("aria-label", textes.fermer);
  document.body.appendChild(voile);
  var declencheur = null;

  function ouvrir(img) {
    declencheur = img;
    grande.src = img.currentSrc || img.src;
    grande.alt = img.alt;
    voile.setAttribute("aria-label", img.alt);
    voile.hidden = false;
    document.documentElement.classList.add("sans-defilement");
    boutonFermer.focus();
  }
  function fermer() {
    voile.hidden = true;
    grande.removeAttribute("src");
    document.documentElement.classList.remove("sans-defilement");
    if (declencheur) declencheur.focus();
  }
  voile.addEventListener("click", fermer);
  document.addEventListener("keydown", function (e) {
    if (!voile.hidden && (e.key === "Escape" || e.key === "Tab")) { e.preventDefault(); if (e.key === "Escape") fermer(); }
  });

  document.querySelectorAll(".fiche.carte figure.cadre img").forEach(function (img) {
    img.tabIndex = 0;
    img.setAttribute("role", "button");
    img.setAttribute("aria-label", textes.agrandir + " : " + img.alt);
    img.addEventListener("click", function () { ouvrir(img); });
    img.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); ouvrir(img); }
    });
  });

  /* ---------- Cartes Datawrapper : hauteur automatique ---------- */
  window.addEventListener("message", function (e) {
    var hauteurs = e.data && e.data["datawrapper-height"];
    if (!hauteurs) return;
    document.querySelectorAll("iframe").forEach(function (iframe) {
      if (iframe.contentWindow !== e.source) return;
      for (var id in hauteurs) iframe.style.height = hauteurs[id] + "px";
    });
  });
})();
