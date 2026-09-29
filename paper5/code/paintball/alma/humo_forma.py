"""[P5-6A · A6] EL HUMO DE LA POLITICA CON FORMAS. Ocho pruebas.

Corre dentro de la imagen y tumba el build si alguna falla, igual que los
dieciseis del cuatro. No llama a nadie de fuera: el sidecar es un servidor de
mentira en 127.0.0.1, como en `humo_cortex.py`.

  (a) con TODO apagado, la politica con formas decide **exactamente** lo mismo
      que la politica del cuatro en 200 tics de una escena grabada;
  (b) con GEMV_FORMA=1 y una forma inyectada a mano: el primer tramo aparece en
      `D.candidatos` con su ventaja, gana cuando debe, y se cae cuando la vida
      proyectada falla;
  (b2) los EMPATES son del cuerpo — la regla que en `policy_cortex.py` no corre;
  (c) ida y vuelta del hilo del hermano;
  (d) la confianza sube y baja como esta escrito, con dos formas de mentira;
  (e) el parte se construye y se manda por el cable;
  (f) el brazo T produce formas validas;
  (g) los frenos muerden y el ciego avisa;
  (h) la subida del artefacto, con el diario entero y los registros nuevos.
"""
import copy
import json
import os
import sys

sys.path.insert(0, "/app")
AQUI = os.path.dirname(os.path.abspath(__file__))
for _p in (AQUI, os.path.join(os.path.dirname(os.path.dirname(AQUI)),
                              "cantera", "paper5")):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

from alma import humo_cortex as HC                   # noqa: E402
from alma import decisor_zs as D                     # noqa: E402
from alma import appraisal_zs_v42_exp as A           # noqa: E402

_mundo_y_obs, _obs = HC._mundo_y_obs, HC._obs


def _recarga(**env):
    """Reimporta `policy_forma` con los interruptores puestos."""
    for k, v in env.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    # OJO: no basta con borrar de `sys.modules`. `from alma import X` devuelve
    # el ATRIBUTO del paquete si existe, sin volver a importar, asi que el
    # modulo viejo (con los interruptores viejos) sobreviviria. Hay que borrar
    # las dos cosas e importar por `importlib`.
    import alma as _pkg
    import importlib
    for m in [k for k in list(sys.modules)
              if k.startswith("alma.policy_forma")]:
        del sys.modules[m]
    if hasattr(_pkg, "policy_forma"):
        delattr(_pkg, "policy_forma")
    PF = importlib.import_module("alma.policy_forma")
    esperado = (env.get("GEMV_FORMA") == "1")
    assert PF.FORMA_ON is esperado, \
        ("la recarga NO tomo los interruptores", PF.FORMA_ON, esperado)
    return PF


def _ds(radio):
    """`radio["candidatos"]` viene aplanado a floats salvo cada 24 tics."""
    return {k: (v["d"] if isinstance(v, dict) else v)
            for k, v in (radio or {}).get("candidatos", {}).items()}


def _prepara(alma, mundo):
    alma.mundo = mundo
    alma.filas_mapa = list(getattr(mundo, "static_map", []) or [])
    return alma


# ── (a) con todo apagado, la misma decision ──────────────────────────────
def a_apagado():
    from alma import policy_cortex as PC
    PF = _recarga(GEMV_FORMA=None, GEMV_HILO_FORMA=None,
                  GEMV_CONSEJERO_FORMA=None, GEMV_FORMAS_AZAR=None)
    assert PF.FORMA_ON is False, "(a) GEMV_FORMA deberia estar apagado"
    mundo, ticks = _mundo_y_obs()
    a1 = _prepara(PC.Alma(), mundo)
    a2 = _prepara(PF.AlmaForma(), mundo)
    n = iguales = 0
    for r in ticks:
        o = _obs(r)
        x1, _r1 = a1.decidir(copy.deepcopy(o))
        x2, _r2 = a2.decidir(copy.deepcopy(o))
        if r.get("phase") != "live":
            continue
        n += 1
        iguales += int(json.dumps(x1, sort_keys=True)
                       == json.dumps(x2, sort_keys=True))
    assert n >= 190, ("(a) pocos tics live", n)
    assert iguales == n, ("(a) la decision NO es identica", iguales, n)
    print(f"humo (a) OK: con todo apagado, {iguales}/{n} tics con la MISMA "
          f"decision que la politica del cuatro (100,00 %)")


