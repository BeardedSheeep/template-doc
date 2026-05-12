#  © 2022 - 2025 Schneider Electric Industries SAS. All rights reserved.


import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import warnings
from pathlib import Path


import nox
from nox import Session


MODULE_NAME = "{{cookiecutter.python_package_name}}"


nox.needs_version = ">=2025.5.1"  # No upper bound to keep compliance with future versions
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_missing_interpreters = True
nox.options.default_venv_backend = "uv"  # Use uv backend by default for all virtual environments


# Specify which sessions will be run (in this order) at command invocation `nox`.
# If you want to run another specific session, explicitly invoke it ; for example `nox -s dev`.
nox.options.sessions = ["format", "lint", "typing", "test", "doc"]


# Technical stuff used by CI, don't touch
VERSION = os.getenv("version_number", "0.1.0")


# Configure UV "common" index for the project
jfrog_read_user = os.getenv("JFROG_READ_USER")
jfrog_read_pat = os.getenv("JFROG_READ_PAT")
if not jfrog_read_user or not jfrog_read_pat:
    raise ValueError("Please set the environment variables 'JFROG_READ_USER' and 'JFROG_READ_PAT'.")
os.environ["UV_INDEX_COMMON_USERNAME"] = jfrog_read_user
os.environ["UV_INDEX_COMMON_PASSWORD"] = jfrog_read_pat


# Python version(s) supported by this project, read from the `pyproject.toml` file.
# Just give the maximum version supported.
PYTHON_VERSIONS = nox.project.python_versions(nox.project.load_toml("pyproject.toml"), max_version="3.11")


PROJECT_DIR = Path(__file__).parent
MODULE_DIR = PROJECT_DIR / MODULE_NAME
ORCHESTRATOR_DIR = MODULE_DIR / "orchestrator"
PROCESSING_DIR = MODULE_DIR / "processing"
REQUIREMENTS_DIR = PROJECT_DIR / "requirements"
UNIT_TESTS_DIR = PROJECT_DIR / "tests" / "unit"
INTEGRATION_TESTS_DIR = PROJECT_DIR / "tests" / "integration"
E2E_TESTS_DIR = PROJECT_DIR / "tests" / "end_to_end"
DOC_DIR = PROJECT_DIR / "doc"
DOC_BUILT_DIR = PROJECT_DIR / "site"
DOC_EXTRA_DIR = DOC_DIR / "extra"  # Folder for extra static pages
REPORT_DIR = DOC_EXTRA_DIR / "reports"
PYTEST_DIR = REPORT_DIR / "pytest"
COVERAGE_DIR = REPORT_DIR / "coverage"
LINTER_DIR = REPORT_DIR / "ruff"
AI_SEARCH_DIR = PROJECT_DIR / "ai-search"
SCRIPTS_DIR = PROJECT_DIR / "scripts"
HADOLINT_DIR = REPORT_DIR / "hadolint"
DOCKERFILES = ["Dockerfile"]



# =================================== Nox development environment session ===================================
# Learn more about Nox sessions usage here:
# https://pages.github.schneider-electric.com/AIHub-Common/usage-documentation/site/verifying/nox_guide.html
@nox.session(venv_backend="none")  # Use the default uv venv
def dev(session: Session) -> None:
    """Set up an environment for a developer, which can be used by an IDE as all in one.


    The virtual environment will be created under `.venv`.
    The Python version used is always the upper allowed on the project.


    Then you can use this environment to run uv commands, such as `uv add`, `uv run`, etc.


    Usage
    -----
    > nox -s dev
    """
    session.run("uv", "sync", "--all-extras", "--all-groups", f"--python={PYTHON_VERSIONS[-1]}", external=True)
    session.run("uv", "run", "pre-commit", "install")



@nox.session(venv_backend="none")  # Use the default uv venv
def lock(session: Session) -> None:
    """Upgrade the lock file for the project. This command includes the authentication.


    Usage
    -----
    > nox -s lock
    """
    session.run("uv", "lock", "--upgrade", external=True)



