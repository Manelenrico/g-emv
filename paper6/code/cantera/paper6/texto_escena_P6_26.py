"""[P6-26 · 2] EL TEXTO DE LA ESCENA PARA EL RAZONADOR EN EL CAMPO: el relato del cinco (`_escena_relator` +
`relator_t5.relato`) + los seis numeros (P5-5B) + las palabras del seis, EXACTAMENTE como en P6-25
(`escenas_P6_25.py`; las funciones de bloque son copia literal, declaradas), mas UN bloque nuevo: el plan
que el hermano ha mandado por el canal de equipo (punto 2 del encargo). Corre en el proceso juez, sobre el
alma espejo; el hilo principal no lo toca.
"""
from __future__ import annotations
import math, re
C = (24, 24)
ARMAS = {"sword": "espada", "spear": "lanza", "bow": "arco", "knives": "cuchillos", "blowgun": "cerbatana", "net": "red"}
VENTANA_RECIENTE = 100
MARCA_PLAN = "P6"        # el mensaje del plan por el canal: "P6 P<slot> t<tick> D<x>,<y> H<H> F<fin_fase>"
_PLAN = re.compile(r"^P6 P(\d+) t(\d+) D(\d+),(\d+) H(\d+) F(\d+)$")


def mensaje_plan(slot, tick, destino, H, fin):
    s = f"P6 P{slot} t{tick} D{int(destino[0])},{int(destino[1])} H{int(H)} F{int(fin)}"
    assert len(s) <= 120 and all(0x20 <= ord(c) <= 0x7E for c in s)
    return s


def parsea_plan(texto):
    m = _PLAN.match(texto or "")
    if not m:
        return None
    g = [int(x) for x in m.groups()]
    return {"slot": g[0], "t": g[1], "destino": (g[2], g[3]), "H": g[4], "fin": g[5]}


def seg(t):
    return f"{t / 24.0:.0f} s"


def seis_numeros(V42, o, mundo, mem, tick):
    st, _radio = V42.appraise(o, mundo, mem, tick)
    return {"necesidad_cuerpo": round(st.nF, 4), "tono_cuerpo": round(st.pF - st.nF, 4), "necesidad_recursos": round(st.nR, 4), "tono_recursos": round(st.pR - st.nR, 4),
            "necesidad_vinculo": round(st.nS, 4), "tono_vinculo": round(st.pS - st.nS, 4)}


def bloque_cuerpo(seis):
    return "\n".join(["**Como esta tu cuerpo ahora, en sus seis numeros** (la necesidad va de 0 a 1: cuanto mas alta, peor; el tono es lo bueno menos lo malo):", "",
                      f"  - la vida y el peligro: necesidad {seis['necesidad_cuerpo']:.3f}, tono {seis['tono_cuerpo']:+.3f}",
                      f"  - lo que llevas en las manos: necesidad {seis['necesidad_recursos']:.3f}, tono {seis['tono_recursos']:+.3f}",
                      f"  - el vinculo con tu hermano: necesidad {seis['necesidad_vinculo']:.3f}, tono {seis['tono_vinculo']:+.3f}"])