# ── (b) la forma inyectada: entra, gana y se cae ─────────────────────────
def b_forma_inyectada():
    PF = _recarga(GEMV_FORMA="1")
    from alma import forma_viva as FV
    mundo, ticks = _mundo_y_obs()
    alma = _prepara(PF.AlmaForma(), mundo)
    # un tic con las PIERNAS LIBRES: si estan enfriando, el cuerpo veta la
    # receta de ir y la forma no llega a la mesa (y eso se prueba aparte).
    vivos = [r for r in ticks if r.get("phase") == "live"
             and not (r.get("move_ready_in") or 0)]
    assert vivos, "(b) no hay tics con piernas libres"
    r0 = vivos[0]
    o = _obs(r0)
    alma.tick = r0["tick"]
    alma.mem.observa(o, mundo, alma.tick)
    alma.bloqueos.actualiza(o, mundo, None, alma.tick)
    pos = tuple(o["you"]["pos"])
    destino = (pos[0] + 1, pos[1])
    fv = FV.FormaViva(1, [{"destino": destino, "intencion": "ir",
                           "esperar": 0}], alma.tick, origen="mano")
    fv.estado, fv.ventaja = "aceptada", 0.25
    fv.curva = [{"tic": alma.tick + 11, "d": 3.0, "vida": 100.0}]
    fv.tics = [alma.tick + 11]
    alma.vivas = [fv]
    # 1) el primer tramo APARECE en D.candidatos con su receta
    visto = {}
    _orig = D.candidatos

    def _espia(ob, mu, me, tk, bl=None, _o=_orig):
        base = list(_o(ob, mu, me, tk, bl))
        visto["base"] = {c[0] for c in base}
        return base
    D.candidatos = _espia
    try:
        accion, radio = alma.decidir(copy.deepcopy(o))
    finally:
        D.candidatos = _orig
    nombre = f"_FM_ir_{destino[0]}_{destino[1]}"
    assert nombre in radio["candidatos"], \
        ("(b) el primer tramo NO entro en la mesa", r0["tick"],
         sorted(radio["candidatos"]))
    assert nombre not in visto["base"], "(b) el cuerpo ya lo ofrecia: mal caso"
    print(f"humo (b1) OK: el primer tramo entra como `{nombre}` "
          f"con ventaja {fv.ventaja}")
    # 2) gana cuando su `d` es la menor
    ds = _ds(radio)
    mejor = min(ds, key=ds.get)
    print(f"humo (b1) OK: elegido `{radio['elegido']}`, mejor `{mejor}` "
          f"(d {ds[mejor]:.5f}); la forma quedo en d {ds[nombre]:.5f}")
    # 2 bis) GANA CUANDO DEBE: se recorre hasta dar con un tic en que la forma
    # tiene la `d` MENOR de la mesa, y ahi tiene que llevarse el tic.
    gano_alguna = None
    for r in vivos[:80]:
        oi = _obs(r)
        al = _prepara(PF.AlmaForma(), mundo)
        al.tick = r["tick"]
        al.mem.observa(oi, mundo, al.tick)
        al.bloqueos.actualiza(oi, mundo, None, al.tick)
        pi = tuple(oi["you"]["pos"])
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1)):
            q = (pi[0] + dx, pi[1] + dy)
            f2 = FV.FormaViva(7, [{"destino": q, "intencion": "ir",
                                   "esperar": 0}], al.tick, origen="mano")
            f2.estado, f2.ventaja = "aceptada", 0.6   # ventaja del area
            f2.curva = [{"tic": al.tick + 11, "d": 3.0, "vida": 100.0}]
            f2.tics = [al.tick + 11]
            al.vivas = [f2]
            _a3, rad3 = al.decidir(copy.deepcopy(oi))
            d3 = _ds(rad3)
            n3 = f2.nombre()
            if n3 not in d3:
                continue
            otros = {k: v for k, v in d3.items() if k != n3}
            if not otros:
                continue
            ajustada = d3[n3] - f2.ventaja
            if ajustada < min(otros.values()) - 1e-9:
                assert rad3["elegido"] == n3, \
                    ("(b) la forma ganaba con su ventaja y NO gano",
                     r["tick"], rad3["elegido"], ajustada, min(otros.values()))
                assert _a3 is not None and _a3.get("type"), \
                    ("(b) la accion emitida no es legal", _a3)
                gano_alguna = (r["tick"], n3, d3[n3], f2.ventaja, ajustada,
                               min(otros.values()), _a3)
                break
        if gano_alguna:
            break
    assert gano_alguna, "(b) no se encontro ningun tic en que la forma sea la mejor"
    print(f"humo (b1) OK: GANA CUANDO DEBE — tic {gano_alguna[0]}, forma "
          f"`{gano_alguna[1]}`: d {gano_alguna[2]:.5f} menos ventaja "
          f"{gano_alguna[3]:.2f} = {gano_alguna[4]:.5f}, contra "
          f"{gano_alguna[5]:.5f} del mejor propio; se lleva el tic y emite "
          f"{json.dumps(gano_alguna[6], sort_keys=True)}")
    # 3) SE CAE cuando la vida proyectada falla
    fv.i_punto = 1
    fv.curva = [{"tic": alma.tick, "d": 3.0, "vida": 100.0}]
    cae, motivo = fv.falla_lo_previsto(80.0, alma.filas_mapa, alma.tick)
    assert cae and "vida real" in motivo, ("(b) no se cayo por vida", motivo)
    print(f"humo (b2) OK: se cae por la vida — {motivo}")
    cae2, motivo2 = fv.falla_lo_previsto(100.0, alma.filas_mapa, alma.tick)
    assert not cae2, ("(b) se cayo sin motivo", motivo2)
    # 4) se cae si el destino deja de ser alcanzable
    fv.i_punto = 0          # vuelve a mirar el primer tramo
    filas_mal = list(alma.filas_mapa)
    _f = list(filas_mal[destino[1]])
    _f[destino[0]] = "#"
    filas_mal[destino[1]] = "".join(_f)
    cae3, motivo3 = fv.falla_lo_previsto(100.0, filas_mal, alma.tick)
    assert cae3 and "alcanzable" in motivo3, ("(b) destino solido", motivo3)
    print(f"humo (b3) OK: se cae por el destino — {motivo3}")
    # 5) con las piernas enfriando, el cuerpo VETA la forma: no llega a la mesa
    frio = next((r for r in ticks if r.get("phase") == "live"
                 and (r.get("move_ready_in") or 0) > 0), None)
    if frio is not None:
        o2 = _obs(frio)
        alma2 = _prepara(PF.AlmaForma(), mundo)
        alma2.tick = frio["tick"]
        alma2.mem.observa(o2, mundo, alma2.tick)
        alma2.bloqueos.actualiza(o2, mundo, None, alma2.tick)
        p2 = tuple(o2["you"]["pos"])
        fv2 = FV.FormaViva(2, [{"destino": (p2[0] + 1, p2[1]),
                                "intencion": "ir", "esperar": 0}],
                           alma2.tick, origen="mano")
        fv2.estado, fv2.ventaja = "aceptada", 0.25
        fv2.curva = [{"tic": alma2.tick, "d": 3.0, "vida": 100.0}]
        fv2.tics = [alma2.tick + 11]
        alma2.vivas = [fv2]
        _a2, radio2 = alma2.decidir(copy.deepcopy(o2))
        n2 = fv2.nombre()
        assert n2 not in (radio2 or {}).get("candidatos", {}), \
            ("(b) una forma vetada llego a la mesa", n2)
        print(f"humo (b4) OK: con las piernas enfriando "
              f"({frio.get('move_ready_in')} tics) el cuerpo VETA la forma "
              f"y no llega a la mesa")


