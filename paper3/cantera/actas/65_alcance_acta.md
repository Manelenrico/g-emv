# Acta — EL ALCANCE Y EL FUEGO AMIGO (v35) · BANCO VERDE

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_65_alcance_y_fuego_amigo.md` · Banco, **coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **v35 = v34 + dos correcciones de FOTO** (`appraisal_zs.py 9f679bdc…`,
  `decisor_zs.py d9c8baab…`). Interruptores `FUEGO_AMIGO_ON` y `ALCANCE_ON`
  (ambos False = v34 bit a bit).
- A y B se miden **sobre los diarios ya pagados del 64**: coste 0.

---

# A · EL RESELLO P2' (precedente del 38)

**OCASIÓN corregida** = hermana bajo caza certificada + la otra a ≤2, sana
(≥70), con arma, **Y el agresor alineado y en alcance del arma**:

| | ocasiones | defensa llega | |
|---|---|---|---|
| **P2 original** (sin alcance en la definición) | 20 | 5 | **25 %** |
| **P2' resellado** (con alcance) | **8** (en 5 episodios) | **5** | **62 %** |

Confirmado el número esperado. Las 12 ventanas que salen de la cuenta son
aquellas en que **el golpe era imposible**: el animal veía a su hermana
atacada, con la certeza y el arma, y no alcanzaba.

# B · LA VARA DE PROTECCIÓN (primera vez que se mide; sin sello)

Pareado por ventana, 120 tics tras cerrarse:

| vara | CON defensa (n=5) | SIN defensa (n=15) |
|---|---|---|
| golpes recibidos por la cazada (mediana) | 0,0 | 0,0 |
| golpes recibidos (**media**) | **0,4** | **0,9** |
| hp de la cazada al cerrar la ventana | 75 | 9 |
| hp 120 tics después | 75 | 1 |
| % ventanas en que el acoso cesa | 80 % | 80 % |

**La frase honesta**: la dirección favorece a la defensa (menos de la mitad de
golpes de media), y en el único episodio con los dos casos limpios
(`ereq_e1daaef0`) la ventana defendida es **la única sin pérdida de vida**
(75→75, frente a 75→39 y 39→3 sin defensa). **Pero no es evidencia**: las
ventanas no son comparables —las defendidas ocurren con la cazada mucho más
sana (hp 75 vs 9 al cerrar)— y n=5. **La vara ya no es ciega, pero todavía no
sella dirección.** El instrumento queda listo para el 66, donde el pareado
puede hacerse dentro del mismo estado.

# C · LAS DOS FOTOS HONESTAS (v35)

## 1 · EL FUEGO AMIGO — corregida, y con un hallazgo de física

La previsión de un golpe que **atraviesa casillas** traza la línea y pone el
daño en el **primer cuerpo** (física certificada en el 41). Si ahí está la
hermana, la foto lo dice — y entonces **S-DANO-PAREJA y S-VINCULO pesan
solas** contra ese golpe. Sin regla nueva (R2).

**El hallazgo**: la foto real del campo (`ereq_feafe3ac` t534) fue con
**LANZA — melee de rango 2**, no con proyectil: gemela11 en [25,26] atacó al
oeste al slot 9 en [23,26] con su hermana en [24,26], en medio. **Por eso la
condición no es el tipo de arma sino el ALCANCE** (`range > 1`): cualquier
golpe que atraviesa puede encontrar a quien no debía.

## 2 · EL ALCANCE — corregida; el flip **se reporta**, no se infla

Con la hermana bajo caza certificada y su agresor fuera de mi alcance, la foto
de un movimiento que **me deja alineada y a rango** alivia la presión
atribuida (`ALCANCE_GANA = 0.5`, tope del sello). Apagada si yo tengo agresor
propio (manda mi muro).

# D · LAS SEIS PRUEBAS (`alma/verifica_65.py`, VERDE)

| prueba | sello | resultado |
|---|---|---|
| **P1 FUEGO AMIGO** | sellado | **VERDE** — con la hermana en la línea: la foto de atacar pone el daño en ella (**S-DANO-PAREJA 0,0061 → 0,0134**) y **el golpe se encarece** (d 3,72444 → 3,74601); v35 no lo elige. **Línea limpia: byte-idéntica a v34 y ataca**. **Alcance 1 (espada): inerte, byte a byte** |
| **P2 EL ALCANCE** | sellado, con cláusula de reporte | **la foto SE CORRIGE** (el candidato que deja a rango se abarata **−0,169**), **pero el flip NO emerge**: la zancada de huida elimina S-7 entera (0,49→0) y gana. **Se reporta, no se infla** (regla de la casa, precedente del 59 P2) |
| **P3 LA JERARQUÍA** | sellado (PARAR) | **VERDE** — yo cazada (hp 90 y 25): v35 **idéntica a v34**, el alcance **apagado** |
| **P4 CANDADOS + HONOR** | sellado | **VERDE** — C2 (hermana en calma): 0 candidatos e idéntica a v32; **0 iniciaciones-estrictas**; 0 ataques contra la hermana |
| **P5 SILENCIOS** | sellado | **VERDE** — sin hermana: **byte-idéntica a v27** |
| **P6 REGRESIÓN** | — | **VERDE** — bancos 13-64: **29/29**; humo 3/3 (hash de siempre); determinismo 3/3 |

# INCÓGNITAS CON MÉTODO

1. **El alcance en el campo**: en banco la huida por zancada gana siempre
   (campo abierto, sin muros ni cuerpos que estorben). En el campo real el 64
   midió `noop` 346 veces —no huida—, así que **el alivio puede tipar allí
   donde en banco no puede**. Es exactamente la pregunta del 66; el código
   está puesto y medido.
2. **El fuego amigo con alcance 1**: la lanza (rango 2) atraviesa; la espada
   no. Si el animal lleva espada, esta corrección es inerte — y las defensas
   del 64 fueron mayoritariamente con espada. El efecto en campo dependerá de
   qué arma encuentre.
3. **La vara de protección** (B): lista, aún no sella. Con el pareado por
   estado del 66 podría hacerlo.

# QUÉ QUEDA EN EL REPO

- `alma/appraisal_zs.py` (`9f679bdc…`) — el alivio del alcance + interruptores.
- `alma/decisor_zs.py` (`d9c8baab…`) — `_primero_en_linea` y la foto honesta
  del golpe que atraviesa.
- `alma/verifica_65.py` **nuevo** (`742bbcdb…`) · `proteccion.py` **nuevo**
  (`85b71a9d…`, A+B sobre los diarios del 64).
- Alma efectiva de taller: **v35**. Liga: v19.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

Dos correcciones de foto, ninguna regla nueva, y la más importante trae un
hallazgo que no esperábamos: el golpe que hirió a la hermana en el campo no
salió de un arco ni de unos cuchillos, sino de una **lanza** — un arma cuerpo
a cuerpo de dos casillas de alcance. El mundo la resuelve como resuelve todo
lo que atraviesa: pega al primero de la línea. Habíamos escrito la corrección
pensando en proyectiles y el campo nos enseñó que la condición correcta es
más simple y más amplia: **cualquier golpe que cruza una casilla puede
encontrar a quien no debía**. Ahora la foto lo dice, y el disparo a través de
la hermana se encarece solo, porque las fuerzas que protegen a la hermana ya
existían desde el 54.

La segunda corrección funciona en la foto y no cambia la decisión, y eso
también se dice. Moverse a un sitio desde donde poder defender se abarata
diecisiete centésimas —medido— pero la zancada de huida borra la presión
entera y sigue ganando en un banco de campo abierto. Podríamos haber subido
la constante hasta forzar el gesto; el sello la topa en la mitad y la casa
tiene precedente: en el 59 medimos, dijimos que no emergía y no inflamos
nada. El campo del 64, donde el animal se quedaba quieto trescientas
cuarenta y seis veces en vez de huir, es el sitio donde esa corrección puede
morder de verdad.

Y el resello deja la manada en su sitio con un número limpio: **donde el
golpe era posible, defendió el sesenta y dos por ciento de las veces**. Lo
que fallaba no era la voluntad sino el alcance — y eso, por fin, es un
problema de geometría y no de carácter.

---

## Reproducción

```bash
cd gemv-coworld
python3 paintball/proteccion.py                                    # A (P2') + B
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_65   # C+D
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53 54 56 59 61 62 63; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done  # 29/29
```
