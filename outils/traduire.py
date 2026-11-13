#!/usr/bin/env python3
"""Génère en/ et it/ à partir des pages françaises (à lancer depuis la racine du site)."""
import os, re, sys

PAGES = ["index.html", "cartes.html", "articles.html", "projets.html"]
SITE = "https://ninameyssonnier.com/"

CV_PDF = {
    "fr": "cv/CV-Nina-Meyssonnier-FR.pdf",
    "en": "../cv/CV-Nina-Meyssonnier-EN.pdf",
    "it": "../cv/CV-Nina-Meyssonnier-IT.pdf",
}

# ---------------------------------------------------------------- CV
CV = {
"en": dict(
  exp="Experience", edu="Education", soft="Software skills", lang="Languages",
  postes=[
    ("Assistant Ambassador for the Language Assistant Exchange Programme run by France Éducation internationale", "September 2026 - ongoing - Veneto, Italy", ["Programme promotion and communication."]),
    ("Language assistant in Italy", "September 2026 - ongoing - Veneto, Italy", ["French lessons at an Italian vocational secondary school."]),
    ("Cartographer and infographic journalist", "September 2025 - September 2026 - Rennes, France", ["Writing articles for print and online newspapers.", "Creating maps and infographics for other journalists."]),
    ("Treasurer of the Géodote association", "September 2024 - September 2026 - Paris, France", ["Management of the association’s bank accounts.", "Organisation of a cartography competition.", "Organisation of conferences on sensitive cartography.", "Launch of the Géopodcast, a podcast dedicated to geopolitics."]),
    ("Private tutor at Complétude", "September 2024 - September 2026 - Paris, France", ["Private tuition from primary school to A-level in French, history and geography, geopolitics and philosophy."]),
    ("Geopolitical risk analyst for AXA International", "September 2025 - February 2026 - Paris, France", ["Thesis: “Geopolitical triggers of hybrid threats to AXA’s operations: mapping cyber-physical risks”.", "Written and defended entirely in English."]),
  ],
  formations=[
    ("Master’s degree in Geopolitics at the French Institute of Geopolitics", "September 2024 - September 2026", ["Awarded a <strong>Master’s 2</strong> degree through a work-study programme with first-class honours (19/20).", "Awarded a <strong>Master’s 1</strong> degree with first-class honours (16/20), following the completion of a research dissertation on the return of the Chagos Archipelago."]),
    ("Bachelor’s degree in geography after 3 years of preparatory classes in literature", "September 2021 - July 2024 - Lyon, France", ["Attended the A/L preparatory classes (hypokhâgne, khâgne, khûbe), specialising in history and geography.", "Achieved the minimum entry requirements for the École normale supérieure de Lyon.", "Represented pupils as class representative."]),
  ],
  logiciels=["Adobe Illustrator", "Datawrapper", "Flourish", "QGIS", "Office suite"],
  langues=["English - professional skills", "French - native language", "Italian - professional skills"],
),
"it": dict(
  exp="Esperienze", edu="Istruzione", soft="Software padroneggiati", lang="Lingue",
  postes=[
    ("Assistente ambasciatrice del programma di scambio di assistenti linguistici di France Éducation internationale", "Settembre 2026 - in corso - Veneto, Italia", ["Promozione del programma e comunicazione."]),
    ("Assistente di lingua francese in Italia", "Settembre 2026 - in corso - Veneto, Italia", ["Corsi di francese presso un istituto professionale statale italiano."]),
    ("Giornalista cartografa-infografica", "Settembre 2025 - settembre 2026 - Rennes, Francia", ["Redazione di articoli per il giornale cartaceo e online.", "Creazione di mappe e infografiche per altri giornalisti."]),
    ("Tesoriera dell’associazione Géodote", "Settembre 2024 - settembre 2026 - Parigi, Francia", ["Gestione dei conti bancari dell’associazione.", "Organizzazione di un concorso di cartografia.", "Organizzazione di conferenze sulla cartografia sensibile.", "Lancio del Géopodcast, un podcast dedicato alla geopolitica."]),
    ("Insegnante privata presso Complétude", "Settembre 2024 - settembre 2026 - Parigi, Francia", ["Lezioni private dalla scuola primaria alla maturità in francese, storia e geografia, geopolitica e filosofia."]),
    ("Analista dei rischi geopolitici per AXA International", "Settembre 2025 - febbraio 2026 - Parigi, Francia", ["Studio intitolato «Fattori geopolitici all’origine delle minacce ibride alle attività di AXA: mappatura dei rischi cyber-fisici».", "Redazione e discussione interamente in inglese."]),
  ],
  formations=[
    ("Master in Geopolitica presso l’Istituto Francese di Geopolitica", "Settembre 2024 - settembre 2026", ["Conseguimento del <strong>Master 2</strong> in alternanza scuola-lavoro con lode (19/20).", "Conseguimento del <strong>Master 1</strong> con lode (16/20), dopo aver redatto una tesi di ricerca sulla restituzione dell’arcipelago delle Chagos."]),
    ("Laurea in geografia dopo 3 anni di corsi preparatori per le Grandes Écoles (indirizzo letterario)", "Settembre 2021 - luglio 2024 - Lione, Francia", ["Accompagnamento degli studenti dei corsi preparatori A/L (hypokhâgne, khâgne, khûbe), indirizzo storia-geografia.", "Ammissione condizionata all’École normale supérieure di Lione.", "Rappresentanza degli studenti in qualità di delegata di classe."]),
  ],
  logiciels=["Adobe Illustrator", "Datawrapper", "Flourish", "QGIS", "Pacchetto Office"],
  langues=["Inglese - competenze professionali", "Francese - madrelingua", "Italiano - competenze professionali"],
),
}