# ── (b5) la carrera: mutar mem y bloqueos MIENTRAS se juzga ─────────────
def b5_carrera():
    """[P5-6C · C1bis] En la tanda 1 descartada, 1 de 176 evaluaciones reventaba
    con `RuntimeError` porque `_juzga` recibia la `mem` y los `bloqueos` VIVOS,
    que el bucle del juego muta cada tic. Aqui se muta a proposito."""
    import copy as _c
    import threading
    PF = _recarga(GEMV_FORMA="1")
    from alma import forma_viva as FV
    mundo, ticks = _mundo_y_obs()
    alma = _prepara(PF.AlmaForma(), mundo)
    vivos = [r for r in ticks if r.get("phase") == "live"
             and not (r.get("move_ready_in") or 0)]
    r0 = vivos[0]
    o = _obs(r0)
    alma.tick = r0["tick"]
    alma.mem.observa(o, mundo, alma.tick)
    alma.bloqueos.actualiza(o, mundo, None, alma.tick)
    pos = tuple(o["you"]["pos"])
    def forma():
        f = FV.FormaViva(1, [{"destino": (pos[0] + 2, pos[1]), "intencion": "ir",
                              "esperar": 0},
                             {"destino": None, "intencion": "esperar",
                              "esperar": 20}], alma.tick, origen="mano")
        return f
    # 1) el juicio LIMPIO, de referencia
    v1, a1, c1, t1 = alma._juzga(forma(), o)
    assert not str(v1).startswith("revienta"), ("(b5) revento en limpio", v1)
    # 2) el mismo juicio, con el bucle mutando la memoria y los bloqueos
    parar = threading.Event()
    fallos = []

    def muta():
        i = 0
        while not parar.is_set():
            i += 1
            # exactamente lo que hace el bucle del juego cada tic, que es la
            # mutacion que de verdad corria contra el hilo
            try:
                r = ticks[i % len(ticks)]
                oi = _obs(r)
                alma.mem.observa(oi, mundo, r["tick"])
                alma.bloqueos.actualiza(oi, mundo, None, r["tick"])
            except Exception as ex:
                fallos.append(repr(ex)[:120])

    h = threading.Thread(target=muta, daemon=True)
    h.start()
    resultados, vivos_rotos = [], 0
    try:
        for _ in range(12):
            m, b = _c.deepcopy(alma.mem), _c.deepcopy(alma.bloqueos)
            resultados.append(alma._juzga(forma(), o, m, b)[0])
        # CONTRAPRUEBA, informativa y NO aseverada (una carrera no siempre
        # dispara): lo mismo con los objetos VIVOS, que es como estaba.
        for _ in range(12):
            if str(alma._juzga(forma(), o)[0]).startswith("revienta"):
                vivos_rotos += 1
    finally:
        parar.set()
        h.join(timeout=2)
    revientan = [r for r in resultados if str(r).startswith("revienta")]
    assert not revientan, ("(b5) siguen reventando con copias", revientan)
    assert all(r == v1 for r in resultados), \
        ("(b5) el veredicto cambia con la mutacion", v1, set(resultados))
    print(f"humo (b5) OK: con la memoria y los bloqueos mutando en otro hilo, "
          f"{len(resultados)} juicios con COPIAS: cero reventones y el "
          f"veredicto es el mismo que en limpio (`{v1}`)")
    print(f"humo (b5) · contraprueba (informativa, no aseverada): con los "
          f"objetos VIVOS y la misma mutacion, {vivos_rotos} de 12 juicios "
          f"revientan")


