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
