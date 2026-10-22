# DESI DR2 BAO: local read-only data copies

These are byte-for-byte copies made for the isolated cosmology backend. The
scientific originals were not changed or imported as executable code.

| Local file | Read-only origin | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `desi_gaussian_bao_ALL_GCcomb_mean.txt` | `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\_originais\desi_gaussian_bao_ALL_GCcomb_mean.txt` | 472 | `9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585` |
| `desi_gaussian_bao_ALL_GCcomb_cov.txt` | `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\_originais\desi_gaussian_bao_ALL_GCcomb_cov.txt` | 2547 | `252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509` |

The origin paths and hashes are recorded in
`state/D10_BAO_LINEAGE_AUDIT.json`. That audit records 13 ordered BAO means
and a 13x13 covariance. The names/provenance claim the DESI DR2 CobayaSampler
`bao_data` release; a remote release commit was not independently verified.
The backend verifies both local hashes at first load, then retains immutable
numeric tuples in RAM. It does not read the originals or the local copies on
warm evaluations. The 12-point historical N2 fallback is not this dataset.
