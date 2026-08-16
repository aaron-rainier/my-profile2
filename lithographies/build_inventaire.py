#!/usr/bin/env python3
"""Construit le classeur d'inventaire pour la vente d'une collection de lithographies."""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment

OUT = "/home/user/my-profile2/lithographies/inventaire-lithographies.xlsx"
LAST = 401  # dernière ligne de saisie de l'onglet Inventaire

FONT = "Arial"
BLUE = Font(name=FONT, size=10, color="0000FF")
BLACK = Font(name=FONT, size=10)
GREEN = Font(name=FONT, size=10, color="008000")
BOLD = Font(name=FONT, size=10, bold=True)
TITLE = Font(name=FONT, size=14, bold=True, color="1F3864")
SUB = Font(name=FONT, size=10, italic=True, color="595959")
HDR_FILL = PatternFill("solid", fgColor="1F3864")
HDR_FONT = Font(name=FONT, size=10, bold=True, color="FFFFFF")
YELLOW = PatternFill("solid", fgColor="FFFF00")
GREY = PatternFill("solid", fgColor="F2F2F2")
BAND = PatternFill("solid", fgColor="EDF2F9")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

EUR = '#,##0 "€";(#,##0 "€");-'
PCT = '0.0%;(0.0%);-'

wb = Workbook()

# ----------------------------------------------------------------------------
# 1. MODE D'EMPLOI
# ----------------------------------------------------------------------------
ws = wb.active
ws.title = "Mode d'emploi"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 30
ws.column_dimensions["C"].width = 95

rows = [
    ("t", "Inventaire & plan de vente — collection de lithographies", ""),
    ("s", "Environ 300 estampes signées et numérotées, 56 x 76 cm, en feuilles — Paris", ""),
    ("b", "", ""),
    ("h", "Comment utiliser ce classeur", ""),
    ("k", "Onglet « Inventaire »", "Une ligne par ŒUVRE (pas par exemplaire). La colonne « Nb exemplaires » gère les doubles. Les cellules à remplir sont en jaune ; le reste se calcule tout seul."),
    ("k", "Onglet « Repères de prix »", "Prix réellement observés sur le marché (adjudications, annonces). À lire AVANT de fixer un prix cible."),
    ("k", "Onglet « Tableau de bord »", "Se met à jour seul. Donne le nombre de pièces par segment, la valeur cible et le net réellement encaissé."),
    ("k", "Onglet « Plan de vente »", "L'ordre des opérations, semaine par semaine."),
    ("b", "", ""),
    ("h", "Les 3 segments (colonne R de l'Inventaire)", ""),
    ("k", "A — Pièce forte", "Artiste coté, sujet recherché (musiciens, maternités, marines, cavaliers), exemplaire unique chez toi, petit tirage. Vente à l'unité, au prix fort, sans se presser."),
    ("k", "B — Courant", "Artiste connu mais sujet banal ou gros tirage (250-300). Vente à l'unité mais prix agressif, ou lots de 2-3."),
    ("k", "C — Volume / doubles", "Doubles, artistes non cotés, sujets difficiles. Lots de 5 à 20, ou cession en bloc à un marchand."),
    ("b", "", ""),
    ("h", "Règles d'or", ""),
    ("k", "Ne jamais inonder", "Ne mets JAMAIS deux exemplaires de la même image en ligne en même temps, ni 50 œuvres du même artiste la même semaine. Tu ferais chuter ton propre marché. Rythme : 5 à 10 annonces actives maximum."),
    ("k", "Prix plancher", "Fixe-le AVANT de publier et ne descends pas en dessous. Sinon tu négocieras dans le vide 300 fois."),
    ("k", "Test avant volume", "Vends d'abord 8-10 pièces représentatives. Les prix obtenus deviennent ta grille de référence pour les 290 autres."),
    ("k", "Jamais d'expertise payante", "Les sites « estimation gratuite » sont des apporteurs d'affaires. Une maison de ventes sérieuse estime gratuitement."),
    ("b", "", ""),
    ("h", "Code couleur", ""),
    ("k", "Fond jaune", "À remplir par toi."),
    ("k", "Texte bleu", "Valeur saisie à la main (hypothèse, prix décidé)."),
    ("k", "Texte noir", "Formule — ne pas écraser."),
]

