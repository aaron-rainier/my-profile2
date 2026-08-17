# Prompt pour générer le site de vente de lithographies

> **Où le coller :** [Lovable](https://lovable.dev) de préférence (il gère bien un catalogue avec base de
> données). Bolt.new ou v0 fonctionnent aussi. Colle tout le bloc ci-dessous d'un seul coup.

---

## CONTEXTE

Je suis un particulier basé à Paris. Je possède une collection d'environ 300 lithographies
originales, toutes signées au crayon par l'artiste et numérotées, achetées auprès d'éditeurs d'art
français (dont Visions Nouvelles) entre les années 1970 et 1990. Elles sont en feuilles, jamais
encadrées, en état neuf, marges intactes, conservées à plat. Format dominant : 56 × 76 cm.
Chaque œuvre est accompagnée de son certificat d'authenticité d'origine.

Artistes principaux : **Charles Lapicque, Yves Brayer, Claude Weisbuch, Louis Toffoli,
Camille Hilaire, Hasegawa.**

Je veux un site vitrine-catalogue pour vendre ces œuvres à des particuliers et des collectionneurs,
en France et à l'international. Le site doit inspirer confiance et donner envie, sans faire
« brocante ».

## OBJECTIF DU SITE

Générer des demandes de contact qualifiées sur des œuvres précises. **Pas de paiement en ligne
en version 1** — les acheteurs me contactent via un formulaire, je gère le règlement et la
livraison en direct. Prévois cependant l'architecture pour pouvoir brancher Stripe plus tard sans
tout refaire.

## STACK

- React + TypeScript + Vite
- Tailwind CSS
- React Router pour la navigation
- Aucune dépendance payante, aucun service externe obligatoire pour faire tourner le site

## STRUCTURE DE DONNÉES — LE POINT LE PLUS IMPORTANT

Toutes les œuvres doivent vivre dans **un seul fichier `src/data/oeuvres.ts`** que je puisse éditer
à la main sans toucher au code. Je vais y ajouter 300 entrées progressivement. Utilise exactement
ce schéma :

```ts
export type Oeuvre = {
  id: string;              // "lapicque-01" — sert d'URL
  artiste: string;         // "Charles Lapicque"
  titre: string;           // "Sans titre" si inconnu
  annee: string;           // "" si inconnue
  technique: string;       // "Lithographie originale en couleurs"
  numerotation: string;    // "LXV/CL (65/150)"
  tirage: number | null;   // 150
  signature: string;       // "Signée au crayon en bas à droite"
  dimensions: string;      // "56 × 76 cm"
  papier: string;          // "Papier à bords barbés"
  etat: string;            // "Neuf, jamais encadrée, marges intactes"
  certificat: boolean;
  prix: number | null;     // null = "Prix sur demande"
  statut: "disponible" | "reservee" | "vendue";
  images: string[];        // ["/oeuvres/lapicque-01.jpg", ".../-signature.jpg"]
  enAvant: boolean;        // true = apparaît sur la page d'accueil
  notes: string;           // texte libre affiché en bas de fiche
};
```

Pré-remplis le fichier avec ces 3 œuvres réelles, en les commentant pour que je comprenne le
format, puis laisse un emplacement clair pour la suite :

1. **Charles Lapicque** — lithographie en couleurs, LXV/CL (65/150), 56 × 76 cm, signée au crayon
   en bas à droite, papier à bords barbés, état neuf — **450 €**
2. **Yves Brayer** — lithographie en couleurs, signée et numérotée, 56 × 76 cm, état neuf — **480 €**
3. **Louis Toffoli** — « Le Bal musette », 134/250, 56 × 76 cm, signée au crayon — **150 €**

Les artistes doivent être **déduits automatiquement** de la liste des œuvres — je ne veux pas
maintenir une seconde liste en parallèle.

## PAGES

**`/` Accueil**
Bandeau sobre : titre de la collection, une phrase d'accroche, un visuel fort. En dessous :
les œuvres marquées `enAvant`, en grille. Puis un bloc court « Pourquoi cette collection »
(origine, état neuf, certificats). Puis les artistes, en vignettes cliquables.

**`/catalogue` Catalogue**
Grille responsive de toutes les œuvres. Filtres combinables, en haut, toujours visibles :
- par artiste (cases à cocher)
- par tranche de prix (curseur ou tranches prédéfinies)
- par disponibilité (masquer les vendues — coché par défaut)
- tri : prix croissant, prix décroissant, artiste A→Z

Les filtres doivent se refléter dans l'URL (`?artiste=brayer&max=500`) pour que je puisse envoyer
un lien filtré à un acheteur.

