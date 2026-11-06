"""Calcul des montants d'une commande.

Règles de facturation (voir conditions générales de vente, art. 7) :
- montant HT d'une ligne = prix unitaire x quantité, moins la remise de la ligne ;
- chaque montant HT de ligne est arrondi au centime, les demi-centimes vers le haut ;
- la TVA est calculée par taux, sur la somme des HT de ce taux, arrondie de la même façon ;
- TTC = total HT + total TVA.
"""
from dataclasses import dataclass

from .lecture import Ligne


@dataclass(frozen=True)
class Totaux:
    ht: float
    tva: float
    ttc: float


def arrondir(montant: float) -> float:
    """Arrondit au centime."""
    return round(montant, 2)


def montant_ht(ligne: Ligne) -> float:
    brut = ligne.prix_unitaire * ligne.quantite
    return arrondir(brut * (1 - ligne.remise_pct / 100))


def totaux(lignes: list[Ligne]) -> Totaux:
    ht_par_taux: dict[float, float] = {}
    for ligne in lignes:
        ht_par_taux[ligne.tva_pct] = ht_par_taux.get(ligne.tva_pct, 0) + montant_ht(ligne)
    ht = arrondir(sum(ht_par_taux.values()))
    tva = arrondir(sum(arrondir(base * taux / 100) for taux, base in ht_par_taux.items()))
    return Totaux(ht=ht, tva=tva, ttc=arrondir(ht + tva))
