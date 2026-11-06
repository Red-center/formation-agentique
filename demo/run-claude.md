# Exécution réelle — Claude Code headless (06/11/2026 10:19 Paris)

Agent : Claude Code, modèle Opus, effort low, dans `exercice/`. Commande :

```bash
claude -p "Ticket support : « les derniers produits du catalogue n'apparaissent jamais quand il y en a 25 ». Corrige le bug en suivant CLAUDE.md ; pytest -q doit passer." \
  --model opus --effort low --permission-mode acceptEdits --allowedTools "Bash(pytest*)" Read Edit
```

## Avant : `pytest -q`
```
boutique/catalogue.py:32: IndexError
=========================== short test summary info ============================
FAILED tests/test_catalogue.py::test_derniere_page_incomplete_est_accessible
1 failed, 4 passed in 0.01s
```

## Réponse de l'agent

C'est corrigé : `pytest -q` passe (5 tests verts).

- **Cause :** `nombre_de_pages` (`boutique/catalogue.py:25`) arrondissait le nombre de pages vers le bas avec `nb_produits // taille_page`. Avec 25 produits et 10 par page, on obtenait 2 pages au lieu de 3, et la page 3, qui contient les 5 derniers produits, était refusée comme « hors limites ».
- **Correction :** le calcul arrondit maintenant vers le haut : `-(-nb_produits // taille_page)`. C'est la seule ligne modifiée.
- **Test qui le prouve :** `test_derniere_page_incomplete_est_accessible` reproduit le ticket (25 produits, page 3 → R021 à R025). Il échouait avant la correction et passe maintenant. Le cas était déjà couvert, donc je n'ai pas ajouté de test.

Rien n'a été commité.

## Diff produit
```diff
diff --git a/exercice/boutique/catalogue.py b/exercice/boutique/catalogue.py
index 7dbda98..b9d01d4 100644
--- a/exercice/boutique/catalogue.py
+++ b/exercice/boutique/catalogue.py
@@ -22,7 +22,7 @@ def nombre_de_pages(nb_produits: int, taille_page: int) -> int:
         raise ValueError("taille_page doit être > 0")
     if nb_produits == 0:
         return 1
-    return nb_produits // taille_page
+    return -(-nb_produits // taille_page)
 
 
 def paginer(produits: list, numero: int, taille_page: int = 10) -> Page:
```

## Après : `pytest -q` (relancé par le formateur)
```
.....                                                                    [100%]
5 passed in 0.01s
```

## Grille 5 questions
1. Cause : oui (arrondi vers le bas du nombre de pages). 2. Tests intacts, verts : oui. 3. Diff minimal : 1 ligne. 4. Cas limites : 0 produit et 20/10 couverts. 5. Défendable : oui — discussion possible : `math.ceil` serait plus lisible que `-(-a // b)`.

Le dépôt est remis à l'état bugué pour les participants ; le correctif est dans `demo/diff.patch`.
Codex CLI : non exécuté (quota épuisé jusqu'au 09/11), commande documentée dans `guide.md`.
