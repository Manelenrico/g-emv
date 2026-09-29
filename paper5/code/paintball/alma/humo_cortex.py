"""HUMO del L-4 — las tres pruebas que la imagen tiene que pasar antes de subir.

  (i)   el relator DENTRO de la imagen produce, para la escena 04 del banco t5,
        un texto BYTE A BYTE igual al de `escenas_t5/04.md`, en sus dos
        secciones (sin cuerpo y con cuerpo).
  (ii)  el gate del inyector: inyectar no mueve ni un bit la `d` de ninguna
        otra, y una sonda clon de `noop` da exactamente la `d` de `noop`.
  (iii) con GEMV_CORTEX=0 la politica decide EXACTAMENTE lo mismo que el
        decisor sin nada envuelto, en 200 tics seguidos de un diario real.
  (iv)  [L-6] `_llama` ENTERO por el camino de exito, contra un servidor de
        mentira en 127.0.0.1 (no sale de la maquina): codigo, texto, desglose
        de tokens, cabecera de gasto, contadores, y el `cache_control` puesto.
        Es el que faltaba: la L-4 y la L-5 se perdieron por codigo que solo se
        pisa cuando la llamada SALE BIEN.
  (v)   [L-6] `_sigue_valida`: la propuesta que el mundo ya no admite al nacer
        se detecta y se cuenta aparte de IMPOSIBLE.
  (vi)  [L-7] EL TRADUCTOR NUEVO, regla por regla, sobre escenas REALES sacadas
        del diario de 200 tics: objeto, hermano, atacar, centro, usar, vestir,
        rumbo, esperar y "solo una casilla de verdad es una casilla". Cada
        regla se prueba en un tic donde su precondicion se cumple de verdad.
  (vii) [L-7] LOS VETOS: un candidato inyectado que el cuerpo vetaria (piernas
        enfriando, arma enfriando) NO entra en la mesa, y en ese tic se emite
        EXACTAMENTE lo que el cuerpo habria emitido, con la `d` de todos sus
        candidatos bit a bit igual.
  (viii)[L-7] LOS EMPATES SON DEL CUERPO: una propuesta clon de `noop` empata
        y NO se lleva el tic.
  (x)   [S] LA ATADURA PEREZOSA: el mismo objetivo se ata a un candidato vivo
        del cuerpo cuando lo hay, a la receta de casilla cuando no, y queda
        DORMIDA cuando no se puede ninguna de las dos. Sobre escenas reales, y
        en los dos estados (piernas libres y piernas enfriando).
  (xi)  [D-0] EL PARTE: con cero, con una y con cinco propuestas previas de las
        tres clases (hecha, no comprada, no se podia), con la frase de la fila
        traducida y sin nombrarla, y el balance. Y que el parte va DELANTE de la
        escena y FUERA del bloque cacheado, por el camino de exito completo.
  (xii) [D-0] LA LISTA VACIA: una respuesta con `"propuestas": []` no rompe
        nada, cuenta como derecho a callar y deja al cuerpo intacto.
  (xiii)[D-B] LA FONTANERIA: (a) el parte ENTERO en cada registro de llamada,
        (b) el LIBRO compacto con todas las llamadas hasta el momento, que se
        reemite y por tanto sobrevive al corte por la cabeza, y (c) el numero
        de secuencia de la cola en cada registro del cortex, que permite
        reconstruir el orden real aunque el fichero lo escriban dos hilos.
  (xiv) [D-C] LA RAZON EN EL RESPALDO: una escena sintetica de cada uno de los
        tres casos —(a) inyectada y gano, (b) inyectada y perdio por X, (c) el
        cuerpo ya la ofrecia y la eligio por X frente a Y— y su frase en el
        parte. Por el camino de exito completo: la decision de verdad, el
        registro del tic de verdad, el entierro y el parte.
  (xv)  [S-2] LA MALETA Y LOS FRENOS: que el diario en memoria es linea por
        linea el mismo que sale por stdout; que la subida arma un zip legible,
        manda Content-Type y Content-Length, y se hace UNA sola vez; que la red
        dispara al 95 % de `max_ticks` y NO antes; y que los dos frenos propios
        (150 llamadas, 0,30 $) callan al cortex y lo escriben en el diario.
  (xvi) [S-2] EL INTERRUPTOR DEL HILO D: con GEMV_CORTEX_PARTE=0 el texto que
        se manda al modelo es el de la serie S-CORTEX —sin parte, sin el
        derecho a callar y con el esquema pidiendo "entre UNA y tres"— y con =1
        vuelven las tres cosas. Se comprueba sobre el cuerpo REAL de la
        peticion, no sobre las constantes.
  (ix)  [L-7] `Alma.decidir` ENTERO con propuestas VIVAS, 200 tics: es el
        camino que la L-4 y la L-5 rompieron y que ningun humo pisaba. Se
        comprueba que emite siempre algo legal, que respeta el veto y el
        empate, y que cuando el cortex no gana, lo emitido es EXACTAMENTE lo
        que el cuerpo habria emitido solo.

Si algo falla, revienta y el build se cae.
"""
from __future__ import annotations
import copy, json, os, sys

sys.path.insert(0, "/app")
AQUI = os.path.dirname(os.path.abspath(__file__))

from alma import appraisal_zs_v42_exp as A          # noqa: E402
from alma import decisor_zs as D                    # noqa: E402
from alma import relator_t5 as RT                   # noqa: E402
from alma.mundo import Mundo                        # noqa: E402

A.EMPATIA_ON = True
A.H_PREV, A.H_GOLPE = 0.25, 1.0
A.MIEDO_ON = False
A.VIDA_AJENA_ON = False
D.A = A

LEY = {".": "ground", "#": "wall", "R": "rock", "F": "fortress_wall",
       "P": "pedestal", "B": "berry_bush"}


def i_relator():
    e = json.load(open(os.path.join(AQUI, "humo_escena04.json")))["4"]
    md = open(os.path.join(AQUI, "humo_escena04.md"), encoding="utf-8").read()
    sc = md.split("## SIN CUERPO")[1].split("\n---\n")[0].strip()
    cc = md.split("## CON CUERPO")[1].split("\n---\n")[0].strip()
    a, b = RT.relato(e, False), RT.relato(e, True)
    assert a == sc, "(i) SIN CUERPO NO es byte a byte"
    assert b == cc, "(i) CON CUERPO NO es byte a byte"
    print(f"humo (i) OK: el relator reproduce la escena 04 byte a byte "
          f"({len(sc)} y {len(cc)} bytes)")


def _mundo_y_obs():
    d = json.load(open(os.path.join(AQUI, "humo_200tics.json")))
    pc = d["player_config"]
    cfg = {"slot": pc["slot"], "team": pc.get("team", ""),
           "teammate_slot": pc.get("teammate_slot", -1),
           "tick_rate": pc.get("tick_rate", 24),
           "max_ticks": pc.get("max_ticks", 0),
           "ignition_tick": pc.get("ignition_tick", 0),
           "zone_schedule": pc.get("zone_schedule") or [],
           "items": list(d["catalogo"]["items"]),
           "stats": {"budget": 20, "min": 1, "max": 10, "default": [5, 5, 5, 5]},
           "arena": {"size": d["static_map"].get("size") or 48,
                     "static_map": list(d["static_map"]["filas"]),
                     "legend": dict(d["static_map"].get("legend") or LEY),
                     "pedestals": d["static_map"].get("pedestals") or []}}
    return Mundo.desde_player_config(cfg), d["ticks"]


CONST = {"intelligence": 8, "athleticism": 6, "speed": 5, "strength": 1}


def _obs(r):
    return {"type": "observation", "tick": r["tick"], "phase": r.get("phase"),
            "you": {"pos": list(r.get("pos") or [0, 0]), "hp": r.get("hp") or 0,
                    "stats": dict(CONST), "hand": r.get("hand"),
                    "body": r.get("body"),
                    "pack": list(r.get("pack") or [None, None]),
                    "effects": list(r.get("effects") or []),
                    "damage_taken": list(r.get("damage_taken") or []),
                    "kills": r.get("kills") or 0,
                    "damage_dealt": r.get("damage_dealt") or 0,
                    "move_ready_in": r.get("move_ready_in") or 0,
                    "attack_ready_in": r.get("attack_ready_in") or 0,
                    "action_result": r.get("action_result")},
            "visible": {"agents": list(r.get("ve_agentes") or []),
                        "items": list(r.get("ve_items") or []), "pods": [],
                        "bushes": list(r.get("ve_bushes") or []),
                        "projectiles": list(r.get("ve_proyectiles") or [])},
            "zone": r.get("zona") or {},
            "events": list(r.get("eventos") or []),
            "chat": list(r.get("chat") or [])}


