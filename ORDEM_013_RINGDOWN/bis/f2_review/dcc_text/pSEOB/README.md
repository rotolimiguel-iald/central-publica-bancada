### pSEOB data release

* This folder includes notebooks to reproduce the figures from the pSEOBNR analysis, including auxiliary data for plotting. 

* Individual event samples (needed for running `pSEOBNR_main_figure.ipynb`) can be downloaded from the associated Zenodo data release. Joint and hierarchically combined results for the 1000 mock catalogs of NRSur7dq4 injections in Gaussian noise (needed for running `mock_catalog_figure.ipynb`) can also be downloaded from the Zenodo data release. The `joint` and `hierarchical` folders contain samples for joint and hierarchically combined results, for all sets of events mentioned in the paper (GWTC-3, GWTC-4, excluding GW190910, including GW250114).

* The notebooks `mock_catalog_figure.ipynb` and `hierarchical_2D_figure.ipynb` can be run from the standard `igwn` environments. An environment suitable for running the `pSEOBNR_main_figure.ipynb` notebook can be created from the `env.yml` file included here with
```
conda env create -f env.yml
```