def bloque_anillo(fases, t, pos, zona):
    i = None
    for k, f in enumerate(fases):
        if t >= f[0]:
            i = k
    r_now = float(zona.get("radius") or 48); dps = zona.get("damage_per_s")
    d = math.dist(pos, C)
    L = ["**El anillo (la zona segura es el circulo alrededor del centro (24,24); fuera de el se arde):**", ""]
    if i is None:
        L.append("  - todavia no ha empezado a cerrarse.")
    else:
        warn, shrink, done, r0, r1, dps_f = fases[i]
        L.append(f"  - fase {i + 1} de {len(fases)}. El circulo de AHORA tiene radio {r_now:g}" + (f"; fuera de el se pierden {dps} de vida por segundo." if dps else "."))
        if t < shrink:
            L.append(f"  - el circulo empieza a encogerse en el tic {shrink} (dentro de {shrink - t} tics, {seg(shrink - t)}) y en el tic {done} habra bajado al radio {r1}.")
        elif t < done:
            L.append(f"  - el circulo se esta encogiendo: en el tic {done} (dentro de {done - t} tics, {seg(done - t)}) habra bajado al radio {r1}.")
        else:
            L.append(f"  - el circulo ya esta en el radio {r1} de esta fase.")
        if i + 1 < len(fases):
            w2, s2, d2, r02, r12, dps2 = fases[i + 1]
            L.append(f"  - el SIGUIENTE aviso llega en el tic {w2} (dentro de {w2 - t} tics, {seg(w2 - t)}); ese circulo bajara del radio {r02} al {r12} entre los tics {s2} y {d2}" + (f", y fuera se perderan {dps2} de vida por segundo." if dps2 else "."))
        else:
            L.append("  - es la ultima fase: despues de esta el circulo no baja mas.")
        dentro_ahora = d <= r_now; dentro_sig = d <= r1
        L.append(f"  - tu casilla ({pos[0]},{pos[1]}) esta a {d:.1f} del centro: {'DENTRO' if dentro_ahora else 'FUERA'} del circulo de ahora y {'dentro' if dentro_sig else 'FUERA'} del circulo al que va esta fase (radio {r1}).")
        resto = [f"radio {f[4]} desde el tic {f[2]}" for f in fases[i + 1:]]
        if resto:
            L.append("  - lo que queda del calendario: " + "; ".join(resto) + ".")
    return "\n".join(L)


def bloque_yo(o):
    you = o.get("you") or {}
    hand = (you.get("hand") or {}).get("id") if isinstance(you.get("hand"), dict) else you.get("hand"); hand = hand if hand and str(hand).lower() != "none" else None; pack = you.get("pack") or []
    return "\n".join(["**Tu, ahora:**", "",
                      f"  - casilla ({you['pos'][0]},{you['pos'][1]}), vida {you.get('hp')} de 100" + (", envenenado" if any("poison" in str(e) for e in (you.get("effects") or [])) else "") + ".",
                      f"  - en la mano: {ARMAS.get(hand, hand) if hand else 'nada'}; en la mochila: " + (", ".join(f"{p.get('id')} x{p.get('n')}" for p in pack if isinstance(p, dict)) if any(isinstance(p, dict) for p in pack) else "nada") + ".",
                      f"  - piernas: {'listas para dar un paso' if int(you.get('move_ready_in') or 0) == 0 else 'ocupadas ' + str(you.get('move_ready_in')) + ' tics'}."])


def bloque_hermano(o, t, herm, muerto, parte, ult_e2):
    visto = next((a for a in ((o.get("visible") or {}).get("agents") or []) if a.get("slot") == herm and a.get("pos")), None)
    L = ["**Tu hermano:**", ""]
    if muerto:
        L.append("  - esta muerto.")
    else:
        if visto:
            L.append(f"  - lo ves: casilla ({visto['pos'][0]},{visto['pos'][1]})" + (f", vida {visto.get('hp')}" if visto.get("hp") is not None else "") + ".")
        if parte:
            edad = t - int(parte.get("t") or t)
            L.append(f"  - su ultimo parte (hace {edad} tics, {seg(edad)}): estaba en la casilla ({parte['pos'][0]},{parte['pos'][1]}) con {parte.get('hp'):g} de vida" + (", envenenado" if parte.get("veneno") else "") + (f", lleva {parte.get('botiquin')} botiquin" if parte.get("botiquin") else "")
                     + (", le estaban pegando" if parte.get("agresor") else "") + (f"; vio {len(parte.get('rivales') or [])} rivales" if parte.get("rivales") else "") + ".")
        if not visto and not parte:
            L.append("  - ni lo ves ni ha mandado parte: no sabes donde esta.")
        if ult_e2:
            L.append(f"  - su ultimo mensaje por el canal de equipo, tal cual: `{ult_e2}`")
    return "\n".join(L)


