# Acta — EL INVENTARIO (v31) · BANCO VERDE (P2 reportado, no forzado)

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_59_el_don_que_se_adelanta.md` · Banco, **coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **v31 = v30 + la provisión**, de taller (`appraisal_zs.py ea5ecd3f…`,
  `decisor_zs.py 76171f7b…`). Interruptor de pareado `PROVISION_ON`
  (False = v30 bit a bit).

---

# LA IDEA (diseño de Manel, "por partes")

El don honesto del 57 llega tarde: se entra en banda porque te cazan, y con
el cazador pegado no hay casilla servible. **EL INVENTARIO adelanta el
gesto**: "si tú no llevas venda y yo llevo, te la dejo ANTES de que haga
falta; y si veo una y tú no tienes, la cojo para ti." El parte ya trae
`b<n>` de la hermana — hecho cierto (R1, caducidad). Sin violencia, sin
riesgo: **la jerarquía del miedo por encima de todo**.

# LA FAMILIA DE FILA, DOS CARAS

## S-PROVISION (dar antes) — funciona

- **Dispara**: hermana `b=0` (parte fresco), yo con **≥2 vendas reales** (el
  decisor estampa `_bot_real` a todas las fotos — patrón `_muro_on` — para
  que la foto del soltar no borre el malestar por sí sola), y **CALMA** (ni
  yo con agresor en la ventana S-7, ni ella con agresor en su parte).
- **Magnitud**: `PROVISION_M = 0.30`, malestar de **fondo** (lección del 46:
  hace importar, no obsesiona).
- **Alivio** (espejo del 56): entrega **servible** para ella (una venda en el
  suelo a ≤2 de ella, casilla libre) → `×PROVISION_ATEN = 0.15`; o, a >2, el
  **camino** (acercarme a su posición del parte) parcial, tope
  `CAMINO_GANA = 0.5`.
- **Actuación**: el candidato `soltar` —que ya existía para la hermana
  herida— **se abre también en calma-provisión** (hermana `b=0`, yo ≥2, sin
  caza). **No es un candidato nuevo** (misma receta `soltar`): es su
  disponibilidad ampliada, la cara de actuación de la fila. Declarado.
- **Tres componentes**: `(0.15, 0.25, 0.6)` — la familia de la pareja.

## R-ACOPIO POR DOS (coger para ti) — la fuerza existe, el flip no emerge

- **La fuerza**: en calma, hermana `b=0`, la carencia del acopio deja de
  saturarse con UNA venda —con **peso menor** que la mía: con una `R-ACOPIO =
  ACOPIO_POR_DOS = 0.10`, con dos `0`, con cero `ACOPIO_M = 0.18` (v30). Lee
  el pack de **la foto** (recoger alivia, como siempre en v30).
- **El reporte honesto** (forense en banco): **v30 ya coge todo botiquín
  ALCANZABLE** —R-CARENCIA satura en una venda (0,667 con 1 = con 2), así que
  el 2º no da riqueza, pero R-LLAMADA (0,05) basta para ir a por él. Más allá
  del horizonte de la mirada, la foto no llega a recogerlo y el por-dos no
  puede aliviar. **No existe una escena honesta donde v30 lo ignore y v31 lo
  coja**: el gesto "coger" es **redundante** con la recogida de botín que ya
  vive en la tabla. Siguiendo la regla del propio encargo ("si no emerge del
  descenso homeostático, NO se guioniza: se reporta") y la casa (46/53):
  **se mantiene la fuerza** (fondo correcto, byte-identidad preservada) y
  **se reporta el flip como no-emergente**, no se infla la constante.

# LAS SIETE PRUEBAS CONTRA SUS SELLOS (`alma/verifica_59.py`, VERDE)

| prueba | sello | resultado |
|---|---|---|
| **P1 DAR ANTES** | sellado | **VERDE** — b=0, yo=2, calma: a ≤2 v31 **suelta** (`soltar_first_aid`, S-PROVISION 0,30) donde v30 hacía `move_SE`; a >2 v31 **se acerca** (acaba a 1,0 de 6,0) |
| **P2 COGER PARA TI** | sellado | **REPORTE** (no gate) — la fuerza enciende (0,10 < 0,18, peso menor) y la venda importa; el **flip no emerge** (v30 ya coge lo alcanzable). Honesto, no forzado |
| **P3 ELLA LO RECOGE** | sellado | **VERDE** — la receptora con b=0 y venda a 1 va a por ella (`ir_objeto`; su propio acopio) |
| **P4 JERARQUÍA DEL MIEDO** | sellado (PARAR) | **VERDE** — perseguida con la hermana sin venda a la vista: v31 `usar_botiquin` == v27; **S-PROVISION apagada bajo caza** |
| **P5 SILENCIO Y SOLA** | sellados | **VERDE** — hermana b=1: v31 **byte-idéntica** a v30; sin hermana: **byte-idéntica a v27** |
| **P6 HONOR** | sellado | **VERDE** — escenas del 39/53 con parte (h10/h28/h72): v31 **byte-idéntica** a v30 — márgenes y tabú intactos |
| **P7 REGRESIÓN** | — | **VERDE** — bancos 13-58: **24/24**, 0 fallos; humo 3/3 (hash idéntico al previo); determinismo del banco 3/3; **0 iniciaciones** (27 decisiones) |

# INCÓGNITAS CON MÉTODO

1. **El coger redundante en el campo**: aunque el flip no se aísle en banco,
   el por-dos podría tipar en un margen real (venda al borde del horizonte,
   pull base marginal). El campo (60) lo dirá con la vara de entregas en
   calma. Si no aparece nunca, la fila se retira sin drama (fue un fondo
   correcto que el mundo no necesitó).
2. **`PROVISION_M = 0.30` y el reparto (0.15/0.25/0.6)**: calibrados en banco
   para que el soltar gane en calma sin competir con el miedo. El campo dirá
   si 0,30 es "fondo" o "obsesión" (lección del 46 de guardia).
3. **La entrega servible en calma no descuenta al agresor** (no lo hay): si
   el campo muestra provisión iniciada y luego interrumpida por un cazador
   que aparece, el apagado-bajo-caza debería cortarla limpiamente — a
   verificar en diario.

# QUÉ QUEDA EN EL REPO

- `alma/appraisal_zs.py` (`ea5ecd3f…`) — S-PROVISION + R-ACOPIO-por-dos +
  helpers `_hermana_b0`/`_provision_calma` + interruptor `PROVISION_ON`.
- `alma/decisor_zs.py` (`76171f7b…`) — sello `_bot_real` a las fotos +
  candidato `soltar` ampliado a calma-provisión (declarado).
- `alma/verifica_59.py` **nuevo** (`d6f92cf7…`) — las siete pruebas.
- Alma efectiva de taller: **v31**. Liga: v19. El campo (60) puede
  escribirse: este acta está en verde.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

La mitad de la idea funcionó como se soñó y la otra mitad resultó que ya
estaba hecha. Dar antes —soltar la venda junto a la hermana desabastecida
cuando todo está en calma, o caminar hacia ella si está lejos— es una
conducta que v30 no tenía y v31 sí: emerge limpia del descenso, sin guion, y
se apaga entera en cuanto asoma un cazador, porque el miedo manda. Es el gesto
que el 57 echaba de menos: la ayuda que llega antes de la emergencia, cuando
todavía hay una casilla servible que ofrecer.

Coger para ti resultó ser una puerta abierta. Quisimos enseñarle a recoger un
botiquín pensando en la hermana, y al medirlo descubrimos que ya lo recogía
pensando en sí mismo: la llamada del botín cercano fetcha cualquier venda a la
vista, y la riqueza se satura con una, así que la segunda solo la quiere quien
pase al lado. No hay hueco honesto donde la hermana cambie esa decisión. La
fuerza está —hace que llevar una sola cuando ella no lleva ninguna incomode un
poco— pero la conducta ya existía. Lo honesto era reportarlo, no inflar una
constante hasta fabricar un flip que el mundo no pide; y así queda, con el
número delante.

El inventario, entonces, aporta una cosa nueva y verdadera —el don que se
adelanta— y confirma que otra ya la teníamos. El campo del 60 dirá si dar
antes cambia la moneda o, como todo desde el 50, cambia solo la conducta. Pero
esta vez el animal, en calma, mira lo que lleva, mira lo que a su hermana le
falta, y se lo deja al lado antes de que la sangre lo haga urgente. Eso, se
puntúe o no, es exactamente lo que Manel pidió.

---

## Reproducción

```bash
cd gemv-coworld
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_59   # las siete pruebas
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53 54 56; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done  # P7: 24/24
```
