# Specification — Generic Python Template


## 1. Objective


This repository aims to provide a clean, minimal, and reusable Python foundation to start any type of project: library, CLI, API, automation, internal tool, prototype, or more complete application.


The template is intentionally neutral:


- no dependency on any organization;
- no dependency on a specific infrastructure platform;
- no imposed business logic;
- no premature application architecture;
- a well-tooled, clean base that is easy to evolve.


The guiding principle is simple: provide common foundations, then let each project add only what it needs.


---


## 2. Expected Functional Scope


### Included in the template


- Python project management with `uv`.
- Local automation with `nox`.
- Reproducible development environment.
- Formatting and linting with `ruff`.
- Static typing with `mypy`.
- Secret detection via `pre-commit` and `gitleaks`.
- Minimal VS Code configuration.
- `.gitignore` suited for Python projects.
- Markdown documentation for project framing.
- Development dependencies useful for most projects.


### Explicitly out of scope


- Imposed application architecture.
- Imposed web framework.
- Imposed database.
- Imposed message queue.
- Imposed AI engine.
- Imposed infrastructure provider.
- Imposed CI/CD.
- Imposed advanced packaging.
- Imposed `src/` structure or application package as long as the use case is unknown.


---


## 3. Current Repository Structure


```text
template-doc/
├── .gitignore
├── .pre-commit-config.yaml
├── .vscode/
│   └── settings.json
├── markdown/
│   ├── cahier-des-charges.md
│   ├── project-template.md
│   └── vscode-extensions.md
├── noxfile.py
├── pyproject.toml
└── uv.lock
```


Local cache and environment directories (`.venv/`, `.nox/`, `.mypy_cache/`, `.ruff_cache/`, `__pycache__/`) are considered local artifacts and must remain ignored by Git.


---


## 4. Existing Tooling


### 4.1 Dependency management


The project uses `uv` with a simple `pyproject.toml`:


- `package = false` to allow immediate usage without an existing Python package;
- `dependencies = []` to avoid imposing runtime dependencies;
- dependency groups separated by usage.


Available groups:


| Group | Usage |
|---|---|
| `dev` | General development tools |
| `format` | Formatting and import sorting |
| `lint` | Static analysis |
| `typing` | Type checking |
| `test` | Testing tools for future evolution |


### 4.2 Nox sessions


| Session | Status | Role |
|---|---|---|
| `dev` | Implemented | Synchronizes the environment and installs pre-commit hooks |
| `format` | Implemented | Checks import sorting and Ruff formatting |
| `lint` | Implemented | Runs Ruff on detected source paths |
| `typing` | Implemented | Runs mypy |
| `docker_build` | Partially implemented | Builds a Docker image if a `Dockerfile` exists |


### 4.3 Code quality


Ruff is configured with a reasonable baseline:


- Python errors (`E`, `F`);
- import sorting (`I`);
- common best practices (`B`, `UP`, `SIM`);
- line length set to 120 characters;
- exclusion of caches, local environments, and build directories.


Mypy is configured to:


- target Python 3.12;
- check untyped functions;
- report unnecessary casts and ignores;
- report unused configurations.


### 4.4 Basic security


`pre-commit` includes only `gitleaks` in version `v8.21.2`.


Goal: prevent accidental commits of secrets, tokens, keys, or passwords.


### 4.5 IDE configuration


VS Code points to the local environment:


```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
}
```


---


## 5. Comparison: Existing vs Remaining Work


| Area | Already implemented | Remaining work |
|---|---|---|
| Project metadata | Minimal `pyproject.toml` | Adapt `name`, `description`, authors, and version per project |
| Runtime dependencies | No imposed dependencies | Add business dependencies case by case with `uv add` |
| Dev dependencies | Groups `dev`, `format`, `lint`, `typing`, `test` | Add specialized groups if needed |
| Local environment | `.venv` managed via `uv`, `dev` session | Document installation command in a README |
| Automation | Main Nox sessions | Add a `test` session when tests are created |
| Formatting | Ruff configured | Add a Ruff pre-commit hook if desired |
| Linting | Ruff configured | Adjust rules based on project maturity |
| Typing | Mypy configured | Gradually move toward `strict = true` if justified |
| Testing | Test dependencies present | Create `tests/` and a Nox `test` session |
| Secret security | Gitleaks configured | Add local rules if needed |
| Git ignore | Clean Python base | Adjust based on added tools |
| VS Code | Local interpreter configured | Add extensions/recommendations if needed |
| Docker | Generic `docker_build` session | Create a `Dockerfile` if containerization is required |
| Documentation | `markdown/` folder present | Create a user-oriented `README.md` |
| Packaging | Disabled with `package = false` | Enable for a distributable library |
| CI/CD | Not implemented | Add GitHub Actions or another CI when delivery flow is defined |
| Source structure | Not imposed | Create `src/`, a package, CLI, or app depending on needs |
| Application config | Not imposed | Add `.env.example`, settings, or config only if needed |
| License | Not present | Add a license if the project is to be shared |


---


## 6. Recommendations for a Truly Robust Base


### Priority 1 — Immediately useful foundation


1. Add a minimal `README.md` with installation, Nox commands, and conventions.
2. Add a `test` Nox session.
3. Add a Ruff hook in `.pre-commit-config.yaml`.
4. Add a `tests/` directory with an initial smoke test.
5. Add a `.env.example` if future projects use environment variables.


### Priority 2 — When a real project starts


1. Choose a source structure (`src/<package>/` or root package).
2. Add only the required runtime dependencies.
3. Create the first application modules.
4. Enable packaging if the project must be installable as a library.
5. Add a `Dockerfile` only if deployment requires it.


### Priority 3 — When the project becomes serious


1. Add CI.
2. Publish test and coverage reports.
3. Define a versioning strategy.
4. Add a release policy.
5. Document project-specific architecture conventions.


---


## 7. Reference Commands


Full installation:


```bash
uv sync --all-groups
```


Developer setup:


```bash
nox -s dev
```


Local quality checks:


```bash
nox -s format lint typing
```


Add a runtime dependency:


```bash
uv add package-name
```


Add a development dependency:


```bash
uv add --group dev package-name
```


---


## 8. Conclusion


The template is now oriented toward a generic foundation: it provides essential tooling without locking future projects into a domain, platform, architecture, or organization.


The current base is solid for getting started, but it intentionally remains incomplete on the application side. The next important improvements are the `README.md`, the `test` session, an initial test directory, and possibly a source structure once the first real use case is known.