r = 1
for kind, a, b in rows:
    if kind == "t":
        ws.cell(r, 2, a).font = TITLE
    elif kind == "s":
        ws.cell(r, 2, a).font = SUB
    elif kind == "h":
        c = ws.cell(r, 2, a)
        c.font = Font(name=FONT, size=11, bold=True, color="1F3864")
        ws.cell(r, 3, "").font = BLACK
    elif kind == "k":
        ws.cell(r, 2, a).font = BOLD
        c = ws.cell(r, 3, b)
        c.font = BLACK
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 30
    r += 1

# ----------------------------------------------------------------------------
# 2. INVENTAIRE
# ----------------------------------------------------------------------------
inv = wb.create_sheet("Inventaire")

cols = [
    ("Réf", 10, "saisie"),
    ("Artiste", 18, "saisie"),
    ("Titre", 26, "saisie"),
    ("Année", 8, "saisie"),
    ("Éditeur / atelier", 18, "saisie"),
    ("Numérotation", 13, "saisie"),
    ("Tirage total", 11, "saisie"),
    ("Type d'épreuve", 14, "saisie"),
    ("Signé au crayon", 14, "saisie"),
    ("Dim. feuille (cm)", 15, "saisie"),
    ("Dim. image (cm)", 15, "saisie"),
    ("Papier", 14, "saisie"),
    ("Timbre sec / cachet", 18, "saisie"),
    ("Certificat", 11, "saisie"),
    ("Nb exemplaires", 13, "saisie"),
    ("État", 12, "saisie"),
    ("Photo faite", 11, "saisie"),
    ("Litho vérifiée (loupe)", 18, "saisie"),
    ("Segment", 10, "saisie"),
    ("Prix plancher (€)", 15, "saisie"),
    ("Prix cible (€)", 13, "saisie"),
    ("Valeur cible stock (€)", 18, "formule"),
    ("Canal prévu", 20, "saisie"),
    ("Statut", 16, "saisie"),
    ("Date mise en ligne", 16, "saisie"),
    ("Prix vendu (€)", 13, "saisie"),
    ("Frais + port (€)", 14, "saisie"),
    ("Net encaissé (€)", 15, "formule"),
    ("Plateforme / acheteur", 20, "saisie"),
    ("Notes", 40, "saisie"),
]

inv.freeze_panes = "D2"
for i, (name, width, _) in enumerate(cols, start=1):
    c = inv.cell(1, i, name)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    c.border = BOX
    inv.column_dimensions[get_column_letter(i)].width = width
inv.row_dimensions[1].height = 34

inv["A1"].comment = Comment(
    "Une ligne par ŒUVRE. Suggestion de réf : TOF-001, WEI-001... "
    "(3 lettres de l'artiste + numéro).", "Inventaire")
inv["O1"].comment = Comment(
    "Nombre d'exemplaires du MÊME tirage que tu possèdes. "
    "Mets 1 s'il est unique chez toi.", "Inventaire")
inv["R1"].comment = Comment(
    "Test à la loupe x10 ou macro du téléphone : une vraie lithographie montre un grain "
    "irrégulier et des aplats continus. Un offset montre une trame régulière de points "
    "(rosettes). C'est LE facteur qui décide du prix.", "Inventaire")
inv["T1"].comment = Comment(
    "Prix en dessous duquel tu refuses de vendre. Décide-le une fois, tiens-le.",
    "Inventaire")

