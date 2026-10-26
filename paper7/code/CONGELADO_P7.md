# CONGELADO_P7 · the code of paper seven that played

*Written by `cantera/paper7/publicar/publica_P7.py` (P7-PUB1). `motor/model.py` = `1e511978c251130e95169ebf8443efa1`, unchanged since paper one. The body of paper seven grew field by field; each field's image is built from a recipe (`Dockerfile.pareja_P7_*`) that copies the pieces of the earlier fields and adds its own. The recipe of the final field, `cantera/paper7/Dockerfile.pareja_P7_67c` (md5 `d29fe05a85a9235075a805a3d6615018`), copies all of them. This list is that image: (1) what it loads, traced by rebuilding its `/app` in a temporary folder with the recipe's environment and doing what the recipe does when it is built (importing the entry point and applying the composition, with CONGELA=0 and 1), with nothing played; (2) what it copies by name and its entry point does not load (the pieces and entry points of the earlier fields, the smoke tests of paper six that run when the image is built); (3) the recipes of the images of the fields this paper reports.*

*An earlier field was played with the version of each piece that its seal names. When a piece was fixed later, the fix is declared in the seal or in the report, and the copy here is the last version. The table at the end compares, seal by seal, every md5 a seal names with the md5 of the file today.*

| class | file | md5 | why it is here |
|---|---|---|---|
| loaded | `cantera/paper5/alcance_g.py` | `bf62b03587506064311c122fd0e09102` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper5/curiosidad.py` | `f803f47c8ed0a8eaf3855d7e1dc7d457` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper5/curiosidad_forma.py` | `141ecb2eb17f76654caf4bbf3c29c642` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper5/forma.py` | `b801876afda071403c5af54a28feff85` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper5/proyeccion.py` | `bbc42daeaa769c783844997067ef148d` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper5/traductor_forma.py` | `b310bb72884ef5f4e3510ab803cd2776` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper6/amenaza11_P6_11.py` | `9d493b05495f55316f29cbffa5561cdb` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper6/arreglos_P6_6.py` | `4d10ea09333553ebf7d6ce0afdb73832` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper6/arreglos_P6_8b.py` | `5028b54d4afd8c7c82bc8e5e3a94a01e` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper6/filas10_P6_10.py` | `af4617ad93a27838376df17d0c78b65c` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper6/oido5_P6_5.py` | `4f7aa3b3ddc4fc32e4b47c1356974415` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper6/oyente2.py` | `4e8b657f9168b0ffda5e411601b1aa14` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper6/parte2.py` | `67ba0003234939c349af12be5764a3b0` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper6/policy_pareja.py` | `796fc64229d047410fb351dfa61f871b` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/campo_P7_66b.py` | `25f6837464dab2a24cd01696967424b1` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/campo_P7_67.py` | `1a56963e35192913157f7625c91dea4c` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/campo_P7_67b.py` | `1bfe2051610a7e542f4d3741d02522ca` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/campo_P7_67c.py` | `660e94164088b6010393219667b72ea0` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/congela_P7_67.py` | `5a9feb0d720ab6ea277e988c93630d37` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/contrafactual_P7_38.py` | `b0efef883215d5046cbfc5db220d0f83` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/cuaderno_P7.py` | `f4c6a9dae0af4831cfa930da18b74376` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/descubre_P7.py` | `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/efecto_P7_39.py` | `f36ea927c5c083f597b5baa20b3d48a7` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/escala_P7_48.py` | `adcdd40ba2b046b5df03964c1cb56f83` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/filo_P7_40.py` | `1fefeef2071af1f2adaf9ab116d0254f` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/hermanas_P7_48.py` | `82083a140a84c9ce2f4134bf8a6aa57d` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/invita_P7_54.py` | `38b3702dd08280e8a308aeebec3791a6` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/invita_P7_57.py` | `019a38bf16ac851455d3ce20ff64d777` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/invita_P7_66b.py` | `c1352e4ad95c7a7515ca8394c8e0185b` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/invita_P7_67.py` | `55de13e237a1484dd533b41b7fe01d0d` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/invita_P7_67b.py` | `a25ebbfce4774cad72fc8439e6e045eb` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/juicio_P7_62.py` | `ded4ac2c1d2acf2899e5d533cf444d6a` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/juicio_P7_65.py` | `60070a5957284fe8056acc738f75cfd7` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/miedo_P7_49.py` | `25926b765096e89116add8dcb3260ddd` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/nace_P7_23.py` | `0083986bd7d2e51ee0295d6860e9e06a` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/nace_P7_29.py` | `f8b85c6f61257b09ae3c1d961382f7e6` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/nace_P7_33.py` | `a56fd98d6148b161a1c07cec9b6ebbfb` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/pide_P7.py` | `4766e5a3b0afdc20b787d0b79da9fe31` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/policy_pareja_P7_67c.py` | `296df35605b424f0efcd34d6dbf56ec6` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/rapido_P7_43.py` | `0ec5f59cba0ff99e16e917ef86c3421b` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `cantera/paper7/recuerdo_P7_23.py` | `519e69e67026c880d49af76bc14eed30` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/appraisal_zs.py` | `87745903992bdf0b4f5a18d13f9d4f5a` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/confianza_viva.py` | `6e1e444435914f0b9df287ea37555bbc` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/cortex_t5.py` | `defb11d3a4661ff57745214ccd1ab14f` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/forma_viva.py` | `b2c87c93f0ed47e48fd8991a5a797a42` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/formas_azar.py` | `eefb5534e9533c8b742f7feb96239588` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/hilo_forma.py` | `aeea06ae4eb5b704e94fe845a5a5e5aa` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/mundo.py` | `e2c2cf7618b61e1280f2e3ea989f1872` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/parte.py` | `80dabc2e78c7c36f0708a2d95e22262a` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/policy_cortex.py` | `6997b00c266f23d6037cc1a018f60a76` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/policy_forma.py` | `896e97a0cca1efcb736596e0b8b15cea` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `paintball/alma/relator_t5.py` | `929c49f6ced9af1cbd37eadec08c54f0` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `planificador/__init__.py` | `d41d8cd98f00b204e9800998ecf8427e` | loaded by the final image (imported, both arms of CONGELA) |
| loaded | `planificador/planificador_v1.py` | `d0a3151d718e6b60d499e258c9dea9b1` | loaded by the final image (imported, both arms of CONGELA) |
| copied | `cantera/paper5/P56A_distribucion_azar.json` | `9092c6c73eda7d81f97e9ac730c8783f` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper5/instruccion_forma.md` | `02653e4edf04f3bdd9a0ac3deda9aa01` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper5/tabla_ensenada.md` | `9d53807699c4ee2be31d8dd173196de0` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/arreglos_P6_8.py` | `f66355ca12b58b075d12f0e7f7ee39d0` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/humo_P6_3.py` | `0a026524989218f9f1a494ac72ae3a61` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/humo_mundo.jsonl` | `3cca4bc022ee76017c03d05e1deca687` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/humo_red_P6_10.py` | `e056bbf0467738f48ffd9781c74a137a` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/humo_red_P6_11.py` | `554fb2c432af274a181ff9e7a4bb2551` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/humo_red_P6_4.py` | `f54065171fce6d73da958ba71fd581d1` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/humo_red_P6_6.py` | `fe35afcde9040123d58709e7c04e9880` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/humo_red_P6_8.py` | `797a33eb76a76b84f0c8d3364499517c` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/policy_pareja10.py` | `f3b3292887b05c408c92c00f7595f521` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/policy_pareja6.py` | `933ad20fd7cc28dcf46c4b46eb741cab` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper6/policy_pareja8.py` | `6f3aee13897bbe9510c61e27e19b05cf` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/azar_P7_41.py` | `b4ef6a1a93e2c1c5b143043b3928e6e2` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/azar_P7_47.py` | `dbbd759372d73d7bbcd1fbefbcfbd103` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/campo_P7_41.py` | `2146861db7a18d24990a016632fc74ab` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/campo_P7_47.py` | `d5f5a488b49c0986728fd21afcfa2a45` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/campo_P7_48.py` | `01f8e552fecf631f5686bebc00e16520` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/campo_P7_49.py` | `d4c725eaafea2318ef3519b4b76e081b` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/campo_P7_54.py` | `621560ff88e89cee6ce06ca86f2cf4c6` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/campo_P7_57.py` | `fd80d259a933250a9829c262132b3aa6` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/campo_P7_62.py` | `6521a985f8428449636b95019e9311b5` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/campo_P7_65.py` | `16a95a521052e3eecb545645cdeed4c9` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/campo_P7_66.py` | `934e3f7becaa6b8b8d4020f0d69a87d8` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/curiosa_P7_37.py` | `afb5112e31ef405727142bac2a2ed2fb` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/habitua_P7_47.py` | `97c53ded5045e90c9561e52ff8b5e24e` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/invita_P7_66.py` | `00e6935f8faa40a72a9403745aa41721` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/pasiva_P7_67.py` | `09faa2e5b4b728fdc8b90cd002f4eb3d` | the still rival's policy (Dockerfile.pasiva_P7_67) |
| copied | `cantera/paper7/policy_pareja_P7.py` | `6eb8202a636e5de20ae8df794eb326a8` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_13.py` | `cbcf43ac1a67a78ee317e207c227f5c7` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_23.py` | `fad2c97ed13783cbe7b8d176a9f96735` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_29.py` | `08db5b71d7e5c5a3dce3f47fcf4b4643` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_33.py` | `e0876e9ab8dfe11de98ac9a0168c8f52` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_41.py` | `f221c8e7b954efbf6ca03d6b5cfec854` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_47.py` | `23f0711c3f95cf083eb75dda4829bead` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_48.py` | `0dda071fe4e687756fa23e2c53f652cf` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_49.py` | `f216f899ad33b4c37d52e522aab5e6f6` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_54.py` | `eb1571e19189bd32451b554244369bd9` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_57.py` | `e206ad589c2daca2eba8d2141b32337a` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_62.py` | `23dc2c88d32eaa36a57fe9c978a44b18` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_65.py` | `07e10fb5af995f80b062e2bc556f0baa` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_66.py` | `15b17ed89986d809437d9de98077439e` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_66b.py` | `4a63526555bdc8e7cf7cc9780198037e` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_67.py` | `4739e58aa8229725b324535527b4142e` | copied by name into the final image, not loaded by its entry point |
| copied | `cantera/paper7/policy_pareja_P7_67b.py` | `8227c906cb8a4d89a5ba712b98384d22` | copied by name into the final image, not loaded by its entry point |
| copied | `paintball/alma/memoria_aprendida_p95.json` | `6535717a27e3188852af8a76d2c3ef60` | read by the body (GEMV_MEMORIA in the recipe) |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_24` | `be589f05420a5a25072391f01f5c08e5` | recipe of the image of field P7-24 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_30` | `7abfd1629235767d8c57018692976ce0` | recipe of the image of field P7-30 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_34` | `9a5e61d86c9bca4e835489653ac67b71` | recipe of the image of field P7-34 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_41` | `b79034f8519a2c50c1755c613db1c73d` | recipe of the image of field P7-42 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_49` | `fa9d3bc4d04143fcef220817e4fc36ae` | recipe of the image of field P7-49/50 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_54` | `8db19be7eec8e21c11c15a67710d3931` | recipe of the image of field P7-56 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_57` | `cfe292616bd33327cf8b3956172eaee3` | recipe of the image of field P7-61 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_63` | `82d3ceca312f8a2523edd345140fbc50` | recipe of the image of field P7-63 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_65` | `99ba2e2c295123176a6838eb6449304f` | recipe of the image of field P7-65 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_67` | `b935bfd99910c9a155f2542bba5a707a` | recipe of the image of field P7-67 |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_67b` | `b206040c48e0d1f910759244ff947d78` | recipe of the image of field P7-67b |
| recipe | `cantera/paper7/Dockerfile.pareja_P7_67c` | `d29fe05a85a9235075a805a3d6615018` | recipe of the image of field P7-67F (final) |
| recipe | `cantera/paper7/Dockerfile.pasiva_P7_67` | `9e28a76c5bd3514b5cede925f67d6f67` | recipe of the still rivals (statues) of P7-67 and P7-67F |

