"""Pinned pure functions extracted from finite_device; no original main/import."""
import numpy as np
import math
import itertools

def residual(a): return float(np.linalg.norm(a, ord="fro"))


def vec(a): return a.reshape(-1, order="F")


def unvec(a, d): return a.reshape((d, d), order="F")


def projector(x): return np.outer(x, x.conj())


def rate(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Rate must be a finite real non-boolean number")
    if not math.isfinite(value) or value < 0:
        raise ValueError("Rate must be finite and nonnegative")
    return float(value)


def validate_density(rho, tol):
    if not np.isfinite(rho).all(): raise ValueError("Nonfinite density")
    if residual(rho-rho.conj().T) > tol: raise ValueError("Density not Hermitian")
    if abs(np.trace(rho)-1) > tol: raise ValueError("Density not normalized")
    m = float(np.linalg.eigvalsh(rho).min())
    if m < -tol: raise ValueError(f"Density not positive semidefinite: {m}")
    return m


def embed(a, region, dims):
    """Actual local matrix algebra embedding, identity on complementary factors."""
    region = tuple(region)
    local_dims = tuple(dims[i] for i in region)
    ld = math.prod(local_dims)
    if a.shape != (ld, ld): raise ValueError("Local operator dimension mismatch")
    n = math.prod(dims)
    tuples = list(itertools.product(*[range(d) for d in dims]))
    out = np.zeros((n,n), complex)
    for i, ii in enumerate(tuples):
        li = int(np.ravel_multi_index(tuple(ii[k] for k in region), local_dims)) if region else 0
        for j, jj in enumerate(tuples):
            if all(ii[k] == jj[k] for k in range(len(dims)) if k not in region):
                lj = int(np.ravel_multi_index(tuple(jj[k] for k in region), local_dims)) if region else 0
                out[i,j] = a[li,lj]
    return out


def liouvillian(h, jumps):
    d = len(h); eye = np.eye(d)
    out = -1j*(np.kron(eye,h)-np.kron(h.T,eye))
    for raw_rate, j in jumps:
        gamma = rate(raw_rate)
        q = j.conj().T@j
        out += gamma*(np.kron(j.conj(),j)-.5*np.kron(eye,q)-.5*np.kron(q.T,eye))
    return out


def direct_generator(h,jumps,rho):
    out = -1j*(h@rho-rho@h)
    for gamma,j in jumps:
        q = j.conj().T@j
        out += gamma*(j@rho@j.conj().T-.5*(q@rho+rho@q))
    return out