# Lignes d'exemple issues des photos fournies
examples = [
    ["TOF-001", "Louis Toffoli", "Le Bal musette", "", "Visions Nouvelles (à confirmer)",
     "134/250", 250, "Numérotée", "Oui", "56 x 76", "", "", "", "Oui", 1, "Neuf", "Non",
     "À faire", "A", 150, 320, None, "Enchères Drouot / eBay", "À photographier", "", None, None,
     None, "", "Musiciens : sujet le plus recherché chez Toffoli. Annotation crayon en marge : « 204/10/151 »."],
    ["TOF-002", "Louis Toffoli", "(sans titre) — personnage à l'établi", "", "À confirmer",
     "à relever", None, "Numérotée", "Oui", "56 x 76", "", "", "", "Oui", 1, "Neuf", "Non",
     "À faire", "B", 90, 180, None, "eBay / Le Bon Coin", "À photographier", "", None, None,
     None, "", "Relever la numérotation en bas à gauche."],
    ["XXX-001", "À IDENTIFIER", "Paysage pointilliste — cerisiers et reflets", "", "À confirmer",
     "15/180", 180, "Numérotée", "Oui", "56 x 76", "", "Vélin à bords barbés", "", "Oui", 1,
     "Neuf", "Non", "À faire", "B", 80, 200, None, "À déterminer", "À photographier", "", None,
     None, None, "", "Signature en haut à gauche à déchiffrer — photo macro nécessaire."],
    ["WEI-001", "Claude Weisbuch", "(exemple à remplacer)", "", "Visions Nouvelles",
     "72/150", 150, "Numérotée", "Oui", "56 x 76", "", "", "", "Oui", 2, "Neuf", "Non",
     "À faire", "B", 80, 190, None, "Catawiki", "À photographier", "", None, None, None, "",
     "LIGNE D'EXEMPLE — montre le format attendu. À supprimer ou remplacer."],
]

for ri, row in enumerate(examples, start=2):
    for ci, val in enumerate(row, start=1):
        c = inv.cell(ri, ci, val)
        c.font = BLUE
        c.border = BOX
        c.alignment = Alignment(vertical="top", wrap_text=(ci == 30))

# Formules + mise en forme sur toute la plage de saisie
for ri in range(2, LAST + 1):
    for ci in range(1, len(cols) + 1):
        c = inv.cell(ri, ci)
        c.border = BOX
        if ri > 5:
            c.font = BLUE
            c.alignment = Alignment(vertical="top", wrap_text=(ci == 30))
    # Valeur cible du stock = nb exemplaires x prix cible
    v = inv.cell(ri, 22, f"=IFERROR(O{ri}*U{ri},0)")
    v.font = BLACK
    v.number_format = EUR
    v.border = BOX
    # Net encaissé = prix vendu - frais
    n = inv.cell(ri, 28, f"=IFERROR(Z{ri}-AA{ri},0)")
    n.font = BLACK
    n.number_format = EUR
    n.border = BOX
    for ci in (20, 21, 26, 27):
        inv.cell(ri, ci).number_format = EUR
    inv.cell(ri, 25).number_format = "DD/MM/YYYY"
    for ci in (20, 21, 22, 28):
        inv.cell(ri, ci).fill = YELLOW if ci in (20, 21) else BAND

# Les colonnes calculées portent un en-tête distinct
for ci, (_, _, kind) in enumerate(cols, start=1):
    if kind == "formule":
        inv.cell(1, ci).fill = PatternFill("solid", fgColor="595959")

# Listes déroulantes
dvs = {
    "S": '"A,B,C"',
    "X": '"À photographier,Photographiée,Prête,En ligne,Négociation,VENDUE,Retirée,Invendue"',
    "P": '"Neuf,Très bon,Bon,Défauts légers,Défauts importants"',
    "I": '"Oui,Non,À vérifier"',
    "N": '"Oui,Non"',
    "Q": '"Oui,Non"',
    "R": '"Oui — litho,Non — offset,À faire"',
    "H": '"Numérotée,EA / Épreuve d\'artiste,HC / Hors commerce,Non numérotée"',
    "W": '"Enchères Drouot / Interencheres,Catawiki,eBay,Le Bon Coin,Marchand en gros,Galerie / dépôt-vente,Etsy,Salon / marché,À déterminer"',
}
for col, formula in dvs.items():
    dv = DataValidation(type="list", formula1=formula, allow_blank=True)
    dv.error = "Choisis une valeur dans la liste."
    dv.errorTitle = "Valeur non autorisée"
    inv.add_data_validation(dv)
    dv.add(f"{col}2:{col}{LAST}")

inv.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{LAST}"

# ----------------------------------------------------------------------------
# 3. TABLEAU DE BORD
# ----------------------------------------------------------------------------
db = wb.create_sheet("Tableau de bord", 1)
db.sheet_view.showGridLines = False
for col, w in (("A", 3), ("B", 34), ("C", 16), ("D", 16), ("E", 18), ("F", 4), ("G", 60)):
    db.column_dimensions[col].width = w

db["B1"] = "Tableau de bord"
db["B1"].font = TITLE
db["B2"] = "Tout se calcule depuis l'onglet Inventaire. Rien à saisir ici."
db["B2"].font = SUB