# ── (b2) los empates son del cuerpo ──────────────────────────────────────
def b2_empates():
    PF = _recarga(GEMV_FORMA="1")
    from alma import forma_viva as FV
    mundo, ticks = _mundo_y_obs()
    alma = _prepara(PF.AlmaForma(), mundo)
    vivos = [r for r in ticks if r.get("phase") == "live"]
    n = empates = 0
    for r in vivos[:25]:
        o = _obs(r)
        alma.tick = r["tick"]
        # una forma cuyo primer tramo es QUEDARSE: clona a `noop` y EMPATA
        fv = FV.FormaViva(99, [{"destino": None, "intencion": "esperar",
                                "esperar": 11}], alma.tick, origen="mano")
        fv.estado = "aceptada"
        fv.curva = [{"tic": alma.tick, "d": 3.0, "vida": 100.0}]
        fv.tics = [alma.tick + 11]
        alma.vivas = [fv]
        accion, radio = alma.decidir(copy.deepcopy(o))
        if radio is None:
            continue
        n += 1
        empates += int(bool(alma.cx_empate))
        # nunca puede EMITIRSE una forma que solo empata
        ds = _ds(radio)
        iny = [k for k in ds if k.startswith("_FM_")]
        if iny and radio["elegido"] in iny:
            propios = {k: v for k, v in ds.items() if k not in iny}
            assert ds[radio["elegido"]] < min(propios.values()) - 1e-9, \
                ("(b2) una forma gano SIN ser estrictamente mejor",
                 r["tick"], ds[radio["elegido"]], min(propios.values()))
    assert n >= 15, ("(b2) pocos tics", n)
    print(f"humo (b2) OK: en {n} tics ninguna forma se lleva el tic por "
          f"empate; la regla que en policy_cortex.py no corre, aqui si")


# ── (c) el hilo del hermano, ida y vuelta ────────────────────────────────
def c_hilo():
    from alma import hilo_forma as HF
    casos = [
        ([{"destino": (23, 20), "intencion": "ir"},
          {"destino": None, "intencion": "usar"},
          {"destino": (24, 24), "intencion": "coger"},
          {"destino": None, "intencion": "esperar"}],
         [4312, 4360, 4470, 4500], 87, 2.5, True),
        ([], [], 100, 0.0, False),
        ([{"destino": (0, 0), "intencion": "ir"}], [18240], 1, 3.525, True),
    ]
    for tramos, tics, hp, W, herido in casos:
        s, ok = HF.codifica(tramos, hp, W, herido, tics)
        assert ok, ("(c) no cabe en 120 ASCII", len(s), s)
        d = HF.decodifica(s)
        assert d is not None, ("(c) no decodifica", s)
        s2, _ = HF.codifica(d["tramos"], d["hp"], d["W"], d["herido"], d["tics"])
        assert s2 == s, ("(c) la ida y vuelta NO es identica", s, s2)
        assert HF.igual(d, HF.decodifica(s2)), "(c) el contenido cambia"
        print(f"humo (c) OK: {len(s):3d} ASCII, ida y vuelta identica · {s}")
    assert HF.decodifica("hola") is None and HF.decodifica("GF1|mal|1,2,3") is None
    print("humo (c) OK: la basura no decodifica")