def bloc_cv(d):
    def poste(t, q, ps):
        return '<article class="poste"><h4>' + t + '</h4><p class="quand">' + q + '</p>' + "".join("<p>" + p + "</p>" for p in ps) + "</article>\n"
    h = '<div class="parcours">\n<h3 class="rubrique">' + d["exp"] + "</h3>\n"
    h += "".join(poste(*p) for p in d["postes"])
    h += '<h3 class="rubrique">' + d["edu"] + "</h3>\n"
    h += "".join(poste(*p) for p in d["formations"])
    h += '<div class="competences">\n'
    h += "<div><h3>" + d["soft"] + "</h3><ul>" + "".join("<li>" + x + "</li>" for x in d["logiciels"]) + "</ul></div>\n"
    h += "<div><h3>" + d["lang"] + "</h3><ul>" + "".join("<li>" + x + "</li>" for x in d["langues"]) + "</ul></div>\n"
    h += "</div>\n</div>\n"
    return h

# ---------------------------------------------------------------- textes (fr, en, it)
COMMUN = [
 ("Nina Meyssonnier, cartographe et analyste en géopolitique basée en Italie : cartes, articles et projets pour décrypter l’actualité internationale.",
  "Nina Meyssonnier, cartographer and geopolitical analyst based in Italy: maps, articles and projects to make sense of international current affairs.",
  "Nina Meyssonnier, cartografa e analista geopolitica con sede in Italia: mappe, articoli e progetti per interpretare l’attualità internazionale."),
 ("Aller au contenu", "Skip to content", "Vai al contenuto"),
 ('aria-label="Menu principal"', 'aria-label="Main menu"', 'aria-label="Menu principale"'),
 ('aria-label="Plan du site"', 'aria-label="Site map"', 'aria-label="Mappa del sito"'),
 (">Présentation<", ">Presentation<", ">Presentazione<"),
 ("<h2>Contact</h2>", "<h2>Contact</h2>", "<h2>Contatti</h2>"),
 ("© 2026 Nina Meyssonnier — Tous droits réservés sur les cartes et les textes.",
  "© 2026 Nina Meyssonnier — All rights reserved on maps and texts.",
  "© 2026 Nina Meyssonnier — Tutti i diritti riservati su mappe e testi."),
 ("Projets transversaux", "Cross-cutting projects", "Progetti trasversali"),
 ("Mes cartes", "My maps", "Le mie mappe"),
 ("Mes articles", "My articles", "I miei articoli"),
 ("Lien vers l’article", "Link to the article", "Link all’articolo"),
 ("Pour en savoir plus", "Learn more", "Per saperne di più"),
]

INDEX = [
 ("Nina Meyssonnier — Cartographe et analyste en géopolitique",
  "Nina Meyssonnier — Cartographer and geopolitical analyst",
  "Nina Meyssonnier — Cartografa e analista geopolitica"),
 ('aria-label="Présentation"', 'aria-label="Introduction"', 'aria-label="Presentazione"'),
 ("Globe terrestre peint à l’aquarelle", "Watercolour globe", "Globo terrestre dipinto ad acquerello"),
 ("Basée en Italie, je suis cartographe et analyste en géopolitique : je conçois des cartes et des analyses pour décrypter l’actualité internationale et les risques géopolitiques.",
  "Based in Italy, I am a cartographer and geopolitical analyst: I produce maps and analyses to make sense of international current affairs and geopolitical risks.",
  "Con sede in Italia, sono cartografa e analista geopolitica: realizzo mappe e analisi per interpretare l’attualità internazionale e i rischi geopolitici."),
 ('aria-label="Rubriques"', 'aria-label="Sections"', 'aria-label="Sezioni"'),
 (">À propos<", ">About<", ">Chi sono<"),
 ("CV à télécharger", "CV to download", "CV da scaricare"),
]

