# Projet : facturation

Outil en ligne de commande qui lit des commandes en CSV, calcule HT / TVA / TTC et exporte les totaux.
Les règles de calcul sont écrites en tête de `facturation/calcul.py`.

## Commandes (depuis ce dossier)
- Installer : `make install`
- Tests : `make test` (doivent être verts avant de conclure)
- Lancer : `make total FICHIER=donnees/commandes-exemple.csv`
- Test par mutation : `make mutants`, puis `make survivants`

## Règles
- Avant de corriger un bug : un test qui le reproduit et qui échoue.
- Ne jamais supprimer ni affaiblir un test existant.
- Changements limités à la demande, pas de nouvelle dépendance.
- Toute affirmation sur le comportement s'appuie sur une exécution (commande lancée et sortie).
