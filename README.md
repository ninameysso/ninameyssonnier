# Portfolio — Nina Meyssonnier

Site personnel publié sur **https://ninameyssonnier.com** (hébergement GitHub Pages).

Le site est fait de pages HTML simples, sans outil ni abonnement :

| Fichier | Page |
|---|---|
| `index.html` | Présentation (accueil, parcours, contact) |
| `cartes.html` | Mes cartes |
| `articles.html` | Mes articles |
| `projets.html` | Projets transversaux |
| `css/style.css` | Couleurs, polices et mise en page |
| `en/`, `it/` | Les mêmes pages en anglais et en italien |
| `cv/` | CV en PDF (FR, EN, IT) : pour mettre à jour un CV, remplace le fichier en gardant le même nom |
| `outils/traduire.py` | Fabrique `en/` et `it/` à partir des pages françaises |

## Ajouter les images

Dépose chaque image dans le bon dossier **avec exactement ce nom**. Tant qu'une image manque, elle est simplement masquée : le texte s'affiche seul.

Aucune image ne manque pour l'instant.

Conseil : exporte les cartes en JPG d'environ 2000 px de large. Elles restent nettes et le site se charge vite.

## Site trilingue (FR, EN, IT)

Les pages françaises sont la référence. Les versions anglaise (`en/`) et italienne (`it/`) sont fabriquées par `outils/traduire.py`, qui contient toutes les traductions et les CV dans chaque langue.

Après avoir modifié une page française, lance dans le terminal, depuis le dossier du site :

```
python3 outils/traduire.py
```

Si un texte français a changé, le script s'arrête et indique la phrase qu'il ne trouve plus : mets à jour la ligne correspondante (français, anglais, italien) dans `outils/traduire.py`, puis relance-le. Ne modifie pas directement les fichiers de `en/` et `it/` : ils seraient écrasés.

## Modifier le site avec VS Code

1. Clone le dépôt (VS Code : *Cloner le dépôt Git*, ou GitHub Desktop).
2. Installe l'extension **Live Server** et fais un clic droit sur `index.html` › *Open with Live Server* pour voir le site en direct pendant que tu modifies.
3. Modifie les fichiers HTML (textes, liens) ou `css/style.css` (couleurs dans `:root`, tout en haut).
4. *Commit* puis *Push* (onglet Contrôle de code source) : le site se met à jour en une ou deux minutes.

## Modifier un texte directement sur GitHub

Ouvre la page sur GitHub, clique sur le crayon (*Edit this file*), modifie le texte entre les balises, puis *Commit changes*. Le site se met à jour en une ou deux minutes.

## Polices

EB Garamond (texte courant) et Averia Serif Libre (titres, logo, menu, rubriques), toutes deux sous licence SIL Open Font License (voir `fonts/OFL.txt`).
