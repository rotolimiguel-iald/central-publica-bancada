### `ringdown` data release

The contents of the release are as follows:
- Each superevent ID sub-directory contains the configuration and posterior files for the relevant analyses of a given event.
- `scripts/` contains plotting scripts for Figs 6-8 of the paper, as well as utility scripts like `directories.py` and `ringdown_directories.py`. To reproduce the paper figures using the plotting scripts, the user should modify the paths in `directories.py` to their own appropriate local paths. There are also `pyproject.toml` and `uv.lock` files for the user to create a `uv` environment for plotting by running the following command in the terminal: `uv sync --python 3.11.10`. Activate the environment with the command `source .venv/bin/activate` before running any plotting scripts.
- `data/` will be populated with .hdf5 data products the first time a plotting script is run.
- `figures/` will contain the figure products of the plotting scripts.
