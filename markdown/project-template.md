## Personal Python Template

This repository is a neutral starting point for Python projects. It does not impose a framework, cloud provider,
business use case, or application architecture.

Goal: provide a clean, understandable, extensible foundation with enough tooling to encourage good habits from
the beginning.

---

## Project Management

### `uv`

`uv` is used to manage the local environment, dependencies, and lock file.

Useful commands:

```bash
uv sync --all-groups
uv add package-name
uv add --group dev package-name
```

The project is configured with `package = false`, so it can be used immediately even before a Python package has
been created.

### Dependency Groups

| Group | Purpose |
|---|---|
| `dev` | General development tools |
| `format` | Formatting with Ruff |
| `lint` | Linting with Ruff |
| `typing` | Static typing with mypy |
| `test` | Test tools available for a future Nox session |

---

## Nox Sessions

| Session | Purpose |
|---|---|
| `dev` | Syncs the environment and installs pre-commit hooks |
| `format` | Checks formatting and import ordering |
| `lint` | Runs Ruff on the project |
| `typing` | Runs mypy |
| `docker_build` | Builds a Docker image if a `Dockerfile` exists |

Common commands:

```bash
nox -s dev
nox -s format lint typing
```

---

## Python Code Standards

### Formatting

- Line length: **120 characters**.
- Formatting: `ruff format`.
- Import sorting: `ruff check --select I`.

### Linting

Ruff is configured with a deliberately reasonable baseline:

- `E` and `F` for common Python errors;
- `I` for import ordering;
- `B` for frequent bug patterns;
- `UP` for Python modernization;
- `SIM` for code simplification.

### Typing

Mypy is configured to check untyped functions and report unused typing artifacts:

- `check_untyped_defs = true`
- `warn_unused_configs = true`
- `warn_redundant_casts = true`
- `warn_unused_ignores = true`

Full strict mode is not enabled by default. It can be enabled per project when useful.

---

## Security

`pre-commit` only contains Gitleaks for detecting secrets before commit.

Configured hook:

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
```

---

## Base Files

| File | Purpose |
|---|---|
| `pyproject.toml` | Metadata, dependencies, and tool configuration |
| `uv.lock` | Reproducible lock file |
| `noxfile.py` | Local automation sessions |
| `.pre-commit-config.yaml` | Pre-commit hooks |
| `.gitignore` | Git exclusions for Python and local tools |
| `.vscode/settings.json` | Local Python interpreter configuration |
| `.env.example` | Example application environment variables |
| `LICENSE` | MIT license placeholder |
| `markdown/` | Project documentation |
| `src/template_doc/` | Minimal importable package scaffold |

---

## Add Per Future Project

- `README.md` to explain installation and commands.
- `tests/` as soon as application code exists.
- A Nox `test` session once tests are created.
- Rename `src/template_doc/` to match the real project package.
- `Dockerfile` only if the project needs containerization.
- CI/CD when the delivery flow becomes clear.
- Replace the license placeholder before the project is shared or published.

---

## Visual Summary

```text
Personal Python template
├── Environment        -> uv + .venv
├── Automation         -> nox
├── Formatting         -> ruff format
├── Linting            -> ruff check
├── Typing             -> mypy
├── Secrets            -> pre-commit + gitleaks
├── IDE                -> VS Code configured on .venv
└── Documentation      -> markdown/
```