@nox.session(python=PYTHON_VERSIONS[-1])
def run_local_server(session: Session) -> None:
    """Run the fast api server.


    Usage
    -----
    > nox -s run_local_server
    """
    session.run("uv", "sync", "--all-extras", "--group=orchestrator", "--group=dev", external=True)
    session.run("run_local_server")  # TODO : have an issue with "--reload" parameter



@nox.session(python=PYTHON_VERSIONS[-1])
def rag_create_dataset(session: Session) -> None:
    """Create a LangSmith dataset for RAG evaluation.


    Usage
    -----
    > nox -s rag_create_dataset
    > nox -s rag_create_dataset -- --dataset_name my_dataset
    """
    session.run("uv", "sync", "--active", "--locked", "--group=evaluation", external=True)
    session.run("rag_create_dataset", *session.posargs)



@nox.session(python=PYTHON_VERSIONS[-1])
def rag_evaluate(session: Session) -> None:
    """Run RAG offline evaluation using LangSmith.


    Requires orchestrator env vars: OPENAI_API_KEY, AZURE_ENDPOINT, VECTOR_STORE_TYPE, etc.


    Usage
    -----
    > nox -s rag_evaluate
    > nox -s rag_evaluate -- --dataset_name my_dataset --max_concurrency 4
    """
    session.run("uv", "sync", "--active", "--locked", "--group=evaluation", "--group=orchestrator", external=True)
    session.run("rag_evaluate", *session.posargs)



# =================================== Nox code quality sessions ===================================
# Mandatory for code quality, CI workflows and project gateway.
# DO NOT DEACTIVATE OR DELETE
@nox.session(python=PYTHON_VERSIONS[-1])
def format(session: Session) -> None:
    """Check all Python code is compliant with Ruff format.


    Note this also apply to the notebooks.


    If your code is not compliant, you can format it with the command `ruff format .`.
    For **very rare cases** where formatting makes code unreadable, you can enclose this code with:
        `# fmt: off` and `#fmt: on`.


    Usage
    -----
    > nox -s format
    """
    session.run("uv", "sync", "--active", "--locked", "--only-group=format", external=True)
    session.run("ruff", "check", ".", "--select", "I")  # Sort imports
    session.run("ruff", "format", ".", "--check")



@nox.session(python=PYTHON_VERSIONS[-1])
def lint(session: Session) -> None:
    """Launch Ruff linter for Python files.


    Usage
    -----
    > nox -s lint
    """
    session.run("uv", "sync", "--active", "--locked", "--only-group=lint", external=True)


    shutil.rmtree(LINTER_DIR, ignore_errors=True)
    LINTER_DIR.mkdir(parents=True)


    with (LINTER_DIR / "ruff.xml").open(mode="w") as f:
        session.run("ruff", "check", MODULE_NAME, "--output-format=junit", "--exit-zero", stdout=f, stderr=None)
    session.run("junit2html", str(LINTER_DIR / "ruff.xml"), "--report-matrix", str(LINTER_DIR / "ruff.html"))
    # To have also the complete output in CI, which fails if any error spotted
    session.run("ruff", "check", MODULE_NAME)


    # Hadolint
    shutil.rmtree(HADOLINT_DIR, ignore_errors=True)
    HADOLINT_DIR.mkdir(parents=True, exist_ok=True)
    with (HADOLINT_DIR / "hadolint.txt").open(mode="w+") as output_file:
        for dockerfile in DOCKERFILES:
            session.run("hadolint", str(dockerfile), "--verbose", "--format=gnu", "--no-fail", stdout=output_file)
            session.run("hadolint", str(dockerfile))



@nox.session(python=PYTHON_VERSIONS[-1])
def typing(session: Session) -> None:
    """Launch PEP484 type hinting checks.


    Usage
    -----
    > nox -s typing
    """
    session.run(
        "uv",
        "sync",
        "--active",
        "--locked",
        "--group=typing",
        f"--group={PROCESSING_DIR.stem}",
        f"--group={ORCHESTRATOR_DIR.stem}",
        external=True,
    )
    session.run("mypy", MODULE_NAME)



