import fs from "node:fs";
import path from "node:path";
// Le CSV est incorporé par Vite au moment de la construction : le fichier n'a donc
// pas à être retrouvé sur le disque depuis le code compilé.
import csvBrut from "../data/oeuvres.csv?raw";

// Les photos vivent dans public/ (non traité par Vite) : on les liste depuis la
// racine du projet, qui est le répertoire courant pendant la construction.
const PHOTOS = path.join(process.cwd(), "public", "oeuvres");

export type Oeuvre = {
  id: string;
  artiste: string;
  artisteSlug: string;
  titre: string;
  annee: string;
  technique: string;
  numerotation: string;
  tirage: string;
  signature: string;
  dimensions: string;
  papier: string;
  etat: string;
  certificat: boolean;
  prix: number | null;
  statut: "disponible" | "reservee" | "vendue";
  enAvant: boolean;
  notes: string;
  images: string[];
  /** Libellé prêt à afficher : "450 €" ou "Prix sur demande". */
  prixTexte: string;
  /** Titre lisible, avec repli quand le titre est inconnu. */
  titreAffiche: string;
};

/** Découpe une ligne CSV en respectant les champs entre guillemets. */
function decouperLigne(ligne: string): string[] {
  const champs: string[] = [];
  let courant = "";
  let dansGuillemets = false;

  for (let i = 0; i < ligne.length; i++) {
    const c = ligne[i];
    if (c === '"') {
      if (dansGuillemets && ligne[i + 1] === '"') {
        courant += '"';
        i++;
      } else {
        dansGuillemets = !dansGuillemets;
      }
    } else if (c === "," && !dansGuillemets) {
      champs.push(courant);
      courant = "";
    } else {
      courant += c;
    }
  }
  champs.push(courant);
  return champs.map((c) => c.trim());
}

export function slugifier(texte: string): string {
  return texte
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

/**
 * Retrouve les photos d'une œuvre par convention de nommage : tout fichier de
 * public/oeuvres/ nommé `{id}.jpg` ou `{id}-*.jpg` lui est rattaché. Aucun
 * chemin d'image n'a donc à être saisi dans le CSV.
 */
function trouverImages(id: string): string[] {
  if (!fs.existsSync(PHOTOS)) return [];
  return fs
    .readdirSync(PHOTOS)
    .filter((f) => /\.(jpe?g|png|webp|avif)$/i.test(f))
    .filter((f) => {
      const base = f.replace(/\.[^.]+$/, "");
      return base === id || base.startsWith(`${id}-`);
    })
    .sort()
    .map((f) => `/oeuvres/${f}`);
}

function estVrai(v: string): boolean {
  return /^(oui|yes|true|1|x)$/i.test(v.trim());
}

let cache: Oeuvre[] | null = null;

export function toutesLesOeuvres(): Oeuvre[] {
  if (cache) return cache;

  const brut = csvBrut.replace(/^\ufeff/, "");
  const lignes = brut.split(/\r?\n/).filter((l) => l.trim() !== "");
  const entetes = decouperLigne(lignes[0]);

  const oeuvres = lignes.slice(1).map((ligne) => {
    const champs = decouperLigne(ligne);
    const l = (nom: string) => {
      const i = entetes.indexOf(nom);
      return i === -1 ? "" : (champs[i] ?? "");
    };

    const artiste = l("artiste");
    const titre = l("titre");
    const prixBrut = l("prix").replace(/[^\d.,]/g, "").replace(",", ".");
    const prix = prixBrut === "" ? null : Number(prixBrut);
    const statutBrut = l("statut").toLowerCase();
    const statut = (["disponible", "reservee", "vendue"].includes(statutBrut)
      ? statutBrut
      : "disponible") as Oeuvre["statut"];

    return {
      id: l("id"),
      artiste,
      artisteSlug: slugifier(artiste),
      titre,
      annee: l("annee"),
      technique: l("technique") || "Lithographie originale",
      numerotation: l("numerotation"),
      tirage: l("tirage"),
      signature: l("signature"),
      dimensions: l("dimensions"),
      papier: l("papier"),
      etat: l("etat"),
      certificat: estVrai(l("certificat")),
      prix: prix !== null && Number.isFinite(prix) ? prix : null,
      statut,
      enAvant: estVrai(l("en_avant")),
      notes: l("notes"),
      images: trouverImages(l("id")),
      prixTexte:
        prix !== null && Number.isFinite(prix)
          ? `${prix.toLocaleString("fr-FR")} €`
          : "Prix sur demande",
      titreAffiche: titre && titre.toLowerCase() !== "sans titre" ? titre : "Sans titre",
    } satisfies Oeuvre;
  });

  cache = oeuvres.filter((o) => o.id !== "");
  return cache;
}

export type Artiste = {
  nom: string;
  slug: string;
  oeuvres: Oeuvre[];
  disponibles: number;
};

/** La liste des artistes est déduite des œuvres — rien à maintenir en double. */
export function tousLesArtistes(): Artiste[] {
  const parNom = new Map<string, Oeuvre[]>();
  for (const o of toutesLesOeuvres()) {
    if (!parNom.has(o.artiste)) parNom.set(o.artiste, []);
    parNom.get(o.artiste)!.push(o);
  }
  return [...parNom.entries()]
    .map(([nom, oeuvres]) => ({
      nom,
      slug: slugifier(nom),
      oeuvres,
      disponibles: oeuvres.filter((o) => o.statut === "disponible").length,
    }))
    .sort((a, b) => a.nom.localeCompare(b.nom, "fr"));
}

export const SITE_NOM = "Collection de lithographies originales";
export const SITE_URL = "https://exemple-a-remplacer.netlify.app";