# ── (d) la confianza, con dos formas de mentira ──────────────────────────
def d_confianza():
    from alma import confianza_viva as CV
    c = CV.Confianza()
    assert abs(c.C - 0.30) < 1e-9 and abs(c.margen() - 0.062) < 1e-9, \
        ("(d) el arranque no es el escrito", c.C, c.margen())
    v, a, b = c.comprueba(3.0, 3.1, 100, "F1", 0)          # acierto
    assert v == "acierto" and abs(b - 0.40) < 1e-9, ("(d) no subio", v, b)
    v, a, b = c.comprueba(3.2, 3.1, 200, "F1", 1)          # fallo (>0,05)
    assert v == "fallo" and abs(b - 0.25) < 1e-9, ("(d) no bajo", v, b)
    assert abs(c.margen() - (0.02 + 0.06 * 0.75)) < 1e-9, "(d) margen mal"
    print(f"humo (d) OK: C 0,30 -> 0,40 (acierto) -> 0,25 (fallo); "
          f"margen {c.margen():.4f}")
    c2 = CV.Confianza()
    callo = False
    for i in range(6):
        c2.comprueba(9.0, 1.0, i * 10, "X", 0)
        callo = c2.forma_cerrada(True, i * 10) or callo
    assert c2.C == 0.0 and callo, ("(d) el cuerpo no callo", c2.C, callo)
    assert c2.callado(10) and not c2.callado(10 ** 6), "(d) el callar no caduca"
    print(f"humo (d) OK: con C=0 y cinco formas malas el cuerpo calla al "
          f"consejero {CV.CALLADO_TICS} tics, y luego vuelve")


# ── (e) el parte se construye y se manda ─────────────────────────────────
def e_parte():
    PF = _recarga(GEMV_FORMA="1", GEMV_CONSEJERO_FORMA="1")
    cap = HC._servidor_de_mentira()
    cuerpo = {"content": [{"type": "text", "text": json.dumps(
        {"formas": [{"tramos": [{"destino": [3, 3], "intencion": "ir",
                                 "vida": "+", "manos": "0", "vinculo": "0",
                                 "por": "F-DANO", "porque": "x"}],
                     "final": "y"}], "callar": False})}],
              "usage": {"input_tokens": 9, "output_tokens": 3}}
    cap["cuerpo"] = cuerpo
    cerradas = [{"id": 1, "estado": "caida", "tramos": [{}, {}],
                 "motivo_caida": "la vida real 60 esta por debajo de la "
                                 "proyectada 90 menos 10",
                 "tramos_detalle": [{"i": 1, "dicho": {"vida": "+", "manos": "0",
                                                       "vinculo": "-"},
                                     "por": "R-CARENCIA",
                                     "proyectado": {"vida": "-", "manos": "0",
                                                    "vinculo": "0"},
                                     "real": {"vida": "-", "manos": "-",
                                              "vinculo": "0"}}]}]
    txt = PF.parte_de_formas(cerradas, 0.45, 0.053)
    for trozo in ("ACEPTADA y luego caida", "dijiste vida +",
                  "el cuerpo proyecto vida -", "de verdad sintio vida -",
                  "R-CARENCIA", "0.45", "0.053"):
        assert trozo in txt, ("(e) falta en el parte", trozo, txt[:400])
    print("humo (e) OK: el parte dice lo dicho, lo proyectado y lo sentido:")
    for linea in txt.splitlines()[:6]:
        print("    " + linea)
    cf = PF.ConsejeroForma(lambda r: None)
    cf.ep, cf.modelo, cf.manual = cap["ep"], "modelo-de-mentira", "MANUAL"
    r = cf._llama("RELATO\n\n" + txt, 100)
    assert r["ok"] and r["codigo"] == 200, ("(e) la llamada fallo", r)
    mandado = cap["body"]["messages"][0]["content"][-1]["text"]
    assert txt in mandado, "(e) el parte NO viajo en el cuerpo de la peticion"
    assert cap["body"]["messages"][0]["content"][0]["cache_control"] == \
        {"type": "ephemeral"}, "(e) falta cache_control en el manual"
    assert "renglones" in cap["body"]["system"] or \
        "renglon" in cap["body"]["system"], "(e) el sistema no lleva la tabla"
    cap["srv"].shutdown()
    print(f"humo (e) OK: el parte viajo por el cable ({len(mandado)} bytes) y "
          f"el manual va cacheado")


