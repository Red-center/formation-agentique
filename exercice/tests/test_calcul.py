from facturation.calcul import montant_ht, totaux
from facturation.lecture import Ligne


def ligne(prix, qte, remise=0, tva=20, commande="C1"):
    return Ligne(commande, "x", prix, qte, remise, tva)


def test_montant_ht_sans_remise():
    assert montant_ht(ligne(3.50, 4)) == 14.00


def test_montant_ht_avec_remise():
    assert montant_ht(ligne(10.00, 2, remise=10)) == 18.00


def test_totaux_une_ligne():
    t = totaux([ligne(10.00, 1)])
    assert (t.ht, t.tva, t.ttc) == (10.00, 2.00, 12.00)


def test_totaux_deux_taux_de_tva():
    t = totaux([ligne(8.90, 2, tva=5.5), ligne(0.80, 3)])
    assert t.ht == 20.20
    assert t.ttc == 21.66
