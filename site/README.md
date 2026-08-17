# Site de la collection de lithographies

Site statique : chaque œuvre a sa **vraie page HTML**, ce qui la rend lisible immédiatement par
Google. Pas d'abonnement, hébergement gratuit à vie.

---

## 1. Mettre le site en ligne (une seule fois, 5 minutes)

1. Va sur [netlify.com](https://netlify.com) et crée un compte gratuit (bouton « Sign up with GitHub »).
2. Clique **Add new site → Import an existing project → GitHub**.
3. Choisis le dépôt `my-profile2`.
4. Netlify lit le fichier `netlify.toml` à la racine et remplit tout seul les réglages.
   Ne touche à rien, clique **Deploy**.
5. Deux minutes plus tard, ton site est en ligne à une adresse du type
   `https://un-nom-au-hasard.netlify.app`.

**Ensuite, une chose importante.** Dans Netlify, va dans *Site configuration → Change site name*
et choisis un nom propre, par exemple `collection-lithographies`. Puis remplace l'adresse
`https://exemple-a-remplacer.netlify.app` aux **trois** endroits suivants :

- `site/astro.config.mjs` → ligne `site:`
- `site/public/robots.txt` → ligne `Sitemap:`
- `site/src/lib/oeuvres.ts` → constante `SITE_URL`

Sans ça, le plan du site et les aperçus de partage pointent vers une adresse qui n'existe pas.

À partir de là, **chaque modification envoyée sur GitHub reconstruit le site automatiquement.**
Tu n'as plus jamais rien à installer sur ton ordinateur.

---

## 2. Ajouter une œuvre

### a) Les photos

Dépose-les dans `site/public/oeuvres/`, nommées d'après l'identifiant de l'œuvre :

```
brayer-02-1.jpg     ← photo principale (l'œuvre entière)
brayer-02-2.jpg     ← gros plan de la signature
brayer-02-3.jpg     ← gros plan de la numérotation
```

Le site les retrouve tout seul, dans l'ordre alphabétique. **Aucun chemin d'image à saisir
nulle part.** La photo `-1` est celle qui s'affiche dans le catalogue.

> Vise 2000 px de large environ, en JPEG. Plus grand ne sert à rien et ralentit le site.

### b) La ligne dans le tableau

Ouvre `site/src/data/oeuvres.csv`. C'est un fichier de tableur : **tu peux l'ouvrir dans Excel**,
ajouter tes lignes, et l'enregistrer au format CSV (UTF-8).

Une ligne par œuvre, dans cet ordre de colonnes :

| Colonne | Ce qu'on y met | Exemple |
|---|---|---|
| `id` | identifiant unique, sans accent ni espace — il devient l'adresse de la page | `brayer-02` |
| `artiste` | nom complet | `Yves Brayer` |
| `titre` | laisse vide si inconnu | `Chevaux de Camargue` |
| `annee` | facultatif | `1978` |
| `technique` | | `Lithographie originale en couleurs` |
| `numerotation` | | `45/150` |
| `tirage` | le nombre seul | `150` |
| `signature` | | `Signée au crayon en bas à droite` |
| `dimensions` | | `56 × 76 cm` |
| `papier` | | `Papier à bords barbés` |
| `etat` | | `Neuf, jamais encadrée` |
| `certificat` | `oui` ou vide | `oui` |
| `prix` | le nombre seul, sans € — vide affiche « Prix sur demande » | `480` |
| `statut` | `disponible`, `reservee` ou `vendue` | `disponible` |
| `en_avant` | `oui` pour l'afficher sur la page d'accueil | `oui` |
| `notes` | texte libre affiché en bas de la fiche | |

**Attention à un seul piège :** si ton texte contient une virgule, mets-le entre guillemets.

```
brayer-02,Yves Brayer,Chevaux,,Lithographie originale,45/150,150,Signée,56 × 76 cm,,"Neuf, marges intactes",oui,480,disponible,oui,
```

C'est tout. Le catalogue, les filtres, la page de l'artiste et le plan du site se mettent à jour
tout seuls.

---

## 3. Marquer une œuvre comme vendue

Dans le CSV, remplace `disponible` par `vendue` dans la colonne `statut`.

**Ne supprime pas la ligne.** La page reste en ligne avec la mention « Vendue » : elle continue
d'attirer des visiteurs sur Google, et ils sont redirigés vers les autres œuvres du même artiste.
Une page supprimée, c'est du référencement perdu pour rien.

---

## 4. Ce qu'il te reste à personnaliser

| Où | Quoi |
|---|---|
| `src/pages/contact.astro` | ton adresse email (constante `EMAIL` en haut) |
| `src/pages/artiste/[slug].astro` | le paragraphe de présentation de chaque artiste |
| `src/pages/mentions-legales.astro` | ton nom, ton adresse, l'hébergeur |
| `src/pages/confidentialite.astro` | ton email de contact |

Les biographies d'artistes ont été **volontairement laissées vides**. Lapicque, Brayer et Weisbuch
sont de vraies personnes : mieux vaut un texte manquant qu'une date inventée qui te décrédibilise
auprès d'un collectionneur qui connaît son sujet.

---

## 5. Le formulaire de contact

Il ouvre le logiciel de messagerie du visiteur avec un message pré-rempli. Ça fonctionne partout,
sans aucun service à configurer.

Si tu préfères recevoir les demandes directement par email, Netlify le fait gratuitement :
ajoute `data-netlify="true"` et `name="contact"` sur la balise `<form>` de
`src/pages/contact.astro`, et les messages arriveront dans l'onglet *Forms* de Netlify.

---

## 6. Travailler en local (facultatif)

```bash
cd site
npm install
npm run dev      # aperçu sur http://localhost:4321
npm run build    # construit le site dans dist/
```

Tu n'en as pas besoin si tu modifies le CSV directement depuis l'interface de GitHub : Netlify
reconstruit à chaque enregistrement.

---

## 7. Détails techniques

- **Astro 5**, site entièrement statique, aucun serveur nécessaire
- Une page HTML par œuvre et par artiste, générées à la construction
- Balisage `JSON-LD` de type `Product` sur chaque fiche (prix, disponibilité, état)
- `sitemap-index.xml` et `robots.txt` générés automatiquement
- Filtres du catalogue reflétés dans l'adresse : `?artiste=yves-brayer&prix=300-500` est un lien
  partageable
- Toutes les œuvres sont dans le HTML même quand elles sont masquées par un filtre — Google voit
  l'intégralité du catalogue
- Chargement différé des images, pensé pour 300 œuvres
- Aucun cookie, aucun traceur

Les polices viennent de Google Fonts. Pour supprimer cette dépendance externe, télécharge
Cormorant Garamond et Inter, place-les dans `public/fonts/` et remplace la balise `<link>` de
`src/layouts/Base.astro` par une règle `@font-face` dans `src/styles/global.css`.