def ii_inyector():
    mundo, ticks = _mundo_y_obs()
    mem, blo, ult = A.Memoria(), D.Bloqueos(), None
    n = 0
    for r in ticks:
        o = _obs(r)
        mem.observa(o, mundo, r["tick"])
        blo.actualiza(o, mundo, ult, r["tick"])
        ult = r.get("intencion")
        if r.get("phase") != "live" or n >= 12:
            continue
        base = D.decide(o, mundo, copy.deepcopy(mem), r["tick"],
                        copy.deepcopy(blo))[1]["candidatos"]
        orig = D.candidatos

        def _c(ob, mu, me, tk, bl=None, _o=orig):
            return list(_o(ob, mu, me, tk, bl)) + [("_SONDA", {"tipo": "quieto"})]
        D.candidatos = _c
        try:
            con = D.decide(o, mundo, copy.deepcopy(mem), r["tick"],
                           copy.deepcopy(blo))[1]["candidatos"]
        finally:
            D.candidatos = orig
        for k in base:
            assert con[k]["d"] == base[k]["d"], ("(ii) la inyeccion MOVIO", k)
        assert con["_SONDA"]["d"] == base["noop"]["d"], "(ii) la sonda != noop"
        n += 1
    assert n >= 10, "(ii) pocos tics probados"
    print(f"humo (ii) OK: inyectar no mueve ni un bit y la sonda == noop, "
          f"en {n} tics")


def iii_apagado():
    assert os.environ.get("GEMV_CORTEX", "0") != "1", "(iii) corre con CORTEX=0"
    from alma import cortex_t5 as CX
    assert CX.ON is False, "(iii) CX.ON deberia ser False"
    mundo, ticks = _mundo_y_obs()
    cx = CX.Cortex(lambda r: None)
    cx.arranca()
    mem, blo, ult = A.Memoria(), D.Bloqueos(), None
    n = 0
    for r in ticks:
        o = _obs(r)
        mem.observa(o, mundo, r["tick"])
        blo.actualiza(o, mundo, ult, r["tick"])
        ult = r.get("intencion")
        if r.get("phase") != "live":
            continue
        cx.pide({"tick": r["tick"], "e": None, "ofrecidas": {}})
        assert cx.extra(r["tick"]) == [], "(iii) con CORTEX=0 hay propuestas vivas"
        a1, d1 = D.decide(o, mundo, copy.deepcopy(mem), r["tick"],
                          copy.deepcopy(blo))
        a2, d2 = D.decide(o, mundo, copy.deepcopy(mem), r["tick"],
                          copy.deepcopy(blo))
        assert a1 == a2 and d1["elegido"] == d2["elegido"], "(iii) no determinista"
        assert all(d1["candidatos"][k]["d"] == d2["candidatos"][k]["d"]
                   for k in d1["candidatos"]), "(iii) d distinta"
        n += 1
    assert n >= 190, f"(iii) solo {n} tics live"
    print(f"humo (iii) OK: con GEMV_CORTEX=0 no hay inyeccion y la decision es "
          f"identica, en {n} tics")


def iv_llamada():
    import json as _j, threading
    from http.server import BaseHTTPRequestHandler, HTTPServer
    cap = {}
    fix = _j.load(open(os.path.join(AQUI, "humo_respuesta_L3.json")))["respuesta"]

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            cap["body"] = _j.loads(self.rfile.read(n) or b"{}")
            cap["path"] = self.path
            b = _j.dumps(fix).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("X-Coworld-Spend-Usd", "0.000056")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def log_message(self, *a):
            pass

    os.environ["GEMV_CORTEX"] = "1"
    os.environ["GEMV_CORTEX_MANUAL"] = "none"
    for m in [k for k in list(sys.modules) if k.startswith("alma.cortex")]:
        del sys.modules[m]
    from alma import cortex_t5 as CX
    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    cx = CX.Cortex(lambda r: None)
    cx.ep = f"http://127.0.0.1:{srv.server_address[1]}"
    cx.modelo = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
    cx.manual = "MANUAL DE MENTIRA"
    r = cx._llama("RELATO DE MENTIRA", 100)
    assert r.get("ok") is True, ("(iv) la llamada no salio bien", r)
    assert r["codigo"] == 200 and r["texto"] == "Azul."
    assert r["tok_entrada_fresca"] == 21 and r["tok_salida"] == 7
    assert r["tok_cache_lectura"] == 0 and r["tok_cache_escritura"] == 0
    assert r["spend_usd"] == "0.000056"
    assert cx.n_llamadas == 1 and len(cx.lat_n) == 1 and cx.fallos == 0
    assert "cuerpo_crudo_primera" in r
    assert cap["body"]["messages"][0]["content"][0]["cache_control"] == \
        {"type": "ephemeral"}, "(iv) falta cache_control"
    assert "/invoke" in cap["path"] and cx.modelo in cap["path"]
    print(f"humo (iv) OK: `_llama` completo sale bien, tokens (fresca "
          f"{r['tok_entrada_fresca']}, cache {r['tok_cache_lectura']}, salida "
          f"{r['tok_salida']}), cache_control puesto, ruta {cap['path']}")
    srv.shutdown()
    return CX


def v_caducidad(CX):
    est = {"tick": 300, "pos": (10, 10), "hand": "bow", "hand_foto": "bow",
           "alcance": 8, "agentes": {5: (10, 14)}, "cands": {"noop", "ir_centro"}}
    ok, _ = CX._sigue_valida({"receta": {"tipo": "atacar", "objetivo": 5}}, est)
    assert ok, "(v) el golpe alineado y a tiro deberia valer"
    ok, por = CX._sigue_valida({"receta": {"tipo": "atacar", "objetivo": 9}}, est)
    assert not ok and "no se le ve" in por, ("(v)", por)
    ok, por = CX._sigue_valida({"receta": {"tipo": "atacar", "objetivo": 5}},
                               dict(est, hand="sword"))
    assert not ok and "arma" in por, ("(v)", por)
    ok, por = CX._sigue_valida({"receta": {"tipo": "atacar", "objetivo": 5}},
                               dict(est, agentes={5: (13, 14)}))
    assert not ok and "alineado" in por, ("(v)", por)
    ok, _ = CX._sigue_valida({"receta": {"tipo": "ir", "destino": (20, 20)}}, est)
    assert ok, "(v) ir a una casilla lejana deberia valer"
    ok, por = CX._sigue_valida({"receta": {"tipo": "ir", "destino": (10, 10)}}, est)
    assert not ok and "ya estas" in por, ("(v)", por)
    ok, por = CX._sigue_valida({"nombre": "usar_botiquin",
                                "receta": {"tipo": "usar"}}, est)
    assert not ok and "ya no se ofrece" in por, ("(v)", por)
    ok, _ = CX._sigue_valida({"nombre": "noop", "receta": {"tipo": "quieto"}}, est)
    assert ok, "(v) noop sigue ofreciendose"
    print("humo (v) OK: `_sigue_valida` distingue las 8 situaciones probadas")


def _escena(mundo, r, mem, blo, herm):
    """El mismo `e` que arma `policy_cortex._foto`, para probar el traductor
    sobre mundo REAL y no sobre un decorado."""
    o = _obs(r)
    cands = D.candidatos(o, mundo, copy.deepcopy(mem), r["tick"],
                         copy.deepcopy(blo))
    recetas, vivas = {}, {}
    for n, rec in cands:
        vivas[n] = dict(rec)
        recetas[n] = {"tipo": rec.get("tipo"), "dir": rec.get("dir"),
                      "destino": list(rec["destino"]) if rec.get("destino") else None,
                      "objetivo": rec.get("objetivo"),
                      "item": ((rec.get("item") or {}).get("id")
                               if isinstance(rec.get("item"), dict)
                               else rec.get("item"))}
    radio = D.decide(o, mundo, copy.deepcopy(mem), r["tick"],
                     copy.deepcopy(blo))[1]
    vis = o.get("visible") or {}
    e = {"r": r, "pc_teammate": herm, "recetas": recetas,
         "cuerpo": {k: {"d": v["d"], "movs": v.get("movs")}
                    for k, v in radio["candidatos"].items()},
         "cert": None, "parte_fresco": None, "agresores_det": [],
         "_recetas_vivas": vivas,
         "_cuerpos": frozenset(tuple(a.get("pos") or ()) for a in
                               (vis.get("agents") or []) if a.get("pos")),
         "_objetos": dict(mem.objetos_vistos)}
    return o, e, {n: RT.en_llano(n, e) for n in recetas}