@nox.session(python=PYTHON_VERSIONS)
def test(session: Session) -> None:
    """Launch tests and coverage.


    Usage
    -----
    > nox -s test  # Launch sessions for every supported Python version
    > nox -s test-{python-version}  # Launch session for the given python version, e.g. {python-version}=3.12
    """
    session.run(
        "uv",
        "sync",
        "--active",
        "--locked",
        "--group=test",
        f"--group={PROCESSING_DIR.stem}",
        f"--group={ORCHESTRATOR_DIR.stem}",
        "--group=evaluation",
        external=True,
    )


    pytest_session_dir = PYTEST_DIR / f"python-{session.python}"
    coverage_session_dir = COVERAGE_DIR / f"python-{session.python}"
    shutil.rmtree(pytest_session_dir, ignore_errors=True)
    shutil.rmtree(coverage_session_dir, ignore_errors=True)
    pytest_session_dir.mkdir(parents=True, exist_ok=True)
    coverage_session_dir.mkdir(parents=True, exist_ok=True)


    session.run(
        "coverage",
        "run",
        "--source",
        str(MODULE_DIR),
        "-m",
        "pytest",
        str(UNIT_TESTS_DIR),
        str(INTEGRATION_TESTS_DIR),
        "--junitxml",
        f"{pytest_session_dir}/pytest.xml",
        "--html",
        f"{pytest_session_dir}/pytest.html",
    )
    # Generate html/xml reports even if coverage is not sufficient, to be able to investigate
    session.run("coverage", "html", "-d", str(coverage_session_dir), success_codes=[0, 2])
    session.run("coverage", "xml", "-o", str(coverage_session_dir / "coverage.xml"), success_codes=[0, 2])
    session.run("coverage", "report")



@nox.session(python=PYTHON_VERSIONS[-1])
def test_end_to_end(session: Session) -> None:
    """Execute end-to-end tests on a deployed environment.


    Usage
    -----
    > nox -s test_end_to_end
    """
    session.run(
        "uv",
        "sync",
        "--active",
        "--locked",
        "--group=test",
        f"--group={PROCESSING_DIR.stem}",
        f"--group={ORCHESTRATOR_DIR.stem}",
        external=True,
    )
    # Force install the package to have the _version.py file updated
    session.run("uv", "pip", "install", "-e", ".")
    env_parameters = read_env_file(environment=os.environ.get("ENVIRONMENT", "dev"))
    settings_dict = read_function_settings(
        session,
        resource_group=env_parameters["RESOURCE_GROUP"],
        function_app_name=env_parameters["PROCESSING_FUNCTION_APP_NAME"],
    )


    session.run(
        "pytest",
        str(E2E_TESTS_DIR),
        env={
            "AI_SEARCH_ENABLED": settings_dict.get("AI_SEARCH_ENABLED", "false"),
            "PG_VECTOR_ENABLED": settings_dict.get("PG_VECTOR_ENABLED", "false"),
            "POSTGRES_USER": get_user_assigned_identity_name(session) if os.getenv("CI") else get_user_name(session),
        },
    )



def read_function_settings(session: Session, resource_group: str, function_app_name: str) -> dict:
    """Read the provided function app env variables."""
    app_settings = session.run(
        "az",
        "functionapp",
        "config",
        "appsettings",
        "list",
        "--name",
        function_app_name,
        "--resource-group",
        resource_group,
        external=True,
        silent=True,
    )
    extracted_settings = re.findall(
        r"\[(.*?)\]", app_settings, re.MULTILINE | re.DOTALL
    )  # Only captures content between [ ] to exclude possible errors before the json part
    app_settings = json.loads(f"[{extracted_settings[0]}]" if extracted_settings else app_settings)
    app_settings_dict = {}
    for setting in app_settings:
        regex = re.compile(
            r"@Microsoft\.KeyVault\(SecretUri=(?P<keyvault_uri>https?://.+)/secrets/(?P<secret_name>[^/]+)/?(?P<secret_version>[a-z0-9]+)?\)"
        )
        if setting["value"] is None:
            continue
        if "KeyVault" in setting["value"] and (ref_match := re.match(regex, setting["value"])):
            app_settings_dict[setting["name"]] = get_secret_value(
                ref_match.group("keyvault_uri").split("/")[-1].split(".")[0], ref_match.group("secret_name")
            )
        else:
            app_settings_dict[setting["name"]] = setting["value"]
    return app_settings_dict



