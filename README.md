# Template Doc

Python project template with:

- a small importable package;
- a console entrypoint;
- typed environment settings;
- `uv` dependency management;
- `nox` developer commands;
- Ruff, mypy, pytest, and pip-audit wiring;
- Docker and GitHub Actions scaffolding.

This repository is meant to be copied, renamed, and adapted. It is not a finished application.

## Layout

```text
template_doc/                  Python package placeholder
markdown/                      Supporting template notes
scripts/                       Repository maintenance scripts
.github/workflows/             CI and CI/CD examples
Dockerfile                     Container build scaffold
noxfile.py                     Local task runner
pyproject.toml                 Package and tool configuration
uv.lock                        Locked dependency graph
```

## Setup

```bash
uv sync --all-groups
```

Install the pre-commit hook:

```bash
uv run nox -s dev
```

Run the default checks:

```bash
uv run nox
```

Run one check:

```bash
uv run nox -s format
uv run nox -s lint
uv run nox -s typing
uv run nox -s test
uv run nox -s audit
```

The current test session is wired but there is no real test suite yet.

## CLI

```bash
template-doc
```

Default output:

```text
template-doc [development]
```

The CLI is only a packaging and configuration smoke test.

## Configuration

Environment variables:

```env
APP_NAME=template-doc
APP_ENV=development
APP_DEBUG=false
```

Settings are read from environment variables. `.env` files are not loaded automatically.

## Docker

Build the image:

```bash
uv run nox -s docker_build
```

Run the container smoke test:

```bash
uv run nox -s docker_smoke
```

Before using Docker for a real project, review the base image, entrypoint, runtime packages, ports, user, registry, tags, and publication rules.

## CI/CD

Workflows:

- `.github/workflows/ci.yaml`: runs the shared quality workflow on pushes and pull requests to `main`;
- `.github/workflows/quality.yaml`: runs audit, format, lint, typing, and tests;
- `.github/workflows/cicd.yaml`: builds the image, runs security scans, and publishes to GHCR after blocking checks pass.

Before enabling CI/CD for a real project, review branch rules, workflow permissions, registry naming, image promotion, secrets, environments, and release policy.

## Renaming Checklist

Replace the placeholders before using this as a real project:

- `template_doc/` package directory;
- `template_doc` imports;
- `template-doc` package name;
- `template-doc` CLI command;
- `PROJECT_PACKAGE` in `noxfile.py`;
- Hatch package and source distribution settings in `pyproject.toml`;
- Docker `COPY` path and `ENTRYPOINT`;
- `APP_NAME` in `.env.example`;
- project URLs containing `CHANGE_ME`;
- README and documentation text that still describes the template.

Search for leftovers:

```bash
rg "template_doc|template-doc|CHANGE_ME"
```

## Before Real Use

At minimum:

1. Rename the package and command.
2. Update `pyproject.toml` metadata.
3. Replace the example CLI with the real entrypoint.
4. Add tests for real behavior.
5. Review Docker and CI/CD before publishing anything.
6. Rewrite this README for the actual project.