*118 files: 58 loaded, 47 copied, 13 recipes.*

## The md5 of each seal, against the file today

Every md5 a seal names next to a file name (for P7-67, the last one, after its amendments). *equal*: the file today is the one that was sealed. *changed later*: the file was changed after that seal; the field was played with the sealed version, and the change is declared in a later seal or report.

| seal | file | md5 in the seal | md5 today | |
|---|---|---|---|---|
| SELLO_P7_10.md | `cantera/paper7/Dockerfile.pareja_P7_8` | `b4f554c8517e826ec4bf74d71586f5dd` | `b4f554c8517e826ec4bf74d71586f5dd` | equal |
| SELLO_P7_10.md | `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` | `98c13d60167c80cc8334c965be75c640` | equal |
| SELLO_P7_10.md | `cantera/paper7/banco_P7_10.py` | `e10696b435c20d333a74b98378dc848e` | `e10696b435c20d333a74b98378dc848e` | equal |
| SELLO_P7_10.md | `cantera/paper7/campo_P7_10.py` | `2f4e87140ecd8b589a225ac1e5672635` | `2f4e87140ecd8b589a225ac1e5672635` | equal |
| SELLO_P7_10.md | `cantera/paper7/cuaderno_P7.py` | `c452a30be823af157193e8705f5c3ef1` | `f4c6a9dae0af4831cfa930da18b74376` | changed later |
| SELLO_P7_10.md | `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` | `8fa03547e3228ef9df4aa94c444f9252` | equal |
| SELLO_P7_10.md | `cantera/paper7/descubre_P7.py` | `9f9080eed55968e5869597ef0c7c7b41` | `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | changed later |
| SELLO_P7_10.md | `cantera/paper7/lanza_P7_10.py` | `645d335007138d9db912238f5b722151` | `d40febfb9a5e1275c038cae6aa3bc156` | changed later |
| SELLO_P7_10.md | `cantera/paper7/limpia_cuaderno_P7_7.py` | `754fae58ad6af07066f96f71b465d526` | `754fae58ad6af07066f96f71b465d526` | equal |
| SELLO_P7_10.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_10.md | `planificador/planificador_v1.py` | `d0a3151d718e6b60d499e258c9dea9b1` | `d0a3151d718e6b60d499e258c9dea9b1` | equal |
| SELLO_P7_10.md | `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` | `e7136f856e6c09dd033bb4658cd135ea` | equal |
| SELLO_P7_10.md | `cantera/paper7/policy_pareja_P7.py` | `6eb8202a636e5de20ae8df794eb326a8` | `6eb8202a636e5de20ae8df794eb326a8` | equal |
| SELLO_P7_10.md | `cantera/paper7/semillas_P7_10.json` | `25eb92133e8c204269b2c55b0f751e6c` | `25eb92133e8c204269b2c55b0f751e6c` | equal |
| SELLO_P7_14.md | `cantera/paper7/Dockerfile.pareja_P7_13` | `a7f97e4bedebf05499b1160a1d890105` | `a7f97e4bedebf05499b1160a1d890105` | equal |
| SELLO_P7_14.md | `cantera/paper7/analiza_P7_11.py` | `5ccc1bc0bef563e380691f1866c39c05` | `5ccc1bc0bef563e380691f1866c39c05` | equal |
| SELLO_P7_14.md | `cantera/paper7/analiza_P7_14.py` | `edeff749afd71f8b0413fa7d1b57eac0` | `edeff749afd71f8b0413fa7d1b57eac0` | equal |
| SELLO_P7_14.md | `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` | `98c13d60167c80cc8334c965be75c640` | equal |
| SELLO_P7_14.md | `cantera/paper7/banco_P7_13.py` | `0e31cf5b9e5f7fe486036928a66f45f5` | `0e31cf5b9e5f7fe486036928a66f45f5` | equal |
| SELLO_P7_14.md | `cantera/paper7/campo_P7_14.py` | `e107c185e104632d29326c85b5a50741` | `e107c185e104632d29326c85b5a50741` | equal |
| SELLO_P7_14.md | `cantera/paper7/cuaderno_P7.py` | `f4c6a9dae0af4831cfa930da18b74376` | `f4c6a9dae0af4831cfa930da18b74376` | equal |
| SELLO_P7_14.md | `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` | `8fa03547e3228ef9df4aa94c444f9252` | equal |
| SELLO_P7_14.md | `cantera/paper7/descubre_P7.py` | `4bc52512d12cad76973f4512613253b3` | `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | changed later |
| SELLO_P7_14.md | `cantera/paper7/lanza_P7_14.py` | `33965f7dff8071cd41de42180f427349` | `33965f7dff8071cd41de42180f427349` | equal |
| SELLO_P7_14.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_14.md | `paintball/alma/parte.py` | `80dabc2e78c7c36f0708a2d95e22262a` | `80dabc2e78c7c36f0708a2d95e22262a` | equal |
| SELLO_P7_14.md | `cantera/paper7/pide_P7.py` | `4bc2ae5d3934a1be61944fa37d90b976` | `4766e5a3b0afdc20b787d0b79da9fe31` | changed later |
| SELLO_P7_14.md | `planificador/planificador_v1.py` | `d0a3151d718e6b60d499e258c9dea9b1` | `d0a3151d718e6b60d499e258c9dea9b1` | equal |
| SELLO_P7_14.md | `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` | `e7136f856e6c09dd033bb4658cd135ea` | equal |
| SELLO_P7_14.md | `cantera/paper7/policy_pareja_P7_13.py` | `cbcf43ac1a67a78ee317e207c227f5c7` | `cbcf43ac1a67a78ee317e207c227f5c7` | equal |
| SELLO_P7_14.md | `cantera/paper7/sello_P7_14.py` | `31e02926334561f25ed4f7a3abe1c8aa` | `31e02926334561f25ed4f7a3abe1c8aa` | equal |
| SELLO_P7_14.md | `cantera/paper7/semillas_P7_14.json` | `960c49b5d6685ef93806407899d079ff` | `960c49b5d6685ef93806407899d079ff` | equal |
| SELLO_P7_14b.md | `cantera/paper7/Dockerfile.pareja_P7_13` | `a7f97e4bedebf05499b1160a1d890105` | `a7f97e4bedebf05499b1160a1d890105` | equal |
| SELLO_P7_14b.md | `cantera/paper7/analiza_P7_11.py` | `5ccc1bc0bef563e380691f1866c39c05` | `5ccc1bc0bef563e380691f1866c39c05` | equal |
| SELLO_P7_14b.md | `cantera/paper7/analiza_P7_14b.py` | `d6f870231b61ebec200fcec983369da8` | `d6f870231b61ebec200fcec983369da8` | equal |
| SELLO_P7_14b.md | `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` | `98c13d60167c80cc8334c965be75c640` | equal |
| SELLO_P7_14b.md | `cantera/paper7/banco_P7_13.py` | `0e31cf5b9e5f7fe486036928a66f45f5` | `0e31cf5b9e5f7fe486036928a66f45f5` | equal |
| SELLO_P7_14b.md | `cantera/paper7/banco_P7_14b.py` | `b09c0d9f4f2b5cafbd6558f5cd82c9ee` | `b09c0d9f4f2b5cafbd6558f5cd82c9ee` | equal |
| SELLO_P7_14b.md | `cantera/paper7/campo_P7_14b.py` | `1f25698d4032b4064d977fedf680c5db` | `1f25698d4032b4064d977fedf680c5db` | equal |
| SELLO_P7_14b.md | `cantera/paper7/cuaderno_P7.py` | `f4c6a9dae0af4831cfa930da18b74376` | `f4c6a9dae0af4831cfa930da18b74376` | equal |
| SELLO_P7_14b.md | `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` | `8fa03547e3228ef9df4aa94c444f9252` | equal |
| SELLO_P7_14b.md | `cantera/paper7/descubre_P7.py` | `5d6de90e491be8d8c6618263023a6534` | `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | changed later |
| SELLO_P7_14b.md | `cantera/paper7/freno_P7_14b.py` | `c1870e9907f7925f6f8badf88a510d8a` | `c1870e9907f7925f6f8badf88a510d8a` | equal |
| SELLO_P7_14b.md | `cantera/paper7/lanza_P7_14b.py` | `04af05dee256157bae9515eeecf0d72f` | `04af05dee256157bae9515eeecf0d72f` | equal |
| SELLO_P7_14b.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_14b.md | `paintball/alma/parte.py` | `80dabc2e78c7c36f0708a2d95e22262a` | `80dabc2e78c7c36f0708a2d95e22262a` | equal |
| SELLO_P7_14b.md | `cantera/paper7/pide_P7.py` | `4bc2ae5d3934a1be61944fa37d90b976` | `4766e5a3b0afdc20b787d0b79da9fe31` | changed later |
| SELLO_P7_14b.md | `planificador/planificador_v1.py` | `d0a3151d718e6b60d499e258c9dea9b1` | `d0a3151d718e6b60d499e258c9dea9b1` | equal |
| SELLO_P7_14b.md | `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` | `e7136f856e6c09dd033bb4658cd135ea` | equal |
| SELLO_P7_14b.md | `cantera/paper7/policy_pareja_P7_13.py` | `cbcf43ac1a67a78ee317e207c227f5c7` | `cbcf43ac1a67a78ee317e207c227f5c7` | equal |
| SELLO_P7_14b.md | `cantera/paper7/sello_P7_14b.py` | `20261bd1cdb3deee2ebd6c8b405b72a4` | `20261bd1cdb3deee2ebd6c8b405b72a4` | equal |
| SELLO_P7_14b.md | `cantera/paper7/semillas_P7_14b.json` | `968117a6bc88b5e6b1aa72c9876a9cbf` | `968117a6bc88b5e6b1aa72c9876a9cbf` | equal |
| SELLO_P7_22.md | `cantera/paper7/P7_22_fijado.json` | `fd382c670253e18e3611d8d5050a07f0` | `fd382c670253e18e3611d8d5050a07f0` | equal |
| SELLO_P7_22.md | `cantera/paper7/P7_22_recuerdos.json` | `74396f5d7a5205b8b77b3a3aa416027c` | `74396f5d7a5205b8b77b3a3aa416027c` | equal |
| SELLO_P7_22.md | `cantera/paper7/banco_P7_22.py` | `d125f2954350557e6ea50eba5c991953` | `d125f2954350557e6ea50eba5c991953` | equal |
| SELLO_P7_22.md | `cantera/paper7/banco_decide_P7_22.py` | `71ec40987425d55b935793f1c2b4fb81` | `71ec40987425d55b935793f1c2b4fb81` | equal |
| SELLO_P7_22.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_22.md | `cantera/paper7/recuerdos_P7_22.py` | `fdfa6b71fccc3080221d15509e47b060` | `fdfa6b71fccc3080221d15509e47b060` | equal |
| SELLO_P7_24.md | `cantera/paper7/Dockerfile.pareja_P7_24` | `be589f05420a5a25072391f01f5c08e5` | `be589f05420a5a25072391f01f5c08e5` | equal |
| SELLO_P7_24.md | `cantera/paper7/cuaderno_P7.py` | `f4c6a9dae0af4831cfa930da18b74376` | `f4c6a9dae0af4831cfa930da18b74376` | equal |
| SELLO_P7_24.md | `cantera/paper7/descubre_P7.py` | `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | equal |
| SELLO_P7_24.md | `cantera/paper7/lanza_P7_24.py` | `dd43c880d4c231e1c4de28e30dd17981` | `62dc8204c6196d9352d1dfc32f365c49` | changed later |
| SELLO_P7_24.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_24.md | `cantera/paper7/nace_P7_23.py` | `6e187039d3189f2af64840f050d2eaac` | `0083986bd7d2e51ee0295d6860e9e06a` | changed later |
| SELLO_P7_24.md | `cantera/paper7/pide_P7.py` | `4766e5a3b0afdc20b787d0b79da9fe31` | `4766e5a3b0afdc20b787d0b79da9fe31` | equal |
| SELLO_P7_24.md | `cantera/paper7/policy_pareja_P7_23.py` | `fad2c97ed13783cbe7b8d176a9f96735` | `fad2c97ed13783cbe7b8d176a9f96735` | equal |
| SELLO_P7_24.md | `cantera/paper7/recuerdo_P7_23.py` | `519e69e67026c880d49af76bc14eed30` | `519e69e67026c880d49af76bc14eed30` | equal |
| SELLO_P7_24.md | `cantera/paper7/semillas_P7_24.json` | `5949267f29e4f0ca8a1bd35b561aeb57` | `5949267f29e4f0ca8a1bd35b561aeb57` | equal |
| SELLO_P7_30.md | `cantera/paper7/Dockerfile.pareja_P7_30` | `7abfd1629235767d8c57018692976ce0` | `7abfd1629235767d8c57018692976ce0` | equal |
| SELLO_P7_30.md | `cantera/paper7/cuaderno_P7.py` | `f4c6a9dae0af4831cfa930da18b74376` | `f4c6a9dae0af4831cfa930da18b74376` | equal |
| SELLO_P7_30.md | `cantera/paper7/descubre_P7.py` | `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | equal |
| SELLO_P7_30.md | `cantera/paper7/guarda_latencia_P7_29.py` | `21696e98acbc8d8e096c63d75694daf1` | `a998e87736e8538ebcacac1fef62df84` | changed later |
| SELLO_P7_30.md | `cantera/paper7/lanza_P7_30.py` | `7d4afba15af5e6bb6b12099e8424e943` | `7a2fc38a3b01c8124c4e02580a7f2e45` | changed later |
| SELLO_P7_30.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_30.md | `cantera/paper7/nace_P7_23.py` | `0083986bd7d2e51ee0295d6860e9e06a` | `0083986bd7d2e51ee0295d6860e9e06a` | equal |
| SELLO_P7_30.md | `cantera/paper7/nace_P7_29.py` | `9f43cd057c0eb6f6e3119b0989bbf233` | `f8b85c6f61257b09ae3c1d961382f7e6` | changed later |
| SELLO_P7_30.md | `cantera/paper7/pide_P7.py` | `4766e5a3b0afdc20b787d0b79da9fe31` | `4766e5a3b0afdc20b787d0b79da9fe31` | equal |
| SELLO_P7_30.md | `cantera/paper7/policy_pareja_P7_29.py` | `08db5b71d7e5c5a3dce3f47fcf4b4643` | `08db5b71d7e5c5a3dce3f47fcf4b4643` | equal |
| SELLO_P7_30.md | `cantera/paper7/recuerdo_P7_23.py` | `519e69e67026c880d49af76bc14eed30` | `519e69e67026c880d49af76bc14eed30` | equal |
| SELLO_P7_30.md | `cantera/paper7/semillas_P7_30.json` | `f1366f62683b3dbd11d17a33c18a3c7b` | `f1366f62683b3dbd11d17a33c18a3c7b` | equal |
| SELLO_P7_34.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_38.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_39.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_40.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_42.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_47.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_49.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_56.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_61.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_63.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_65.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_67.md | `cantera/paper7/Dockerfile.pareja_P7_67c` | `d29fe05a85a9235075a805a3d6615018` | `d29fe05a85a9235075a805a3d6615018` | equal |
| SELLO_P7_67.md | `cantera/paper7/P7_67F_diseno.json` | `8f11cc7c0c1e97cfb95e8acade3b184c` | `8f11cc7c0c1e97cfb95e8acade3b184c` | equal |
| SELLO_P7_67.md | `cantera/paper7/analiza_P7_67.py` | `7bef2e46106bb860c366b0bdb1dba037` | `7bef2e46106bb860c366b0bdb1dba037` | equal |
| SELLO_P7_67.md | `cantera/paper7/archiva_P7_67F.py` | `0ecefbb9a148d154654d4450cfcd3c93` | `0ecefbb9a148d154654d4450cfcd3c93` | equal |
| SELLO_P7_67.md | `cantera/paper7/campo_P7_67.py` | `1a56963e35192913157f7625c91dea4c` | `1a56963e35192913157f7625c91dea4c` | equal |
| SELLO_P7_67.md | `cantera/paper7/campo_P7_67b.py` | `1bfe2051610a7e542f4d3741d02522ca` | `1bfe2051610a7e542f4d3741d02522ca` | equal |
| SELLO_P7_67.md | `cantera/paper7/campo_P7_67c.py` | `660e94164088b6010393219667b72ea0` | `660e94164088b6010393219667b72ea0` | equal |
| SELLO_P7_67.md | `cantera/paper7/congela_P7_67.py` | `5a9feb0d720ab6ea277e988c93630d37` | `5a9feb0d720ab6ea277e988c93630d37` | equal |
| SELLO_P7_67.md | `cantera/paper7/disena_P7_67F.py` | `7ee24f0ee5fc60e81de6e11c82487578` | `7ee24f0ee5fc60e81de6e11c82487578` | equal |
| SELLO_P7_67.md | `cantera/paper7/invita_P7_66b.py` | `c1352e4ad95c7a7515ca8394c8e0185b` | `c1352e4ad95c7a7515ca8394c8e0185b` | equal |
| SELLO_P7_67.md | `cantera/paper7/invita_P7_67.py` | `55de13e237a1484dd533b41b7fe01d0d` | `55de13e237a1484dd533b41b7fe01d0d` | equal |
| SELLO_P7_67.md | `cantera/paper7/invita_P7_67b.py` | `a25ebbfce4774cad72fc8439e6e045eb` | `a25ebbfce4774cad72fc8439e6e045eb` | equal |
| SELLO_P7_67.md | `cantera/paper7/lanza_P7_67F.py` | `b632b91869a4af0ee18959589e843b00` | `b632b91869a4af0ee18959589e843b00` | equal |
| SELLO_P7_67.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_67.md | `cantera/paper7/pasiva_P7_67.py` | `09faa2e5b4b728fdc8b90cd002f4eb3d` | `09faa2e5b4b728fdc8b90cd002f4eb3d` | equal |
| SELLO_P7_67.md | `cantera/paper7/policy_pareja_P7_67c.py` | `296df35605b424f0efcd34d6dbf56ec6` | `296df35605b424f0efcd34d6dbf56ec6` | equal |
| SELLO_P7_8.md | `cantera/paper7/Dockerfile.pareja_P7_8` | `b4f554c8517e826ec4bf74d71586f5dd` | `b4f554c8517e826ec4bf74d71586f5dd` | equal |
| SELLO_P7_8.md | `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` | `98c13d60167c80cc8334c965be75c640` | equal |
| SELLO_P7_8.md | `cantera/paper7/banco_P7_8.py` | `a25ff85edcbf56347135013f0b245c34` | `a25ff85edcbf56347135013f0b245c34` | equal |
| SELLO_P7_8.md | `cantera/paper7/campo_P7_8.py` | `a6553d0e162b57aa4896eaf131045210` | `1b6175a1f56396d353970a5644cfb1e4` | changed later |
| SELLO_P7_8.md | `cantera/paper7/cuaderno_P7.py` | `c452a30be823af157193e8705f5c3ef1` | `f4c6a9dae0af4831cfa930da18b74376` | changed later |
| SELLO_P7_8.md | `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` | `8fa03547e3228ef9df4aa94c444f9252` | equal |
| SELLO_P7_8.md | `cantera/paper7/descubre_P7.py` | `ff3bb96aa384ed9831630c0dbf7b05a4` | `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | changed later |
| SELLO_P7_8.md | `cantera/paper7/lanza_P7_8.py` | `a821a6006eecda9de578bc6031b2ca8a` | `a821a6006eecda9de578bc6031b2ca8a` | equal |
| SELLO_P7_8.md | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | `1e511978c251130e95169ebf8443efa1` | equal |
| SELLO_P7_8.md | `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` | `e7136f856e6c09dd033bb4658cd135ea` | equal |
| SELLO_P7_8.md | `cantera/paper7/policy_pareja_P7.py` | `6eb8202a636e5de20ae8df794eb326a8` | `6eb8202a636e5de20ae8df794eb326a8` | equal |
| SELLO_P7_8.md | `cantera/paper7/semillas_P7_8.json` | `ff6c2fb5754cf0bab67e72cda145ca6e` | `ff6c2fb5754cf0bab67e72cda145ca6e` | equal |

*104 equal, 15 changed later.*