def head(row, label):
    c = db.cell(row, 2, label)
    c.font = Font(name=FONT, size=11, bold=True, color="1F3864")
    for i in range(2, 6):
        db.cell(row, i).fill = GREY

def line(row, label, formula, fmt=None, bold=False):
    lc = db.cell(row, 2, label)
    lc.font = BOLD if bold else BLACK
    vc = db.cell(row, 3, formula)
    vc.font = BOLD if bold else BLACK
    if fmt:
        vc.number_format = fmt
    vc.alignment = Alignment(horizontal="right")
    return vc

def rg(col):
    """Plage absolue d'une colonne de l'onglet Inventaire, lignes 2 à LAST."""
    return f"Inventaire!${col}$2:${col}${LAST}"

head(4, "Volume")
line(5, "Œuvres différentes référencées", f"=COUNTA({rg('A')})", "#,##0")
line(6, "Exemplaires au total (doubles inclus)", f"=SUM({rg('O')})", "#,##0")
line(7, "Photographiées et prêtes", f'=COUNTIFS({rg("Q")},"Oui")', "#,##0")
line(8, "Vérifiées à la loupe (litho confirmée)", f'=COUNTIFS({rg("R")},"Oui — litho")', "#,##0")

head(10, "Répartition par segment")
db.cell(10, 3, "Œuvres").font = HDR_FONT
db.cell(10, 4, "Exemplaires").font = HDR_FONT
db.cell(10, 5, "Valeur cible").font = HDR_FONT
for i in (3, 4, 5):
    db.cell(10, i).fill = HDR_FILL
    db.cell(10, i).alignment = Alignment(horizontal="center")
for i, (seg, lbl) in enumerate([("A", "A — Pièces fortes"), ("B", "B — Courant"), ("C", "C — Volume / doubles")]):
    row = 11 + i
    db.cell(row, 2, lbl).font = BLACK
    db.cell(row, 3, f'=COUNTIFS({rg("S")},"{seg}")').font = BLACK
    db.cell(row, 3).number_format = "#,##0"
    db.cell(row, 4, f'=SUMIFS({rg("O")},{rg("S")},"{seg}")').font = BLACK
    db.cell(row, 4).number_format = "#,##0"
    db.cell(row, 5, f'=SUMIFS({rg("V")},{rg("S")},"{seg}")').font = BLACK
    db.cell(row, 5).number_format = EUR
db.cell(14, 2, "Total").font = BOLD
db.cell(14, 3, "=SUM(C11:C13)").font = BOLD
db.cell(14, 3).number_format = "#,##0"
db.cell(14, 4, "=SUM(D11:D13)").font = BOLD
db.cell(14, 4).number_format = "#,##0"
db.cell(14, 5, "=SUM(E11:E13)").font = BOLD
db.cell(14, 5).number_format = EUR
for i in (2, 3, 4, 5):
    db.cell(14, i).fill = BAND

head(16, "Avancement")
line(17, "En ligne actuellement", f'=COUNTIFS({rg("X")},"En ligne")', "#,##0")
line(18, "Vendues", f'=COUNTIFS({rg("X")},"VENDUE")', "#,##0")
line(19, "Invendues / retirées", f'=COUNTIFS({rg("X")},"Invendue")+COUNTIFS({rg("X")},"Retirée")', "#,##0")
db.cell(17, 7, "Garde ce chiffre entre 5 et 10. Au-delà, tu casses tes propres prix.").font = SUB

head(21, "Argent")
line(22, "Chiffre d'affaires brut", f"=SUM({rg('Z')})", EUR)
line(23, "Frais et ports payés", f"=SUM({rg('AA')})", EUR)
line(24, "Net réellement encaissé", f"=SUM({rg('AB')})", EUR, bold=True)
db.cell(24, 2).fill = BAND
db.cell(24, 3).fill = BAND
line(25, "Prix net moyen par pièce vendue",
     f'=IFERROR(SUM({rg("AB")})/COUNTIFS({rg("X")},"VENDUE"),0)', EUR)
line(26, "Réalisé / valeur cible totale", "=IFERROR(C24/E14,0)", PCT)
db.cell(26, 7, "Sous 60 %, tes prix cibles sont trop optimistes : révise-les.").font = SUB