# ── (e2) el parte YA NO VA MUDO ─────────────────────────────────────────
def e2_parte_no_mudo():
    """[P5-6C · C1bis] En la tanda 1 descartada, «el cuerpo proyecto» salia `?`
    en todos los partes porque `forma.curva_H` no devuelve las necesidades.
    Aqui se comprueba que el parte lleva signos de verdad."""
    PF = _recarga(GEMV_FORMA="1")
    from alma import forma_viva as FV
    mundo, ticks = _mundo_y_obs()
    alma = _prepara(PF.AlmaForma(), mundo)
    vivos = [r for r in ticks if r.get("phase") == "live"
             and not (r.get("move_ready_in") or 0)]
    r0 = vivos[0]
    o = _obs(r0)
    alma.tick = r0["tick"]
    alma.mem.observa(o, mundo, alma.tick)
    alma.bloqueos.actualiza(o, mundo, None, alma.tick)
    pos = tuple(o["you"]["pos"])
    fv = FV.FormaViva(1, [
        {"destino": (pos[0] + 2, pos[1]), "intencion": "ir", "esperar": 0,
         "_mitad": {"vida": "0", "manos": "+", "vinculo": "0"},
         "_por": "R-CARENCIA", "_porque": "voy a por el arma"},
        {"destino": None, "intencion": "esperar", "esperar": 30,
         "_mitad": {"vida": "+", "manos": "0", "vinculo": "0"},
         "_por": "F-DANO", "_porque": "espero a curarme"}],
        alma.tick, origen="mano")
    ver, ar, cf, tics = alma._juzga(fv, o)
    fv.curva, fv.tics = cf, tics
    assert any(p.get("nec") for p in cf), \
        ("(e2) la curva sigue sin necesidades", [list(p) for p in cf[:2]])
    det = alma._detalle(fv)
    con = [d for d in det if d.get("proyectado")]
    assert con, ("(e2) el parte sigue MUDO", det)
    for d in con:
        for k in ("vida", "manos", "vinculo"):
            assert d["proyectado"][k] in ("+", "0", "-"), (d)
    txt = PF.parte_de_formas(
        [dict(fv.registro(), estado="rechazada_area", tramos_detalle=det)],
        0.3, 0.062)
    assert "vida ?" not in txt, ("(e2) el parte todavia escribe `?`", txt[:300])
    print(f"humo (e2) OK: la curva trae necesidades en "
          f"{sum(1 for p in cf if p.get('nec'))}/{len(cf)} puntos, y el parte "
          f"escribe signos de verdad en {len(con)}/{len(det)} tramos")
    for linea in txt.splitlines():
        if linea.strip().startswith("Tramo"):
            print("    " + linea.strip())


# ── (f) el brazo T ───────────────────────────────────────────────────────
def f_azar():
    PF = _recarga(GEMV_FORMA="1", GEMV_FORMAS_AZAR="1",
                  GEMV_CONSEJERO_FORMA=None)
    assert PF.AZAR_ON and not PF.CONSEJERO_ON, "(f) interruptores mal"
    mundo, ticks = _mundo_y_obs()
    alma = _prepara(PF.AlmaForma(), mundo)
    vivos = [r for r in ticks if r.get("phase") == "live"]
    n = malos = 0
    largos = {}
    filas = alma.filas_mapa
    for r in vivos[:60]:
        o = _obs(r)
        alma.tick = r["tick"]
        fv = alma._forma_al_azar(o)
        n += 1
        largos[len(fv.tramos)] = largos.get(len(fv.tramos), 0) + 1
        assert 1 <= len(fv.tramos) <= 4, ("(f) tramos fuera de rango",
                                          len(fv.tramos))
        for tr in fv.tramos:
            d = tr.get("destino")
            assert tr["intencion"] in ("ir", "coger", "esperar"), tr
            if d is None:
                continue
            if not (0 <= d[0] < len(filas) and 0 <= d[1] < len(filas)) \
                    or filas[d[1]][d[0]] in ("#", "F", "R"):
                malos += 1
    assert malos == 0, ("(f) destinos inalcanzables", malos)
    assert n >= 50, ("(f) pocas formas", n)
    print(f"humo (f) OK: {n} formas al azar, 0 destinos inalcanzables, "
          f"tramos {dict(sorted(largos.items()))}")


# ── (g) los frenos ───────────────────────────────────────────────────────
def g_frenos():
    PF = _recarga(GEMV_FORMA="1", GEMV_CONSEJERO_FORMA="1")
    avisos = []
    cf = PF.ConsejeroForma(avisos.append)
    cf.ep, cf.modelo = "http://127.0.0.1:1", "m"
    cf.n_llamadas = PF.TOPE_LLAMADAS
    r = cf._llama("x", 10)
    assert not r["ok"] and "llamadas" in r["motivo"], ("(g) freno 1", r)
    assert cf.callado and any(a.get("k") == "forma_freno" for a in avisos)
    print(f"humo (g) OK: el freno de llamadas muerde en {PF.TOPE_LLAMADAS} "
          f"y calla al consejero")
    avisos2 = []
    cf2 = PF.ConsejeroForma(avisos2.append)
    cf2.ep, cf2.modelo = "http://127.0.0.1:1", "m"
    cf2.gasto_visto = PF.TOPE_GASTO_USD + 0.01
    r2 = cf2._llama("x", 10)
    assert not r2["ok"] and "gasto" in r2["motivo"], ("(g) freno 2", r2)
    print(f"humo (g) OK: el freno de gasto muerde en "
          f"{PF.TOPE_GASTO_USD:.2f} $")
    # el freno CIEGO: respuesta sin la cabecera de gasto
    cap = HC._servidor_de_mentira()
    avisos3 = []
    cf3 = PF.ConsejeroForma(avisos3.append)
    cf3.ep, cf3.modelo, cf3.manual = cap["ep"], "m", None
    cf3._llama("x", 10)
    cap["srv"].shutdown()
    ciego = [a for a in avisos3 if a.get("k") == "forma_freno_ciego"]
    assert ciego, ("(g) el freno ciego NO aviso", avisos3)
    assert "NO protege" in ciego[0]["efecto"]
    print(f"humo (g) OK: sin la cabecera X-Coworld-Spend-Usd el freno AVISA "
          f"de que va ciego: «{ciego[0]['efecto']}»")


