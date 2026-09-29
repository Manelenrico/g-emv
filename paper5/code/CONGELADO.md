# CONGELADO · el código con el que se jugó y se midió el paper cinco

*[P6-0 A] Inventario cerrado el 26 de septiembre de 2026. Sólo lectura: no se
modificó ni un archivo para hacer esta lista. Generado por
`cantera/paper6/congela_paper5.py`.*

A partir de aquí, **todo lo del paper seis va en `cantera/paper6/`**, que ya
está creada. Lo de esta lista no se toca: si algo hay que cambiar para el seis,
se copia con otro nombre.

---

## EL ESTADO DE GIT · NO SE HA ETIQUETADO NADA

**Hay cambios sin guardar, así que no he creado la etiqueta.** Tal como pedía el
encargo, lo digo antes y no hago nada.

| | |
|---|---|
| rama | `paintball` |
| commit actual (HEAD) | `8a77e23` · 2026-09-05 19:15 · *«PROMPT_72: la ablacion de campo — la manada no aparece sin sus filas»* |
| etiquetas existentes | ninguna |
| archivos modificados sin guardar | **2** — `.claude/settings.local.json`, `.gitignore` |
| entradas sin seguir (`??`) | **90** |

**El problema no son los dos modificados: es que el paper cinco entero está sin
seguir.** El último commit es del **5 de septiembre**, y el trabajo del cinco
empieza el **16 de septiembre**. Nada de esto está en git:

* `cantera/` **completa** (los dos papeles, la cantera del cuatro y la del cinco);
* `paintball/alma/policy_forma.py`, `forma_viva.py`, `confianza_viva.py`,
  `appraisal_zs_v42_exp.py`, `cortex_t5.py`, `hilo_forma.py`, `relator_t5.py`,
  `formas_azar.py`, los siete `Dockerfile.*` y los cuatro `humo_*.py`;
* `paintball/runs/` con los diarios de las series.

En la tabla de abajo, la columna **«¿en git?»** dice `**no**` en **155 de los
199 archivos**. Y el reparto de los 44 que sí están es el que importa:

| dónde | en git | fuera de git |
|---|---:|---:|
| `motor/` + `planificador/` | **5** | 0 |
| `paintball/alma/` | 39 (los `verifica_*.py` de papeles anteriores, `policy.py`, `mundo.py`, `parte.py`, `decisor_zs.py`, `appraisal_zs.py`) | **24** (`policy_forma.py`, `forma_viva.py`, `confianza_viva.py`, `appraisal_zs_v42_exp.py`, `cortex_t5.py`, `hilo_forma.py`, `relator_t5.py`, los `humo_*.py`, el `Dockerfile.forma`…) |
| `cantera/paper5/` | **0** | **129** |
| `cantera/paper4/` | 0 | 2 |

**De los 129 archivos del paper cinco, cero están en git.** Lo que sí está
seguido es el poso de los papeles tres y cuatro.

**Una etiqueta sobre `8a77e23` no congelaría el paper cinco: congelaría un
commit anterior a él que no contiene ni una línea de su código.** Sería peor que
no etiquetar, porque parecería que sí.

### Lo que propongo (decides tú, yo no lo hago)

1. **Revisar el `.gitignore`** — `cantera/` y `paintball/runs/` no aparecen en
   él (comprobado con `git check-ignore`), así que están sin seguir porque nunca
   se añadieron, no porque se excluyeran a propósito.
2. **Decidir qué entra**: el código sí; los diarios (`paintball/runs/`) pesan
   mucho y quizá quieras dejarlos fuera con una regla explícita en `.gitignore`
   y un `CONGELADO.md` —este— como registro de md5.
3. **Un commit «paper cinco, final»** con el código, y **entonces** la etiqueta
   local `paper5-final` sobre él.

Mientras tanto, **los md5 de esta tabla son el congelado real**: reproducen
byte a byte lo que jugó y midió, esté o no en git.

---

## LAS TRES CUSTODIAS QUE LA IMAGEN YA COMPROBABA EN CADA BUILD

`paintball/alma/Dockerfile.forma` tumbaba el build si cambiaba alguno:

| archivo | md5 exigido | md5 hoy | ¿coincide? |
|---|---|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | **sí** |
| `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` | `8fa03547e3228ef9df4aa94c444f9252` | **sí** |
| `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` | `98c13d60167c80cc8334c965be75c640` | **sí** |

