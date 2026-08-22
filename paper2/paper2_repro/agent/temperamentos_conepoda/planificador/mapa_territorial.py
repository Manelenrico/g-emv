"""Reconstrucción del mapa territorial de la ventana egocéntrica (D2, Lab 1.2b).

Desde los marcadores direccionales de frontera (territory:{N,S,E,W}, encoding D0 verificado:
valor = here*3 + vecino) + territory:here, reconstruye el territorio (0 neutral / 1 propio / 2 rival)
de CADA celda del ventana 13×13 por flood-fill a través de aristas sin frontera. Sin tocar el motor.
"""
from __future__ import annotations
from collections import deque

STRIDE = 16          # empaquetado del ventana egocéntrica (13 usadas + padding)
AGENT_ROWCOL = (6, 6)
GRID = 13
_DIR = {"N": (-1, 0), "S": (+1, 0), "E": (0, +1), "W": (0, -1)}
_OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}


def reconstruct_map(scalar_map: dict, here: int,
                    fid_terr: dict[int, str],
                    global_loc: int, padding_loc: int) -> dict[tuple[int, int], int]:
    """scalar_map: {(loc,fid):val}. fid_terr: {fid:'N'/'S'/'E'/'W'}. here: territory:here (0/1/2).
    Devuelve {(row,col): territorio} para las celdas alcanzables del ventana."""
    known: dict[tuple[int, int], int] = {}
    boundaries: dict[tuple[int, int, str], int] = {}
    ar, ac = AGENT_ROWCOL
    known[(ar, ac)] = here if here is not None else 0

    for (loc, fid), val in scalar_map.items():
        if fid not in fid_terr:
            continue
        if loc == global_loc or loc == padding_loc:
            continue
        r, c = divmod(loc, STRIDE)
        if not (0 <= r < GRID and 0 <= c < GRID):
            continue
        d = fid_terr[fid]
        here_cell, nbr = val // 3, val % 3
        known[(r, c)] = here_cell
        dr, dc = _DIR[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < GRID and 0 <= nc < GRID:
            known[(nr, nc)] = nbr
        boundaries[(r, c, d)] = nbr

    # Flood-fill: propaga territorio a vecinos SIN frontera (misma región).
    q = deque(known.keys())
    while q:
        r, c = q.popleft()
        t = known[(r, c)]
        for d, (dr, dc) in _DIR.items():
            nr, nc = r + dr, c + dc
            if not (0 <= nr < GRID and 0 <= nc < GRID):
                continue
            if (nr, nc) in known:
                continue
            if (r, c, d) in boundaries:
                nt = boundaries[(r, c, d)]
            elif (nr, nc, _OPP[d]) in boundaries:
                nt = boundaries[(nr, nc, _OPP[d])]
            else:
                nt = t  # sin frontera ⇒ misma región
            known[(nr, nc)] = nt
            q.append((nr, nc))
    return known


def territory_at(cell_map: dict, drow: int, dcol: int, default: int = 0) -> int:
    """Territorio predicho de la celda a (drow,dcol) del agente (para el forward model de mapa)."""
    ar, ac = AGENT_ROWCOL
    return cell_map.get((ar + drow, ac + dcol), default)
