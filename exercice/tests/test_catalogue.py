import pytest
from boutique.catalogue import Produit, paginer, nombre_de_pages, formater_prix


def catalogue(n):
    return [Produit(f"R{i:03d}", f"Produit {i}", 100 * i) for i in range(1, n + 1)]


def test_pages_exactes():
    assert nombre_de_pages(20, 10) == 2


def test_catalogue_vide_a_une_page():
    assert nombre_de_pages(0, 10) == 1


def test_derniere_page_incomplete_est_accessible():
    # Signalé par le support : "les 5 derniers produits n'apparaissent jamais"
    page = paginer(catalogue(25), 3, taille_page=10)
    assert page.total_pages == 3
    assert [p.ref for p in page.produits] == ["R021", "R022", "R023", "R024", "R025"]


def test_page_hors_limites():
    with pytest.raises(IndexError):
        paginer(catalogue(5), 2, taille_page=10)


def test_formater_prix():
    assert formater_prix(1999) == "19,99 €"
    assert formater_prix(5) == "0,05 €"
