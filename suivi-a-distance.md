# Suivi à distance des participants

Principe : chaque participant pousse **sa branche**, la CI lance `pytest -q`, le formateur lit un tableau de statut.

## Mise en place (formateur, une fois)

1. Créer un dépôt d'exercice à partir de `exercice/` (il contient déjà `.github/workflows/tests.yml`).
2. Donner l'accès en écriture aux participants (ou leur faire forker).

## Côté participant

```bash
git clone <dépôt> && cd <dépôt>
git switch -c participant/<prenom>
# ... agent, tests, relecture du diff ...
git commit -am "Fix last catalogue page missing" && git push -u origin participant/<prenom>
```

## Workflow CI (`exercice/.github/workflows/tests.yml`)

```yaml
name: tests
on:
  push:
    branches: ["participant/**"]
  pull_request:
jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pytest
      - run: pytest -q
```

## Tableau de statut

Source : onglet *Actions* du dépôt, ou en ligne de commande :

```bash
gh run list --workflow tests.yml --json headBranch,conclusion,createdAt \
  --jq '.[] | "\(.headBranch)\t\(.conclusion)\t\(.createdAt)"'
```

| Participant | Branche | Statut | Signification | Action formateur |
|---|---|---|---|---|
| Alice | participant/alice | 🟢 vert | Tests verts | Relire son diff avec la grille |
| Bob | participant/bob | 🔴 rouge | Push fait, tests rouges | Regarder le log CI, relancer l'agent avec le log |
| Chloé | — | ⚪ bloqué | Aucun push après 30 min | Appel : installation, quota, ou consigne |

Règle « bloqué » : pas de push 30 min après le lancement, ou rouge 3 fois de suite.
Attention : vert ≠ réussi. Le vert ouvre la revue de diff (grille du `guide.md`) ; c'est elle qui valide.
