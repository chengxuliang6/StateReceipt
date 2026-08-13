# PyPI Trusted Publishing runbook

StateReceipt intends to publish Python distributions to PyPI using **Trusted Publishing (OIDC)** rather than a long-lived API token.

This document is a maintainer runbook. Adding the workflow does **not** itself publish a package.

## Security model

The release workflow is `.github/workflows/publish.yml`.

It deliberately separates two trust domains:

1. **build job** — reads the released tag, verifies the tag matches `pyproject.toml`, builds wheel + sdist, checks metadata, and uploads those exact files as an immutable workflow artifact;
2. **publish job** — downloads only that artifact and receives `id-token: write` so PyPI can authenticate the workflow via OIDC.

The build job does not receive an OIDC publishing token. The publish job does not run the project build.

Third-party Actions in the workflow are pinned to full commit SHAs. Update those pins only in reviewed PRs.

## Trigger

The workflow runs only for a future GitHub Release `published` event and skips prereleases.

It is not retroactive. Adding this workflow after `v0.1.0` does not publish the existing release.

Before every future publication:

- the GitHub Release tag MUST be `v<project.version>`;
- the tag MUST refer to the reviewed source intended for publication;
- normal CI and release-package checks MUST already be green;
- package-name ownership/availability MUST be checked again immediately before first publication.

## Required GitHub environment

Create a repository environment named exactly:

```text
pypi
```

Recommended protections:

- restrict deployment to protected/release tags as appropriate;
- require maintainer approval if the repository/plan supports it;
- do not store a long-lived PyPI password or API token for the normal publication path.

The workflow references this environment by name, so the PyPI Trusted Publisher configuration must use the same environment value.

## Required PyPI publisher configuration

For a GitHub Actions Trusted Publisher, configure:

```text
PyPI project: statereceipt
Owner: chengxuliang6
Repository: StateReceipt
Workflow filename: publish.yml
Environment: pypi
```

If the PyPI project does not yet exist, configure a **pending publisher** from the PyPI account publishing page. A pending publisher does not reserve the project name; another user can register the name before the first successful publication. Re-check immediately before first use.

## Publication behavior

The publish job uses `pypa/gh-action-pypi-publish` with Trusted Publishing and no explicit username/password. The action prints distribution hashes and, under PyPI Trusted Publishing, can produce the platform-supported publication attestations.

## v0.1.0 policy

The existing GitHub `v0.1.0` release predates this publishing workflow. Do not rebuild `0.1.0` later and present the resulting files as the exact artifacts reviewed at the time of that GitHub Release.

If StateReceipt proceeds with its first PyPI publication after this workflow is merged and configured, prefer a subsequent patch release (for example `v0.1.1`) built and published end-to-end by the reviewed workflow.

## Post-publication verification

After the first successful PyPI publication, verify from a clean environment:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install statereceipt
statereceipt --help
statereceipt validate examples/python-auth.yaml
```

Also verify the PyPI project metadata links back to the canonical GitHub repository and confirm the installed package contains the StateReceipt JSON Schema resource.
