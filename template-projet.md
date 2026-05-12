## Template (Cookiecutter + Cruft)

**Paramétisation Cookiecutter** : tout le projet est un template instanciable. Les variables (`{{cookiecutter.use_case_name}}`, `{{cookiecutter.python_package_name}}`, etc.) apparaissent dans les noms de dossiers, les fichiers de configuration, les URL, les noms de ressources Azure, et même dans le code source Python.

**Synchronisation avec le template parent** (`[tool.cruft]` dans `pyproject.toml`) : `cruft` permet de resynchroniser un projet instancié avec les évolutions du template d'origine. La liste `skip` définit explicitement les dossiers propres au projet (code métier, tests, doc) qui ne doivent pas être écrasés lors d'une mise à jour.

**Workflow de mise à jour automatique** : `update-from-template.yaml` déclenche la synchronisation via GitHub Actions et ouvre une pull request avec les différences à fusionner.

---

## Standards de code Python

### Formatage — Ruff
- Longueur de ligne : **120 caractères**
- `ruff format` + tri des imports (`ruff check . --select I`)
- Couvre aussi les **notebooks Jupyter** (`extend-include = ["*.ipynb"]`)
- Échappement `# fmt: off / # fmt: on` documenté pour les rares exceptions

### Linting — Ruff (`select = ["ALL"]`)
Toutes les règles Ruff sont activées par défaut. Les exclusions sont explicitement justifiées :

| Famille ignorée | Raison |
|---|---|
| `D` (pydocstyle) | Docstrings non obligatoires |
| `ANN` (annotations) | Types non exigés partout |
| `FIX` (fixme) | TODO autorisés en dev |
| `COM` (commas) | Conflit avec le formateur |
| `G004` | Loguru n'utilise pas le lazy logging standard |

Règles spécifiques par fichier :
- `tests/*` : `S101` ignoré (assert autorisé)
- `noxfile.py` : familles `A` et `SIM` ignorées (code historique)
- `_version.py` : règles de style ignorées (fichier auto-généré)
- `doc/examples/*.py` et `*.ipynb` : `E402` ignoré (imports non placés en tête de fichier acceptés)

Limites de complexité :
- **Complexité cyclomatique max : 10** (McCabe)
- **Nombre max d'arguments par fonction : 10** (pylint)

### Imports
- **Imports relatifs interdits** : `ban-relative-imports = "all"` — tous les imports doivent être absolus.

### Copyright
- **En-tête obligatoire** sur chaque fichier non vide : `# © YYYY - YYYY Schneider Electric Industries SAS. All rights reserved.`
- Vérifié par la règle `CPY001` (Ruff preview).

### Typage statique — mypy
- Plugin Pydantic activé
- `check_untyped_defs = true` : les fonctions sans annotations sont quand même vérifiées
- `warn_redundant_casts`, `warn_unused_ignores` activés
- `disallow_untyped_defs = false` : non bloquant (mais encouragé)
- Module `azure.*` entièrement ignoré (stubs incomplets)
- `init_forbid_extra = true` sur les modèles Pydantic

---

## Tests et couverture

- **Seuil de couverture : 80%** (`fail_under = 80`) — la configuration de `pyproject.toml` indique 80, le code et `AGENTS.md` mentionnent 79 à un endroit ; le chiffre dans `pyproject.toml` fait foi.
- `branch = true` : couverture des branches (pas seulement des lignes)
- `addopts = "-s"` : les logs apparaissent en direct pendant les tests
- Exclusions de couverture documentées : blocs `TYPE_CHECKING`, méthodes abstraites, `__repr__`, etc.

---

## Sécurité des secrets — Gitleaks

- Héritage de la configuration par défaut Gitleaks (`useDefault = true`)
- Règle `generic-api-key` avec **whitelist explicite** des faux positifs connus (noms de Key Vault, UUID de partition CosmosDB)
- Hook pre-commit Gitleaks **v8.21.2** : bloque tout commit contenant un secret détecté

---

## Dockerfile — Hadolint

- Seuil : erreur uniquement (`failure-threshold: "error"`)
- Labels stricts (`strict-labels: true`), versioning `semver`
- Deux règles ignorées documentées : `DL3008` (pin apt versions), `DL3049` (label manquant)

---

## Gestion des changements

- **CHANGELOG** au format [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- **Versioning SemVer** strict depuis les tags Git
- **Template de PR** avec lien vers le processus de code review interne SE
- **Templates d'issues** GitHub (`.github/ISSUE_TEMPLATE/`)

---

## Résumé visuel

```
Standards de code
├── Formatage        → Ruff format (ligne ≤120, imports triés)
├── Linting          → Ruff ALL (complexité ≤10, args ≤10, imports absolus)
├── Copyright        → CPY001 (en-tête SE sur chaque fichier)
├── Typage           → mypy + pydantic plugin
├── Tests            → pytest, couverture ≥80% branches
├── Secrets          → Gitleaks pre-commit (whitelist faux positifs)
├── Dockerfile       → Hadolint (erreurs bloquantes)
└── Template         → Cookiecutter + Cruft (synchro depuis template parent)
```