head(28, "Seuil fiscal à surveiller (France)")
line(29, "Ventes individuelles > 5 000 €", f'=COUNTIFS({rg("Z")},">5000")', "#,##0")
db.cell(29, 7, "Au-delà de 5 000 € par cession : taxe forfaitaire de 6,5 % sur le prix de vente "
        "(ou option plus-value). En dessous : exonéré.").font = SUB
db.cell(29, 7).alignment = Alignment(wrap_text=True)
line(30, "Nombre de ventes sur l'année", f'=COUNTIFS({rg("X")},"VENDUE")', "#,##0")
db.cell(30, 7, "Au-delà de 30 ventes OU 2 000 € par plateforme et par an, la plateforme "
        "transmet tes données au fisc (DAC7). Ce n'est pas un impôt, mais anticipe-le.").font = SUB
db.cell(30, 7).alignment = Alignment(wrap_text=True)

# ----------------------------------------------------------------------------
# 4. REPÈRES DE PRIX
# ----------------------------------------------------------------------------
px = wb.create_sheet("Repères de prix")
px.sheet_view.showGridLines = False
for col, w in (("A", 3), ("B", 24), ("C", 38), ("D", 14), ("E", 14), ("F", 14), ("G", 44)):
    px.column_dimensions[col].width = w

px["B1"] = "Repères de prix — 5 artistes identifiés"
px["B1"].font = TITLE
px["B2"] = ("Règle n°1 : un PRIX DEMANDÉ n'est pas un PRIX OBTENU. Les galeries affichent "
            "400-1 200 €, les salles adjugent 50-550 €. Cale-toi sur la colonne ADJUGÉ.")
px["B2"].font = SUB
px["B2"].alignment = Alignment(wrap_text=True)
px.row_dimensions[2].height = 28

def sect(row, label):
    c = px.cell(row, 2, label)
    c.font = Font(name=FONT, size=11, bold=True, color="1F3864")
    for i in range(2, 8):
        px.cell(row, i).fill = GREY

def thead(row, labels):
    for i, h in enumerate(labels, start=2):
        c = px.cell(row, i, h)
        c.font = HDR_FONT
        c.fill = HDR_FILL
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        c.border = BOX

# --- A. Hiérarchie des artistes ---------------------------------------------
sect(4, "Hiérarchie de tes artistes — par où commencer")
thead(5, ["Artiste", "Priorité", "Net bas", "Net haut", "", "Pourquoi"])
hierarchie = [
    ("Yves Brayer (1907-1990)", "1 — LE MEILLEUR", 150, 500,
     "Membre de l'Institut, musée à son nom aux Baux. Camargue, taureaux, Provence. "
     "Seul de tes artistes dont les lithos passent régulièrement les 500 € en salle."),
    ("Hasegawa", "2 — À CLARIFIER", 60, 250,
     "S'il s'agit de KIYOSHI Hasegawa (1891-1980, manière noire), la cote est nettement "
     "supérieure. Si c'est SHOICHI (1929-2023), on reste dans la fourchette ci-contre. "
     "Vérifie le prénom sur les certificats — l'écart est énorme."),
    ("Claude Weisbuch (1927-2014)", "3", 60, 200,
     "Cavaliers, musiciens, théâtre. Cote en baisse mais les estampes résistent mieux "
     "que ses huiles."),
    ("Camille Hilaire (1916-2004)", "4", 50, 150,
     "Paysages, forêts, chevaux. Très présent sur le marché, prix courants 89-150 €."),
    ("Louis Toffoli (1907-1999)", "5 — LE PLUS COMMUN", 50, 180,
     "Éditions très nombreuses. Sujets musiciens et maternités = le haut de la fourchette ; "
     "le reste peine à dépasser 100 €."),
]
for i, (a, prio, bas, haut, why) in enumerate(hierarchie):
    r0 = 6 + i
    px.cell(r0, 2, a).font = BOLD
    c = px.cell(r0, 3, prio)
    c.font = BOLD if i == 0 else BLACK
    c.alignment = Alignment(horizontal="center")
    if i == 0:
        c.fill = PatternFill("solid", fgColor="E2EFDA")
    px.cell(r0, 4, bas).number_format = EUR
    px.cell(r0, 5, haut).number_format = EUR
    px.cell(r0, 4).font = BLUE
    px.cell(r0, 5).font = BLUE
    px.merge_cells(start_row=r0, start_column=6, end_row=r0, end_column=7)
    w = px.cell(r0, 6, why)
    w.font = BLACK
    w.alignment = Alignment(wrap_text=True, vertical="top")
    for ci in range(2, 8):
        px.cell(r0, ci).border = BOX
    px.row_dimensions[r0].height = 46