# ── (h) la subida del artefacto con los registros nuevos ─────────────────
def h_artefacto():
    import io
    import threading
    import zipfile
    from http.server import BaseHTTPRequestHandler, HTTPServer
    PF = _recarga(GEMV_FORMA="1")
    from alma import policy_cortex as PC
    cap = {"n": 0}

    class H(BaseHTTPRequestHandler):
        def do_PUT(self):
            n = int(self.headers.get("Content-Length") or 0)
            cap["datos"] = self.rfile.read(n)
            cap["tipo"] = self.headers.get("Content-Type")
            cap["n"] += 1
            self.send_response(201 if cap["n"] == 1 else 204)
            self.end_headers()

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    os.environ["COWORLD_PLAYER_ARTIFACT_UPLOAD_URL"] = \
        f"http://127.0.0.1:{srv.server_address[1]}/subir"
    mundo, ticks = _mundo_y_obs()
    alma = _prepara(PF.AlmaForma(), mundo)
    # se escriben, a mano, los ocho registros nuevos
    nuevos = ("forma_propuesta", "forma_evaluada", "forma_aceptada",
              "forma_caida", "confianza", "parte", "hilo_forma", "tiempo_tic")
    for k in nuevos:
        PF.log({"k": k, "tick": 1, "humo": True})
    ok = PC.sube_artefacto(alma, "humo (h)")
    srv.shutdown()
    os.environ.pop("COWORLD_PLAYER_ARTIFACT_UPLOAD_URL", None)
    assert ok and cap["n"] == 1, ("(h) no subio una vez", ok, cap)
    assert cap["tipo"] == "application/zip", ("(h) tipo", cap.get("tipo"))
    z = zipfile.ZipFile(io.BytesIO(cap["datos"]))
    nombre = z.namelist()[0]
    cuerpo = z.read(nombre).decode()
    faltan = [k for k in nuevos if f'"k":"{k}"' not in cuerpo]
    assert not faltan, ("(h) faltan registros en el artefacto", faltan)
    print(f"humo (h) OK: artefacto subido UNA vez ({len(cap['datos'])} bytes "
          f"de zip, entrada `{nombre}`) con los ocho registros nuevos: "
          f"{', '.join(nuevos)}")





# ── (i) el bucle de RED entero, con un websocket de mentira ──────────────
def i_bucle_de_red():
    """Lo que ningun humo probaba: `run()` de punta a punta sin plataforma.

    Se le da a `PC.decisor` un websocket falso que escupe el `player_config`,
    doscientos `observation` de una partida grabada y el `final`, y se recoge
    todo lo que la politica manda por el cable. Esto es lo que habria que
    haber probado ANTES de gastar una partida.
    """
    import asyncio
    PF = _recarga(GEMV_FORMA="1", GEMV_HILO_FORMA="1",
                  GEMV_CONSEJERO_FORMA="1", GEMV_FORMAS_AZAR=None)
    from alma import policy_cortex as PC
    d = json.load(open(os.path.join(AQUI, "humo_200tics.json")))
    pc = dict(d["player_config"])
    pc["type"] = "player_config"
    pc["arena"] = {"size": d["static_map"].get("size") or 48,
                   "static_map": list(d["static_map"]["filas"]),
                   "legend": dict(d["static_map"].get("legend") or HC.LEY),
                   "pedestals": d["static_map"].get("pedestals") or []}
    pc["items"] = list(d["catalogo"]["items"])
    pc["stats"] = {"budget": 20, "min": 1, "max": 10, "default": [5, 5, 5, 5]}
    mensajes = [json.dumps(pc)]
    for r in d["ticks"]:
        mensajes.append(json.dumps(_obs(r)))
    mensajes.append(json.dumps({"type": "final", "placement": 9, "kills": 0,
                                "score": 0.0, "reason": "humo",
                                "match_ticks": d["ticks"][-1]["tick"]}))
    enviados = []

    class WS:
        def __aiter__(self):
            self._i = 0
            return self

        async def __anext__(self):
            if self._i >= len(mensajes):
                raise StopAsyncIteration
            m = mensajes[self._i]
            self._i += 1
            return m

        async def send(self, s):
            enviados.append(json.loads(s))

    alma = PF.AlmaForma()
    diario0 = len(PC._DIARIO)
    # el canal `team` pasa a ser la forma, como en `run()`
    _orig_emite = PC.PARTE.emite

    def _emite(msg, tick, mundo, mem, ventana, _o=_orig_emite, _a=alma):
        s = _a.texto_hilo(msg)
        return s if s else _o(msg, tick, mundo, mem, ventana)
    PC.PARTE.emite = _emite
    try:
        alma.cf.arranca()
        asyncio.run(PC.decisor(WS(), alma))
    finally:
        PC.PARTE.emite = _orig_emite
    nuevas = PC._DIARIO[diario0:]
    claves = {}
    for linea in nuevas:
        try:
            k = json.loads(linea).get("k")
        except Exception:
            continue
        claves[k] = claves.get(k, 0) + 1
    acciones = [e for e in enviados if e.get("type") == "action"]
    charlas = [e for e in enviados if e.get("type") == "talk"]
    n_obs = sum(1 for r in d["ticks"])
    assert len(acciones) == n_obs, \
        ("(i) una emision por observacion", len(acciones), n_obs)
    assert claves.get("tick", 0) >= 190, ("(i) faltan registros de tic", claves)
    assert claves.get("tiempo_tic", 0) >= 190, ("(i) falta tiempo_tic", claves)
    assert claves.get("final"), "(i) no se registro el final"
    assert charlas, "(i) no salio ni un mensaje por el canal team"
    from alma import hilo_forma as HF
    gf = [t for t in charlas if (t.get("text") or "").startswith("GF1|")]
    assert gf, ("(i) el canal team no llevo la forma", charlas[:2])
    d0 = HF.decodifica(gf[0]["text"])
    assert d0 is not None, ("(i) lo emitido no decodifica", gf[0])
    # el hermano lo OYE: se le mete el mensaje por el chat y tiene que quedarse
    alma2 = PF.AlmaForma()
    alma2.mundo = alma.mundo
    alma2.tick = 300
    alma2._oye({"chat": [{"from": alma.mundo.teammate_slot,
                          "text": gf[0]["text"]}]})
    assert alma2.herm_dicho is not None, "(i) el hermano no oyo nada"
    assert HF.igual(alma2.herm_dicho, d0), "(i) lo oido no es lo dicho"
    print(f"humo (i) OK: el bucle de red entero — {len(acciones)} acciones "
          f"(una por observacion), {len(charlas)} mensajes de canal, "
          f"{len(gf)} con forma; el hermano los oye y decodifica igual")
    print(f"humo (i) OK: registros escritos: "
          f"{json.dumps({k: v for k, v in sorted(claves.items())}, ensure_ascii=False)}")