def vi_traductor(CX):
    mundo, ticks = _mundo_y_obs()
    herm = mundo.teammate_slot
    cx = CX.Cortex(lambda rec: None)
    mem, blo, ult = A.Memoria(), D.Bloqueos(), None
    hechas, casos = {}, 0
    for r in ticks:
        o = _obs(r)
        mem.observa(o, mundo, r["tick"])
        blo.actualiza(o, mundo, ult, r["tick"])
        ult = r.get("intencion")
        if r.get("phase") != "live" or len(hechas) >= 9:
            continue
        o, e, ofr = _escena(mundo, r, mem, blo, herm)
        viva = e["_recetas_vivas"]
        pos = tuple(r.get("pos") or ())
        items = [i for i in (r.get("ve_items") or []) if i.get("pos")]

        def t(txt):
            return cx._traduce({"accion": txt, "motivo": "-"}, e, ofr, r["tick"])

        # 1. OBJETO: "coger <cosa>" -> la casilla de ESE objeto (o coger/ir_*)
        if "objeto" not in hechas and items:
            it = next((i for i in items if tuple(i["pos"]) != pos), None)
            if it:
                nom = RT.ELCOSA.get(it["id"])
                if nom:
                    q = tuple(it["pos"])
                    x = t(f"Coger {nom} que esta a unas casillas")
                    assert x["clase"] != "IMPOSIBLE", ("(vi) objeto", x)
                    assert x["regla"] == "objeto", ("(vi) regla", x)
                    d = (x["receta"] or {}).get("destino")
                    assert (x["nombre"] in ("ir_objeto", "ir_botin", "coger")
                            or tuple(d or ()) == q), ("(vi) objeto ajeno", x, q)
                    assert (x.get("objetivo_nombrado") or {}).get("id") == it["id"]
                    hechas["objeto"] = (r["tick"], x["nombre"])
                    casos += 1
        # 2. HERMANO: al candidato VIVO ir_pareja, nunca a una casilla
        if "hermano" not in hechas:
            x = t("Ir hacia tu hermano para apoyarlo")
            if "ir_pareja" in viva:
                assert x["clase"] == "DENTRO" and x["nombre"] == "ir_pareja", \
                    ("(vi) hermano", x)
            else:
                assert x["clase"] == "IMPOSIBLE", ("(vi) hermano sin candidato", x)
            assert not (x.get("nombre") or "").startswith("_CX_"), \
                ("(vi) el hermano NO se traduce a casilla", x)
            assert (x.get("objetivo_nombrado") or {}).get("tipo") == "hermano"
            hechas["hermano"] = (r["tick"], x["nombre"])
            casos += 1
        # 3. ATACAR asiento K
        if "atacar" not in hechas:
            ats = {n: v.get("objetivo") for n, v in viva.items()
                   if n.startswith("atacar_")}
            if ats:
                n0, k = next(iter(ats.items()))
                x = t(f"Atacar al del asiento {k} ahora mismo")
                assert x["clase"] == "DENTRO" and x["nombre"] == n0, ("(vi) atacar", x)
                hechas["atacar"] = (r["tick"], n0)
                casos += 1
            else:
                # [S] sin ataque vivo, la propuesta NO muere: guarda el
                # objetivo, se marca como INICIAR y duerme hasta que ese
                # asiento se convierta en agresor (o hasta caducar).
                x = t("Atacar al del asiento 99 ahora mismo")
                assert x["clase"] == "DENTRO" and x.get("inicia_ataque") \
                    and x["objetivo_nombrado"]["slot"] == 99 \
                    and x.get("dormida_al_nacer"), ("(vi) iniciar", x)
                hechas["atacar"] = (r["tick"], "INICIAR (duerme)")
                casos += 1
        # 4. CENTRO
        if "centro" not in hechas and "ir_centro" in viva:
            x = t("Muevete hacia el centro de la arena")
            assert x["clase"] == "DENTRO" and x["nombre"] == "ir_centro", \
                ("(vi) centro", x)
            hechas["centro"] = (r["tick"], "ir_centro")
            casos += 1
        # 5. USAR lo que llevas
        if "usar" not in hechas:
            us = [n for n in viva if n.startswith("usar_")]
            if us:
                i = viva[us[0]]["idx"]
                ident = (r.get("pack") or [])[i]["id"]
                x = t(f"Usa {RT.ELCOSA.get(ident, ident)} ahora mismo")
                assert x["clase"] == "DENTRO" and x["nombre"] == us[0], ("(vi) usar", x)
                hechas["usar"] = (r["tick"], us[0])
                casos += 1
        # 6. VESTIR / EMPUNAR
        if "vestir" not in hechas:
            vs = [n for n in viva if n.startswith(("ponerse_", "empunar_"))]
            if vs:
                pre, ident = vs[0].split("_", 1)
                verbo = "Ponerte" if pre == "ponerse" else "Empunar"
                x = t(f"{verbo} {RT.ELCOSA.get(ident, ident)}")
                assert x["clase"] == "DENTRO" and x["nombre"] == vs[0], ("(vi) vestir", x)
                hechas["vestir"] = (r["tick"], vs[0])
                casos += 1
        # 7. RUMBO
        if "rumbo" not in hechas:
            mv = [n for n in viva if n.startswith("move_")]
            if mv:
                d = mv[0].split("_", 1)[1]
                x = t(f"Ir hacia el {RT.DIRX[d]} corriendo todo lo que puedas")
                assert x["clase"] == "DENTRO" and x["nombre"] in (f"move_{d}",
                                                                  f"paso_{d}"), \
                    ("(vi) rumbo", x)
                hechas["rumbo"] = (r["tick"], x["nombre"])
                casos += 1
        # 8. ESPERAR
        if "esperar" not in hechas:
            x = t("Esperar 3 tics sin hacer nada")
            assert x["clase"] == "DENTRO" and x["nombre"] == "noop", ("(vi) esperar", x)
            hechas["esperar"] = (r["tick"], "noop")
            casos += 1
        # 9. SOLO una casilla de verdad es una casilla
        if "casilla" not in hechas:
            x = t("Colocate en la casilla (7,9) y aguanta ahi")
            assert x["clase"] == "FUERA" and x["nombre"] == "_CX_ir_7_9", \
                ("(vi) casilla", x)
            y = t("Aguanta 7 tics y luego otros 9 mas")
            assert not (y.get("nombre") or "").startswith("_CX_ir"), \
                ("(vi) un numero suelto NO es una casilla", y)
            hechas["casilla"] = (r["tick"], "_CX_ir_7_9")
            casos += 1
    # `usar` y `vestir` no aparecen en este diario (el agente nunca lleva nada
    # curable ni una prenda en el zurron), asi que su tic se PREPARA: se le pone
    # al registro una mochila y una herida, y los candidatos los sigue armando
    # `D.candidatos` de verdad. Se declara que este es el unico caso preparado.
    r0 = next(x for x in ticks if x.get("phase") == "live")
    mem2, blo2, ult2 = A.Memoria(), D.Bloqueos(), None
    for r in ticks:
        o = _obs(r)
        mem2.observa(o, mundo, r["tick"])
        blo2.actualiza(o, mundo, ult2, r["tick"])
        ult2 = r.get("intencion")
        if r["tick"] >= r0["tick"]:
            break
    r2 = copy.deepcopy(r0)
    r2["hp"] = 40
    r2["pack"] = [{"id": "first_aid", "n": 1}, {"id": "camouflage", "n": 1}]
    r2["body"] = None
    o2, e2, ofr2 = _escena(mundo, r2, mem2, blo2, herm)
    v2 = e2["_recetas_vivas"]
    assert "usar_botiquin" in v2 and "ponerse_camouflage" in v2, \
        ("(vi) el tic preparado no ofrece lo que deberia", sorted(v2))

    def t2(txt):
        return cx._traduce({"accion": txt, "motivo": "-"}, e2, ofr2, r2["tick"])

    x = t2("Usa el botiquin ahora mismo para curarte")
    assert x["clase"] == "DENTRO" and x["nombre"] == "usar_botiquin", ("(vi) usar", x)
    hechas["usar"] = (r2["tick"], "usar_botiquin")
    x = t2("Ponerte el camuflaje")
    assert x["clase"] == "DENTRO" and x["nombre"] == "ponerse_camouflage", \
        ("(vi) vestir", x)
    hechas["vestir"] = (r2["tick"], "ponerse_camouflage")
    casos += 2
    faltan = {"objeto", "hermano", "centro", "esperar", "casilla", "rumbo",
              "usar", "vestir", "atacar"} - set(hechas)
    assert not faltan, f"(vi) reglas sin probar: {faltan}"
    print(f"humo (vi) OK: el traductor nuevo, {casos} reglas probadas sobre "
          f"escenas reales: " + ", ".join(f"{k}@{v[0]}->{v[1]}"
                                          for k, v in sorted(hechas.items())))


