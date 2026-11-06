"""python -m facturation {total,export} FICHIER.csv [--format texte|csv]"""
import argparse
import sys

from .calcul import totaux
from .export import en_csv, en_texte
from .lecture import ErreurDonnees, lire_commandes


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="facturation")
    p.add_argument("action", choices=["total", "export"])
    p.add_argument("fichier")
    p.add_argument("--format", choices=["texte", "csv"], default="texte")
    args = p.parse_args(argv)
    try:
        commandes = lire_commandes(args.fichier)
    except FileNotFoundError:
        print(f"Erreur : fichier introuvable : {args.fichier}", file=sys.stderr)
        return 1
    except ErreurDonnees as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 2
    resultats = {numero: totaux(lignes) for numero, lignes in commandes.items()}
    if args.action == "total":
        print(en_texte(resultats))
    else:
        sys.stdout.write(en_csv(resultats) if args.format == "csv" else en_texte(resultats) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
