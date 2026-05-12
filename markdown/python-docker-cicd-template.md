# Python Docker CI/CD Template

## Objective

Provide a reusable Python template for projects built and deployed as Docker images.

The template must be simple, secure by default, and ready to duplicate for new projects.

## Target Structure

```text
template-doc/
├── .github/
│   └── workflows/
│       ├── ci.yaml
│       └── cd.yaml
├── .vscode/
│   └── settings.json
├── markdown/
├── src/
│   └── template_doc/
├── tests/
├── .dockerignore
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── LICENSE
├── noxfile.py
├── pyproject.toml
├── README.md
└── uv.lock
```

## Tooling

| Need | Tool |
|---|---|
| Environment and dependencies | `uv` |
| Local automation | `nox` |
| Formatting and linting | `ruff` |
| Static typing | `mypy` |
| Tests and coverage | `pytest`, `coverage` |
| Python dependency audit | `pip-audit` |
| Secret detection | `gitleaks` |
| Container build | Docker |
| Container registry | GHCR |
| Image and repository scanning | Trivy |
| Dependency scanning | OSV Scanner |
| CI/CD | GitHub Actions |

## Local Workflow

```bash
uv sync --all-groups
nox -s dev
nox
```

## Nox Sessions

| Session | Purpose |
|---|---|
| `dev` | Bootstrap the local environment and install pre-commit hooks |
| `format` | Check formatting and import ordering with Ruff |
| `lint` | Run Ruff lint checks |
| `typing` | Run Mypy |
| `test` | Run Pytest, and pass when no tests exist yet |
| `audit` | Run `pip-audit` |
| `docker_build` | Build the Docker image |
| `docker_smoke` | Run a minimal container smoke test |

## Pre-commit

The repository uses one Git hook: `pre-commit`.

It runs:

- Gitleaks secret detection;
- Nox quality sessions: `format`, `lint`, `typing`, `test`.

## CI

The CI workflow runs on every pushed commit and pull request update.

```yaml
on:
  push:
  pull_request:
```

It runs:

```bash
nox -s audit
nox -s format
nox -s lint
nox -s typing
nox -s test
```

The dependency audit runs first. The four quality sessions then run as parallel blocking checks.

## CD

The CD workflow runs after a pull request is validated and merged into `master`.

```yaml
on:
  push:
    branches: [master]
```

Branch protection must require pull request validation before merging into `master`.

It performs:

- Docker image build;
- container smoke test;
- image push to GHCR;
- image scan with Trivy;
- repository scan with Trivy filesystem mode;
- dependency scan with OSV Scanner;
- Git history secret scan with Gitleaks;
- SARIF upload to GitHub Security when supported.

## Acceptance Criteria

- `uv sync --all-groups && nox -s dev` bootstraps the project.
- A commit runs the `pre-commit` hook.
- CI runs on every pushed commit and pull request update.
- CI runs without manual project-specific configuration.
- CI runs dependency audit before the quality checks.
- CI runs the four Nox quality sessions as separate blocking checks.
- The template includes a Dockerfile.
- CD builds and pushes a GHCR image after a validated pull request is merged into `master`.
- Security scans are blocking.
- Supported security scans upload SARIF results to GitHub Security.