CARTES = [
 ("Réalisations personnelles", "Personal work", "Progetti personali"),
 ("Cartes interactives", "Interactive maps", "Mappe interattive"),
 ("Cartographier, c’est faire des choix et proposer une lecture argumentée de l’espace. Mes cartes ne se contentent pas de représenter un territoire : elles en offrent une interprétation, fondée sur une analyse rigoureuse, pour rendre accessibles des enjeux complexes.",
  "Mapping involves making choices and offering a reasoned interpretation of space. My maps do more than simply depict a territory: they offer an interpretation of it, based on rigorous analysis, to make complex issues accessible.",
  "Mappare significa fare delle scelte e proporre una lettura argomentata dello spazio. Le mie mappe non si limitano a rappresentare un territorio: ne offrono un’interpretazione, basata su un’analisi rigorosa, per rendere accessibili tematiche complesse."),
 # carrousels
 ('aria-roledescription="carrousel"', 'aria-roledescription="carousel"', 'aria-roledescription="carosello"'),
 ('aria-label="Carte précédente"', 'aria-label="Previous map"', 'aria-label="Mappa precedente"'),
 ('aria-label="Carte suivante"', 'aria-label="Next map"', 'aria-label="Mappa successiva"'),
 ('aria-label="Cartes sur l’Asie du Sud-Est"', 'aria-label="Maps of Southeast Asia"', 'aria-label="Mappe sul Sud-est asiatico"'),
 ('aria-label="Cartes sur l’archipel des Chagos"', 'aria-label="Maps of the Chagos Archipelago"', 'aria-label="Mappe sull’arcipelago delle Chagos"'),
 ('aria-label="Carte de localisation"', 'aria-label="Location map"', 'aria-label="Mappa di localizzazione"'),
 # textes alternatifs
 ("Carte : l’eau au Moyen-Orient", "Map: water in the Middle East", "Mappa: l’acqua in Medio Oriente"),
 ("Carte : localisation de l’Asie du Sud-Est", "Map: location of Southeast Asia", "Mappa: localizzazione del Sud-est asiatico"),
 ("Carte : densité de population en Asie du Sud-Est", "Map: population density in Southeast Asia", "Mappa: densità di popolazione nel Sud-est asiatico"),
 ("Carte : les réseaux économiques de l’Asie du Sud-Est", "Map: Southeast Asia’s economic networks", "Mappa: le reti economiche del Sud-est asiatico"),
 ("Carte : la ligne de démarcation dans le Jura", "Map: the demarcation line in the Jura", "Mappa: la linea di demarcazione nel Giura"),
 ("Carte : Global hyperconnectivity", "Map: global hyperconnectivity", "Mappa: iperconnettività globale"),
 ("Carte : Milan olympics ice dancing", "Map: Milan Olympics ice dancing", "Mappa: la danza su ghiaccio alle Olimpiadi di Milano"),
 ("Carte : un parcours professionnel cartographié", "Map: a mapped-out career path", "Mappa: un percorso di carriera mappato"),
 ("Carte : l’élargissement de l’OTAN vers l’Est depuis 1949", "Map: NATO’s eastward expansion since 1949", "Mappa: l’allargamento della NATO verso Est dal 1949"),
 ("Carte : la rétrocession de l’archipel des Chagos à Maurice, révélatrice des rapports de force dans l’océan Indien",
  "Map: the return of the Chagos Archipelago to Mauritius, revealing the balance of power in the Indian Ocean",
  "Mappa: la restituzione dell’arcipelago delle Chagos a Mauritius, rivelatrice dei rapporti di forza nell’Oceano Indiano"),
 ("Carte : l’archipel des Chagos, une ressource géostratégique convoitée",
  "Map: the Chagos Archipelago, a coveted geostrategic resource",
  "Mappa: l’arcipelago delle Chagos, una risorsa geostrategica ambita"),
 ("Carte interactive : la peine de mort aux États-Unis", "Interactive map: the death penalty in the United States", "Mappa interattiva: la pena di morte negli Stati Uniti"),
 # Eau
 ("L’eau au Moyen-Orient : une vulnérabilité structurelle", "Water in the Middle East: a structural vulnerability", "L’acqua in Medio Oriente: una vulnerabilità strutturale"),
 ("Carte réalisée pour la revue annuelle du think tank Eurasiapeace.", "Map produced for the annual review of the Eurasiapeace think tank.", "Mappa realizzata per la rivista annuale del think tank Eurasiapeace."),
 ("Région parmi les plus arides du monde, le Moyen-Orient fait de l’eau une ressource à la fois vitale et stratégique. Le partage des grands bassins transfrontaliers (Tigre, Euphrate, Jourdain, Nil) oppose les États d’amont, qui maîtrisent le débit grâce à leurs barrages, aux États d’aval, qui en dépendent. Sous l’effet du changement climatique et de la pression démographique, ce stress hydrique devient un facteur de vulnérabilité et de rivalités, que cette carte s’attache à décrypter.",
  "As one of the world’s driest regions, the Middle East regards water as a resource that is both vital and strategic. The sharing of major transboundary river basins (the Tigris, Euphrates, Jordan and Nile) pits upstream states, which control the flow through their dams, against downstream states, which depend on it. Driven by climate change and demographic pressure, this water stress is becoming a factor in vulnerability and rivalries, which this map seeks to analyse.",
  "Essendo una delle regioni più aride del mondo, il Medio Oriente considera l’acqua una risorsa al tempo stesso vitale e strategica. La condivisione dei grandi bacini transfrontalieri (Tigri, Eufrate, Giordano, Nilo) oppone gli Stati a monte, che controllano la portata grazie alle loro dighe, agli Stati a valle, che ne dipendono. A causa dei cambiamenti climatici e della pressione demografica, questa carenza idrica diventa un fattore di vulnerabilità e di rivalità, che questa mappa si propone di analizzare."),
 # Asie du Sud-Est
 ("L’Asie du Sud-Est en trois cartes", "Southeast Asia in three maps", "Il Sud-est asiatico in tre mappe"),
 ("Série de trois cartes réalisées pour le magazine annuel de Classe Internationale, avec Aloïs Valade, dans le cadre du partenariat avec les associations étudiantes de l’Institut français de géopolitique (IFG) et du Magistère Relations internationales et action à l’étranger (MRIAE).",
  "A series of three maps created for the annual magazine of Classe Internationale, in collaboration with Aloïs Valade, as part of a partnership with the student associations of the French Institute of Geopolitics (IFG) and the Master’s Programme in International Relations and International Action (MRIAE).",
  "Serie di tre mappe realizzate per la rivista annuale di Classe Internationale, in collaborazione con Aloïs Valade, nell’ambito di una partnership con le associazioni studentesche dell’Institut français de géopolitique (IFG) e del Magistère Relations internationales et action à l’étranger (MRIAE)."),
 ("Ce travail accompagne un article consacré à l’Asie du Sud-Est. Les trois cartes localisent et représentent différentes données liées au sujet traité, afin d’en faciliter la compréhension et d’en illustrer les principaux enjeux. Complémentaires, elles permettent de mettre en perspective les informations développées dans l’article et d’en proposer une lecture cartographique.",
  "This work accompanies an article focusing on Southeast Asia. The three maps locate and represent different sets of data related to the topic, helping to make the subject easier to understand while illustrating its main issues. Designed to complement one another, they provide a cartographic perspective on the information developed in the article.",
  "Questo lavoro accompagna un articolo dedicato al Sud-est asiatico. Le tre mappe localizzano e rappresentano diversi dati legati al tema trattato, contribuendo a facilitarne la comprensione e a illustrarne i principali aspetti. Pensate come complementari, permettono di mettere in prospettiva le informazioni sviluppate nell’articolo e di offrirne una lettura cartografica."),
 # Jura
 ("La ligne(s) de démarcation du Jura", "The demarcation line(s) in the Jura", "La linea (o le linee) di demarcazione del Giura"),
 ("Série de trois cartes réalisées dans le cadre du Master 2 d’histoire contemporaine de Nathan Colombo Valette, consacré au sujet « Un département dans la guerre : pour une histoire sensible de la ligne de démarcation dans le Jura (1940-1944) ».",
  "A series of three maps produced as part of Nathan Colombo Valette’s Master’s degree in Contemporary History, focusing on the topic “A department at war: towards a sensitive history of the demarcation line in the Jura (1940–1944)”.",
  "Serie di tre mappe realizzate nell’ambito del Master 2 in Storia contemporanea di Nathan Colombo Valette, dedicato al tema «Un dipartimento in guerra: per una storia sensibile della linea di demarcazione nel Giura (1940-1944)»."),
 ("Ce travail comprend une carte générale du contexte ainsi que deux cartes détaillant des situations particulières liées à la ligne de démarcation. Elles permettent de localiser précisément les différents tracés, les points de passage et les zones où la ligne se prolonge ou se chevauche à l’échelle de plusieurs départements, afin d’appuyer et d’illustrer le propos de l’étudiant.",
  "This work comprises a general map providing context, as well as two maps detailing specific situations relating to the demarcation line. They enable the precise location of the various routes, crossing points and areas where the line extends or overlaps across several departments, in order to support and illustrate the student’s argument.",
  "Questo lavoro comprende una mappa generale del contesto e due mappe che descrivono in dettaglio situazioni particolari legate alla linea di demarcazione. Esse consentono di localizzare con precisione i diversi tracciati, i punti di passaggio e le zone in cui la linea si estende o si sovrappone su un’area che comprende diversi dipartimenti, al fine di sostenere e illustrare la tesi dello studente."),
 # Monde connecté
 ("Comment le monde est-il connecté ?", "How is the world connected?", "Come è connesso il mondo?"),
 ("Aujourd’hui, la connexion à Internet est devenue déterminante dans le fonctionnement du monde. Elle permet les échanges d’informations, le développement économique, la communication et l’accès aux services essentiels.",
  "Today, internet access has become essential to the functioning of the world. It enables the exchange of information, economic development, communication, and access to essential services.",
  "Oggi, l’accesso a Internet è diventato essenziale per il funzionamento del mondo. Permette lo scambio di informazioni, lo sviluppo economico, la comunicazione e l’accesso ai servizi essenziali."),
 ("Grâce aux infrastructures numériques et aux réseaux de communication, les sociétés sont de plus en plus interconnectées. Cependant, garantir un accès stable et rapide à Internet reste un enjeu majeur à l’échelle mondiale.",
  "Thanks to digital infrastructure and communication networks, societies are becoming increasingly interconnected. However, ensuring stable and fast internet access remains a major global challenge.",
  "Grazie alle infrastrutture digitali e alle reti di comunicazione, le società sono sempre più interconnesse. Tuttavia, garantire un accesso stabile e veloce a Internet rimane una grande sfida a livello globale."),
 # Milan
 ("Jeux olympiques d’hiver de Milan Cortina 2026", "Milan Cortina 2026 Winter Olympics", "Olimpiadi invernali Milano Cortina 2026"),
 ("Cette carte consacrée à la danse sur glace montre comment certains patineurs changent de nationalité pour augmenter leurs chances de sélection, et comment les couples se regroupent autour de quelques grands centres d’entraînement.",
  "This map on ice dancing shows how some skaters change nationality to increase their chances of selection, and how couples cluster around a few major training centres.",
  "Questa mappa dedicata alla danza su ghiaccio mostra come alcuni pattinatori cambino nazionalità per aumentare le loro possibilità di essere selezionati, e come le coppie si concentrino attorno ad alcuni grandi centri di allenamento."),
 # Parcours
 ("Un parcours professionnel cartographié", "A mapped-out career path", "Un percorso di carriera mappato"),
 ("Exemple anonymisé d’une carte qui raconte un parcours professionnel comme un itinéraire, avec ses étapes et ses bifurcations. Il ne s’agit pas du projet livré.",
  "An anonymised example of a map that tells a career path as a journey, with its stages and turning points. This is not the final project.",
  "Esempio anonimo di una mappa che racconta un percorso professionale come un itinerario, con le sue tappe e i suoi bivi. Non si tratta del progetto consegnato."),
 # OTAN
 ("L’élargissement de l’OTAN depuis 1949", "The expansion of NATO since 1949", "L’allargamento della NATO dal 1949"),
 ("Cette carte retrace les vagues successives d’élargissement de l’Organisation du traité de l’Atlantique nord (OTAN) depuis sa création en 1949 par douze États fondateurs. Elle montre d’abord l’ancrage de l’Alliance en Europe occidentale pendant la guerre froide, face au bloc soviétique.",
  "This map traces the successive waves of enlargement of the North Atlantic Treaty Organisation (NATO) since its creation in 1949 by the twelve founding states. It first shows the Alliance’s establishment in Western Europe during the Cold War, in the face of the Soviet bloc.",
  "Questa mappa illustra le successive ondate di allargamento dell’Organizzazione del Trattato del Nord Atlantico (NATO) dalla sua fondazione nel 1949 ad opera dei dodici Stati fondatori. Mostra innanzitutto il radicamento dell’Alleanza nell’Europa occidentale durante la Guerra Fredda, di fronte al blocco sovietico."),
 ("Elle met ensuite en évidence l’extension progressive vers l’Europe centrale et orientale après 1991, avec les grandes vagues de 1999 et 2004. Les adhésions récentes de la Finlande (2023) et de la Suède (2024), décidées après l’invasion de l’Ukraine par la Russie, illustrent la recomposition stratégique du continent.",
  "It then highlights the gradual expansion into Central and Eastern Europe after 1991, with the major waves of enlargement in 1999 and 2004. The recent accessions of Finland (2023) and Sweden (2024), decided following Russia’s invasion of Ukraine, illustrate the strategic realignment of the continent.",
  "Evidenzia poi la progressiva espansione verso l’Europa centrale e orientale dopo il 1991, con le grandi ondate del 1999 e del 2004. Le recenti adesioni della Finlandia (2023) e della Svezia (2024), decise dopo l’invasione dell’Ucraina da parte della Russia, illustrano la ricomposizione strategica del continente."),
 # Chagos
 ("La rétrocession de l’archipel des Chagos", "The return of the Chagos Archipelago", "La restituzione dell’arcipelago delle Chagos"),
 ("Ce mémoire analyse la rétrocession de l’archipel des Chagos, détaché de Maurice par le Royaume-Uni en 1965, du point de vue mauricien. Il replace ce différend de souveraineté dans le contexte électoral de 2024, au moment où la question devient un enjeu majeur de politique intérieure et diplomatique.",
  "This dissertation analyses the return of the Chagos Archipelago, which was separated from Mauritius by the United Kingdom in 1965, from the Mauritian perspective. It places this sovereignty dispute within the context of the 2024 general election, at a time when the issue is becoming a major domestic and diplomatic concern.",
  "Questa tesi analizza la restituzione dell’arcipelago delle Chagos, separato da Mauritius dal Regno Unito nel 1965, dal punto di vista mauriziano. Colloca questa controversia di sovranità nel contesto elettorale del 2024, in un momento in cui la questione sta diventando una sfida fondamentale per la politica interna e diplomatica."),
 ("Il met en lumière les rapports de force qui structurent l’océan Indien, entre puissances occidentales, Inde et Chine. Il montre aussi pourquoi l’archipel est si convoité : sa position centrale, son vaste espace maritime et la base militaire américaine de Diego Garcia en font un point d’appui stratégique de premier plan.",
  "It highlights the balance of power shaping the Indian Ocean, between Western powers, India and China. It also explains why the archipelago is so coveted: its central location, its vast maritime zone and the US military base at Diego Garcia make it a key strategic foothold.",
  "Mette in luce i rapporti di forza che caratterizzano l’Oceano Indiano, tra le potenze occidentali, l’India e la Cina. Mostra inoltre perché l’arcipelago sia così ambito: la sua posizione centrale, il suo vasto spazio marittimo e la base militare statunitense di Diego Garcia ne fanno un punto d’appoggio strategico di primo piano."),
 # Cartes interactives
 ("<h2>La peine de mort aux États-Unis</h2>", "<h2>The death penalty in the United States</h2>", "<h2>La pena di morte negli Stati Uniti</h2>"),
 ("Carte interactive.</span>", "Interactive map.</span>", "Mappa interattiva.</span>"),
 ("Ouvrir en plein écran", "Open full screen", "Apri a schermo intero"),
 ("Vacances dans les stations balnéaires de l’Ouest : combien ça coûte ?", "Seaside holidays in western France: how much does it cost?", "Vacanze nelle località balneari della Francia occidentale: quanto costano?"),
 ("Carte interactive réalisée le 3 juin 2026 pour", "Interactive map produced on 3 June 2026 for", "Mappa interattiva realizzata il 3 giugno 2026 per"),
 ("Liberté 250 : la mission de la Patrouille de France aux États-Unis", "Liberté 250: the Patrouille de France’s mission to the United States", "Liberté 250: la missione della Patrouille de France negli Stati Uniti"),
 ("Carte interactive réalisée le 4 mai 2026 pour", "Interactive map produced on 4 May 2026 for", "Mappa interattiva realizzata il 4 maggio 2026 per"),
 ("Maine-et-Loire : la station qui protège 60 000 personnes des inondations", "Maine-et-Loire: the pumping station protecting 60,000 people from flooding", "Maine-et-Loire: la stazione che protegge 60.000 persone dalle inondazioni"),
 ("Carte réalisée pour <em>Ouest-France</em>.", "Map produced for <em>Ouest-France</em>.", "Mappa realizzata per <em>Ouest-France</em>."),
]

