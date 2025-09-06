# Convert the new cleaned BMP to SVG with exact filled shapes, preserving orientation.
from PIL import Image
import numpy as np

bmp_path = "/mnt/data/duckie_logo.bmp"
svg_out = "/mnt/data/duckie_logo_exactfilled.svg"

# Load and binarize: True for black pixels
img = Image.open(bmp_path).convert("L")
arr = np.array(img)
# Decide which color is "ink": if background is white (high), black is low
binary = arr < 128  # black = True
h, w = binary.shape

# Build boundary edges by cancelling shared edges between adjacent black pixels
edges = set()
def add_edge(a, b):
    key = (a, b) if a < b else (b, a)
    if key in edges:
        edges.remove(key)
    else:
        edges.add(key)

for y in range(h):
    for x in range(w):
        if not binary[y, x]:
            continue
        add_edge((x, y), (x+1, y))       # top
        add_edge((x+1, y), (x+1, y+1))   # right
        add_edge((x, y+1), (x+1, y+1))   # bottom
        add_edge((x, y), (x, y+1))       # left

from collections import defaultdict
adj = defaultdict(list)
for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)

# Trace loops
visited = set()
loops = []

def mark(u, v):
    key = (u, v) if u < v else (v, u)
    visited.add(key)

def neighbors(u):
    return sorted(adj[u])

for start in sorted(adj.keys()):
    for nb in neighbors(start):
        key = (start, nb) if start < nb else (nb, start)
        if key in visited:
            continue
        loop = [start]
        prev, cur = None, start
        nxt = nb
        mark(cur, nxt)
        prev, cur = cur, nxt
        loop.append(cur)
        while cur != start:
            # pick next not-yet-visited neighbor; simple deterministic order
            picked = None
            for cand in neighbors(cur):
                k2 = (cur, cand) if cur < cand else (cand, cur)
                if k2 not in visited:
                    picked = cand
                    break
            if picked is None:
                break
            mark(cur, picked)
            prev, cur = cur, picked
            loop.append(cur)
        loops.append(loop)

# Simplify loops by removing collinear points (orthogonal)
def simplify_orth(loop):
    if len(loop) <= 3:
        return loop
    res = [loop[0], loop[1]]
    for i in range(2, len(loop)):
        x0,y0 = res[-2]
        x1,y1 = res[-1]
        x2,y2 = loop[i]
        if (x0 == x1 == x2) or (y0 == y1 == y2):
            res[-1] = (x2,y2)
        else:
            res.append((x2,y2))
    if res[0] != res[-1]:
        res.append(res[0])
    return res

loops_simplified = [simplify_orth(l) for l in loops]

# Build SVG with even-odd fill
subpaths = []
for loop in loops_simplified:
    cmds = [f"M {loop[0][0]} {loop[0][1]}"]
    for (x,y) in loop[1:]:
        cmds.append(f"L {x} {y}")
    cmds.append("Z")
    subpaths.append(" ".join(cmds))

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
    f'<path d="{" ".join(subpaths)}" fill="black" stroke="none" fill-rule="evenodd"/>',
    '</svg>'
]

with open(svg_out, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

svg_out