px.cell(11, 2, "Fourchettes NETTES par pièce, après frais de plateforme — synthèse des "
        "résultats observés ci-dessous, pas une cotation officielle.").font = SUB
px.merge_cells("B11:G11")

# --- B. Prix observés --------------------------------------------------------
sect(13, "Prix réellement observés, avec sources")
thead(14, ["Artiste", "Référence", "Type de prix", "Bas", "Haut", "Source"])
data = [
    ["Yves Brayer", "Scène taurine, litho couleur signée au crayon",
     "ADJUGÉ", 550, 550, "Résultat de salle"],
    ["Yves Brayer", "Suite de 6 lithographies, Camargue, bon état",
     "ADJUGÉ", 1800, 1800, "Résultat de salle — l'intérêt des séries complètes"],
    ["Yves Brayer", "Lithographies signées et numérotées",
     "Fourchette marché", 200, 600, "mr-expert.com / gazette-drouot.com"],
    ["Shoichi Hasegawa", "Estampes et multiples, estimation en salle",
     "Fourchette marché", 40, 300, "mr-expert.com"],
    ["Shoichi Hasegawa", "Estampes-multiples selon base Artprice",
     "Fourchette base", 100, 3000, "Artprice, via galerie-creation"],
    ["Kiyoshi Hasegawa", "À NE PAS CONFONDRE — maître de la manière noire",
     "Repère", 300, 5000, "mr-expert.com — cote très supérieure"],
    ["Claude Weisbuch", "« Grande parade », litho signée en bas à droite",
     "Estimation salle (2025)", 200, 300, "primardeco.com"],
    ["Claude Weisbuch", "Multiples, fourchette générale",
     "Fourchette marché", 30, 400, "mr-expert.com"],
    ["Claude Weisbuch", "« Deux Cavaliers », litho signée /125",
     "PRIX DEMANDÉ", 487, 487, "1stdibs.com"],
    ["Camille Hilaire", "Multiples en salle, fourchette générale",
     "Fourchette marché", 10, 1500, "mr-expert.com"],
    ["Camille Hilaire", "Lithographies signées, prix courants en ligne",
     "PRIX DEMANDÉ", 89, 280, "leboncoin / passion-estampes"],
    ["Louis Toffoli", "« Maternité » 50x65, n° 53/150 — estimée 60-80 €",
     "ADJUGÉ (2021)", 100, 100, "mw-encheres.com"],
    ["Louis Toffoli", "« Couple sur un banc », litho sur japon 50x73",
     "Estimation salle (2023)", 50, 100, "richardmdv.com, vente du 12/12/2023"],
    ["Louis Toffoli", "Estampes, fourchette générale en salle",
     "Fourchette marché", 30, 300, "mr-expert.com / expertisez.com"],
    ["Louis Toffoli", "Annonces particuliers et galeries",
     "PRIX DEMANDÉ", 120, 1090, "leboncoin, eBay, passion-estampes"],
]
for ri, row in enumerate(data, start=15):
    for ci, val in enumerate(row, start=2):
        c = px.cell(ri, ci, val)
        c.font = BOLD if "ADJUG" in row[2] else BLACK
        c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if ci in (5, 6):
            c.number_format = EUR
            c.alignment = Alignment(horizontal="right")
    px.row_dimensions[ri].height = 26
    if "DEMANDÉ" in row[2]:
        for ci in range(2, 8):
            px.cell(ri, ci).fill = PatternFill("solid", fgColor="FDE9E9")
    elif "ADJUG" in row[2]:
        for ci in range(2, 8):
            px.cell(ri, ci).fill = PatternFill("solid", fgColor="E2EFDA")