ARTICLES = [
 ("Le texte permet d’entrer dans l’analyse fine d’enjeux complexes. Parce que les écrits restent, j’attache une grande importance à écrire sur les sujets qui me tiennent à cœur et à les illustrer par des cartes et des infographies.",
  "Writing enables me to delve into a detailed analysis of complex issues. Because the written word endures, I attach great importance to writing about the subjects close to my heart and illustrating them with maps and infographics.",
  "Il testo consente di approfondire l’analisi di tematiche complesse. Poiché ciò che si scrive rimane, attribuisco grande importanza al fatto di scrivere sugli argomenti che mi stanno a cuore e di illustrarli con mappe e infografiche."),
 ("Publication sur le site web de <em>Ouest-France</em>", "Published on the <em>Ouest-France</em> website", "Pubblicato sul sito di <em>Ouest-France</em>"),
 ("CARTE. Glace, hôtel, camping, sorties : voici combien coûtent vos vacances dans les terres à l’Ouest",
  "MAP. Ice cream, hotels, campsites, nights out: here’s how much your holiday in the western inland regions will cost",
  "MAPPA. Gelati, hotel, campeggi, attività: ecco quanto costano le vostre vacanze nell’entroterra occidentale"),
 ("« Melancholia » sur Arte : l’onirisme de l’éclipse totale façon Lars von Trier",
  "“Melancholia” on Arte: the dreamlike quality of a total eclipse, Lars von Trier-style",
  "«Melancholia» su Arte: l’atmosfera onirica dell’eclissi totale alla Lars von Trier"),
 ("CARTE. Incendies en Gironde : visualisez la situation sur place",
  "MAP. Fires in Gironde: visualise the situation on the ground",
  "MAPPA. Incendi in Gironda: visualizzare la situazione sul posto"),
 ("INFOGRAPHIE. La Coupe du monde 2026 a-t-elle été impactée par la politique migratoire de Donald Trump ?",
  "INFOGRAPHIC. Was the 2026 World Cup affected by Donald Trump’s migration policy?",
  "INFOGRAFICA. La Coppa del Mondo 2026 è stata influenzata dalla politica migratoria di Donald Trump?"),
 ("ENTRETIEN. Pascal Boniface : « Dans cette Coupe du monde, Donald Trump veut montrer qu’il est le boss »",
  "INTERVIEW. Pascal Boniface: “In this World Cup, Donald Trump wants to show that he is the boss”",
  "INTERVISTA. Pascal Boniface: «In questa Coppa del Mondo, Donald Trump vuole mostrare che è il boss»"),
 ("CARTES. Les Casques bleus vont-ils quitter le Liban ?", "MAPS. Will the peacekeepers leave Lebanon?", "MAPPE. I Caschi blu lasceranno il Libano?"),
 ("CARTE. Comment Pékin construit des îles artificielles pour asseoir son influence",
  "MAP. How Beijing is building artificial islands to assert its influence",
  "MAPPA. Come Pechino costruisce isole artificiali per esercitare la sua influenza"),
 ("CARTE. Hantavirus : dans quels pays sont rapatriés les passagers du « MV Hondius » et quelles mesures ont-ils prises ?",
  "MAP. Hantavirus: in which countries are the passengers of the “MV Hondius” being repatriated and what measures have they taken?",
  "MAPPA. Hantavirus: in quali paesi vengono rimpatriati i passeggeri della «MV Hondius» e quali misure hanno adottato?"),
 ("CARTE. Guerre au Moyen-Orient : quels sont les sites stratégiques sur le territoire iranien ?",
  "MAP. War in the Middle East: what are the strategic sites on Iranian territory?",
  "MAPPA. Guerra in Medio Oriente: quali sono i siti strategici sul territorio iraniano?"),
 ("CARTES. Pourquoi l’archipel des Chagos est-il au cœur des convoitises internationales ?",
  "MAPS. Why is the Chagos Archipelago the subject of international covetousness?",
  "MAPPE. Perché l’arcipelago delle Chagos è al centro delle mire internazionali?"),
 ("CARTES. Pourquoi le Groenland, géant de glace, attire-t-il la convoitise de Donald Trump ?",
  "MAPS. Why is Greenland, the ice giant, attracting Donald Trump’s covetousness?",
  "MAPPE. Perché la Groenlandia, il gigante di ghiaccio, attira le mire di Donald Trump?"),
 ("Publication sur le site web le 13 janvier 2026 et dans le journal papier <em>Dimanche Ouest-France</em> le 18 janvier 2026",
  "Published on the website on 13 January 2026 and in the print edition of <em>Dimanche Ouest-France</em> on 18 January 2026",
  "Pubblicato sul sito web il 13 gennaio 2026 e nell’edizione cartacea di <em>Dimanche Ouest-France</em> il 18 gennaio 2026"),
 ("Double page du Dimanche Ouest-France du 18 janvier 2026 consacrée au Groenland",
  "Double-page spread from Dimanche Ouest-France of 18 January 2026 on Greenland",
  "Doppia pagina di Dimanche Ouest-France del 18 gennaio 2026 dedicata alla Groenlandia"),
 ("INFOGRAPHIES. Breton, corse, basque… L’enseignement des langues régionales est-il en panne ?",
  "INFOGRAPHICS. Breton, Corsican, Basque… Is regional language teaching failing?",
  "INFOGRAFICHE. Bretone, corso, basco… L’insegnamento delle lingue regionali è in crisi?"),
 (">24 août 2026<", ">24 August 2026<", ">24 agosto 2026<"),
 (">12 août 2026<", ">12 August 2026<", ">12 agosto 2026<"),
 (">24 juillet 2026<", ">24 July 2026<", ">24 luglio 2026<"),
 (">11 juillet 2026<", ">11 July 2026<", ">11 luglio 2026<"),
 (">11 juin 2026<", ">11 June 2026<", ">11 giugno 2026<"),
 (">13 mai 2026<", ">13 May 2026<", ">13 maggio 2026<"),
 (">11 mai 2026<", ">11 May 2026<", ">11 maggio 2026<"),
 (">1er avril 2026<", ">1 April 2026<", ">1° aprile 2026<"),
 (">26 février 2026<", ">26 February 2026<", ">26 febbraio 2026<"),
 (">4 décembre 2025<", ">4 December 2025<", ">4 dicembre 2025<"),
]

