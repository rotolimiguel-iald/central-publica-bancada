### pSEOB data release

* This folder includes notebooks to reproduce the figures from the pSEOBNR analysis, including auxiliary data for plotting. 

* Individual event samples (needed for running `pSEOBNR_main_figure.ipynb`) can be found in the `metafiles` folder.Note that the user should adjust the `path/to/metafiles/` in `pSEOBNR_main_figure.ipynb` accordingly. The `joint` and `hierarchical` folders contain samples for joint and hierarchically combined results.

* The notebooks `mock_catalog_figure.ipynb` and `hierarchical_2D_figure.ipynb` can be run from the standard `igwn` environments. An environment suitable for running the `pSEOBNR_main_figure.ipynb` notebook can be created from the `env.yml` file included here with
```
conda env create -f env.yml
```
