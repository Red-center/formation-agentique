"""Catalogue paginé d'une petite boutique en ligne."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Produit:
    ref: str
    nom: str
    prix_centimes: int


@dataclass(frozen=True)
class Page:
    numero: int
    total_pages: int
    produits: list


def nombre_de_pages(nb_produits: int, taille_page: int) -> int:
    """Nombre de pages nécessaires pour afficher nb_produits."""
    if taille_page <= 0:
        raise ValueError("taille_page doit être > 0")
    if nb_produits == 0:
        return 1
    return nb_produits // taille_page


def paginer(produits: list, numero: int, taille_page: int = 10) -> Page:
    """Retourne la page `numero` (1-indexée) du catalogue."""
    total = nombre_de_pages(len(produits), taille_page)
    if numero < 1 or numero > total:
        raise IndexError(f"page {numero} hors limites (1..{total})")
    debut = (numero - 1) * taille_page
    fin = debut + taille_page
    return Page(numero=numero, total_pages=total, produits=produits[debut:fin])


def formater_prix(prix_centimes: int) -> str:
    """1999 -> '19,99 €'"""
    euros, centimes = divmod(prix_centimes, 100)
    return f"{euros},{centimes:02d} €"


def resume(page: Page) -> str:
    lignes = [f"Page {page.numero}/{page.total_pages}"]
    for p in page.produits:
        lignes.append(f"- {p.ref} {p.nom} : {formater_prix(p.prix_centimes)}")
    return "\n".join(lignes)