# --- C. Avertissement Artprice ----------------------------------------------
sect(31, "Artprice : outil de recherche, PAS un canal de vente")
arts = [
    ("Ce que c'est", "Une base de 30 millions de résultats d'enchères sur 700 000 artistes. "
     "C'est l'outil que les commissaires-priseurs consultent pour estimer."),
    ("Le coût", "Abonnement obligatoire : 196 €/an en basique, jusqu'à 407 €/an en pro. "
     "Sa marketplace prend en plus 5 à 9 % TTC de frais vendeur."),
    ("Le problème", "L'audience y vient CHERCHER DES PRIX, pas acheter de la décoration murale. "
     "Pour écouler 300 lithographies d'éditeur, le débit est quasi nul."),
    ("Verdict", "Ne t'abonne pas pour vendre. Si tu veux des résultats d'enchères, "
     "Interencheres, Gazette Drouot, Barnebys et le filtre « objets vendus » d'eBay "
     "te donnent l'essentiel gratuitement."),
]
for i, (a, b) in enumerate(arts):
    r0 = 32 + i
    px.cell(r0, 2, a).font = BOLD
    c = px.cell(r0, 3, b)
    c.font = BLACK
    c.alignment = Alignment(wrap_text=True, vertical="top")
    px.merge_cells(start_row=r0, start_column=3, end_row=r0, end_column=7)
    px.row_dimensions[r0].height = 30

# --- D. Ce que disent les experts -------------------------------------------
sect(37, "Ce que disent les experts du marché")
notes = [
    ("Toffoli", "« Très nombreuses sur le marché de l'art, la réelle valeur des estampes "
     "est aujourd'hui très faible. » — expertisez.com"),
    ("Weisbuch", "« La cote subit une tendance à la baisse et une désaffection des acquéreurs, "
     "car les estimations trop élevées ne trouvent pas d'acheteurs. » — mr-expert.com"),
    ("Hilaire", "Marché stable mais encombré : la plupart des lithos signées se négocient "
     "entre 89 et 150 €."),
    ("Brayer", "Le seul dont les séries complètes atteignent 1 000 à 2 000 €. "
     "Ne casse jamais une suite pour la vendre à la pièce."),
]
for i, (a, b) in enumerate(notes):
    r0 = 38 + i
    px.cell(r0, 2, a).font = BOLD
    c = px.cell(r0, 3, b)
    c.font = BLACK
    c.alignment = Alignment(wrap_text=True, vertical="top")
    px.merge_cells(start_row=r0, start_column=3, end_row=r0, end_column=7)
    px.row_dimensions[r0].height = 30

# --- E. Ce qui fait monter le prix ------------------------------------------
sect(43, "Ce qui fait monter le prix")
plus = [
    "Petit tirage (moins de 150) plutôt que 250-300.",
    "Sujet recherché : Camargue, taureaux et Provence pour Brayer ; cavaliers, musiciens et "
    "théâtre pour Weisbuch ; musiciens, maternités et marines pour Toffoli.",
    "Épreuve d'artiste (EA) ou hors commerce (HC) plutôt qu'un simple numéro.",
    "Suite ou portfolio complet gardé groupé — chez Brayer, ça double la mise.",
    "Papier de qualité à bords barbés (Arches, BFK Rives) + timbre sec d'atelier.",
    "État neuf, marges intactes, jamais massicotées.",
]
for i, t in enumerate(plus):
    c = px.cell(44 + i, 3, "•  " + t)
    c.font = BLACK
    c.alignment = Alignment(wrap_text=True, vertical="top")
    px.merge_cells(start_row=44 + i, start_column=3, end_row=44 + i, end_column=7)
    px.row_dimensions[44 + i].height = 26

# ----------------------------------------------------------------------------
# 5. PLAN DE VENTE
# ----------------------------------------------------------------------------
pl = wb.create_sheet("Plan de vente")
pl.sheet_view.showGridLines = False
for col, w in (("A", 3), ("B", 16), ("C", 34), ("D", 72), ("E", 14)):
    pl.column_dimensions[col].width = w

pl["B1"] = "Plan de vente — quelques heures par semaine"
pl["B1"].font = TITLE
pl["B2"] = "Objectif : maximiser le prix. Horizon réaliste : 18 à 24 mois."
pl["B2"].font = SUB