### 1 · EL MOTOR Y EL PLANIFICADOR (intocables; la imagen los copia tal cual)

| archivo | md5 | ¿en git? |
|---|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | sí |
| `planificador/__init__.py` | `d41d8cd98f00b204e9800998ecf8427e` | sí |
| `planificador/mapa_territorial.py` | `7e81f483c5914bdd7285ca677fe47fd0` | sí |
| `planificador/planificador_v1.py` | `d0a3151d718e6b60d499e258c9dea9b1` | sí |
| `planificador/transicion_v1.py` | `1ee061d1932dca55971ae5697a78d3c2` | sí |

*5 archivos.*

### 2 · LA RECETA DE LA IMAGEN QUE JUGÓ EL CINCO

| archivo | md5 | ¿en git? |
|---|---|---|
| `paintball/alma/Dockerfile.forma` | `4603512854740a0b3aae2f4994f83560` | **no** |

*1 archivos.*

### 3 · EL ALMA (`paintball/alma/`, que la imagen copia entera)

| archivo | md5 | ¿en git? |
|---|---|---|
| `paintball/alma/appraisal_zs.py` | `87745903992bdf0b4f5a18d13f9d4f5a` | sí |
| `paintball/alma/appraisal_zs_v35_miedo_exp.py` | `a5fa314c23dce4d029ef251b09ed057b` | **no** |
| `paintball/alma/appraisal_zs_v38_exp.py` | `ecd00602c1befdc2fbd32f7aa7d52b7f` | **no** |
| `paintball/alma/appraisal_zs_v38_exp_forma1.py` | `4e2d89370463f7d28f44e471b573aa0b` | **no** |
| `paintball/alma/appraisal_zs_v39_exp.py` | `49680f274250dfae75bc2f3c81f6b859` | **no** |
| `paintball/alma/appraisal_zs_v40_exp.py` | `e729a0293673abe200620419ccb8683a` | **no** |
| `paintball/alma/appraisal_zs_v41_exp.py` | `690dabb60f5587d53dc7c966e39fc530` | **no** |
| `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` | **no** |
| `paintball/alma/confianza_viva.py` | `6e1e444435914f0b9df287ea37555bbc` | **no** |
| `paintball/alma/cortex_t5.py` | `defb11d3a4661ff57745214ccd1ab14f` | **no** |
| `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` | sí |
| `paintball/alma/forma_viva.py` | `b2c87c93f0ed47e48fd8991a5a797a42` | **no** |
| `paintball/alma/formas_azar.py` | `eefb5534e9533c8b742f7feb96239588` | **no** |
| `paintball/alma/hilo_forma.py` | `aeea06ae4eb5b704e94fe845a5a5e5aa` | **no** |
| `paintball/alma/humo_cortex.py` | `302e7d691c17c719d4343ea92a943d90` | **no** |
| `paintball/alma/humo_curforma.py` | `1660fb118bb2287f036bdb02c74fc11e` | **no** |
| `paintball/alma/humo_curiosidad.py` | `7b38d5a64f8562e3d092b4bf72c681eb` | **no** |
| `paintball/alma/humo_forma.py` | `4aefd120bf739736a3c4719029b7283c` | **no** |
| `paintball/alma/mundo.py` | `e2c2cf7618b61e1280f2e3ea989f1872` | sí |
| `paintball/alma/parte.py` | `80dabc2e78c7c36f0708a2d95e22262a` | sí |
| `paintball/alma/policy.py` | `da6c6a01db83677ce01213328c2ab66a` | sí |
| `paintball/alma/policy_cortex.py` | `6997b00c266f23d6037cc1a018f60a76` | **no** |
| `paintball/alma/policy_forma.py` | `896e97a0cca1efcb736596e0b8b15cea` | **no** |
| `paintball/alma/policy_mapa.py` | `dddead38c25e929f25824e7b886210d4` | **no** |
| `paintball/alma/policy_red.py` | `14c6a2a15639d4f901aec14a9cff4512` | **no** |
| `paintball/alma/policy_repetidor_forense.py` | `b4df57d3e328eeec527e5db2acf4b5e4` | sí |
| `paintball/alma/policy_serie.py` | `8cea3227244c0591c72f3e31f599a343` | **no** |
| `paintball/alma/policy_sonda_sonnet.py` | `67d18ce801d8e616dd85547baf7c627d` | **no** |
| `paintball/alma/relator_t5.py` | `929c49f6ced9af1cbd37eadec08c54f0` | **no** |
| `paintball/alma/smoke_alma.py` | `455b75295619d76dffc43fb4332f7156` | sí |
| `paintball/alma/verifica_13.py` | `2d9a43e8df28349a14b8d00507c0bf66` | sí |
| `paintball/alma/verifica_14.py` | `1db3c5a392ceecf4fed35cdb138f04ac` | sí |
| `paintball/alma/verifica_15.py` | `9fd1af038ba8b35c63d7e46104c053ca` | sí |
| `paintball/alma/verifica_16.py` | `0d76283627bd2eabb62a089ea0e2f620` | sí |
| `paintball/alma/verifica_17.py` | `e1afa582f9c8d92a70788b078e1a6dba` | sí |
| `paintball/alma/verifica_18.py` | `1d8c09985917ab228c0b418e27067c0a` | sí |
| `paintball/alma/verifica_21.py` | `4be45ca02fd421acccde75470c311b2e` | sí |
| `paintball/alma/verifica_22.py` | `5b407637f1d18ec58b2d09bdeacee47c` | sí |
| `paintball/alma/verifica_23.py` | `e6435d13f63cc9b72691b1c08548e63e` | sí |
| `paintball/alma/verifica_24.py` | `212bf40e16fba15fb0cda8e7e0593301` | sí |
| `paintball/alma/verifica_28.py` | `b98b5a7b24314eb2b4e6faf4f7a06427` | sí |
| `paintball/alma/verifica_33.py` | `25fa64f0813a037a851bdf856b0ddeff` | sí |
| `paintball/alma/verifica_35.py` | `be09ef1d78b2b0898595c9760bbbbd84` | sí |
| `paintball/alma/verifica_37.py` | `82ac993b87515a12fc56dbd3768da431` | sí |
| `paintball/alma/verifica_39.py` | `86db27516dbc850fc8dcf4deaba326ae` | sí |
| `paintball/alma/verifica_41.py` | `e9a667b77ffe6433f9be00fbe6208510` | sí |
| `paintball/alma/verifica_43.py` | `a4075293798c3c09c5944d6c6a847e2a` | sí |
| `paintball/alma/verifica_46.py` | `658ccfb19d56293d93e3f56ffaee4cf2` | sí |
| `paintball/alma/verifica_47.py` | `24c1e878b8bfd0a89fc445f30b7ef551` | sí |
| `paintball/alma/verifica_48.py` | `4162cd4d7e0fa58d31e428c238e6cdf0` | sí |
| `paintball/alma/verifica_53.py` | `fa0cbf4f3eda281a52473a05635f0ef6` | sí |
| `paintball/alma/verifica_54.py` | `8359630dc3a216c82889b85a790c6a9c` | sí |
| `paintball/alma/verifica_56.py` | `4da300577616976c54878eeadadd44d8` | sí |
| `paintball/alma/verifica_59.py` | `3866bf7219d7cd540148863b24e7c849` | sí |
| `paintball/alma/verifica_61.py` | `5cd751ca7c41b6abd3062c34eb2d3bed` | sí |
| `paintball/alma/verifica_62.py` | `d83ceb35612d683123cc6f015bc0490d` | sí |
| `paintball/alma/verifica_63.py` | `5133500b4f850594ab448d81aab1b126` | sí |
| `paintball/alma/verifica_65.py` | `a79f8c89b8d3a2864d384d0c6dba506b` | sí |
| `paintball/alma/verifica_68.py` | `3e9b950885c2c36ca5897f5da2bbd004` | sí |
| `paintball/alma/verifica_70.py` | `77c0c5d8d0fd5a9e2df70b61b532c5ab` | sí |
| `paintball/alma/verifica_71.py` | `b285de16d7ee8d669e55e47d11fbf5d4` | sí |
| `paintball/alma/verifica_s7.py` | `9631b71c3d944b11f8bc5c84d6c9a112` | sí |