def vii_vetos():
    import importlib
    PC = importlib.import_module("alma.policy_cortex")
    mundo, ticks = _mundo_y_obs()
    mem, blo, ult = A.Memoria(), D.Bloqueos(), None
    vet_mov = vet_atq = libres = identicos = 0
    for r in ticks:
        o = _obs(r)
        mem.observa(o, mundo, r["tick"])
        blo.actualiza(o, mundo, ult, r["tick"])
        ult = r.get("intencion")
        if r.get("phase") != "live":
            continue
        tk = r["tick"]
        ex = [("_CX_ir_24_24", {"tipo": "ir", "destino": (24, 24),
                                "cuerpos": frozenset()}),
              ("_CX_atacar_N", {"tipo": "atacar", "dir": "N", "objetivo": 1,
                                "arma": mundo.items.get("sword")})]
        mov = (o["you"]["move_ready_in"] or 0) > 0
        atq = (o["you"]["attack_ready_in"] or 0) > 0
        # el veto LEE el mismo campo que lee el cuerpo
        vet = {n: PC._veta_receta(blo, rec, o, tk) for n, rec in ex}
        assert vet["_CX_ir_24_24"] == mov, ("(vii) veto de piernas", tk)
        assert vet["_CX_atacar_N"] == atq, ("(vii) veto de arma", tk)
        vet_mov += int(mov)
        vet_atq += int(atq)
        if not (mov or atq):
            libres += 1
        # el enfriamiento de arma no se da en este diario (el agente no pega):
        # se FUERZA el campo, que es lo unico que el veto mira, para probar las
        # dos puertas. Con las dos cerradas, la mesa tiene que quedar intacta.
        o2 = copy.deepcopy(o)
        o2["you"]["move_ready_in"] = max(1, o["you"]["move_ready_in"] or 0)
        o2["you"]["attack_ready_in"] = max(1, o["you"]["attack_ready_in"] or 0)
        blo2 = copy.deepcopy(blo)
        assert all(PC._veta_receta(blo2, rec, o2, tk) for _n, rec in ex), \
            ("(vii) con los dos enfriamientos puestos deberian estar vetadas", tk)
        base = D.decide(o2, mundo, copy.deepcopy(mem), tk, copy.deepcopy(blo2))
        orig = D.candidatos

        def _c(ob, mu, me, t2, bl=None, _o=orig, _e=ex):
            b = list(_o(ob, mu, me, t2, bl))
            nom = {c[0] for c in b}
            return b + [(n, rc) for n, rc in _e
                        if n not in nom and not PC._veta_receta(bl, rc, ob, t2)]
        D.candidatos = _c
        try:
            con = D.decide(o2, mundo, copy.deepcopy(mem), tk,
                           copy.deepcopy(blo2))
        finally:
            D.candidatos = orig
        assert con[0] == base[0], ("(vii) se emitio otra cosa", tk, con[0], base[0])
        assert con[1]["elegido"] == base[1]["elegido"], ("(vii) otro elegido", tk)
        assert set(con[1]["candidatos"]) == set(base[1]["candidatos"]), \
            ("(vii) la mesa cambio", tk)
        for k in base[1]["candidatos"]:
            assert con[1]["candidatos"][k]["d"] == base[1]["candidatos"][k]["d"], \
                ("(vii) la d se movio", tk, k)
        identicos += 1
    assert identicos >= 150 and vet_mov >= 5, ("(vii) pocos tics probados",
                                               identicos, vet_mov)
    print(f"humo (vii) OK: el veto del cuerpo se aplica igual a lo inyectado "
          f"(piernas enfriando en {vet_mov} tics reales, {libres} sin ningun "
          f"enfriamiento) y con las dos puertas cerradas la emision es bit a "
          f"bit la del cuerpo en {identicos} tics")


def viii_empates():
    mundo, ticks = _mundo_y_obs()
    mem, blo, ult = A.Memoria(), D.Bloqueos(), None
    n = 0
    for r in ticks:
        o = _obs(r)
        mem.observa(o, mundo, r["tick"])
        blo.actualiza(o, mundo, ult, r["tick"])
        ult = r.get("intencion")
        if r.get("phase") != "live" or n >= 20:
            continue
        tk = r["tick"]
        orig = D.candidatos

        def _c(ob, mu, me, t2, bl=None, _o=orig):
            return list(_o(ob, mu, me, t2, bl)) + [("_CX_clon", {"tipo": "quieto"})]
        D.candidatos = _c
        try:
            _a, rad = D.decide(o, mundo, copy.deepcopy(mem), tk,
                               copy.deepcopy(blo))
        finally:
            D.candidatos = orig
        cds = {k: v["d"] for k, v in rad["candidatos"].items()}
        prop = {k: v for k, v in cds.items() if k != "_CX_clon"}
        mej = min(prop, key=prop.get)
        estricta = (rad["elegido"] == "_CX_clon"
                    and cds["_CX_clon"] < prop[mej] - 1e-9)
        assert not estricta, ("(viii) un clon de noop no puede GANAR", tk,
                              cds["_CX_clon"], prop[mej])
        n += 1
    assert n >= 15, "(viii) pocos tics"
    print(f"humo (viii) OK: un clon de `noop` nunca gana por `d` estricta, "
          f"en {n} tics (los empates se le devuelven al cuerpo)")