# ── (j) /spend: la segunda lectura del gasto ─────────────────────────────
def j_spend():
    """[P5-6C · C0] El consejero pregunta `/spend` cada 10 llamadas, y lo que
    lee CUADRA con la cabecera `X-Coworld-Spend-Usd`."""
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer
    PF = _recarga(GEMV_FORMA="1", GEMV_CONSEJERO_FORMA="1")
    estado = {"n": 0, "spend": 0.0, "gets": 0}
    cuerpo = {"content": [{"type": "text", "text": '{"formas":[],"callar":true}'}],
              "usage": {"input_tokens": 9, "output_tokens": 3}}

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            self.rfile.read(n)
            estado["n"] += 1
            estado["spend"] = round(estado["n"] * 0.004, 6)
            b = json.dumps(cuerpo).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("X-Coworld-Spend-Usd", f"{estado['spend']:.6f}")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            estado["gets"] += 1
            b = json.dumps({"spend_usd": estado["spend"],
                            "limit_usd": 5.0}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    diario = []
    cf = PF.ConsejeroForma(diario.append)
    cf.ep = f"http://127.0.0.1:{srv.server_address[1]}"
    cf.modelo, cf.manual = "modelo-de-mentira", None
    for i in range(1, 11):
        r = cf._llama("RELATO", 100 * i)
        assert r["ok"], ("(j) llamada mala", i, r)
    srv.shutdown()
    sp = [x for x in diario if x.get("k") == "forma_spend"]
    assert sp, ("(j) no se pidio /spend ni una vez", [x.get("k") for x in diario])
    assert estado["gets"] >= 1, "(j) el sidecar no recibio el GET"
    u = sp[-1]
    assert u.get("error") is None, ("(j) /spend fallo", u.get("error"))
    assert u.get("cuadra") is True, ("(j) /spend NO cuadra con la cabecera", u)
    assert u["por_que"].startswith("cada"), u
    print(f"humo (j) OK: tras {estado['n']} llamadas el consejero pidio "
          f"/spend {len(sp)} vez/veces; cabecera {u['cabecera_usd']} $ y "
          f"/spend {u['spend_usd']} $ CUADRAN (diferencia {u['diferencia']})")
    print(f"humo (j) OK: el registro que va al diario es "
          f"{json.dumps({k: v for k, v in u.items() if k != 'spend'}, ensure_ascii=False)}")


if __name__ == "__main__":
    a_apagado()
    b_forma_inyectada()
    b5_carrera()
    b2_empates()
    c_hilo()
    d_confianza()
    e_parte()
    e2_parte_no_mudo()
    f_azar()
    g_frenos()
    h_artefacto()
    i_bucle_de_red()
    j_spend()
    print("HUMO DE FORMAS COMPLETO")