*62 archivos.*

### 4 · LAS PIEZAS DEL CINCO QUE VIAJAN DENTRO DE LA IMAGEN

| archivo | md5 | ¿en git? |
|---|---|---|
| `cantera/paper5/forma.py` | `b801876afda071403c5af54a28feff85` | **no** |
| `cantera/paper5/proyeccion.py` | `bbc42daeaa769c783844997067ef148d` | **no** |
| `cantera/paper5/traductor_forma.py` | `b310bb72884ef5f4e3510ab803cd2776` | **no** |
| `cantera/paper5/alcance_g.py` | `bf62b03587506064311c122fd0e09102` | **no** |
| `cantera/paper5/curiosidad.py` | `f803f47c8ed0a8eaf3855d7e1dc7d457` | **no** |
| `cantera/paper5/curiosidad_forma.py` | `141ecb2eb17f76654caf4bbf3c29c642` | **no** |
| `cantera/paper5/instruccion_forma.md` | `02653e4edf04f3bdd9a0ac3deda9aa01` | **no** |
| `cantera/paper5/tabla_ensenada.md` | `9d53807699c4ee2be31d8dd173196de0` | **no** |
| `cantera/paper5/P56A_distribucion_azar.json` | `9092c6c73eda7d81f97e9ac730c8783f` | **no** |