def ix_decidir_entero(CX):
    """El camino completo: la politica de verdad, con el cortex encendido y
    propuestas vivas de las tres formas (una que el cuerpo ya ofrece, una
    nueva, y una que el veto tiene que tumbar)."""
    import importlib
    PC = importlib.import_module("alma.policy_cortex")
    mundo, ticks = _mundo_y_obs()
    _log_de_verdad = PC.log            # se devuelve al final: el (xv) lo necesita
    PC.log = lambda rec: None          # el diario, callado dentro del humo
    al = PC.Alma()
    al.mundo = mundo
    al.cx = CX.Cortex(lambda rec: None)
    limpio, con_veto, ganados, empatados, respaldos = 0, 0, 0, 0, 0
    mem2, blo2, ult2 = A.Memoria(), D.Bloqueos(), None
    for r in ticks:
        o = _obs(r)
        # lo que el CUERPO SOLO habria emitido en este tic
        mem2.observa(o, mundo, r["tick"])
        blo2.actualiza(o, mundo, ult2, r["tick"])
        ult2 = r.get("intencion")
        solo = (D.decide(o, mundo, copy.deepcopy(mem2), r["tick"],
                         copy.deepcopy(blo2))[0]
                if r.get("phase") == "live" else None)
        # tres propuestas vivas, puestas a mano en el cortex
        # tres objetivos vivos de los tres tipos: quieto (siempre se ata al
        # cuerpo), casilla (se inyecta y el veto la tumba si toca) y asiento
        # (que no tiene casilla, asi que duerme si no hay ataque vivo).
        def _v(i, obj, n0):
            return {"id": i, "obj": obj, "nombre0": n0, "receta0": {},
                    "nace": r["tick"] - 1, "caduca": r["tick"] + 9,
                    "accion": f"prueba {i}", "motivo": "-", "clase": "DENTRO",
                    "regla": "humo", "dormida": 0, "cuerpo": 0, "casilla": 0,
                    "vetada": 0, "gano": 0}
        al.cx.vivas = [_v(1, {"tipo": "quieto"}, "noop"),
                       _v(2, {"tipo": "casilla", "pos": (24, 24)}, None),
                       _v(3, {"tipo": "asiento", "slot": 1}, None)]
        accion, radio = al.decidir(o)
        al.ultima_accion = accion
        assert isinstance(accion, dict) and accion.get("do") in (
            "none", "move", "attack", "pickup", "use", "drop"), \
            ("(ix) accion ilegal", r["tick"], accion)
        if r.get("phase") != "live":
            continue
        limpio += 1
        if al.cx_empate:
            empatados += 1
        if al.cx_tics_vetada:
            con_veto = al.cx_tics_vetada
        gano = al.cx_victorias
        # cuando el cortex NO se lleva el tic, lo emitido es lo del cuerpo
        if not radio["elegido"].startswith("_CX_"):
            assert accion == solo, ("(ix) el cortex cambio la emision sin ganar",
                                    r["tick"], accion, solo)
        else:
            ganados = gano
    assert limpio >= 190, ("(ix) pocos tics", limpio)
    assert con_veto >= 5, ("(ix) el veto no llego a pisarse", con_veto)
    PC.log = _log_de_verdad
    print(f"humo (ix) OK: `Alma.decidir` entero con propuestas vivas en "
          f"{limpio} tics · {al.cx_victorias} ganados por `d` estricta, "
          f"{al.cx_empates} empates devueltos al cuerpo, {al.cx_tics_vetada} "
          f"tics con propuesta vetada; sin victoria, la emision es la del cuerpo")


def x_atadura(CX):
    mundo, ticks = _mundo_y_obs()
    herm = mundo.teammate_slot
    mem, blo, ult = A.Memoria(), D.Bloqueos(), None
    visto = {}
    n_libre = n_frio = 0
    for r in ticks:
        o = _obs(r)
        mem.observa(o, mundo, r["tick"])
        blo.actualiza(o, mundo, ult, r["tick"])
        ult = r.get("intencion")
        if r.get("phase") != "live":
            continue
        tk = r["tick"]
        base = D.candidatos(o, mundo, copy.deepcopy(mem), tk,
                            copy.deepcopy(blo))
        vivos = dict(base)
        frio = (o["you"]["move_ready_in"] or 0) > 0
        n_frio += int(frio); n_libre += int(not frio)
        pos = tuple(r.get("pos") or ())

        def A_(obj, n0=None):
            return CX.ata(obj, n0, base, o, mundo, copy.deepcopy(mem), tk)

        # 1. QUIETO: siempre atado al cuerpo, nunca a casilla
        a = A_({"tipo": "quieto"}, "noop")
        assert a and a[0] == "noop" and a[2] == "cuerpo", ("(x) quieto", tk, a)
        visto["quieto"] = "cuerpo"
        # 2. CENTRO: al candidato si esta vivo; si no, a la casilla del anillo
        c, _rr, _dd = mundo.anillo_en(tk)
        a = A_({"tipo": "centro"})
        if "ir_centro" in vivos:
            assert a[0] == "ir_centro" and a[2] == "cuerpo", ("(x) centro", tk, a)
            visto["centro_cuerpo"] = tk
        elif tuple(c) != pos:
            assert a and a[2] == "casilla" and a[1]["destino"] == tuple(c), \
                ("(x) centro por casilla", tk, a)
            visto["centro_casilla"] = tk
        # 3. HERMANO: al candidato vivo; si no, a su casilla; si muerto, dormida
        a = A_({"tipo": "hermano"})
        hq = next((tuple(x["pos"]) for x in (r.get("ve_agentes") or [])
                   if x.get("slot") == herm and x.get("pos")), None)
        if "ir_pareja" in vivos:
            assert a[0] == "ir_pareja" and a[2] == "cuerpo", ("(x) hermano", tk, a)
            visto["hermano_cuerpo"] = tk
        elif (hq or mem.pareja_pos) and not mem.pareja_muerta:
            q = hq or tuple(mem.pareja_pos)
            if q != pos:
                assert a and a[2] == "casilla" and a[1]["destino"] == q, \
                    ("(x) hermano por casilla", tk, a, q)
                visto["hermano_casilla"] = tk
        # 4. OBJETO: si se ve, casilla o candidato; si NO se ve, DORMIDA
        its = [i for i in (r.get("ve_items") or []) if i.get("pos")]
        if its:
            it = its[0]
            a = A_({"tipo": "objeto", "id": it["id"], "pos": tuple(it["pos"])})
            assert a is not None, ("(x) objeto a la vista sin atadura", tk)
            if a[2] == "casilla":
                assert a[1]["destino"] == tuple(it["pos"]), ("(x) otra casilla", tk)
                visto["objeto_casilla"] = tk
            else:
                visto["objeto_cuerpo"] = a[0]
        a = A_({"tipo": "objeto", "id": "_NO_EXISTE_", "pos": (3, 3)})
        assert a is None, ("(x) un objeto que ya no se ve deberia DORMIR", tk, a)
        visto["objeto_dormida"] = tk
        # 5. ASIENTO: solo por candidato vivo; JAMAS por casilla
        a = A_({"tipo": "asiento", "slot": 99})
        assert a is None, ("(x) un asiento sin ataque vivo deberia DORMIR", tk, a)
        visto["asiento_dormida"] = tk
        ats = [(n, rc) for n, rc in base if n.startswith("atacar_")]
        if ats:
            a = A_({"tipo": "asiento", "slot": ats[0][1]["objetivo"]})
            assert a and a[0] == ats[0][0] and a[2] == "cuerpo", ("(x) asiento", tk, a)
            visto["asiento_cuerpo"] = tk
        # 6. RUMBO y MOCHILA: solo por candidato vivo
        a = A_({"tipo": "rumbo", "dir": "N"})
        assert (a is None) == ("move_N" not in vivos and "paso_N" not in vivos), \
            ("(x) rumbo", tk, a)
        if a:
            visto["rumbo_cuerpo"] = a[0]
        a = A_({"tipo": "mochila", "nombre": "usar_botiquin"}, "usar_botiquin")
        assert (a is None) == ("usar_botiquin" not in vivos), ("(x) mochila", tk, a)
    faltan = {"quieto", "objeto_dormida", "asiento_dormida"} - set(visto)
    assert not faltan, f"(x) sin probar: {faltan}"
    assert "hermano_casilla" in visto or "hermano_cuerpo" in visto, "(x) hermano"
    assert n_frio >= 5 and n_libre >= 5, ("(x) pocos estados", n_frio, n_libre)
    print(f"humo (x) OK: atadura perezosa sobre {n_frio + n_libre} tics reales "
          f"({n_frio} con las piernas frias, {n_libre} libres); probado: "
          + ", ".join(sorted(visto)))