for i, h in enumerate(["Période", "Action", "Détail", "Fait ?"], start=2):
    c = pl.cell(4, i, h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center")
    c.border = BOX

plan = [
    ("Semaines 1-3", "Inventaire complet",
     "Photographier et saisir les 300 pièces. 20 par séance. Pour chaque : vue entière + macro de la signature + macro de la numérotation. Fond blanc, lumière du jour, pas de flash."),
    ("Semaine 2", "Test loupe x10",
     "Sur 10 pièces représentatives : grain irrégulier = vraie litho ; trame de points réguliers = offset. Décide du vocabulaire de tes annonces en conséquence."),
    ("Semaine 3", "Identifier les artistes manquants",
     "Photo macro de chaque signature illisible. Recouper avec les certificats d'authenticité et les bons de livraison de l'éditeur."),
    ("Semaine 4", "Segmentation A / B / C",
     "Croiser artiste + sujet + tirage + doubles. Vise environ 15 % en A, 45 % en B, 40 % en C."),
    ("Semaines 5-8", "Test de marché",
     "Mettre en vente 8 à 10 pièces seulement : 3 en enchères (Drouot Online / Interencheres), 3 sur eBay au prix cible, 3 sur Le Bon Coin en remise en main propre Paris. Noter les prix obtenus."),
    ("Semaine 9", "Recalibrer",
     "Réviser tous les prix cibles à partir des résultats réels. C'est ici que le tableau de bord sert."),
    ("Mois 3-12", "Écoulement du segment A puis B",
     "5 à 10 annonces actives en permanence, jamais deux fois la même image. Renouveler chaque pièce vendue."),
    ("Mois 3-24", "Segment C en lots",
     "Lots thématiques de 5 à 20 sur eBay/Catawiki, ou cession en bloc à un marchand (compter 20-30 % du prix de détail, mais tout part d'un coup)."),
    ("En parallèle", "Consignation en salle",
     "Prendre rendez-vous avec 2-3 maisons parisiennes (Drouot, Millon, Lucien Paris, Richard). Estimation gratuite. Leur confier des lots groupés d'artistes secondaires."),
    ("En continu", "Logistique",
     "Tubes rigides Ø10 cm et pochettes cristal. Pour du 56x76, la remise en main propre à Paris évite 15-25 € de port et les litiges pour pliure — privilégie-la."),
]
for ri, (a, b, c) in enumerate(plan, start=5):
    pl.cell(ri, 2, a).font = BOLD
    pl.cell(ri, 3, b).font = BLACK
    cc = pl.cell(ri, 4, c)
    cc.font = BLACK
    cc.alignment = Alignment(wrap_text=True, vertical="top")
    pl.cell(ri, 5, "").fill = YELLOW
    for ci in range(2, 6):
        pl.cell(ri, ci).border = BOX
        pl.cell(ri, ci).alignment = Alignment(wrap_text=True, vertical="top")
    pl.row_dimensions[ri].height = 46

pl.cell(17, 2, "Comparatif des canaux").font = Font(name=FONT, size=11, bold=True, color="1F3864")
for i, h in enumerate(["Canal", "Frais vendeur", "Vitesse / effort", "Pour quel segment"], start=2):
    c = pl.cell(18, i, h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.border = BOX
    c.alignment = Alignment(horizontal="center", wrap_text=True)

canaux = [
    ("Le Bon Coin (Paris)", "0 %", "Rapide, main propre, zéro port", "A et B — le meilleur rapport effort/net pour du 56x76"),
    ("eBay", "~12 % + port", "Moyen, audience large", "A et B, et lots du segment C"),
    ("Catawiki", "~12,5 % vendeur", "Lent (sélection), acheteurs internationaux", "A surtout — met en valeur les belles pièces"),
    ("Enchères en salle", "15-25 % + frais", "Aucun effort, mais prix bas et invendus", "C et doubles, ou test de marché"),
    ("Marchand en gros", "20-30 % du détail", "Immédiat, tout part", "C — la queue de collection"),
    ("Etsy", "~9 % + port", "Lent, marché déco international", "B, sujets décoratifs"),
    ("Galerie en dépôt-vente", "30-50 %", "Très lent", "A uniquement, si la galerie est spécialisée estampe"),
]
for ri, row in enumerate(canaux, start=19):
    for ci, val in enumerate(row, start=2):
        c = pl.cell(ri, ci, val)
        c.font = BLACK
        c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical="top")
    pl.row_dimensions[ri].height = 30

wb.save(OUT)
print("écrit :", OUT)
