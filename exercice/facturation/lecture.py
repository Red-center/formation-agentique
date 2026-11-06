"""Lecture des commandes depuis un fichier CSV."""
import csv
from dataclasses import dataclass

COLONNES = ["commande", "produit", "prix_unitaire", "quantite", "remise_pct", "tva_pct"]


class ErreurDonnees(ValueError):
    """Une ligne du fichier est invalide."""


@dataclass(frozen=True)
class Ligne:
    commande: str
    produit: str
    prix_unitaire: float
    quantite: int
    remise_pct: float
    tva_pct: float


def _ligne_depuis(row: dict, numero: int) -> Ligne:
    try:
        ligne = Ligne(
            commande=row["commande"].strip(),
            produit=row["produit"].strip(),
            prix_unitaire=float(row["prix_unitaire"]),
            quantite=int(row["quantite"]),
            remise_pct=float(row["remise_pct"] or 0),
            tva_pct=float(row["tva_pct"]),
        )
    except (KeyError, ValueError) as exc:
        raise ErreurDonnees(f"ligne {numero} : valeur illisible ({exc})") from exc
    if ligne.quantite < 0:
        raise ErreurDonnees(f"ligne {numero} : quantité négative")
    if not 0 <= ligne.remise_pct <= 100:
        raise ErreurDonnees(f"ligne {numero} : remise hors de 0..100")
    return ligne


def lire_commandes(chemin: str) -> dict[str, list[Ligne]]:
    """Retourne les lignes regroupées par numéro de commande, dans l'ordre du fichier."""
    commandes: dict[str, list[Ligne]] = {}
    with open(chemin, newline="", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames is None:
            return {}
        manquantes = [c for c in COLONNES if c not in lecteur.fieldnames]
        if manquantes:
            raise ErreurDonnees(f"colonnes manquantes : {', '.join(manquantes)}")
        for numero, row in enumerate(lecteur, start=2):
            ligne = _ligne_depuis(row, numero)
            commandes.setdefault(ligne.commande, []).append(ligne)
    return commandes