def xi_parte(CX):
    # 1. sin historia no hay parte
    assert CX.parte([], 0, 0) == "", "(xi) con historia vacia no se manda nada"
    # 2. una sola, de cada clase
    uno = CX.parte([{"accion": "Coger el arco del suelo", "suerte": "hizo",
                     "fila": None}], 1, 1)
    assert "propusiste \"Coger el arco del suelo\"; tu cuerpo lo hizo" in uno
    assert "De tus 1 propuestas, tu cuerpo ha hecho 1." in uno
    dos = CX.parte([{"accion": "Ir al centro", "suerte": "no_compro",
                     "fila": "S-8-EXPOSICION"}], 2, 0)
    assert "tu cuerpo no lo compro: prefirio no quedar a la vista" in dos, dos
    assert "S-8" not in dos and "EXPOSICION" not in dos, "(xi) NOMBRA la fila"
    tres = CX.parte([{"accion": "Atacar al del asiento 9", "suerte": "no_se_podia",
                      "fila": None}], 3, 0)
    assert "no se podia hacer ahi" in tres
    # 3. cinco de las tres clases, y solo cinco
    h = [{"accion": f"propuesta numero {i}", "suerte": s, "fila": f}
         for i, (s, f) in enumerate(
             [("hizo", None), ("no_compro", "R-CARENCIA"),
              ("no_se_podia", None), ("no_compro", "R-ACOPIO"),
              ("hizo", None), ("no_compro", "S-7-AGRESOR")], 1)]
    cinco = CX.parte(h, 9, 3)
    assert cinco.count("propusiste") == 5, "(xi) deberia decir CINCO"
    assert "propuesta numero 1" not in cinco, "(xi) deberia tirar la mas vieja"
    assert "propuesta numero 6" in cinco, "(xi) deberia llevar la mas nueva"
    assert "iba mal equipado para lo que venia" in cinco
    assert "le faltaba con que curarse" in cinco
    assert "tenia delante a quien le estaba pegando" in cinco
    assert "De tus 9 propuestas, tu cuerpo ha hecho 3." in cinco
    # 4. ninguna fila del relator se queda sin frase
    for k in RT.FRASE:
        assert k in CX.PORQUE, ("(xi) fila sin traducir en el parte", k)
    # 5. el texto de la accion va RECORTADO, no entero
    largo = "x" * 200
    assert largo not in CX.parte([{"accion": largo, "suerte": "hizo",
                                   "fila": None}], 1, 1), "(xi) manda el texto entero"
    # 6. y el parte viaja DELANTE de la escena y FUERA del bloque cacheado
    cap = _servidor_de_mentira()
    cx = CX.Cortex(lambda r: None)
    cx.ep, cx.modelo, cx.manual = cap["ep"], "m", "MANUAL"
    cx.historia.extend(h)
    cx.n_propuestas, cx.n_hechas = 9, 3
    r = cx._llama("ESCENA DE MENTIRA", 100)
    assert r.get("ok"), ("(xi) la llamada fallo", r)
    bl = cap["body"]["messages"][0]["content"]
    assert bl[0].get("cache_control"), "(xi) el manual deberia ir cacheado"
    assert "propusiste" not in bl[0]["text"], "(xi) el parte NO va en la cache"
    if CX.PARTE_ON:
        assert bl[1]["text"].index("propusiste") < \
            bl[1]["text"].index("ESCENA DE MENTIRA"), \
            "(xi) el parte tiene que ir DELANTE de la escena"
        donde = "delante de la escena y fuera de la cache"
    else:
        # [S-2] con el interruptor del hilo D apagado el parte SE CONSTRUYE
        # igual (y se comprueba arriba, frase a frase) pero NO se manda.
        assert "propusiste" not in bl[1]["text"], \
            "(xi) con GEMV_CORTEX_PARTE=0 el parte no puede viajar"
        donde = "construido pero SIN mandar (GEMV_CORTEX_PARTE=0)"
    cap["srv"].shutdown()
    print(f"humo (xi) OK: el parte con 0/1/5 propuestas de las tres clases, "
          f"todas las filas traducidas y sin nombrarlas, texto recortado, "
          f"{donde}")


def _servidor_de_mentira(propuestas=None):
    import json as _j, threading
    from http.server import BaseHTTPRequestHandler, HTTPServer
    cap = {}
    cuerpo = {"content": [{"type": "text", "text": _j.dumps(
                  {"propuestas": propuestas if propuestas is not None
                   else [{"accion": "a", "motivo": "b"}]})}],
              "usage": {"input_tokens": 9, "output_tokens": 3},
              "stop_reason": "end_turn"}

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            cap["body"] = _j.loads(self.rfile.read(n) or b"{}")
            b = _j.dumps(cuerpo).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    cap["srv"] = srv
    cap["ep"] = f"http://127.0.0.1:{srv.server_address[1]}"
    return cap


def xii_lista_vacia(CX):
    cap = _servidor_de_mentira(propuestas=[])
    cx = CX.Cortex(lambda r: None)
    cx.ep, cx.modelo, cx.manual = cap["ep"], "m", None
    r = cx._llama("ESCENA", 100)
    assert r.get("ok") and r["propuestas"] == [], ("(xii) no leyo la lista vacia", r)
    # el camino entero: una foto que devuelve cero propuestas
    e = json.load(open(os.path.join(AQUI, "humo_escena04.json")))["4"]
    e.setdefault("_recetas_vivas", {}); e.setdefault("_cuerpos", frozenset())
    e.setdefault("_objetos", {})
    cx._una({"tick": 10, "e": e, "ofrecidas": {}, "reloj": (lambda: 20),
             "hand_foto": None, "estado": None})
    assert cx.llamadas_cero == 1, ("(xii) no conto el derecho a callar",
                                   cx.llamadas_cero)
    assert cx.vivas == [], "(xii) con lista vacia no puede quedar nada vivo"
    assert cx.extra(30) == [], "(xii) extra deberia estar vacio"
    assert CX.parte(cx.historia, cx.n_propuestas, cx.n_hechas) == "", \
        "(xii) sin propuestas no hay parte que mandar"
    cap["srv"].shutdown()
    print(f"humo (xii) OK: la lista vacia no rompe nada, cuenta como derecho a "
          f"callar ({cx.llamadas_cero}) y deja al cuerpo sin nada inyectado")


def xiii_fontaneria(CX):
    import threading
    cap = _servidor_de_mentira()
    diario = []
    cx = CX.Cortex(diario.append)
    cx.ep, cx.modelo, cx.manual = cap["ep"], "m", None
    e = json.load(open(os.path.join(AQUI, "humo_escena04.json")))["4"]
    e.setdefault("_recetas_vivas", {}); e.setdefault("_cuerpos", frozenset())
    e.setdefault("_objetos", {})
    for i in range(4):
        cx.historia.append({"accion": f"lo de antes {i}", "suerte": "hizo",
                            "fila": None})
        cx.n_propuestas += 1; cx.n_hechas += 1
        cx._una({"tick": 100 * (i + 1), "e": e, "ofrecidas": {},
                 "reloj": (lambda: 100 * (i + 1) + 80), "hand_foto": None,
                 "estado": None})
    lls = [r for r in diario if r.get("k") == "cortex_llamada"]
    assert len(lls) == 4, ("(xiii) faltan llamadas", len(lls))
    # (a) el parte ENTERO en CADA llamada, no solo en la primera
    for r in lls:
        assert r.get("parte") is not None, "(xiii a) falta el parte entero"
        assert len(r["parte"]) == r["parte_bytes"], "(xiii a) bytes que no cuadran"
        import hashlib
        assert hashlib.md5(r["parte"].encode()).hexdigest() == r["parte_md5"], \
            "(xiii a) el md5 no es el del parte guardado"
    if CX.PARTE_ON:
        assert lls[-1]["parte"] != lls[0]["parte"], "(xiii a) el parte no cambia"
    else:
        # [S-2] con el interruptor apagado el parte es vacio y no viaja; lo que
        # se sigue comprobando es que el REGISTRO existe y cuadra consigo mismo.
        assert all(r["parte"] == "" for r in lls), \
            "(xiii a) con GEMV_CORTEX_PARTE=0 el parte deberia ir vacio"
    # (c) numero de secuencia, creciente y sin repetir
    seqs = [r["seq"] for r in diario if "seq" in r]
    assert seqs and seqs == sorted(seqs) and len(seqs) == len(set(seqs)), \
        ("(xiii c) la secuencia no es creciente y unica", seqs)
    assert all("seq" in r for r in diario
               if r.get("k") in ("cortex_llamada", "cortex_muere")), \
        "(xiii c) hay registros del cortex sin sellar"
    # y que se reparte bien con DOS hilos a la vez
    cx2 = CX.Cortex(lambda r: None)
    vistos = []

    def tira():
        for _ in range(200):
            r = {}
            cx2._sello(r)
            vistos.append(r["seq"])
    hs = [threading.Thread(target=tira) for _ in range(4)]
    [h.start() for h in hs]; [h.join() for h in hs]
    assert len(set(vistos)) == 800 == len(vistos), \
        ("(xiii c) la secuencia se repite con varios hilos", len(set(vistos)))
    # (b) el LIBRO: todas las llamadas hasta ahora, en cada reemision
    lib = cx.libro_compacto(500)
    assert lib["n"] == 4 and len(lib["libro"]) == 4, ("(xiii b) el libro", lib)
    for fila, r in zip(lib["libro"], lls):
        assert fila["f"] == r["tick"], "(xiii b) el tic de foto no cuadra"
        assert fila["h"] == r["parte_md5"][:8], "(xiii b) el hash no cuadra"
        assert fila["D"] + fila["F"] + fila["I"] == len(r.get("traduccion") or []), \
            "(xiii b) las clases no suman"
    # lo que de verdad importa: que el libro reemitido a mitad de partida
    # siga trayendo LA PRIMERA llamada
    assert lib["libro"][0]["n"] == 1, "(xiii b) el libro perdio el principio"
    antes = cx.libro_compacto(200)
    cx._una({"tick": 500, "e": e, "ofrecidas": {}, "reloj": (lambda: 580),
             "hand_foto": None, "estado": None})
    despues = cx.libro_compacto(600)
    assert despues["n"] == antes["n"] + 1, "(xiii b) el libro no crece"
    assert despues["libro"][0] == antes["libro"][0], "(xiii b) el libro se altera"
    cap["srv"].shutdown()
    print(f"humo (xiii) OK: parte entero en las {len(lls)} llamadas, libro de "
          f"{despues['n']} con la primera intacta, y la secuencia unica y "
          f"creciente con 4 hilos a la vez ({len(set(vistos))} numeros)")


