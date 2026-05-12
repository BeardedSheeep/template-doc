import os
import re
from pathlib import Path

import nox
from nox.sessions import Session

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = os.getenv("PROJECT_NAME", PROJECT_DIR.name)
SOURCE_PATHS = [path for path in ("src", "tests") if (PROJECT_DIR / path).exists()] or ["."]

nox.needs_version = ">=2025.5.1"
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_missing_interpreters = True
nox.options.default_venv_backend = "uv"
nox.options.sessions = ["format", "lint", "typing", "test"]


def docker_image_name() -> str:
    """Return the local Docker image name used by Docker Nox sessions."""
    default_image_name = re.sub(r"[^a-z0-9_.-]+", "-", PROJECT_NAME.lower()).strip("-") or "app"
    image_name = os.getenv("DOCKER_IMAGE", default_image_name)
    image_tag = os.getenv("DOCKER_TAG", "latest")
    return f"{image_name}:{image_tag}"


@nox.session(venv_backend="none")
def dev(session: Session) -> None:
    """Set up the local development environment."""
    session.run("uv", "sync", "--all-extras", "--all-groups", external=True)
    session.run("uv", "run", "pre-commit", "install")


@nox.session
def format(session: Session) -> None:
    """Check Python formatting and import order with Ruff."""
    session.run("uv", "sync", "--active", "--all-extras", "--all-groups", "--locked", external=True)
    session.run("ruff", "check", *SOURCE_PATHS, "--select", "I")
    session.run("ruff", "format", *SOURCE_PATHS, "--check")


@nox.session
def lint(session: Session) -> None:
    """Run Ruff lint checks."""
    session.run("uv", "sync", "--active", "--all-extras", "--all-groups", "--locked", external=True)
    session.run("ruff", "check", *SOURCE_PATHS)


@nox.session
def typing(session: Session) -> None:
    """Run mypy type checks."""
    session.run("uv", "sync", "--active", "--all-extras", "--all-groups", "--locked", external=True)
    session.run("mypy", *SOURCE_PATHS)


@nox.session
def test(session: Session) -> None:
    """Run pytest."""
    tests_dir = PROJECT_DIR / "tests"
    if not tests_dir.exists():
        session.log("tests directory not found; nothing to run")
        return

    session.run("uv", "sync", "--active", "--all-extras", "--all-groups", "--locked", external=True)
    session.run("pytest", str(tests_dir), *session.posargs)


@nox.session
def audit(session: Session) -> None:
    """Run Python dependency vulnerability checks."""
    session.run("uv", "sync", "--active", "--all-extras", "--all-groups", "--locked", external=True)
    session.run("pip-audit")


@nox.session
def docker_build(session: Session) -> None:
    """Build the project Docker image."""
    dockerfile = Path(os.getenv("DOCKERFILE", "Dockerfile"))
    if not dockerfile.exists():
        session.error(f"Dockerfile not found: {dockerfile}")

    image_name = docker_image_name()
    docker_target = os.getenv("DOCKER_TARGET")

    command = ["docker", "build", "-f", str(dockerfile), "-t", image_name]
    if docker_target:
        command.extend(["--target", docker_target])
    command.extend(session.posargs)
    command.append(".")

    session.run(*command, external=True)


@nox.session
def docker_smoke(session: Session) -> None:
    """Run a minimal smoke test against the project Docker image."""
    image_name = docker_image_name()
    command = ["docker", "run", "--rm", image_name]
    command.extend(session.posargs)
    session.run(*command, external=True)
