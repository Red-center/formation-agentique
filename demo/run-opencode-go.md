# Tentative — Claude Code sur OpenCode Go (DeepSeek Flash 4.1), 06/11/2026 10:20 Paris

Même ticket, même prompt et mêmes outils autorisés que `run-claude.md`, mais Claude Code pointé sur l'endpoint OpenCode Go (snippet brain 8b5496e7) :

```bash
CLAUDE_CONFIG_DIR=<dossier isolé> ANTHROPIC_BASE_URL=https://opencode.ai/inference/go/anthropic \
 ANTHROPIC_AUTH_TOKEN="<clé opencode-go lue depuis auth.json, non affichée>" ANTHROPIC_API_KEY= \
 ANTHROPIC_MODEL=deepseek-v4.1-flash ANTHROPIC_SMALL_FAST_MODEL=deepseek-v4.1-flash \
 claude -p "Ticket support : … Corrige le bug en suivant CLAUDE.md ; pytest -q doit passer." \
 --permission-mode acceptEdits --allowedTools "Bash(pytest*)" Read Edit
```

## Avant : `pytest -q`
```
1 failed, 4 passed
```

## Résultat : échec, aucune modification
```
[claude-code:unrecognized_model] {"model":"deepseek-v4.1-flash","query_source":"sdk"}
API Error: Request rejected (429) · Go usage limit exceeded
```
Code de sortie 1 au bout de 4 s. Aucun diff : l'arbre est resté à l'état bugué (`pytest -q` : 1 échec, 4 réussis).

**Cause** : l'endpoint et la clé sont acceptés (sinon on aurait eu une 401), le modèle est reconnu côté serveur ; c'est le **quota OpenCode Go** du compte qui est épuisé. Le même 429 avait déjà été vu le 01/11. L'avertissement `unrecognized_model` vient de Claude Code et ne bloque rien.

**À retenir pour la formation** : prévoir le cas « quota épuisé ». C'est un argument de plus pour savoir faire l'exercice avec deux outils ou deux fournisseurs.