*9 archivos.*

### 5 · LOS PRESETS DEL MUNDO

| archivo | md5 | ¿en git? |
|---|---|---|
| `cantera/paper5/lento_v0.json` | `d213ba5d90a64875ce77f02390f46cf2` | **no** |
| `cantera/paper5/roster_lento_v1.json` | `a2293bd16ee94e6d4c2f4683b57c2a09` | **no** |
| `cantera/paper5/manifiesto_zero_sum_0_1_18.json` | `07ffcf2e63975ffe0a0d0cecc4198c69` | **no** |
| `cantera/paper4/catalogo_zero_sum_0_1_18.json` | `100acc95bad0fdab42ec396363131cfc` | **no** |

*4 archivos.*

### 6 · UTILIDAD HEREDADA DEL CUATRO QUE IMPORTAN LOS SCRIPTS DEL CINCO

| archivo | md5 | ¿en git? |
|---|---|---|
| `cantera/paper4/serie_util.py` | `c65b52969d5334b6dc0ed36cb10f943f` | **no** |

*1 archivos.*

### 7 · SCRIPTS DE BANCO, MEDIDA, LANZAMIENTO Y FIGURAS DEL CINCO

| archivo | md5 | ¿en git? |
|---|---|---|
| `cantera/paper5/E1_maxW.py` | `2febb9a411d9daf717cea2b9713b63ec` | **no** |
| `cantera/paper5/E2_concilia.py` | `2f00c8e768b1eca28fcd99909645a197` | **no** |
| `cantera/paper5/E3_golpes.py` | `262ae5ec5eb3510cf1136586e75b0d9c` | **no** |
| `cantera/paper5/E3_participantes.py` | `1b780fa2116dc606d6bea06b82ba4b85` | **no** |
| `cantera/paper5/G5G6.py` | `400bbbd0530d1498c5b6cfaf88ad10eb` | **no** |
| `cantera/paper5/H3H4.py` | `e9c278fa920fe2c4a6914f6b22aa807e` | **no** |
| `cantera/paper5/P53A_reproduce.py` | `f48c0936417e749eeec08204ee00aa05` | **no** |
| `cantera/paper5/analiza_B1.py` | `3e1ccf1d9e6643aa1bca33b3547421a6` | **no** |
| `cantera/paper5/analiza_C.py` | `c1383dd8e69570d8195c86e327b4b04b` | **no** |
| `cantera/paper5/analiza_D.py` | `51c8843a44efa16e21a0304c06d15bbf` | **no** |
| `cantera/paper5/analiza_P55A.py` | `56768b5a6d911deccb1a9f7e7c9ef0d9` | **no** |
| `cantera/paper5/analiza_P56C.py` | `93fd5ee69cdfb528aeb2de1cf6f0c474` | **no** |
| `cantera/paper5/analiza_P57A.py` | `ff2e2462fa887f31661021c9e2a43d9b` | **no** |
| `cantera/paper5/analiza_P57B.py` | `0809945175bd1d6abbfd6ac36d4f419a` | **no** |
| `cantera/paper5/analiza_P57C.py` | `c2c67882a31024d23c16670e5e081d8e` | **no** |
| `cantera/paper5/analiza_P58A.py` | `7aebcd42428aae968bf39afc99f0d6b5` | **no** |
| `cantera/paper5/analiza_P58M.py` | `454fad7565c597b3a80da46e4340a498` | **no** |
| `cantera/paper5/baja_B1.py` | `ada405f62fc53abfe1eca1ed9a3322c1` | **no** |
| `cantera/paper5/baja_P56B.py` | `cc705384e77db157be0b4f64b96665d6` | **no** |
| `cantera/paper5/baja_P56C.py` | `097c8b5ad32e2c319e1cad7b4c9fc727` | **no** |
| `cantera/paper5/baja_P57C.py` | `6baac1f41ac88aa214290962ad67c867` | **no** |
| `cantera/paper5/baja_P58B.py` | `2603964fb916bfad3444d705cf559365` | **no** |
| `cantera/paper5/baja_P58D.py` | `5c0a92d2fdf0656f251667fd6a67bfbc` | **no** |
| `cantera/paper5/baja_P58E.py` | `851030a0728dfb0a8db8f407eb1920a3` | **no** |
| `cantera/paper5/baja_P58H.py` | `8d06faf15749d7dc3ba9e40c5f3a6214` | **no** |
| `cantera/paper5/baja_P58I.py` | `26cce9094acbe82aaf1297af26276fe9` | **no** |
| `cantera/paper5/baja_P58K.py` | `8a850b64a5fb41c7ff2b359ad278b25e` | **no** |
| `cantera/paper5/baja_P58M.py` | `9ff6c9a0a9e83514e787ff3c565ba1ec` | **no** |
| `cantera/paper5/banco_P55B.py` | `191571fde570610c41f244ef5b3efde9` | **no** |
| `cantera/paper5/banco_confianza.py` | `ce73e66b328e5308e6682424f6956184` | **no** |
| `cantera/paper5/banco_confianza2.py` | `5902fbb8a57a98961c5fde45fdf9c61c` | **no** |
| `cantera/paper5/banco_forma.py` | `9d7051e9cdf0c5e9bf70b402a7ff97f2` | **no** |
| `cantera/paper5/banco_forma3.py` | `f0db54a894fcda321aef9e4614676c15` | **no** |
| `cantera/paper5/banco_forma4.py` | `5f66d20f7833a91d614aa3b1ca08702a` | **no** |
| `cantera/paper5/banco_forma5.py` | `2457f69eb2d2fed5f83e9de8a7eb7e84` | **no** |
| `cantera/paper5/banco_forma6.py` | `1aa28ad30615fa2826e473f431f1d44e` | **no** |
| `cantera/paper5/banco_forma7.py` | `da3ff97637beab0980f29afcbc65aecf` | **no** |
| `cantera/paper5/banco_llaves.py` | `7bdccd88c6f8ac5a18514a5ffd85e05d` | **no** |
| `cantera/paper5/banco_llaves2.py` | `73c042178ec3e5d03cdafcffdc26b3ee` | **no** |
| `cantera/paper5/banco_llaves3.py` | `22fd590f779307be72569926e09d08eb` | **no** |
| `cantera/paper5/ciclo_P56C.py` | `9bf01a1adacc9e6da409ed40686048e4` | **no** |
| `cantera/paper5/clases_consejo.py` | `4df13ea6d512f8e5cd585fff8c652635` | **no** |
| `cantera/paper5/comprueba_consejo.py` | `b339569c209aaa08142cbee1e7570ad1` | **no** |
| `cantera/paper5/confianza.py` | `72018777fcb18c8e7f18e7720c913020` | **no** |
| `cantera/paper5/consejero_forma.py` | `ac164782a620e8f58f49bfa3873313ab` | **no** |
| `cantera/paper5/costes_A.py` | `aed97cdefe25b748fc13f92dafb45f2a` | **no** |
| `cantera/paper5/cruza_P58J.py` | `854867eaf90d5369b86d1bf7212a20bd` | **no** |
| `cantera/paper5/descompone_F2.py` | `ed8a6af9d680156418361f08ceca2bce` | **no** |
| `cantera/paper5/ejemplos_P55A.py` | `fba3a43de91bfc33b44628f264c6c73a` | **no** |
| `cantera/paper5/escenas_P55B.py` | `b6d4b71b630921ca75ddb325441dc438` | **no** |
| `cantera/paper5/estado_P56B.py` | `599a40422d16a85cb058abbd9668ea26` | **no** |
| `cantera/paper5/extrae_consejo.py` | `66db58852c7e88851dd7f8b7895f83a8` | **no** |
| `cantera/paper5/fig13_datos.py` | `617aeaabea6e7875e1c19462cf77628e` | **no** |
| `cantera/paper5/fig2_datos.py` | `f191d049d85ac9934dabad107012a420` | **no** |
| `cantera/paper5/fig45_datos.py` | `e8e9fb7e6a2d2a63004d7b2b1f8ceb3b` | **no** |
| `cantera/paper5/fig_D3.py` | `279b15ee9e55644c2a6e339699587a96` | **no** |
| `cantera/paper5/fig_P53A.py` | `768f2093058c56babaa7181a32790bf7` | **no** |
| `cantera/paper5/fig_P53B.py` | `2765926c766be7093f5aae7722fc6bb7` | **no** |
| `cantera/paper5/fig_P54A.py` | `5855531b5140cccbff3ccef8b6cd35f7` | **no** |
| `cantera/paper5/fig_P56C.py` | `929137685da3f56dfa31cfc2cf7fb2ab` | **no** |
| `cantera/paper5/fig_P57A.py` | `9dc46ed07ba3e21907943bdb70e98fd3` | **no** |
| `cantera/paper5/fig_P57B.py` | `4fe60e68516571c453a480a0f5e8d693` | **no** |
| `cantera/paper5/fig_P57C.py` | `816488410e253fcff2ed67f07a7d291c` | **no** |
| `cantera/paper5/fig_P58M.py` | `c60704b947b01f914ada0527cf096972` | **no** |
| `cantera/paper5/fig_paper5.py` | `59660fcfecdac387a2b093d87f21845f` | **no** |
| `cantera/paper5/hace_lento_v0.py` | `f2b0c34c60b2d4a632f2d677e72a81f5` | **no** |
| `cantera/paper5/humo_P58A.py` | `4b8f769a81022a74b8ba18353f34802e` | **no** |
| `cantera/paper5/humo_campo_P56B.py` | `386b015f55419f525479d1485165f0e2` | **no** |
| `cantera/paper5/k2_P58M.py` | `4a13adf852fd2526768e492a23a39708` | **no** |
| `cantera/paper5/lanza_B1.py` | `9a9f26a757be1208cc43f4597c2ce619` | **no** |
| `cantera/paper5/lanza_P56B.py` | `63d2e38d9a4f6e5d4e1c8f1c5b762aaa` | **no** |
| `cantera/paper5/lanza_P56C.py` | `bad2c9c2c510bea055f3a173e54f6202` | **no** |
| `cantera/paper5/lanza_P56C_amp.py` | `936d3708d71cfa8fd0c429154550d775` | **no** |
| `cantera/paper5/lanza_P57C.py` | `656fc145d06321496f4e81ad9e9d5f6d` | **no** |
| `cantera/paper5/lanza_P58B.py` | `cf4d71aa1c0288b977152847c8a236db` | **no** |
| `cantera/paper5/lanza_P58D.py` | `543a4a62a7bbcfb2ca016fbf3ddb5090` | **no** |
| `cantera/paper5/lanza_P58E.py` | `7235d4a9b2e0ac41d0ccc53f35e6d01c` | **no** |
| `cantera/paper5/lanza_P58H.py` | `128a1d01b81c205bde1815004b208ce1` | **no** |
| `cantera/paper5/lanza_P58I.py` | `1bb5f2ca0043b3e5f6adbf22141ae127` | **no** |
| `cantera/paper5/lanza_P58K.py` | `68b9fdbfcbe78b174846e582ff566ccf` | **no** |
| `cantera/paper5/lanza_P58M.py` | `8583cdd6b4ee624a4d0196cdf4ecc536` | **no** |
| `cantera/paper5/mide_P53A.py` | `8f647959ce1f48419777207a35ae54e7` | **no** |
| `cantera/paper5/mide_P57A.py` | `8374fb65babeec4e4b880d27558f2e87` | **no** |
| `cantera/paper5/mide_P57B.py` | `f6d0425e9aa8010844badcf60a298cd1` | **no** |
| `cantera/paper5/mide_P58A.py` | `c7de662c76eac021c6ce8d2773b11efe` | **no** |
| `cantera/paper5/mide_P58C.py` | `118190ceb367da8c1faff34e91823030` | **no** |
| `cantera/paper5/mide_P58F.py` | `34142d87885ea79e75f05fa7b8eb333c` | **no** |
| `cantera/paper5/mide_P58G.py` | `265ed60584112e85e07cdeb86c5000fd` | **no** |
| `cantera/paper5/mide_P58I.py` | `4045ebd03d963b2a411fd89036de3b43` | **no** |
| `cantera/paper5/mide_P58J.py` | `93dc5d56c4a87598b0c36b299a5ab402` | **no** |
| `cantera/paper5/mide_P58K.py` | `b4cb0a32f67fafd957d1691ab65d7126` | **no** |
| `cantera/paper5/mide_P58L.py` | `7c5c8d341918985306e26f464c637c18` | **no** |
| `cantera/paper5/mide_P58L_b.py` | `83e33c249d553e1b8f83dd4f1cb2fb2e` | **no** |
| `cantera/paper5/mide_P58M.py` | `4436b9969c876e994da54044de327f4e` | **no** |
| `cantera/paper5/mide_P58N.py` | `6f0e464073b489b0b4d3c3021aab074c` | **no** |
| `cantera/paper5/mide_P58N_inv.py` | `65e317d39f763dca218749d0edd19581` | **no** |
| `cantera/paper5/mide_P58O.py` | `03b47b010e972aea3e2825538da360e9` | **no** |
| `cantera/paper5/mide_P5AP2.py` | `e2acf8083b8ee845ddc0d916528bb28b` | **no** |
| `cantera/paper5/mide_W.py` | `d237567e9c7f473e69464cd9ee406401` | **no** |
| `cantera/paper5/otros.py` | `1a6216004fa847a97d7fd118170e8c32` | **no** |
| `cantera/paper5/participantes_P56B.py` | `fb9f3adf6f0611c8e149d4ade73fa073` | **no** |
| `cantera/paper5/perfil_P53D.py` | `7beafc0a95725699202b4403b72a6201` | **no** |
| `cantera/paper5/porque_gana_azar.py` | `8217e14dccc14bc378c400fcaed54087` | **no** |
| `cantera/paper5/porque_gana_azar_E1.py` | `763aef6eb36b3411b56ed6e62a5c11c7` | **no** |
| `cantera/paper5/recoge_P58I.py` | `5ee8998a37dd835c83ae63f56e90e6cc` | **no** |
| `cantera/paper5/recoge_P58K.py` | `3a9c0755097eefa3730babe02386f803` | **no** |
| `cantera/paper5/recoge_P58M.py` | `a9daa6cff79f7e24b80e2ba3e4bd0ff3` | **no** |
| `cantera/paper5/relanza_P56C.py` | `1d3c03c65d7ac1ba1808eb41bf2da1a6` | **no** |
| `cantera/paper5/sellos_P56C.py` | `650356dbf22d8420cba8d5bfa55433c4` | **no** |
| `cantera/paper5/sonda_A.py` | `b093d43f72a6af0e5296e4493076b542` | **no** |
| `cantera/paper5/tablas_C.py` | `1af49635a409b8e442d7681e45ad2798` | **no** |
| `cantera/paper5/tablas_P52.py` | `48a56bf66542ffc61ecacb1b0eec7801` | **no** |
| `cantera/paper5/tablas_P52b.py` | `70e9c1d13ec1057dfff6f10dd6f5bc9c` | **no** |
| `cantera/paper5/tablas_P52c.py` | `0d24342bd7d9b9803b8877117049e823` | **no** |
| `cantera/paper5/verifica_relato.py` | `e9e1133c6f4816dc5f54fa9a43283bbd` | **no** |
| `cantera/paper5/vigila_B1.py` | `23eddba97e66c4615e569c1e421e1d3f` | **no** |
| `cantera/paper5/vigila_P56B.py` | `341c0024e60b9342c60c4b8cf9e119eb` | **no** |

*117 archivos.*


---

## CÓMO SE COMPRUEBA

```bash
python3 cantera/paper6/congela_paper5.py     # vuelve a imprimir esta tabla
```

Si un md5 de la tabla ya no cuadra, ese archivo se tocó después del paper cinco
y cualquier número medido con él deja de ser reproducible.