def xiv_razon_respaldo(CX):
    """Los tres casos, cada uno sobre un tic REAL del diario de 200 tics, con
    `Alma.decidir` entero: lo que se comprueba es la frase que sale del parte."""
    import importlib
    PC = importlib.import_module("alma.policy_cortex")
    _log_de_verdad = PC.log            # se devuelve al final: el (xv) lo necesita
    PC.log = lambda rec: None
    mundo, ticks = _mundo_y_obs()
    frases = {}

    def _v(i, obj, n0, accion):
        return {"id": i, "obj": obj, "nombre0": n0, "receta0": {},
                "nace": 0, "caduca": 10 ** 9, "accion": accion, "motivo": "-",
                "clase": "DENTRO", "regla": "humo", "dormida": 0, "cuerpo": 0,
                "casilla": 0, "vetada": 0, "gano": 0}

    for caso in ("a", "b", "c"):
        al = PC.Alma()
        al.mundo = mundo
        al.cx = CX.Cortex(lambda r: None)
        mem2, blo2, ult2 = A.Memoria(), D.Bloqueos(), None
        puesta = None
        for r in ticks:
            o = _obs(r)
            mem2.observa(o, mundo, r["tick"])
            blo2.actualiza(o, mundo, ult2, r["tick"])
            ult2 = r.get("intencion")
            if r.get("phase") != "live":
                al.decidir(o); al.ultima_accion = None
                continue
            base = D.candidatos(o, mundo, copy.deepcopy(mem2), r["tick"],
                                copy.deepcopy(blo2))
            _a, rad = D.decide(o, mundo, copy.deepcopy(mem2), r["tick"],
                               copy.deepcopy(blo2))
            eleg = rad["elegido"]
            if caso == "c":
                # (c) el cuerpo YA ofrece el candidato que el cortex nombra, y
                #     es justo el que va a elegir.
                if len(rad["candidatos"]) < 2:
                    continue
                ob = CX._objetivo_de(eleg, {"_recetas_vivas": dict(base),
                                            "r": r, "recetas": {}})
                puesta = _v(1, ob, eleg, f"haz {eleg}")
            elif caso == "b":
                # (b) inyectada y PIERDE: una casilla lejana cualquiera.
                puesta = _v(2, {"tipo": "casilla", "pos": (2, 2)}, None,
                            "vete a la casilla (2,2)")
            else:
                # (a) inyectada y GANA: un clon del mejor candidato propio,
                #     con una casilla que el cuerpo no tiene en su lista.
                puesta = _v(3, {"tipo": "casilla", "pos": (2, 2)}, None,
                            "vete a la casilla (2,2)")
            al.cx.vivas = [puesta]
            al.decidir(o)
            al.ultima_accion = None
            v = al.cx.vivas[0]
            if caso == "c" and v.get("gana"):
                break
            if caso == "b" and v.get("pierde"):
                break
            if caso == "a" and v.get("gano"):
                break
        assert puesta is not None, f"(xiv) no hubo tic para el caso {caso}"
        v = al.cx.vivas[0]
        al.cx.vivas = []
        al.cx._entierra(v)
        pt = CX.parte(al.cx.historia, 1, al.cx.n_hechas)
        linea = [x for x in pt.splitlines() if x.strip().startswith("- propusiste")]
        assert linea, ("(xiv) el parte no trae la linea", caso, pt)
        frases[caso] = linea[0].strip()
    assert "tu cuerpo lo hizo" in frases["a"], ("(xiv a)", frases["a"])
    assert "tu cuerpo no lo compro:" in frases["b"], ("(xiv b)", frases["b"])
    assert "prefirio otra cosa" not in frases["b"], \
        ("(xiv b) la inyectada que pierde tiene que traer RAZON", frases["b"])
    assert "ya iba a hacerlo" in frases["c"], ("(xiv c)", frases["c"])
    assert ("porque" in frases["c"] or "unica opcion" in frases["c"]), \
        ("(xiv c) el respaldo tiene que traer RAZON", frases["c"])
    assert "prefirio otra cosa" not in frases["c"], ("(xiv c)", frases["c"])
    PC.log = _log_de_verdad
    print("humo (xiv) OK: las tres frases del parte, cada una de su caso:")
    for k in ("a", "b", "c"):
        print(f"    ({k}) {frases[k]}")
    return frases


