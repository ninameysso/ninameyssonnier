/* Fait apparaître les blocs de texte au fur et à mesure du défilement */
(function () {
  if (!("IntersectionObserver" in window)) return;
  document.documentElement.classList.add("js");

  var blocs = document.querySelectorAll(
    ".accroche, .tuiles a, .apropos-visuel > div, .poste, .parcours h3, .competences > div, " +
    ".encart .etroit, .fiche .conteneur > *, .article .conteneur > *, .contact"
  );

  var observateur = new IntersectionObserver(function (entrees) {
    entrees.forEach(function (entree) {
      if (entree.isIntersecting) {
        entree.target.classList.add("visible");
        observateur.unobserve(entree.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.1 });

  blocs.forEach(function (bloc) {
    bloc.classList.add("apparait");
    observateur.observe(bloc);
  });
})();