PROJETS = [
 ("Curieuse par nature, j’aime explorer différents formats et sortir du cadre strict de la cartographie. Chaque expérience est pour moi une manière d’expérimenter, d’apprendre et de transmettre autrement.",
  "Curious by nature, I enjoy exploring different formats and stepping outside the strict confines of cartography. Each experience is a way for me to experiment, learn and communicate in a different way.",
  "Curiosa per natura, mi piace esplorare formati diversi e uscire dai rigidi schemi della cartografia. Ogni esperienza è per me un modo per sperimentare, imparare e comunicare in modo diverso."),
 ("Changer de support, c’est aussi changer de regard. Analyser, cartographier ou prendre la parole relèvent finalement d’une même démarche : rendre le monde plus lisible.",
  "Changing medium also means changing perspective. Analysing, mapping or speaking out are ultimately part of the same process: making the world more understandable.",
  "Cambiare mezzo significa anche cambiare prospettiva. Analizzare, mappare o prendere la parola derivano in ultima analisi dallo stesso approccio: rendere il mondo più leggibile."),
 ("Affiche de la conférence « Ça sert à quoi… la cartographie ? », Géodote x P1SD",
  "Poster for the conference “What is… cartography for?”, Géodote x P1SD",
  "Locandina della conferenza «A cosa serve… la cartografia?», Géodote x P1SD"),
 ("Conférence : Ça sert à quoi la cartographie géopolitique ?", "Lecture: What is the purpose of geopolitical mapping?", "Conferenza: A cosa serve la cartografia geopolitica?"),
 ("Conférence organisée le 24 janvier 2026 à l’université Paris 1 Panthéon-Sorbonne, dans le cadre du partenariat entre les associations P1SD et Géodote.",
  "A conference organised on 24 January 2026 at the University of Paris 1 Panthéon-Sorbonne, as part of the partnership between the P1SD and Géodote associations.",
  "Conferenza organizzata il 24 gennaio 2026 presso l’Università Paris 1 Panthéon-Sorbonne, nell’ambito della collaborazione tra le associazioni P1SD e Géodote."),
 ("Une carte géopolitique n’est plus un simple support visuel. C’est un véritable outil d’analyse et d’aide à la décision, essentiel pour comprendre les dynamiques et les rapports de force internationaux. Démocratiser le savoir géopolitique passe aussi par la carte.",
  "A geopolitical map is no longer merely a visual aid. It is a genuine tool for analysis and decision-making, essential for understanding international dynamics and power relations. Democratising geopolitical knowledge also relies on maps.",
  "Una mappa geopolitica non è più un semplice supporto visivo. È un vero e proprio strumento di analisi e di supporto decisionale, essenziale per comprendere le dinamiche e i rapporti di forza internazionali. La democratizzazione delle conoscenze geopolitiche passa anche attraverso la mappa."),
 ("Vidéo « Master géopolitique : témoignage » de Thotis", "Thotis video “Master’s in geopolitics: testimonial”", "Video «Master in geopolitica: testimonianza» di Thotis"),
 ("Témoignage : être étudiant en géopolitique", "Testimonial: being a student of geopolitics", "Testimonianza: essere studente di geopolitica"),
 ("Dans ce témoignage, je partage mon expérience du master de géopolitique à l’Institut français de géopolitique : semaine type, matières approfondies et préparation nécessaire pour réussir ce cursus exigeant. Je raconte la gestion des difficultés, l’avancement du mémoire, et mon regard sur les perspectives professionnelles après ce master.",
  "In this testimonial, I share my experience of the Master’s degree in Geopolitics at the French Institute of Geopolitics: a typical week, in-depth subjects and the preparation required to succeed in this demanding course. I talk about how I dealt with difficulties, the progress of my dissertation, and my views on career prospects after completing this Master’s degree.",
  "In questa testimonianza, condivido la mia esperienza del Master in Geopolitica presso l’Istituto Francese di Geopolitica: una settimana tipo, lo studio approfondito delle materie e la preparazione necessaria per affrontare con successo questo percorso impegnativo. Descrivo come ho superato le difficoltà, i progressi della mia tesi e il mio sguardo sulle prospettive di carriera dopo questo Master."),
 ("Voir sur YouTube", "Watch on YouTube", "Guarda su YouTube"),
 ("Géopodcast sur Spotify", "Géopodcast on Spotify", "Géopodcast su Spotify"),
 ("Géopodcast – un podcast créé avec des camarades de promotion de l’Institut français de géopolitique.",
  "Géopodcast – a podcast created with fellow students from the French Institute of Geopolitics.",
  "Géopodcast – un podcast creato con i compagni di corso dell’Istituto Francese di Geopolitica."),
 ("Réalisé par des étudiant·es, ce projet propose un regard authentique sur le métier de chercheur·se et les enjeux de l’actualité géopolitique. Le podcast combine partage d’expériences, réflexion académique et exploration des coulisses de la préparation du terrain.",
  "Produced by students, this project offers an authentic look at the profession of researcher and the challenges of current geopolitical issues. The podcast combines experience sharing, academic reflection and an exploration of the behind-the-scenes work involved in preparing fieldwork.",
  "Realizzato da studenti, questo progetto offre uno sguardo autentico sulla professione di ricercatore e sulle attuali questioni geopolitiche. Il podcast combina esperienze condivise, riflessioni accademiche e un’esplorazione del dietro le quinte della preparazione al lavoro sul campo."),
 ("Le premier cycle, composé de trois épisodes, aborde la phase de terrain : découverte, questionnements, défis logistiques et adrénaline du départ en autonomie.",
  "The first series, consisting of three episodes, addresses the fieldwork phase: discovery, questions, logistical challenges and the adrenaline rush of setting off on your own.",
  "Il primo ciclo, composto da tre episodi, affronta la fase sul campo: la scoperta, le domande, le sfide logistiche e l’adrenalina di partire da soli."),
 ("Un projet qui illustre la collaboration, la curiosité et l’engagement étudiant dans le domaine de la géopolitique.",
  "A project that illustrates collaboration, curiosity and student engagement in the field of geopolitics.",
  "Un progetto che illustra la collaborazione, la curiosità e l’impegno degli studenti nel campo della geopolitica."),
 ("Lien vers le podcast", "Link to the podcast", "Link al podcast"),
]