def bloque_plan_hermano(plan, t):
    """[nuevo en P6-26] el plan que el hermano mando por el canal en lugar de su parte."""
    if not plan:
        return "**El plan de tu hermano:** no te ha mandado ninguno todavia."
    edad = t - int(plan.get("t") or t)
    return "\n".join(["**El plan de tu hermano (te lo mando por el canal, hace " + f"{edad} tics, {seg(edad)}):**", "",
                      f"  - va a la casilla ({plan['destino'][0]},{plan['destino'][1]}) y se queda alli hasta el tic {plan['fin']} (su cuerpo acepto ese plan). Si puedes, ve a su lado o cerca."])


def bloque_rivales(rivales, ag, propio):
    L = ["**Los rivales:**", ""]
    if not rivales:
        L.append("  - ninguno a la vista ni contado por tu hermano.")
    for s, p, contado in rivales:
        a = ag.get(s) or {}; hand = (a.get("hand") or {}).get("id") if isinstance(a.get("hand"), dict) else a.get("hand")
        L.append(f"  - {'contado por tu hermano' if contado else 'visto'}: en la casilla ({p[0]},{p[1]}), a {math.dist(p, C):.1f} del centro" + (f", con {ARMAS.get(hand, hand)} en la mano" if hand and not contado else (", con las manos vacias" if (not contado and not hand) else "")) + (f", vida {a.get('hp')}" if (not contado and a.get("hp") is not None) else "") + ".")
    return "\n".join(L)


def bloque_reciente(hist, t):
    h = [x for x in hist if t - VENTANA_RECIENTE <= x["t"] <= t]
    if len(h) < 2:
        return "**Tu estado reciente:** acabas de empezar."
    hp0, hp1 = h[0]["hp"], h[-1]["hp"]
    anillo = sum(1 for x in h if x["zone_hit"]); riv = sum(1 for x in h if x["riv_hit"]); ard = sum(1 for x in h if x["arde"]); pasos = sum(1 for x in h if x["movio"])
    return "\n".join([f"**Tu estado reciente (los ultimos {t - h[0]['t']} tics, {seg(t - h[0]['t'])}):**", "",
                      f"  - vida: de {hp0:g} a {hp1:g}." + (f" Te ha quemado el anillo en {anillo} instantes." if anillo else " El anillo no te ha quemado.") + (f" Te han pegado rivales en {riv} instantes." if riv else " Ningun rival te ha pegado."),
                      f"  - has estado fuera del circulo {ard} de esos tics; has dado {pasos} pasos."])


def texto(alma, RT, V42, O, o, cands, t, fases, hist, ult_e2, parte, plan_hermano):
    """El texto entero, sobre el alma espejo (mem, bloqueos, mundo, tick ya puestos)."""
    e = alma._escena_relator(o, {"candidatos": dict(cands or {}), "ahora": {}})
    relato = RT.relato(e, True)
    seis = seis_numeros(V42, o, alma.mundo, alma.mem, t)
    pos = tuple(int(x) for x in (o.get("you") or {}).get("pos"))
    herm = alma.mundo.teammate_slot; propio = alma.mundo.slot
    riv = O.Oraculo.rivales_de(o, herm, propio); ag = {a.get("slot"): a for a in ((o.get("visible") or {}).get("agents") or [])}
    bloques = [bloque_anillo(fases, t, pos, o.get("zone") or {}), bloque_yo(o), bloque_hermano(o, t, herm, bool(getattr(alma.mem, "pareja_muerta", False)), parte, ult_e2),
               bloque_plan_hermano(plan_hermano, t), bloque_rivales(riv, ag, propio), bloque_reciente(hist, t)]
    return relato + "\n\n" + bloque_cuerpo(seis) + "\n\n" + "\n\n".join(bloques)
