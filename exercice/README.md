# Exercice niveau 1 — « Le premier bug corrigé »

Ticket support : *« Sur le catalogue, les derniers produits n'apparaissent jamais quand il y en a 25. »*

```bash
cd exercice
python -m venv .venv && . .venv/bin/activate && pip install pytest
pytest -q            # 1 test rouge : c'est le bug
```

1. Relire `CLAUDE.md` / `AGENTS.md` (fichier d'instructions de l'agent).
2. Lancer votre agent (voir `../guide.md`) : `claude`, `codex` ou `opencode`.
3. Demander : « Corrige le bug du ticket ; pytest -q doit passer. »
4. `pytest -q` vert, puis `git diff` relu avec la grille en 5 questions.
