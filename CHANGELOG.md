# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows semantic versioning.

## [Unreleased]

### Added

- Add complete README documentation for using, renaming, configuring, validating, and adapting the template.
- Add reusable GitHub Actions quality workflow for dependency audit, formatting, linting, typing, and tests.
- Add CI/CD workflow with manual dispatch, Docker image build, smoke test, Trivy image scan, Trivy filesystem scan, OSV Scanner, Gitleaks history scan, GHCR publishing, and security report artifact generation.
- Add `.trivyignore.yaml` with documented temporary vulnerability exceptions.
- Add `scripts/check-trivyignore-expiry.sh` to fail CI/CD when Trivy ignore exceptions are missing, invalid, or expired.
- Add ADR documentation for Trivy ignore exception expiry.
- Add expanded project metadata, classifiers, keywords, project URLs, and README packaging metadata in `pyproject.toml`.
- Add supporting template documentation for project structure, Docker/CI-CD behavior, requirements, and VS Code extensions.

### Changed

- Move the Python package from `src/template_doc` to direct package layout under `template_doc`.
- Update Hatch wheel and source distribution configuration for the direct `template_doc` package layout.
- Update Nox source path detection to use `template_doc` instead of `src`.
- Replace duplicated CI quality jobs with the shared `quality.yaml` workflow.
- Update CI triggers to target `main`, include manual dispatch, and call the shared quality workflow.
- Replace the previous CD workflow with the consolidated CI/CD workflow.
- Pin Docker base images more explicitly and build the project as a non-editable runtime install.
- Update the Docker build context to copy `README.md`, allowing Hatch to validate `readme = "README.md"` during image builds.
- Add a targeted runtime `libgnutls30` security upgrade in the Dockerfile.
- Update settings to ignore extra environment variables via `SettingsConfigDict(extra="ignore")`.
- Document the reusable quality workflow shared by CI and CI/CD.
- Document blocking Trivy filesystem checks for high/critical secrets and misconfigurations.

### Fixed

- Fix Docker image build failure caused by missing `README.md` during package build metadata validation.
- Fix stale documentation that referred to `src/template_doc` after the package moved to direct layout.

### Removed

- Remove the old standalone `.github/workflows/cd.yaml` workflow in favor of `.github/workflows/cicd.yaml`.
- Remove repository-level VS Code settings from the template baseline.
