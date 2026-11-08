"""Precompute contour sheets of a smooth 3D density (sum of Gaussians along a bent path) -> contours.json.
An abstract density map for the 'stacked contours' schematic; not a molecule."""
import json, numpy as np, contourpy
from scipy.interpolate import CubicSpline
P = np.array([(0.12,0.35,0.06),(0.72,0.18,0.10),(0.93,0.48,0.27),(0.58,0.78,0.47),(0.22,0.66,0.60),
              (0.08,0.30,0.50),(0.40,0.14,0.36),(0.70,0.30,0.44),(0.88,0.66,0.66),(0.62,0.86,0.86),
              (0.24,0.74,0.94),(0.40,0.46,0.80)])  # irregular, doubles back (z not monotonic), no symmetry
t = np.linspace(0,1,len(P)); cs = CubicSpline(t,P,bc_type='natural')
ts = np.linspace(0,1,160); path = cs(ts)
sig = 0.075
g = np.linspace(0,1,120); X,Y = np.meshgrid(g,g)
N = 14
zs = [0.05 + k*(0.90/(N-1)) for k in range(N)]
sheets = []
for z in zs:
    f = np.zeros_like(X)
    for (px,py,pz) in path:
        f += np.exp(-((X-px)**2+(Y-py)**2+(z-pz)**2)/(2*sig**2))
    f = f/ f.max() if False else f
    out = []
    gen = contourpy.contour_generator(g,g,f)
    for lev in (1.2, 3.5, 6.5):
        for line in gen.lines(lev):
            if len(line) > 6:
                out.append({"lev": lev, "pts": np.round(line,4).tolist()})
    sheets.append({"z": z, "lines": out})
    print(round(z,2), len(out), round(float(f.max()),2))
json.dump({"sheets": sheets, "path": np.round(path,4).tolist()}, open('contours.json','w'))
