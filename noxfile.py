import os
import tempfile

import nox
from nox.sessions import Session

locations = "src", "noxfile.py"

nox.options.sessions = "lint", "tests", "docs"


def install_with_poetry(session: Session, *args: str) -> None:
    requirements = tempfile.NamedTemporaryFile(mode="w", delete=False)
    try:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("-r", requirements.name)
        session.install(*args)
    finally:
        requirements.close()
        os.remove(requirements.name)


@nox.session(python=["3.10"])
def tests(session: Session) -> None:
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_poetry(
        session,
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-mock",
    )
    session.run("pytest", *args)


@nox.session(python=["3.10"])
def lint(session: Session) -> None:
    args = session.posargs or locations
    install_with_poetry(
        session, "flake8", "flake8-black", "flake8-bugbear", "flake8-import-order"
    )
    session.run("flake8", *args)


@nox.session(python=["3.10"])
def black(session: Session) -> None:
    args = session.posargs or locations
    install_with_poetry(session, "black")
    session.run("black", *args)


@nox.session(python=["3.10"])
def docs(session: Session) -> None:
    args = session.posargs or ["docs", "docs/_build"]
    install_with_poetry(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", *args)