PAR_PAGE = {"index.html": INDEX, "cartes.html": CARTES, "articles.html": ARTICLES, "projets.html": PROJETS}
LANGUE_LABEL = {"fr": "Langue", "en": "Language", "it": "Lingua"}

def url_page(lang, page):
    chemin = "" if page == "index.html" else page
    return SITE + ("" if lang == "fr" else lang + "/") + chemin

def lien_langue(depuis, vers, page):
    if depuis == vers: return page
    if depuis == "fr": return vers + "/" + page
    return "../" + page if vers == "fr" else "../" + vers + "/" + page

def ajouter_langues(s, lang, page):
    s = re.sub(r'\n<link rel="alternate" hreflang="[^"]+" href="[^"]+">', "", s)
    s = re.sub(r'\n<nav class="langues".*?</nav>', "", s, flags=re.S)
    alt = "".join('\n<link rel="alternate" hreflang="%s" href="%s">' % (l, url_page(l, page)) for l in ("fr", "en", "it"))
    alt += '\n<link rel="alternate" hreflang="x-default" href="%s">' % url_page("fr", page)
    s = s.replace('<link rel="canonical" href="%s">' % url_page(lang, page),
                  '<link rel="canonical" href="%s">' % url_page(lang, page) + alt, 1)
    liens = []
    for l in ("fr", "en", "it"):
        cur = ' aria-current="true"' if l == lang else ""
        liens.append('<a href="%s" lang="%s" hreflang="%s"%s>%s</a>' % (lien_langue(lang, l, page), l, l, cur, l.upper()))
    nav = '\n<nav class="langues" aria-label="%s">%s</nav>' % (LANGUE_LABEL[lang], "".join(liens))
    assert s.count("</nav>\n</header>") == 1
    s = s.replace("</nav>\n</header>", "</nav>" + nav + "\n</header>")
    return s

