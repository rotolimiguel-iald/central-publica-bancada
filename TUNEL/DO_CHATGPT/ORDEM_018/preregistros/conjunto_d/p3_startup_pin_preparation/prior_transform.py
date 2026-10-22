"""Normalized fixed joint prior; standard library only, no data or scientific imports."""
import math
FREE = ("mass_1","mass_2","chi_1","chi_2","dtau220","luminosity_distance",
        "theta_jn","ra","dec","psi","phase","geocent_time")
FIXED = {"domega220":0.0,"dtau440":0.0,"domega440":0.0}
PERIODIC = (7,9,10)
MASS_AREA = 3477.5
def transform(u):
    if len(u)!=12 or any(not math.isfinite(v) or not 0<=v<=1 for v in u):
        raise ValueError("Twelve finite unit-cube coordinates required")
    a = float(u[0])*MASS_AREA
    if a<=1687.5:
        m1=20+math.sqrt(225+2*a)
    elif a<=2887.5:
        m1=80+(a-1687.5)/60
    else:
        v=a-2887.5
        m1=100+2*v/(60+math.sqrt(3600-0.4*v))
    low=max(20.,0.2*m1); high=min(80.,m1)
    m2=low+(high-low)*u[1]
    return [m1,m2,-.8+1.75*u[2],-.8+1.75*u[3],-.8+2.8*u[4],
            10+9990*u[5],math.acos(1-2*u[6]),2*math.pi*u[7],
            math.asin(2*u[8]-1),math.pi*u[9],2*math.pi*u[10],
            999999999.9+.2*u[11]]
def parameters(v):
    if len(v)!=12 or any(not math.isfinite(x) for x in v):
        raise ValueError("Twelve finite physical coordinates required")
    p=dict(zip(FREE,map(float,v)));p.update(FIXED)
    p["mass_ratio"]=p["mass_2"]/p["mass_1"]
    if not 0.2-1e-14<=p["mass_ratio"]<=1+1e-14:
        raise ValueError("Mass constraint is not a likelihood rejection")
    return p
