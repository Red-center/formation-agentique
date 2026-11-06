# Exécution réelle — Mistral Vibe CLI, non interactif (06/11/2026 10:21 Paris)

Vibe lit `AGENTS.md`. Modèle : celui de la configuration Vibe (mistral-large par défaut). Commande, depuis `exercice/` :

```bash
vibe -p "Ticket support : « les derniers produits du catalogue n'apparaissent jamais quand il y en a 25 ». Corrige le bug en suivant AGENTS.md ; pytest -q doit passer." \
  --workdir . --trust --auto-approve --max-turns 15 --max-price 1 < /dev/null
```

Durée : 45 s, code de sortie 0.

## Avant : `pytest -q`
```
1 failed, 4 passed
```

## Réponse de l'agent

`pytest -q` : 5 passed.

**Cause** : `nombre_de_pages` utilisait la division entière par le bas (`25 // 10 = 2`), donc la dernière page partielle n'existait jamais et les 5 derniers produits étaient inaccessibles.
**Correction** : division au supérieur dans `boutique/catalogue.py:22` — `(nb_produits + taille_page - 1) // taille_page`, soit 3 pages pour 25 produits.
**Test qui le prouve** : `test_derniere_page_incomplete_est_accessible` (déjà existant, couvre exactement le cas 25 produits) passe désormais ; aucun test modifié ni ajouté, diff d'une ligne.

## Diff produit
```diff
diff --git a/exercice/boutique/catalogue.py b/exercice/boutique/catalogue.py
index 7dbda98..5c73576 100644
--- a/exercice/boutique/catalogue.py
+++ b/exercice/boutique/catalogue.py
@@ -22,7 +22,7 @@ def nombre_de_pages(nb_produits: int, taille_page: int) -> int:
         raise ValueError("taille_page doit être > 0")
     if nb_produits == 0:
         return 1
-    return nb_produits // taille_page
+    return (nb_produits + taille_page - 1) // taille_page
 
 
 def paginer(produits: list, numero: int, taille_page: int = 10) -> Page:
```

## Après : `pytest -q` (relancé par le formateur)
```
5 passed in 0.01s
```

## Comparaison avec Claude Code
Les deux agents trouvent la même cause et livrent un diff d'une ligne, mais pas le même : `-(-n // t)` pour Claude Code, `(n + t - 1) // t` pour Vibe. Bon support pour la question 5 de la grille : lequel est le plus lisible ? (`math.ceil(n / t)` est une 3e option).

Le dépôt est remis à l'état bugué ; le correctif est dans `demo/diff-vibe.patch`.