def traduire(fr, lang, page):
    i = 1 if lang == "en" else 2
    s = fr.replace('\xa0', ' ').replace('\u202f', ' ')
    for paire in PAR_PAGE[page]:
        if paire[0] not in s:
            sys.exit("Introuvable dans %s : %s" % (page, paire[0][:80]))
        s = s.replace(paire[0], paire[i])
    for paire in COMMUN:
        s = s.replace(paire[0], paire[i])
    s = s.replace('<html lang="fr">', '<html lang="%s">' % lang)
    # chemins vers les ressources (les pages sont un dossier plus bas)
    s = re.sub(r'(href|src)="(css|js|fonts|images)/', r'\1="../\2/', s)
    # URL canonique et Open Graph
    s = s.replace('href="%s"' % url_page("fr", page), 'href="%s"' % url_page(lang, page))
    s = s.replace('content="%s"' % url_page("fr", page), 'content="%s"' % url_page(lang, page))
    if page == "index.html":
        s = s.replace(CV_PDF["fr"], CV_PDF[lang])
        a = s.index('<div class="parcours">'); b = s.index("</section>", a)
        s = s[:a] + bloc_cv(CV[lang]) + s[b:]
    return ajouter_langues(s, lang, page)

def versionner(s):
    """Ajoute ?v=<empreinte> aux liens CSS/JS : les navigateurs rechargent dès qu'un fichier change."""
    import hashlib
    def remplacer(m):
        empreinte = hashlib.md5(open(m.group(1), "rb").read()).hexdigest()[:8]
        return m.group(1) + "?v=" + empreinte + '"'
    return re.sub(r'((?:css|js)/[\w-]+\.(?:css|js))(?:\?v=\w+)?"', remplacer, s)

for page in PAGES:
    fr = versionner(open(page, encoding="utf-8").read())
    fr_base = re.sub(r'\n<link rel="alternate" hreflang="[^"]+" href="[^"]+">', "", fr)
    fr_base = re.sub(r'\n<nav class="langues".*?</nav>', "", fr_base, flags=re.S)
    for lang in ("en", "it"):
        os.makedirs(lang, exist_ok=True)
        with open(os.path.join(lang, page), "w", encoding="utf-8") as f:
            f.write(traduire(fr_base, lang, page))
    with open(page, "w", encoding="utf-8") as f:
        f.write(ajouter_langues(fr_base, "fr", page))
print("OK")
