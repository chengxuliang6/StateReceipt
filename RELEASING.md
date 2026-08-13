# Releasing StateReceipt

## Versioning

The Python package and the StateReceipt specification have separate identities:

- package version: semantic version such as `0.1.0`;
- specification version: schema/spec value such as `0.1`.

A package patch release does not necessarily change the specification version.

## Release checklist

1. Ensure the working tree is clean.
2. Run `python -m pip install -e ".[dev]"` and `pytest`.
3. Validate all files under `examples/`.
4. Confirm `CHANGELOG.md` contains the release entry.
5. Confirm the package version in `pyproject.toml`.
6. Build distributions with `python -m build` in a clean environment.
7. Inspect wheel/sdist contents before publication.
8. Tag the commit `vX.Y.Z` only after CI succeeds.
9. Publish a GitHub Release from that tag.
10. Publish to PyPI only when package-name ownership and release contents have been reviewed.

The first public milestone is `v0.1.0`: specification draft + reference implementation, not a 1.0 stability promise.
