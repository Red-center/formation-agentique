import pytest

from facturation.lecture import ErreurDonnees, lire_commandes

ENTETE = "commande,produit,prix_unitaire,quantite,remise_pct,tva_pct\n"


def ecrire(tmp_path, contenu):
    f = tmp_path / "c.csv"
    f.write_text(ENTETE + contenu, encoding="utf-8")
    return str(f)


def test_regroupe_par_commande(tmp_path):
    chemin = ecrire(tmp_path, "A,x,1,1,0,20\nB,y,2,1,0,20\nA,z,3,1,0,20\n")
    commandes = lire_commandes(chemin)
    assert list(commandes) == ["A", "B"]
    assert len(commandes["A"]) == 2


def test_quantite_negative_refusee(tmp_path):
    with pytest.raises(ErreurDonnees):
        lire_commandes(ecrire(tmp_path, "A,x,1,-1,0,20\n"))
