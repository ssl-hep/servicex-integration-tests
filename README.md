# ServiceX Integration Tests

A collection of Python scripts and ServiceX YAML configs used to exercise a
ServiceX deployment. Everything runs against the **latest release** of the
[`servicex`](https://pypi.org/project/servicex/) package.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A `servicex.yaml` with your endpoint and credentials, in the working
  directory or your home directory (see the
  [ServiceX docs](https://servicex-frontend.readthedocs.io/)).

No manual virtualenv or `pip install` is needed: `uv run` creates the
environment from `pyproject.toml` on first use.

## Running scripts

```bash
uv run rucio/dataset_torture.py
```

## Running YAML configs

```bash
uv run servicex deliver path/to/config.yaml
```

## Staying on the newest `servicex`

`servicex` is deliberately unpinned in `pyproject.toml`, and `uv.lock` is
gitignored so a stale lock never holds the version back. uv caches the
environment, though, so to pick up a newly released version, add
`--upgrade-package servicex`:

```bash
uv run --upgrade-package servicex rucio/dataset_torture.py
uv run --upgrade-package servicex servicex deliver path/to/config.yaml
```

Or upgrade the environment once with:

```bash
uv sync --upgrade-package servicex
```

Check which version you are running with `uv run servicex --version`
(or `uv pip show servicex`).

## Adding new tests

- Scripts: add them anywhere in the repo; extra third-party imports go in
  `dependencies` in `pyproject.toml` (keep `servicex` unpinned).
- Configs: add a YAML file and run it with `servicex deliver`.
