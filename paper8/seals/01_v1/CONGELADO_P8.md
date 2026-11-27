# El valle, congelado (paper ocho)

*2-nov-2026. Etiqueta `valle-congelado-v1`. Lo que juega el experimento, con su huella md5. Cambiar cualquiera de estos archivos rompe el sello.*

## El motor (no se toca)

| md5 | archivo |
|---|---|
| `1e511978c251130e95169ebf8443efa1` | `motor/model.py` |

## Las criaturas de regla general y de sumas (RG32r, RG032r, S32, S032: el mismo código, distintos interruptores)

| md5 | archivo |
|---|---|
| `cfb4ebf6b8d3c5a74e09cfe99d3c589f` | `cantera/paper8/cuerpo_valle.py` |
| `384086221d3cd3644b0f03d676e4a95d` | `cantera/paper8/banco_v7.py` |
| `d5a2ca88fae5d760e9fcbc7bf67b2acf` | `cantera/paper8/banco_cuerpo_valle.py` |
| `21ed1aaad7c2c8dc85d73ec91c274e50` | `cantera/paper8/config_cuerpo_valle.json` |
| `c97950bcd253297110b7319f546b9586` | `cantera/paper8/cultura_matorrales_medio.json` |
| `0cfc9573dc4dbea283400dd6c1078221` | `cantera/paper7/cuaderno_P7.py` |
| `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | `cantera/paper7/descubre_P7.py` |
| `25926b765096e89116add8dcb3260ddd` | `cantera/paper7/miedo_P7_49.py` |
| `f8b85c6f61257b09ae3c1d961382f7e6` | `cantera/paper7/nace_P7_29.py` |
| `0083986bd7d2e51ee0295d6860e9e06a` | `cantera/paper7/nace_P7_23.py` |
| `a56fd98d6148b161a1c07cec9b6ebbfb` | `cantera/paper7/nace_P7_33.py` |
| `519e69e67026c880d49af76bc14eed30` | `cantera/paper7/recuerdo_P7_23.py` |
| `1fefeef2071af1f2adaf9ab116d0254f` | `cantera/paper7/filo_P7_40.py` |
| `b0efef883215d5046cbfc5db220d0f83` | `cantera/paper7/contrafactual_P7_38.py` |
| `4766e5a3b0afdc20b787d0b79da9fe31` | `cantera/paper7/pide_P7.py` |
| `f803f47c8ed0a8eaf3855d7e1dc7d457` | `cantera/paper5/curiosidad.py` |
| `67ba0003234939c349af12be5764a3b0` | `cantera/paper6/parte2.py` |
| `98c13d60167c80cc8334c965be75c640` | `paintball/alma/appraisal_zs_v42_exp.py` |
| `87745903992bdf0b4f5a18d13f9d4f5a` | `paintball/alma/appraisal_zs.py` |
| `8fa03547e3228ef9df4aa94c444f9252` | `paintball/alma/decisor_zs.py` |
| `80dabc2e78c7c36f0708a2d95e22262a` | `paintball/alma/parte.py` |
| `d0a3151d718e6b60d499e258c9dea9b1` | `planificador/planificador_v1.py` |
| `d41d8cd98f00b204e9800998ecf8427e` | `planificador/__init__.py` |

## El tonto y el recolector

| md5 | archivo |
|---|---|
| `c90ea81dfafea4c935fc9904a19e0a5c` | `valle/jugadores.py` |
| `3b226323a9896479a6e85f8fba02d2ac` | `valle/banco_base_v5.py` |

## El mundo y su config (con los mandos de estrés: sequía dura ×0,7 y bestia de día, apagados en la config; se encienden en la partida)

| md5 | archivo |
|---|---|
| `a1c2eacb15ba6b9bd745fc289d108276` | `valle/mundo.py` |
| `f2b925a9043cc24e15f8da2de0192fdb` | `valle/config_valle.json` |

## El experimento: lanzador, medidas, evaluación y predicciones

| md5 | archivo |
|---|---|
| `d0e0254cdd73b80196cac79448acbf37` | `cantera/paper8/lanzador.py` |
| `9674da51067607ecd745a5a219ba2694` | `cantera/paper8/pasada_v22.py` |
| `a3d0dd51c12e160b32b364094261ea17` | `cantera/paper8/pasada_v18.py` |
| `39d8c5f76cad996c06f88c647cec4fcd` | `cantera/paper8/medidas_valle.py` |
| `79e25dadfb07c319d05c0d120e691e3e` | `cantera/paper8/evalua_predicciones.py` |
| `1439321abae5ad0553b7fe319d66cf9c` | `cantera/paper8/tabla_valle.py` |
| `1640ccbc10b69e094899be06e1c64857` | `cantera/paper8/predicciones_selladas.md` |

## Las clases (`banco_v7.VARS`: los interruptores de cada una)

- **RG32r**: todos los interruptores: `alarma_zona_v20=True`, `anticipa=True`, `aprende_v7=True`, `aprender_mirando_v26=True`, `atencion_huida=False`, `cansancio_suelta=True`, `cinco_matorrales=True`, `comida_por_dia=True`, `comida_sin_hambre=True`, `comida_sin_hermana=True`, `comida_sobra=True`, `compromiso=True`, `compromiso_emocion_v18=True`, `contagio_vecinas_v25=True`, `cuenta_despensa_v23=True`, `cultura_sin_olvido_v22=True`, `dar_comida=True`, `dar_cura_v24=True`, `distancias=True`, `dormir_en_casa=False`, `duelo_para=False`, `duelo_suma_v15=True`, `duelo_v19=True`, `empates_sigue_v23=True`, `enfado=False`, `escala_v6=True`, `frio_sabe_v17=True`, `hambre_dolor=True`, `histeresis_llamadas=True`, `juntar_viejos_v27=True`, `llamadas_contraste_v20=True`, `llamadas_opcion_v19=True`, `matorrales=True`, `medicina_herida_v22=True`, `memoria_v2=True`, `memoria_v3=True`, `noche_entera_v18=True`, `oye_sin_hermana=True`, `plantas=True`, `provision_necesidad_v22=True`, `rapido_v28=True`, `recuerdo_vacio=True`, `regla_general=True`, `reloj_dentro_v27=True`, `responde_llamadas=True`, `rg_ganancias=True`, `robo_noche=False`, `sabe_reglas_trabajo=False`, `satura_v8=True`, `sentir=True`, `simetria_v7=True`, `simetria_vista_v8=True`, `sin_techo_v11=True`, `ve_vida_v9=True`, `vecinas=True`, `voz_v16=True`
- **RG032r**: como RG32r salvo `escala_v6=(no está: apagado)` (en RG32r, `True`), `rg_ganancias=False` (en RG32r, `True`), `sentir=(no está: apagado)` (en RG32r, `True`)
- **S32**: como RG32r salvo `sumas_v29=True` (en RG32r, `(no está: apagado)`)
- **S032**: como RG32r salvo `escala_v6=(no está: apagado)` (en RG32r, `True`), `rg_ganancias=False` (en RG32r, `True`), `sentir=(no está: apagado)` (en RG32r, `True`), `sumas_v29=True` (en RG32r, `(no está: apagado)`)
- **tonto** y **recolector**: `valle/jugadores.py`, por `valle/banco_base_v5.partida`, con el margen de comida de la config.

## El experimento

`python3 cantera/paper8/lanzador.py RG32r,RG032r,S32,S032,tonto,recolector normal,abundancia,sequia,sequia_dura,bestia_dia 1001-1040 40`: 6 clases × 5 mundos × 40 semillas = 1.200 partidas de 40 días, por mundos en ese orden. Registros en el T7 (`/Volumes/Mem G-EMV/valle_experimento/`).