@nox.session(python=PYTHON_VERSIONS[-1])
def doc(session: Session) -> None:
    """Build the documentation.


    Usage
    -----
    > nox -s doc -- -h  # Display documentation
    > nox -s doc  # To generate the site
    > nox -s doc -- -s  # To serve the documentation on a local server for faster editing.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--serve",
        action="store_true",
        default=False,
        help="Launch a server with built documentation (changes are applied without to have to relaunch the server).",
    )


    additional_args = parser.parse_args(session.posargs)


    session.run(
        "uv",
        "sync",
        "--active",
        "--locked",
        "--group=doc",
        f"--group={PROCESSING_DIR.stem}",
        f"--group={ORCHESTRATOR_DIR.stem}",
        external=True,
    )


    session.run(
        "gizeh",
        "build",
        str(PROJECT_DIR),
        "--watch-directory",
        str(MODULE_DIR),
        "--re-ignore",
        "generated",
        "--serve" if additional_args.serve else "--",
    )



# =================================== Nox build and deploy sessions ===================================
@nox.session(python=PYTHON_VERSIONS)
def build(session: Session, output_dir: Path = PROJECT_DIR / "dist") -> Path:
    """Build wheel for this repository, and put it in the ``output_dir`` (default="dist").


    Note: the ``output_dir`` is not cleaned.


    Usage
    -----
    > nox -s build
    """
    session.run("uv", "build", "--wheel", "--out-dir", output_dir, external=True)
    # List of wheels ordered by modification time and get more recent
    return (sorted((output_dir).glob("*.whl"), key=os.path.getmtime))[-1]



def incrementally_deploy_ai_search_index(session: Session, vector_store_address: str) -> None:
    """Deploy the AI Search index."""
    logger = logging.getLogger("Deploy ai search")
    # setting up the no_proxy variable on-site
    no_proxy_rule = {}
    if not os.getenv("CI") and os.getenv("http_proxy"):
        logger.info("Local proxy detected, updating the no_proxy rule")
        no_proxy_sites = os.getenv("NO_PROXY", "").split(",")
        if ".search.windows.net" not in no_proxy_sites:
            no_proxy_rule["NO_PROXY"] = f".search.windows.net,{os.getenv('NO_PROXY', '')}"
            no_proxy_rule["no_proxy"] = os.getenv("NO_PROXY", "")
    else:
        logger.info("No proxy detected")


    # No need to install dependencies, as this depends on the deploy session


    # Deploy Index in AI Search
    if AI_SEARCH_DIR.exists() and (indices := AI_SEARCH_DIR.glob("*index*.json")):
        index_list = "|".join(str(index) for index in indices)
        session.run(
            "create_collections",
            "--indexes",
            index_list,
            "--vector_store_address",
            vector_store_address,
            env=no_proxy_rule,
        )



def get_user_name(session: Session) -> str:
    """Get the user name from the az cli."""
    return session.run(
        "az", "account", "show", "--query", "user.name", "--output", "tsv", external=True, silent=True
    ).strip()



def get_user_assigned_identity_name(session: Session) -> str:
    """Get the user assigned identity name from the az cli."""
    user_assigned_identity_info = (
        session.run(
            "az",
            "account",
            "show",
            "--query",
            "user.assignedIdentityInfo",
            "--output",
            "tsv",
            external=True,
            silent=True,
        )
        .strip()
        .split("/")
    )
    return user_assigned_identity_info[-1] if user_assigned_identity_info else ""



def deploy_pg_vector_store(
    session: Session, environment: str, read_only_users: str, write_users: str, postgres_host: str, postgres_db: str
) -> None:
    """Initialize the postgres database."""


    session.run(
        "uv",
        "sync",
        "--active",
        "--locked",
        "--group=dev",
        f"--group={PROCESSING_DIR.stem}",
        f"--group={ORCHESTRATOR_DIR.stem}",
        external=True,
    )
    session.run(
        "python",
        str(SCRIPTS_DIR / "pg_vector_deployment.py"),
        "--postgres-host",
        postgres_host,
        "--postgres-db",
        postgres_db,
        "--postgres-user",
        get_user_assigned_identity_name(session) if os.getenv("CI") else get_user_name(session),
        "--read-only-user",
        read_only_users,
        "--write-user",
        write_users,
        # Grants permissions on tables for admin user only in dev and qa
        *(["--grant-admin-users"] if environment in ["dev", "qa"] else []),
    )



# Docker cache helper for buildx
def _get_cache_from_and_to(image) -> tuple[list[str] | None, list[str] | None]:
    """
    Compute cache-from and cache-to options for Docker buildx based on CI context.
    """
    # Try to guess the base URL for images on JFrog
    org, repo = "aihub-common", "{{cookiecutter.repository_name}}"  # Adapt repo name as needed
    jfrog_repository_name = f"sd-{org.lower()}-docker-prod-fed"
    image_destination = f"global-artifacts.se.com/{jfrog_repository_name}/{{cookiecutter.python_package_name}}_{image}"
    # Main cache
    main_cache = f"type=registry,ref={image_destination}:cache"
    cache_from: list[str] | None = [main_cache]
    cache_to: list[str] | None = None
    cache_to_options = ",mode=max,oci-mediatypes=true,compression=zstd,image-manifest=true,ignore-error=true"
    # Use CI env var to mimic ctx.runs_on_github
    if os.environ.get("CI"):
        ref = os.environ.get("GITHUB_REF")
        github_event = os.environ.get("GITHUB_EVENT_NAME")
        if ref is not None:
            if ref.startswith(("refs/heads/master", "refs/heads/main", "refs/heads/develop", "refs/tags/")):
                cache_to = [main_cache + cache_to_options]
            elif ref.startswith("refs/pull/"):
                parts = ref.split("/")
                pr_number = parts[2] if len(parts) >= 3 and parts[2].isdigit() else None
                if pr_number:
                    pr_cache = f"type=registry,ref={image_destination}:cache-pr-{pr_number}"
                    cache_from.insert(0, pr_cache)
                    cache_to = [pr_cache + cache_to_options]
                else:
                    cache_to = [main_cache + cache_to_options]
        if github_event == "workflow_dispatch":
            cache_to = [main_cache + cache_to_options]
    return cache_from, cache_to



@nox.session(python=PYTHON_VERSIONS[-1])
@nox.parametrize(
    "function_app_code_path",
    [nox.param(PROCESSING_DIR, id="processing"), nox.param(ORCHESTRATOR_DIR, id="orchestrator")],
)
def docker_build(
    session: Session,
    function_app_code_path: Path,
    environment: str = os.environ.get("ENVIRONMENT", "dev"),
) -> None:
    """Builds docker images for the function apps.


    The session is executed once per function app.


    Usage
    -----
    Build all the images:
    > nox -s docker_build
    Build a specific image:
    > nox -s docker_build(orchestrator)
    > nox -s docker_build(processing)
    """
    env_parameters = read_env_file(environment=environment)
    image_version = os.getenv("IMAGE_TAG", "latest")  # IMAGE_TAG is set by the cicd pipeline
    # local image has az cli installed to authenticate to azure with interactive web browser
    build_target = "local" if image_version == "latest" else "lean"


    with tempfile.TemporaryDirectory() as build_dir:
        # Build wheel
        wheel_file_path = build(session=session, output_dir=Path(build_dir))


        # Export requirements file from the locked dependencies to be sure to be reproducible
        requirements_file = Path(build_dir) / "requirements.txt"
        session.run(
            "uv",
            "export",
            f"--group={function_app_code_path.stem}",
            "--format",
            "requirements.txt",
            "--no-hashes",
            "--no-annotate",
            "--no-header",
            "--no-emit-project",
            "--output-file",
            str(requirements_file),
            external=True,
        )


        # This local prefix is handy for faster local push to ACR
        local_prefix = (
            f"{env_parameters['CONTAINER_REGISTRY_NAME']}.azurecr.io/" if "IMAGE_TAG" not in os.environ else ""
        )


        # Copy resources needed by the Dockerfile inside the build directory
        shutil.copy("Dockerfile", Path(build_dir) / "Dockerfile")
        shutil.copy(".dockerignore", Path(build_dir) / ".dockerignore")
        shutil.copytree(function_app_code_path / "function_app", Path(build_dir) / "function_app")


        # Build docker image
        cache_from, cache_to = _get_cache_from_and_to(function_app_code_path.stem)
        docker_cmd = [
            "docker",
            "buildx",
            "build",
            "--load",
            "--network=host",
            "--secret",
            "id=extra_index,env=EXTRA_INDEX",
            "--secret",
            "id=trusted_host,env=PIP_TRUSTED_HOST",
            "--build-arg",
            f"wheel_name={wheel_file_path.name}",
            f"--target={build_target}",
            "-t",
            f"{local_prefix}{{cookiecutter.python_package_name}}_{function_app_code_path.stem}:{image_version}",
        ]
        # In CI, also create a plain local ":latest" tag so the publish step can retag from it.
        # Keep this non-prefixed to match the publish loop's "docker tag $image:latest ..."
        if os.environ.get("CI") and image_version != "latest" and local_prefix == "":
            docker_cmd.extend(
                [
                    "-t",
                    f"{{cookiecutter.python_package_name}}_{function_app_code_path.stem}:latest",
                ]
            )
        docker_cmd.append(".")
        if cache_from is not None:
            for c in cache_from:
                docker_cmd.extend(["--cache-from", c])
        if cache_to is not None:
            for c in cache_to:
                docker_cmd.extend(["--cache-to", c])
        with session.chdir(build_dir):
            session.run(
                *docker_cmd,
                external=True,
                env={
                    "DOCKER_BUILDKIT": "1",
                    "EXTRA_INDEX": os.getenv(
                        "PIP_EXTRA_INDEX_URL",  # Should be set by the python-configure in the CI
                        (
                            f"https://{os.getenv('JFROG_READ_USER')}:{os.getenv('JFROG_READ_PAT')}"
                            "@global-artifacts.se.com/artifactory/api/pypi/sd-aihub-common-pypi-prod-fed/simple/"
                        ),
                    ),
                    # The trusted host should also be set by the python-configure in the CI
                    "PIP_TRUSTED_HOST": os.getenv("PIP_TRUSTED_HOST", "global-artifacts.se.com"),
                },
            )



@nox.session(python=PYTHON_VERSIONS[-1])
def docker_deploy(session: Session) -> None:
    """Deploy the locally built docker image to the ACR in order to update the Azure Function Apps.


    This ensures the connection to the ACR is OK and then push all the locally built images for the data pipeline and
    the orchestrator.


    Usage
    -------
    > nox -s docker_deploy
    """
    image_version = os.getenv("IMAGE_TAG", "latest")  # IMAGE_TAG is set by the cicd pipeline


    env_parameters = read_env_file(environment=os.environ.get("ENVIRONMENT", "dev"))
    acr_name = env_parameters["CONTAINER_REGISTRY_NAME"]
    resource_group = env_parameters["RESOURCE_GROUP"]
    function_apps = {
        env_parameters["ORCHESTRATOR_FUNCTION_APP_NAME"]: ORCHESTRATOR_DIR,
        env_parameters["PROCESSING_FUNCTION_APP_NAME"]: PROCESSING_DIR,
    }


    # Ensure you are connected to the ACR for image push
    session.run("az", "acr", "login", "-n", acr_name, external=True)


    for resource_fa, function_app in function_apps.items():
        session.run(
            "docker", "push", f"{acr_name}.azurecr.io/{{cookiecutter.python_package_name}}_{function_app.stem}:{image_version}", external=True
        )


        # Then restart the Function to take into account the changes
        session.run("az", "functionapp", "restart", "-g", resource_group, "-n", resource_fa, external=True)



@nox.session(python=PYTHON_VERSIONS[-1])
def deploy(session: Session, environment: str = os.environ.get("ENVIRONMENT", "dev")) -> None:
    """Deploy Azure Function Apps (conversational + data processing).


    Usage
    -----
    > nox -s deploy
    """
    session.run("uv", "sync", "--active", "--locked", "--group=deploy", external=True)


    image_version = os.getenv("IMAGE_TAG", "latest")  # IMAGE_TAG is set by the cicd pipeline


    env_parameters = read_env_file(environment=environment)
    resource_group = env_parameters["RESOURCE_GROUP"]
    acr_name = env_parameters["CONTAINER_REGISTRY_NAME"]
    function_apps = {
        env_parameters["ORCHESTRATOR_FUNCTION_APP_NAME"]: ORCHESTRATOR_DIR,
        env_parameters["PROCESSING_FUNCTION_APP_NAME"]: PROCESSING_DIR,
    }


    ai_search_enabled = get_secret_value(env_parameters["KEYVAULT_NAME"], "InfraEnableCognitiveSearch") == "true"
    pg_vector_enabled = (
        get_secret_value(env_parameters["KEYVAULT_NAME"], "InfraEnablePostgresqlFlexibleServer") == "true"
    )


    # Check if no vector store is enabled
    if not (ai_search_enabled or pg_vector_enabled):
        message = "No vector store enabled. Please ensure this is the desired configuration."
        logging.warning(message)
        warnings.warn(message, category=UserWarning, stacklevel=1)


    # Deploy PGVector store
    if pg_vector_enabled:
        deploy_pg_vector_store(
            session=session,
            environment=environment,
            postgres_host=env_parameters["POSTGRES_HOST"],
            postgres_db=env_parameters["POSTGRES_DB"],
            # Comma separated list of users. (e.g. "user1,user2")
            # Don't hesitate to add more users if required. Those users have to exists in the Azure Active Directory.
            read_only_users=env_parameters["ORCHESTRATOR_FUNCTION_APP_NAME"],
            write_users=env_parameters["PROCESSING_FUNCTION_APP_NAME"],
        )


    # Deploy index in AI Search
    if ai_search_enabled:
        incrementally_deploy_ai_search_index(session, env_parameters["AI_SEARCH_ENDPOINT"])


    for resource_fa, function_app in function_apps.items():
        generic_config_relative_path = function_app.relative_to(Path(__file__).parent)
        # Deploy to Azure Function App
        function_app_details = session.run(
            "az", "functionapp", "show", "-g", resource_group, "-n", resource_fa, silent=True, external=True
        )
        function_app_details = function_app_details[
            function_app_details.find("{") :
        ]  # exclude possible errors before the json part
        action = "restart" if json.loads(str(function_app_details))["state"] == "Running" else "start"


        # Set environments variables in function app based on the ones inside the deployment .env file
        session.run(
            "python",
            str(SCRIPTS_DIR / "azure_function_settings.py"),
            "--app-settings-file",
            function_app / "function_app" / "runtime-settings.env",
            "--resource-group-name",
            resource_group,
            "--function-app-name",
            resource_fa,
        )
        session.run(
            "az",
            "functionapp",
            "config",
            "container",
            "set",
            "--name",
            resource_fa,
            "--resource-group",
            resource_group,
            "--image",
            f"{acr_name}.azurecr.io/{{cookiecutter.python_package_name}}_{function_app.stem}:{image_version}",
            external=True,
        )
        session.run(
            "az",
            "functionapp",
            "config",
            "set",
            "--name",
            resource_fa,
            "--resource-group",
            resource_group,
            "--generic-configurations",
            f"@{generic_config_relative_path / 'function_app' / 'host.json'}",
            external=True,
        )
        session.run("az", "functionapp", action, "-g", resource_group, "-n", resource_fa, external=True)



# =================================== Utils ===================================
def read_env_file(environment: str) -> dict[str, str]:
    import tomllib


    environment_file_path = PROJECT_DIR / ".github" / "env" / f"{environment}.env"
    with environment_file_path.open("rb") as f:
        return tomllib.load(f)



def get_secret_value(keyvault: str, secret: str) -> str:
    """Retrieves the value of a secret from Azure Key Vault."""
    result = subprocess.run(
        [
            "az",
            "keyvault",
            "secret",
            "show",
            "--name",
            secret,
            "--vault-name",
            keyvault,
            "--query",
            "value",
            "-o",
            "tsv",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()