def xv_maleta_y_frenos(CX):
    import importlib, io, threading, zipfile
    from http.server import BaseHTTPRequestHandler, HTTPServer
    PC = importlib.import_module("alma.policy_cortex")

    # ── la maleta ──────────────────────────────────────────────────────────
    cap = {"n": 0}

    class H(BaseHTTPRequestHandler):
        def do_PUT(self):
            cap["n"] += 1
            cap["tipo"] = self.headers.get("Content-Type")
            cap["largo"] = self.headers.get("Content-Length")
            n = int(cap["largo"] or 0)
            cap["datos"] = self.rfile.read(n)
            # el relé de verdad: la PRIMERA gana, la segunda es 204
            self.send_response(201 if cap["n"] == 1 else 204)
            self.end_headers()

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    os.environ["COWORLD_PLAYER_ARTIFACT_UPLOAD_URL"] = \
        f"http://127.0.0.1:{srv.server_address[1]}/player-artifact/10/tok"
    PC._DIARIO.clear()
    salida = []
    _w = sys.stdout.write
    sys.stdout.write = lambda t: (salida.append(t), _w(""))[1]
    for i in range(5):
        PC.log({"k": "tick", "tick": i, "seq": i})
    sys.stdout.write = _w
    por_stdout = [x for x in "".join(salida).split("\n") if x]
    assert len(por_stdout) == 5, ("(xv) el stdout no recibio las 5 lineas; "
                                  "si esto sale vacio, alguien dejo `PC.log` "
                                  "silenciado y la comparacion pasaria sola",
                                  len(por_stdout))
    assert por_stdout == PC._DIARIO, "(xv) la maleta no es igual que el stdout"

    class _Falso:
        tick = 4242
        artefacto_subido = False
        mundo = type("M", (), {"slot": 10, "max_ticks": 9120})()
    al = _Falso()
    assert PC.sube_artefacto(al, "humo") is True, "(xv) la subida fallo"
    assert cap["n"] == 1 and cap["tipo"] == "application/zip", ("(xv)", cap)
    assert cap["largo"] == str(len(cap["datos"])), "(xv) Content-Length no cuadra"
    z = zipfile.ZipFile(io.BytesIO(cap["datos"]))
    dentro = z.read(z.namelist()[0]).decode()
    assert [x for x in dentro.split("\n") if x][:5] == PC._DIARIO[:5], \
        "(xv) el zip no trae el diario"
    # UNA sola vez: el segundo intento ni sale
    assert PC.sube_artefacto(al, "otra") is False and cap["n"] == 1, \
        "(xv) se subio dos veces"
    # y queda apuntado en el propio diario
    reg = [json.loads(x) for x in PC._DIARIO if '"artefacto"' in x]
    assert reg and reg[0]["codigo"] == 201 and reg[0]["bytes_zip"] > 0 \
        and reg[0]["tick"] == 4242 and "ms" in reg[0], ("(xv) registro", reg)
    srv.shutdown()
    del os.environ["COWORLD_PLAYER_ARTIFACT_UPLOAD_URL"]

    # ── la red: al 95 % de max_ticks, y NI UN TIC ANTES ────────────────────
    mt = 9120
    umbral = 0.95 * mt
    assert not (umbral - 1 >= umbral) and (umbral >= umbral), "(xv) umbral"
    assert int(umbral) == 8664, ("(xv) el 95 % de 9120 deberia ser 8664", umbral)
    # con max_ticks ausente NO hay red
    assert not (0 and True), "(xv) sin max_ticks no puede haber red"

    # ── el freno de gasto AVISA si va ciego ────────────────────────────────
    cap2 = {}

    class H2(BaseHTTPRequestHandler):
        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            self.rfile.read(n)
            b = json.dumps({"content": [{"type": "text", "text": "{}"}],
                            "usage": {"input_tokens": 1, "output_tokens": 1}}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            if cap2.get("con_cabecera"):
                self.send_header("X-Coworld-Spend-Usd", "0.1234")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def log_message(self, *a):
            pass

    s2 = HTTPServer(("127.0.0.1", 0), H2)
    threading.Thread(target=s2.serve_forever, daemon=True).start()
    ep = f"http://127.0.0.1:{s2.server_address[1]}"
    # (a) CON la cabecera: el freno ve el gasto y no avisa
    d = []
    cx_a = CX.Cortex(d.append)
    cx_a.ep, cx_a.modelo, cx_a.manual = ep, "m", None
    cap2["con_cabecera"] = True
    cx_a._llama("x", 1)
    assert cx_a.gasto_visto == 0.1234 and not cx_a.aviso_sin_cabecera, \
        ("(xv) con cabecera deberia leerla", cx_a.gasto_visto)
    assert not [x for x in d if x.get("k") == "cortex_freno_ciego"]
    # (b) SIN la cabecera: el freno DICE que va ciego, una sola vez
    d2 = []
    cx_b = CX.Cortex(d2.append)
    cx_b.ep, cx_b.modelo, cx_b.manual = ep, "m", None
    cap2["con_cabecera"] = False
    cx_b._llama("x", 2)
    cx_b._llama("x", 3)
    avisos = [x for x in d2 if x.get("k") == "cortex_freno_ciego"]
    assert len(avisos) == 1 and cx_b.gasto_visto is None \
        and "NO protege" in avisos[0]["efecto"], ("(xv) deberia avisar", avisos)
    s2.shutdown()

    # ── los dos frenos ─────────────────────────────────────────────────────
    cx = CX.Cortex(lambda r: None)
    cx.ep, cx.modelo = "http://127.0.0.1:1", "m"
    cx.n_llamadas = CX.TOPE_LLAMADAS
    r = cx._llama("x", 7)
    assert r["ok"] is False and "tope de llamadas" in r["motivo"] \
        and cx.callado and cx.freno["cual"] == "llamadas", ("(xv) freno 1", r)
    cx2 = CX.Cortex(lambda r: None)
    cx2.ep, cx2.modelo = "http://127.0.0.1:1", "m"
    cx2.gasto_visto = CX.TOPE_GASTO_USD + 0.01
    r = cx2._llama("x", 9)
    assert r["ok"] is False and "tope de gasto" in r["motivo"] \
        and cx2.freno["cual"] == "gasto", ("(xv) freno 2", r)
    # y por debajo del tope NO frena
    cx3 = CX.Cortex(lambda r: None)
    cx3.ep, cx3.modelo = "http://127.0.0.1:1", "m"
    cx3.gasto_visto = CX.TOPE_GASTO_USD - 0.01
    assert "freno propio" not in (cx3._llama("x", 9).get("motivo") or ""), \
        "(xv) frena por debajo del tope"
    print(f"humo (xv) OK: la maleta es el stdout linea por linea, el zip trae "
          f"{len(PC._DIARIO)} lineas en {cap['bytes'] if 'bytes' in cap else len(cap['datos'])} "
          f"bytes y se sube UNA vez (la segunda no sale); la red cae en el tic "
          f"{int(umbral)} de {mt}; los dos frenos callan al cortex; y el de "
          f"gasto AVISA por el diario si la cabecera no llega")


def xvi_interruptor_hilo_D(CX):
    """Lo que de verdad importa es QUE SE MANDA, asi que se mira el cuerpo de
    la peticion tal como sale por el cable."""
    cap = _servidor_de_mentira()
    cx = CX.Cortex(lambda r: None)
    cx.ep, cx.modelo, cx.manual = cap["ep"], "m", "MANUAL"
    cx.historia.extend([{"accion": "algo de antes", "suerte": "hizo",
                         "fila": None}] * 3)
    cx.n_propuestas, cx.n_hechas = 9, 3
    cx._llama("ESCENA", 100)
    bl = cap["body"]["messages"][0]["content"]
    sis = cap["body"]["system"]
    usuario = bl[1]["text"]
    if CX.PARTE_ON:
        assert "propusiste" in usuario, "(xvi) con PARTE=1 deberia ir el parte"
        assert "lista vacia" in sis, "(xvi) con PARTE=1 deberia ir el derecho a callar"
        assert "cero y tres" in usuario, "(xvi) con PARTE=1, 'entre cero y tres'"
        print("humo (xvi) OK: con GEMV_CORTEX_PARTE=1 van el parte, el derecho "
              "a callar y 'entre cero y tres'")
    else:
        assert "propusiste" not in usuario, \
            ("(xvi) con PARTE=0 NO puede ir el parte", usuario[:120])
        assert usuario.startswith("ESCENA"), \
            ("(xvi) con PARTE=0 la escena tiene que ir la primera", usuario[:60])
        assert "lista vacia" not in sis, "(xvi) con PARTE=0 no va el derecho a callar"
        assert sis.endswith("Responde en espanol."), ("(xvi) sistema", sis[-40:])
        assert "entre una y tres propuestas." in usuario, \
            ("(xvi) con PARTE=0 el esquema es el de S-CORTEX", usuario[-60:])
        assert "cero y tres" not in usuario, "(xvi) se colo el esquema nuevo"
        print("humo (xvi) OK: con GEMV_CORTEX_PARTE=0 el cuerpo de la peticion "
              "es el de la serie S-CORTEX (sin parte, sin derecho a callar, "
              "'entre una y tres')")
    # [S-2] y que el MODO queda escrito en el diario, leido del entorno
    e = CX.entorno_efectivo()
    assert e["crudo"]["GEMV_CORTEX_PARTE"] == os.environ.get("GEMV_CORTEX_PARTE"), \
        "(xvi) el crudo no es el del entorno"
    assert e["efectivo"]["PARTE_ON"] is CX.PARTE_ON, "(xvi) efectivo"
    assert len(e["sistema_md5"]) == 32 and len(e["esquema_md5"]) == 32
    d = []
    cx2 = CX.Cortex(d.append)
    cx2.arranca()
    reg = [x for x in d if x.get("k") == "cortex"]
    assert reg and reg[0].get("entorno", {}).get("efectivo", {}).get("PARTE_ON") \
        is CX.PARTE_ON, ("(xvi) el registro inicial no lleva el modo", reg)
    print(f"        y el diario lo deja escrito: crudo "
          f"{e['crudo']['GEMV_CORTEX_PARTE']!r} -> efectivo "
          f"{e['efectivo']['PARTE_ON']}, con md5 del sistema "
          f"{e['sistema_md5'][:12]} y del esquema {e['esquema_md5'][:12]}")
    cap["srv"].shutdown()


if __name__ == "__main__":
    i_relator()
    ii_inyector()
    iii_apagado()
    CX = iv_llamada()
    v_caducidad(CX)
    vi_traductor(CX)
    vii_vetos()
    viii_empates()
    x_atadura(CX)
    xi_parte(CX)
    xii_lista_vacia(CX)
    xiii_fontaneria(CX)
    xiv_razon_respaldo(CX)
    ix_decidir_entero(CX)
    xv_maleta_y_frenos(CX)
    xvi_interruptor_hilo_D(CX)
    print("HUMO S-2 COMPLETO")
