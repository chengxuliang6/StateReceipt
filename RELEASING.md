# Releasing StateReceipt

## Versioning

The Python package and the StateReceipt specification have separate identities:

- package version: semantic version such as `0.1.0`;
- specification version: schema/spec value such as `0.1`.

A package patch release does not necessarily change the specification version.

## Release-blocking checklist

A tag MUST NOT be created until every item below is satisfied for the exact commit to be tagged.

1. **Release blockers are closed.** Search the repository for open issues explicitly identified as release blockers. For v0.1.0, Issues #11, #12, and #13 must be completed.
2. **Package/spec metadata is consistent.** `pyproject.toml` and `statereceipt.__version__` must agree. Repository and packaged copies of the v0.1 JSON Schema must remain semantically identical. CI enforces these checks.
3. **CHANGELOG is final.** `CHANGELOG.md` must describe the actual release, including replay safety, lifecycle validation, multilingual documentation, and package-distribution checks.
4. **Documentation is current.** README examples must include the current replay trust model and `validate-chain`. English remains the normative specification and security source; zh-CN/es documents must be clearly labeled translations.
5. **License and provenance are reviewed.** `LICENSE`, `THIRD_PARTY_NOTICES.md`, `DESIGN_PROVENANCE.md`, and `PRIOR_ART.md` must still describe the shipped implementation accurately. No copied third-party implementation should be introduced without license review and attribution.
6. **Pull-request CI is green.** The release-preparation PR must pass the full CI workflow.
7. **Main CI is green after merge.** The exact `main` commit intended for tagging must pass all current jobs. For v0.1.0 this means:
   - 9 runtime jobs: Ubuntu/Windows/macOS × Python 3.11/3.12/3.13;
   - 1 release-package job.
8. **Built distributions pass.** The release-package job must successfully:
   - run `python -m build`;
   - build wheel and sdist;
   - install the wheel into a fresh virtual environment;
   - install the sdist into a separate fresh virtual environment;
   - run the installed CLI;
   - validate an example Receipt;
   - confirm the packaged JSON Schema resource is present.
9. **Tag does not already exist.** Confirm `vX.Y.Z` is absent before creation.
10. **Release notes are reviewed.** The release description must not overclaim originality, sandboxing, cryptographic authenticity, or proof of Claim truth.

Only after all ten checks pass should the exact `main` commit be tagged `vX.Y.Z` and a GitHub Release be created from that tag.

## Suggested local verification

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip build
python -m pip install -e ".[dev]"
pytest
statereceipt validate examples/python-auth.yaml
statereceipt validate examples/fpga-verilog.yaml
statereceipt validate examples/matlab-qpsk.yaml
python -m build
```

CI is the release gate for the cross-platform and clean-distribution checks; a maintainer should not substitute a single local platform run for the required CI results.

## GitHub Release

Use the reviewed release notes under `docs/releases/` as the basis for the GitHub Release body. The English release notes are authoritative; Chinese and Spanish translations are accessibility documents.

The first public milestone is `v0.1.0`: a specification draft plus reference implementation. It is not a 1.0 stability promise.

## PyPI is a separate release boundary

Creating a GitHub tag/release does not by itself authorize a PyPI publication.

Future PyPI publication uses `.github/workflows/publish.yml` and PyPI Trusted Publishing. The workflow:

- triggers only on a future non-prerelease GitHub Release publication;
- checks out the released tag rather than a moving branch;
- verifies `vX.Y.Z` matches the package version;
- builds wheel and sdist in an unprivileged job;
- transfers those exact distributions to a separate publish job;
- grants `id-token: write` only to the publish job;
- uses the GitHub environment named `pypi`;
- does not require a long-lived PyPI API token.

Before the first PyPI publication, maintainers MUST configure the matching PyPI Trusted Publisher/pending publisher and the GitHub `pypi` environment, and MUST re-check the `statereceipt` project name immediately before publishing.

The existing GitHub `v0.1.0` release predates the trusted publishing workflow. Do not later rebuild `0.1.0` and present the new files as the exact artifacts reviewed for that GitHub Release. Prefer a subsequent patch release for the first end-to-end PyPI publication.

See [`docs/PYPI_PUBLISHING.md`](docs/PYPI_PUBLISHING.md) for the maintainer setup and post-publication verification procedure.
