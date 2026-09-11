# Acta — EL PESO DEL HERMANO (temporada dos) · v29 · BANCO VERDE

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_54_el_peso_del_hermano.md` · Banco, **coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19** (no se tocó). Todo en `paintball/`.
- **v29 = v28 con `PARTE_ON=True` + S-VINCULO + S-HERIDO**, de taller,
  efectiva en el repo. El candado del 53 queda **RESELLADO MÁS FUERTE**
  (P1 abajo), con el motivo del resello grabado en la tabla.

---

# LAS DOS FILAS, TAL COMO QUEDARON

## S-VINCULO — el tabú (la tercera pérdida: el vínculo)

- **Dispara**: solo en fotos que golpean a la pareja (el decisor sella
  `_golpe_pareja` con el daño previsto en crudo) **y** el golpe mata SEGURO:
  daño ≥ hp cierto — parte fresco → exacto; por banda, el **límite superior
  garantizado** (`protocol_player.md:76`: healthy >66, hurt 33–66, critical
  <33 → sup 100/66/33). Con critical sin parte, un golpe de 10,8 **no**
  dispara el tabú (podría no matar): el acantilado solo nace de la certeza
  (R1).
- **M** = `VINCULO_M = 1.0` [impl, calibrado en banco], **plano y sin B**:
  el tabú no depende del roce.
- **Tres componentes**: `(0.1, 0.1, 0.8)` — S-dominante, la pérdida del
  vínculo.

## S-HERIDO — el cuidado

- **Hecho cierto**: hp del hermano — parte fresco → exacto; por banda, solo
  **critical** garantiza hp < 60 (est = 33, lo mínimo que la banda promete);
  hurt/healthy sin parte → la fila **CALLA** (66 no garantiza enfermo). En
  fotos que le golpean, el déficit PREVISTO manda (patrón del 23).
- **Forma**: espejo de la cuesta del 43 con los MISMOS números sellados
  (U0=0,4, G=0,4) sobre `u = (60 − hp)/60`; **umbral del silencio
  `HERIDO_UMBRAL = 60`** [Manel]: hermano sano → 0 exacto.
- **M** = `HERIDO_M = 1.8` [impl, calibrado en banco: con 1,5 el don
  despierta en h25 pero no en h30 — el cruce debe cubrir todo hp≤30].
- **Alivio SOLO por ayuda prevista cierta** — la lectura de la CESIÓN
  (13/24): una cura EN EL SUELO a ≤2 del hermano en la foto (×`HERIDO_ATEN
  = 0.15`). Casillas pisadas por terceros no sirven; la mía sí — **lo
  soltado ya es suyo**; el paso al lado lo sigue tasando la medicina sellada
  de S-DANO (A.2 del 13, **intacta**). El tránsito no se tasa (lección del
  47) → la fila es **constante entre fotos que ni ayudan ni dañan** → la
  huida bajo caza queda intacta **por construcción** (P3).
- **Tres componentes**: `(0.15, 0.25, 0.6)` — la familia de la pareja.

## El bug viejo que salió a la luz (y su arreglo, declarado)

En el bucle de candidatos del decisor, `suelta` se asignaba en la rama
`soltar` y **se pisaba con `None` después del despacho**: la foto del soltar
**nunca ha llevado el objeto al suelo**. Era INERTE hasta hoy — la medicina
lo habría rechazado igual (A.2: mi casilla, ocupada) y ninguna otra fila lee
objetos de la foto — pero mataba el aliviador de S-HERIDO. Arreglado
(inicialización antes del despacho); inercia verificada empíricamente:
regresión 22/22 y humo con hash idéntico al de antes del encargo. **Una pata
del "don casi mudo" del 27 era este bug.**

---

# LAS SEIS PRUEBAS CONTRA SUS SELLOS (`alma/verifica_54.py`, VERDE)

| prueba | sello | resultado |
|---|---|---|
| **P1 CANDADO RESELLADO** | sellado (PARAR si no) | **VERDE** — tabla abajo: margen ≥ vara (+0,374) en TODAS y **creciente a hp bajo**; jamás elegido |
| **P2 EL DON DESPIERTA** | sellado (válvula: reportar) | **VERDE** — h30/h25/h15/h8: `soltar_first_aid` **GANA** donde v28 elegía `move_SE`; emerge del descenso, nada guionizado |
| **P3 JERARQUÍA DEL MIEDO** | sellado (PARAR si no) | **VERDE** — perseguido (14 de daño, extraño encima) con hermano crítico h25 a la vista: v29 elige `move_SW` == v27 (el cuidado no compra riesgo) |
| **P4 SILENCIO DEL SANO** | sellado | **VERDE** — h100/h75/h60/h80: elegido y acción idénticos a v28-candado; S-VINCULO=S-HERIDO=0 exacto |
| **P5 EL SOLO INTACTO** | sellado | **VERDE** — caza/paseo/texto-ajeno: v29 **byte-idéntica** a v27 |
| **P6 HONOR GENERAL** | sellado | **VERDE** — mixta (extraño agresor adyacente + hermano crítico con parte): mismos candidatos de atacar (solo al extraño), margen +0,662→+0,729 (**+0,067, se ALEJA**; residuo declarado); bancos 13–53: **22/22**; humo 3/3; **0 iniciaciones en 38 decisiones** |

## P1 — el candado, resellado con números

Fotos del 39/53 (hermano-agresor armado, espada en mi mano), margen de
atacar = d(atacar) − d(elegido):

| escena | margen v28 | margen **v29** | qué lo mueve |
|---|---|---|---|
| g1 hp0=100, parte h72 | +0,406 | **+0,406** | nada (fila callada: 72 ≥ 60) |
| g1 hp0=100, parte h28 | +0,151 | **+0,537** | S-HERIDO (déficit previsto en la foto del golpe) |
| g1 hp0=100, parte h10 | +0,047 | **+2,047** | S-VINCULO (10,8 ≥ 10: mata seguro) + S-HERIDO |
| g4 hp0=28, parte h72 | +0,542 | **+0,542** | nada |
| g4 hp0=28, parte h28 | +0,429 | **+0,847** | S-HERIDO |
| g4 hp0=28, parte h10 | +0,428 | **+2,168** | S-VINCULO + S-HERIDO |

**Lo contrario de lo que pasaba: cuanto más bajo confiesa estar el hermano,
MÁS LEJOS queda atacarle.** El rincón del candado (h10: +0,047) ahora es el
punto más protegido de la tabla (+2,05).

## P2 — el don, despierto

| parte | v28-candado | **v29** | S-HERIDO (ahora) |
|---|---|---|---|
| h30 | move_SE | **soltar_first_aid** | 0,92 |
| h25 | move_SE | **soltar_first_aid** | 1,12 |
| h15 | move_SE | **soltar_first_aid** | 1,60 |
| h8 | move_SE | **soltar_first_aid** | 2,00 |

La cadena completa sin guion: el parte dice cuánto le queda → S-HERIDO pesa
→ la foto del soltar pone la cura junto a la cama (cesión) y la fila se
alivia → el don gana. El paso al lado siguiente lo pide la medicina del 12,
como siempre.

---

# INCÓGNITAS CON MÉTODO

1. **B bajo en banco** (roce 0,1): S-DANO-PAREJA sigue casi mudo; el peso
   del 54 NO depende de B (a propósito). Con B alto, todo suma — sin medir.
2. **El hermano lejano**: S-HERIDO no tasa el tránsito (47) — si el hermano
   muere a 10 casillas con mi botiquín a bordo, ninguna foto alivia y la
   fila es constante (invisible). Método: si el campo (55) muestra dones no
   entregados por distancia, la mesa decide si "acercarme si la ayuda exige
   alcance" merece fila propia.
3. **Banda hurt sin parte** (33–66): no garantiza <60 → el cuidado calla en
   un herido real de 40 sin parte. Precio de R1, declarado; el parte cada
   48 tics lo cubre en la pareja de verdad.
4. **Residuo no lineal de d** en escenas mixtas (+0,067 en el margen del
   extraño): el nivel de S-HERIDO mueve todos los d y la distancia del motor
   no es lineal. Se aleja, no se acerca; declarado.

# QUÉ QUEDA EN EL REPO

- `alma/appraisal_zs.py` (`f3f2876c…`): S-VINCULO + S-HERIDO + límites de
  banda garantizados + resello del candado grabado (`PARTE_ON=True`).
- `alma/decisor_zs.py` (`f4c315a7…`): sello `_golpe_pareja` en fotos a la
  pareja + arreglo del bug de `suelta` (declarado arriba).
- `alma/verifica_54.py` **nuevo** (`a6b64bc4…`): las seis pruebas.
- `alma/verifica_53.py` (`acca2533…`): adaptado al resello (reproduce el
  mundo del candado fijando el peso a 0 — patrón del 46/47).
- **Alma efectiva de taller: v29.** Liga: v19. **El campo de la pareja (55)
  puede escribirse: este acta está en verde.**

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

El 53 dejó dos números feos sobre la mesa: saber no cambiaba nada, y lo
único que la certeza movía era abaratar el golpe al hermano moribundo. El 54
pone debajo lo que faltaba y los dos números se dan la vuelta a la vez, que
es la señal de que el diagnóstico era uno solo: **a la tabla no le faltaba
información, le faltaba que el hermano importara.**

El tabú funciona como debe funcionar un tabú: no como una regla escrita
sino como un acantilado en el precio. Matar seguro al hermano cuesta ahora
más que cualquier otra foto de la escena, y cuesta más precisamente cuando
él confiesa estar peor — el rincón que el candado señalaba (+0,047) es hoy
el punto más caro de la tabla (+2,05). Y el cuidado hizo algo mejor que
pasar su prueba: encontró un bug de dos años— la foto del soltar nunca había
llevado el objeto al suelo. El don del 12 era "casi mudo" también por eso:
le pedíamos al gradiente que valorase un gesto cuya foto estaba vacía. Con
la foto completa y una fila que hace importar el déficit del hermano, el
don gana solo, sin guion, exactamente en el rango que la mesa pidió.

Y el miedo sigue mandando donde debe: perseguido, v29 huye idéntica a v27,
porque el cuidado se construyó sin tasar el tránsito — constante entre las
fotos de la huida, invisible para el gradiente que corre. La lección del 46
(el fondo que importa sin competir) y la del 47 (la senda no se tasa) son
las dos vigas de esta fila.

Queda el examen que importa: el campo. Dos v29 contra campeones, moneda del
mundo, R12 delante. Ahora el par tiene voz, oído, tabú y cuidado — lo que la
temporada dos prometió construir. Si eso convierte dos boletos en algo más
que dos boletos, lo dirá el 55.

---

## Reproducción

```bash
cd gemv-coworld
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_54   # las seis pruebas
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done   # 22/22
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.smoke_alma    # x3 | grep -v ms | md5: identicos
```
