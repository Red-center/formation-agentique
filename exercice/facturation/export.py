"""Mise en forme des totaux pour l'écran ou pour un fichier."""
import csv
import io

from .calcul import Totaux


def euros(montant: float) -> str:
    """12.5 -> '12,50 €'"""
    return f"{montant:,.2f} €".replace(",", " ").replace(".", ",")


def en_texte(resultats: dict[str, Totaux]) -> str:
    if not resultats:
        return "Aucune commande."
    lignes = [f"{'Commande':<10}{'HT':>14}{'TVA':>12}{'TTC':>14}"]
    for numero, t in resultats.items():
        lignes.append(f"{numero:<10}{euros(t.ht):>14}{euros(t.tva):>12}{euros(t.ttc):>14}")
    return "\n".join(lignes)


def en_csv(resultats: dict[str, Totaux]) -> str:
    sortie = io.StringIO()
    w = csv.writer(sortie, lineterminator="\n")
    w.writerow(["commande", "ht", "tva", "ttc"])
    for numero, t in resultats.items():
        w.writerow([numero, f"{t.ht:.2f}", f"{t.tva:.2f}", f"{t.ttc:.2f}"])
    return sortie.getvalue()