**`/oeuvre/:id` Fiche œuvre**
Grande image à gauche (cliquable pour zoomer en plein écran), miniatures dessous pour les autres
photos. À droite : artiste, titre, toutes les caractéristiques techniques dans un tableau propre,
le prix en grand, un bouton **« Demander cette œuvre »** qui ouvre le formulaire pré-rempli avec la
référence. Si `statut` vaut `vendue`, affiche un bandeau « Vendue » et remplace le bouton par un
lien vers les autres œuvres du même artiste. En bas : 4 autres œuvres du même artiste.

**`/artiste/:nom` Page artiste**
Un court paragraphe de présentation, puis toutes ses œuvres disponibles.
**IMPORTANT : n'invente aucune donnée biographique.** Mets un texte de remplacement explicite
du type `[À COMPLÉTER : biographie de {artiste}]` que je remplirai moi-même. Ce sont de vrais
artistes, je ne veux aucune date ni aucun fait inventé sur le site.

**`/a-propos` La collection**
L'origine (achats auprès d'éditeurs d'art français, années 1970-1990), l'état de conservation,
les certificats d'authenticité, le fait que ce sont des lithographies originales signées et
numérotées et non des reproductions.

**`/contact`**
Formulaire : nom, email, téléphone (facultatif), œuvre concernée (pré-remplie si on vient d'une
fiche), message. Mentionne la remise en main propre possible à Paris et l'expédition en tube
rigide assuré. Le formulaire doit fonctionner via `mailto:` en solution de repli si aucun backend
n'est configuré, et être prêt à brancher un service d'envoi d'emails.

## DESIGN

C'est un site d'art : **les œuvres sont le seul élément coloré de la page.**

- Fond blanc cassé (#FAFAF8), texte gris très foncé (#1A1A1A), un seul accent discret en gris-bleu profond
- Beaucoup de blanc, marges généreuses, rien de tassé
- Typographie : une serif élégante pour les titres (Cormorant Garamond ou Playfair Display), une
  sans-serif neutre pour le texte (Inter)
- Aucune ombre portée marquée, aucun dégradé, aucun coin très arrondi, aucune animation tape-à-l'œil
- Les images d'œuvres s'affichent entières, jamais rognées — utilise `object-fit: contain` sur un
  fond neutre, car le format des feuilles varie
- Chargement différé des images (lazy loading) : il y aura 300 œuvres avec plusieurs photos chacune
- Entièrement responsive, pensé mobile d'abord — beaucoup d'acheteurs consulteront depuis leur téléphone

## SEO — TRAITE ÇA SÉRIEUSEMENT

C'est par Google que viendront la majorité des acheteurs. Ils tapent « lithographie Toffoli »,
« Brayer lithographie signée », etc.

- Balise `<title>` unique par page. Pour une fiche : `{Artiste} — {Titre} — Lithographie originale signée et numérotée`
- Meta description unique par fiche, construite à partir des caractéristiques réelles
- Balisage `JSON-LD` de type `Product` sur chaque fiche (nom, image, description, offre, prix, devise, disponibilité)
- Un seul `<h1>` par page, hiérarchie de titres cohérente
- Attribut `alt` descriptif sur chaque image : `{Artiste} — {Titre} — lithographie originale signée`
- URLs lisibles et stables : `/oeuvre/lapicque-01`, `/artiste/yves-brayer`
- Génère `sitemap.xml` et `robots.txt`
- Balises Open Graph pour un partage propre sur les réseaux et messageries

## PAGES LÉGALES (France)

Crée `/mentions-legales` et `/confidentialite` avec des gabarits à compléter, adaptés à un
**vendeur particulier** (pas une entreprise) : identité du responsable, hébergeur, usage des
données du formulaire de contact, droit d'accès et de suppression, absence de cookies de suivi.
Laisse mes coordonnées en champs `[À COMPLÉTER]`.

## À NE PAS FAIRE

- N'invente aucune biographie, date, cote ou fait sur les artistes — ce sont de vraies personnes
- Pas de faux avis clients, pas de fausses statistiques, pas de compteur « X personnes regardent cette œuvre »
- Pas de bandeau de compte à rebours ni d'urgence artificielle
- Pas de panier ni de paiement en version 1
- Pas de CMS externe, pas de base de données à configurer : tout doit tourner à partir du fichier de données
- Pas de fausses images d'œuvres en remplissage : utilise des blocs gris neutres avec le nom du
  fichier attendu, que je remplacerai par mes photos

## LIVRABLE ATTENDU

Un site fonctionnel dès le premier rendu avec les 3 œuvres d'exemple, où il me suffit de :
1. déposer mes photos dans `/public/oeuvres/`
2. ajouter mes entrées dans `src/data/oeuvres.ts`

et tout le reste — catalogue, filtres, pages artistes, fiches, SEO — se met à jour tout seul.

Ajoute un fichier `README.md` à la racine qui explique en français, pas à pas, comment j'ajoute
une nouvelle œuvre et comment je marque une œuvre comme vendue.
