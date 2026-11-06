PY ?= python3
VENV = .venv
BIN = $(VENV)/bin

.PHONY: install test total mutants survivants clean

install:            ## crée l'environnement et installe pytest + mutmut
	$(PY) -m venv $(VENV)
	$(BIN)/pip install -q pytest mutmut

test:               ## lance les tests
	$(BIN)/pytest -q

FICHIER ?= donnees/commandes-exemple.csv
total:              ## affiche les totaux d'un fichier : make total FICHIER=...
	$(BIN)/python -m facturation total $(FICHIER)

mutants:            ## test par mutation (quelques minutes)
	$(BIN)/mutmut run

survivants:         ## liste les mutants que les tests n'ont pas attrapés
	$(BIN)/mutmut results

clean:
	rm -rf mutants .pytest_cache .mutmut-cache
