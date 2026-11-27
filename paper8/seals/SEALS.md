# The ten sealed experiments

Each file is the version stored in the git tag of the seal (`git show <tag>:<file>`), that is, as it was sealed, before the games were played. Date and commit are those of the tag; for seals 5 and 6 the tag froze the code and the bets were stored in their own commit minutes later, before the games were played: date and commit are then those of that commit («own commit»). «same today» says whether the working file is still identical.

| # | name | tag | commit | date | file | md5 | same today |
|---|---|---|---|---|---|---|---|
| 1 | v1 | `valle-congelado-v1` | `ccd88251` (tag) | 2026-11-02 09:33 | `01_v1/predicciones_selladas.md` | `1640ccbc10b69e094899be06e1c64857` | yes |
| 1 | v1 | `valle-congelado-v1` | `ccd88251` (tag) | 2026-11-02 09:33 | `01_v1/CONGELADO_P8.md` | `486caa660e515f43a4be061dc48dd197` | NO |
| 2 | confirmacion | `valle-confirmacion-v1` | `79afe666` (tag) | 2026-11-03 07:19 | `02_confirmacion/predicciones_confirmacion.md` | `d86a9658d6b76503e0d4f28c088e1d49` | yes |
| 3 | dilemas | `valle-dilemas-v1` | `aa7fd4b1` (tag) | 2026-11-03 13:24 | `03_dilemas/predicciones_dilemas.md` | `e4c0baf6a43985457bb5b4cd6aa0cc71` | yes |
| 4 | mesa | `valle-mesa-v1` | `caf63cda` (tag) | 2026-11-03 15:27 | `04_mesa/predicciones_mesa.md` | `0fa0d61498932e39e79850ef4568b82e` | yes |
| 5 | v2 | `valle-congelado-v2` | `648475e6` (own commit) | 2026-11-07 00:13 | `05_v2/predicciones_selladas_v2.md` | `94393fdd9c703cd48e3cb60cf01fe309` | yes |
| 5 | v2 | `valle-congelado-v2` | `af7605a5` (tag) | 2026-11-07 00:02 | `05_v2/CONGELADO_P8_v2.md` | `2500fd7333f24091ae2c72b79bf24a54` | yes |
| 6 | v3 | `valle-congelado-v3` | `61276d6b` (own commit) | 2026-11-10 00:04 | `06_v3/predicciones_selladas_v3.md` | `8680a19d5c46d4a380f035bdab4046e1` | yes |
| 6 | v3 | `valle-congelado-v3` | `34bf8e78` (tag) | 2026-11-09 23:06 | `06_v3/CONGELADO_P8_v3.md` | `874ae88fde078346efbbe9d8c62d5145` | yes |
| 6 | v3 | `valle-congelado-v3` | `34bf8e78` (tag) | 2026-11-09 23:06 | `06_v3/md5_v3d.md` | `f9a7a1e99efcc29f207782d49f0d2366` | yes |
| 7 | v4 | `valle-congelado-v4` | `27b23137` (tag) | 2026-11-11 12:56 | `07_v4/predicciones_selladas_v4.md` | `96acde2d8495083b06c5409e77d0e60a` | yes |
| 7 | v4 | `valle-congelado-v4` | `27b23137` (tag) | 2026-11-11 12:56 | `07_v4/CONGELADO_P8_v4.md` | `979d20062eb66cee1425d50dfdd4314b` | yes |
| 7 | v4 | `valle-congelado-v4` | `27b23137` (tag) | 2026-11-11 12:56 | `07_v4/md5_v4.md` | `b6a32882b9c05a3becca5dc41c9c9086` | yes |
| 8 | v5 | `valle-congelado-v5` | `65ee6048` (tag) | 2026-11-15 09:47 | `08_v5/predicciones_selladas_v5.md` | `f6ae001568065dba14715e3ecee74aad` | yes |
| 8 | v5 | `valle-congelado-v5` | `65ee6048` (tag) | 2026-11-15 09:47 | `08_v5/CONGELADO_P8_v5.md` | `27540ecfd66ee14ab96dd192942fa413` | yes |
| 8 | v5 | `valle-congelado-v5` | `65ee6048` (tag) | 2026-11-15 09:47 | `08_v5/md5_v5.md` | `225322c20b0f3893b25edc4516ba35c2` | yes |
| 9 | v6 | `valle-congelado-v6` | `759acc39` (tag) | 2026-11-18 00:03 | `09_v6/predicciones_selladas_v6.md` | `95036770934d2c0d5b91a131e155befe` | yes |
| 9 | v6 | `valle-congelado-v6` | `759acc39` (tag) | 2026-11-18 00:03 | `09_v6/CONGELADO_P8_v6.md` | `3c332f41cc9510b5ce59b1cf2d31f92d` | yes |
| 9 | v6 | `valle-congelado-v6` | `759acc39` (tag) | 2026-11-18 00:03 | `09_v6/md5_v6.md` | `6b4ed760b32270468b3d875241af8290` | yes |
| 10 | escalera | `valle-escalera-v6` | `24cdb2db` (tag) | 2026-11-19 00:35 | `10_escalera/predicciones_selladas_v6_escalera.md` | `09264179d2523332bcfa805051a648c4` | yes |

## Seals 5 and 6: the bets were stored before the first game

In seals 5 and 6 the git tag froze the code, and the file of bets was stored in its own commit a few minutes later. The first game of each seal, by the creation time of its folder on the disk where the games are kept, started after that commit. The date in table A.1 of the paper is that of the tag.

| seal | code frozen (tag) | bets stored (commit) | first game (folder on disk) | first game started |
|---|---|---|---|---|
| 5 | `af7605a5` 2026-11-07 00:02:46 | `648475e6` 2026-11-07 00:13:31 | `valle_experimento_v2/tonto_abundancia_s30001_d40` | 2026-11-07 00:14:00, 30 s after the bets |
| 6 | `34bf8e78` 2026-11-09 23:06:40 | `61276d6b` 2026-11-10 00:04:26 | `valle_experimento_v3/tonto_abundancia_s30041_d40` | 2026-11-10 00:04:48, 23 s after the bets |

For seal 6, the code was frozen on 9 November 2026 at 23:06 and the bets were stored 58 minutes later, before playing.
