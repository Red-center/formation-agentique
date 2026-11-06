from facturation.__main__ import main


def test_total_affiche_les_commandes(capsys):
    assert main(["total", "donnees/commandes-exemple.csv"]) == 0
    sortie = capsys.readouterr().out
    assert "C001" in sortie and "C005" in sortie


def test_fichier_introuvable(capsys):
    assert main(["total", "absent.csv"]) == 1
