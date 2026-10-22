import h5py, numpy as np
from pathlib import Path
root=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN')
with h5py.File(root/'cache/gwosc/on_source/H-H1_GWOSC_O4b_4KHZ_R1-1420877824-4096.hdf5','r') as f:
 for k in ['quality/simple/DQmask','quality/injections/Injmask','quality/simple/DQShortnames','quality/injections/InjShortnames']:
  d=f[k]; print(k,d.shape,dict(d.attrs))
  if 'Shortnames' in k: print(d[()].tolist())
for det in ['H1','L1']:
 with np.load(root/f'cache/empirical_noise/{det}_noise.npz',allow_pickle=False) as z:
  print(det,[(k,z[k].shape) for k in z.files])
