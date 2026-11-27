# Paper eight: G-EMV: Emotion and Reason in an Agent. A Body That Lives in the Present: A Creature, Its Sister and a Valley

Eighth work in a line of research that began with the engine; it follows directly from the previous one ([`../paper7`](../paper7)). This one presents an artificial creature that lives in the present, in a valley where it has to survive and live together with seven others, and asks what life it makes on its own.

**Status:** preprint, version 1, November 2026. DOI [10.5281/zenodo.24579960](https://doi.org/10.5281/zenodo.24579960). The English version is the one deposited on Zenodo; the Spanish version is in this folder.

## Author

- Manel Enrico, Independent Researcher, Barcelona. ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)

## What is here

- `GEMV_paper8_EN.pdf`: the English version of the paper.
- `GEMV_paper8_ES.pdf`: the Spanish version, laid out like the English one.
- `paper8_EN.md`, `paper8_ES.md`: the markdown sources of the two versions (with the image paths pointing to `fig/`; see «Declared redactions»).
- `fig/`: the final figures, in English (`_en`) and in Spanish (`_es`), PNG and PDF.
- `code/`: the code, at its repository paths. `code/CHECKSUMS_code.md` gives the md5 of every file, in its source and in this copy.
  - **The engine**, `code/motor/model.py`, md5 `1e511978c251130e95169ebf8443efa1`: the same file as in papers one to seven, copied, not modified.
  - **The valley** (the world): `code/valle/mundo.py` with its configuration `code/valle/config_valle.json`. The simpleton and the gatherer, the two players of simple rules, are in `code/valle/jugadores.py`.
  - **The creature**: `code/cantera/paper8/cuerpo_valle.py` (the body: what it feels, what it imagines and how it decides), with its configuration `config_cuerpo_valle.json`, the culture it is born with (`cultura_*.json`, `banco_v6.json`) and the switches of each version (`banco_v7.py`, `VARS`). The pieces it inherits from earlier papers are at their paths: `code/paintball/alma/`, `code/planificador/`, `code/cantera/paper5/curiosidad.py`, `code/cantera/paper6/parte2.py` and `code/cantera/paper7/`. `cantera/paper7/cuaderno_P7.py` is a later revision of the file published with paper seven; the md5 of the version used here is in the checksums.
  - **The launchers** of sealed experiments 8, 9 and 10, their evaluators and the measures they import, and the programs of the figures with the file of labels in both languages (`rotulos_figuras.csv`).
- `seals/`: the ten sealed experiments, one folder each, with the file of bets as it was sealed and the register of the frozen code of that seal where there was one. `seals/SEALS.md` gives the tag, commit, date and md5 of each file, and when the first game of seals 5 and 6 started.
- `reports/`: the internal reports the appendix and the seals rest on (see below).
- `tables/`: the full tables of the appendix (see `tables/README.md`).
- `data/paper8/`: the summarised data, at paths relative to `cantera/paper8/`: the evaluation of each sealed experiment, the numbers drawn in each figure (`figuras/fig*.txt`), the summaries some figures read, and the one line of a game that figure 1 reads (`figura1_turno0/`).
- `games/`: the manifest of the complete games (`games/GAMES.md` and `games/games_manifest.csv`): folder, game, file, size and md5 of every file of every sealed game.

## Names in the code and in the paper

The code, the folders of the games and the reports use working names. The players of the paper are:

| in the paper | in the code and the reports | class and switches |
|---|---|---|
| the complete creature (decides with the engine) | `RG69rvoz` (RG69r+voz) | `cuerpo_vr1.RG69V`, `VARS["RG68r"]` + reserve + voice |
| the earlier creature with the reserve | `RG69r` | `cuerpo_rg69.RG69`, `VARS["RG68r"]` + reserve |
| the earlier creature | `RG68r` | `cuerpo_valle.Criatura`, `VARS["RG68r"]` |
| the twin | `RG068r` | `cuerpo_valle.Criatura`, `VARS["RG068r"]` |
| decides by adding | `S69voz` (S69+voz) | `cuerpo_vr1.RG69V`, `VARS["S68"]` + reserve + voice |
| decides with the position | `P69voz` (P69+voz) | `cuerpo_vr1.RG69V`, `VARS["P68"]` + reserve + voice |
| the simpleton | `tonto` | `valle/jugadores.Tonto` |
| the gatherer | `recolector` | `valle/jugadores.Recolector` |

The sealed experiments are numbered 1 to 10 in the paper; in the code, the reports and the git tags they are called `v1`, `confirmacion`, `dilemas`, `mesa`, `v2`, `v3`, `v4`, `v5`, `v6` and `escalera` (`seals/SEALS.md`). A «taller» is a test game, and a «puerta» is the check, before a seal, that the frozen code plays exactly as before.

## The reports

`reports/` holds, unchanged and in Spanish, the report of each sealed experiment and every report the table of the appendix cites, at the paths the table uses (`salida/…` for program outputs; `paper9/informe_C1.md` for the one report of later work that the table cites, `../paper9/informe_C1.md` in the table). `reports/informe_prompt_169.md` holds, in its parts 3 to 10, the full tables with where each thing is in the code. **These are working reports:** they name the prompts they answered and use working names, and they may cite working files that are not published.

## What is not here

The complete games, because of their size (85,080 files, 38.2 GB). They are available from the author on request; their md5, one by one, is in `games/`.

The code to launch and evaluate sealed experiments 1 to 7 is not here. They were played with earlier versions of the same creature (other switches of the same `cuerpo_valle.py`) and cannot be remade from this folder; their bets, frozen-code registers, evaluations and reports are here.

## Requirements

Python 3.12 with `numpy==2.4.0`, `matplotlib==3.10.8`, `gymnasium==1.2.3` and `pettingzoo==1.27.0`.

## How to play a game

From `code/cantera/paper8/`:

```
python3 -c "import lanza_experimento_v6 as X; print(X.una(('RG69rvoz', 'normal+sabores', 30161, 40, '/tmp/valle_test')))"
```

The tuple is (player, world, seed, days, folder). The creatures play in the worlds with flavours (`abundancia`, `normal`, `sequia`, `sequia_dura` or `bestias_crian`, followed by `+sabores`); the simpleton and the gatherer play in the plain worlds. The game is written to `folder/<player>_<world>_s<seed>_d<days>/`. For the players that decide by adding or with the position, import `lanza_escalera_v6` instead and call its `una` the same way. The games of the paper last 40 days, with seeds 30161 to 30200. The sweet-fruit tree is drawn over the whole length of the game, so a shorter game does not reproduce the first days of a 40-day one.

This was checked from a copy of this folder: the complete creature, normal world, seed 30161, 40 days, comes out line by line equal to the game of sealed experiment 9 (the 14 files of the game compared; md5 of `mundo.jsonl.gz` uncompressed, `b42068408cd3162a4786a38249bb7482`).

## How to remake a figure from the summarised data

Copy `data/paper8/` into `code/cantera/paper8/` and, from there:

```
python3 figura5_tres_maneras_171.py --idioma en
python3 rehace_figura1.py --idioma en
```

Each figure is written to `figuras_171/` and is byte for byte the one in `fig/`. Figure 5 reads only summarised data. Figure 1 reads one line of one game, turn 0 of the complete creature in the drought, seed 30182, which is in `data/paper8/figura1_turno0/`; `rehace_figura1.py` points the figure's unchanged program to it. Figures 2 to 4 are computed from the complete games, which are not here; the numbers each one draws are in `data/paper8/figuras/`. `--idioma es` gives the Spanish ones.

## Declared redactions

Some copies differ from the originals by a declared redaction, and nothing else:

- `code/`, `seals/`, `data/`, `tables/`, `games/`, `fig/` and the PDFs: none.
- `reports/`: 2 files, one line each; the number of lines does not change.
  - `reports/informe_experimento_v5.md`, line 22: a path in the author's home folder replaced by `[ruta local]` (md5 of the source `0a6134ea55cd59fca21dfb10e5bbcb19`, of the copy `c43232c653e50f6344d21d220b6ac40b`).
  - `reports/informe_prompt_169.md`, line 5: a path in the author's home folder replaced by `[carpeta local]` (md5 of the source `301e0f44b590b13ab0cbab1ab66d5a8a`, of the copy `acf1e466aecb5f7fb4c342408ce0d3e5`).
- `paper8_EN.md`, `paper8_ES.md`: the six image paths point to `fig/` with the language suffix (`![](fig/fig2_vivas_en.png)` instead of `![](fig2_vivas.png)`); nothing else changes.

## Abstract

This work presents an artificial creature that lives in the present, and asks what kind of life it leads on its own. It feels what it loses and what it gains in three dimensions at once, the body, resources and its bonds with the others, and it seeks its equilibrium in all three: it imagines a short while ahead and decides no further than that. There is no reward and no training. It has no reasoning part and almost no curiosity. We put it with seven others in a small world where they have to survive and live together, because they can die there. That world is a valley made for the creature, the same for every player.

What can be felt in the moment comes to it without anyone telling it: it gathers with the others in the face of danger, kills none of them, looks after its sister and the hungry, and goes home to sleep. In hard worlds it outlives a player that follows simple rules. When it loses its sister it becomes restless, calls and seeks out its neighbors. We wrote the grief ourselves, and that company relieves it; the restlessness and the calls we did not.

What requires looking far ahead it does not manage: it does not store for later or go for what is far away. The valley is played in 5 variants, which we call worlds. In the hardest one, where food runs short twice for 5 days in a row, about 4 of the 8 reach the end alive: they starve even though the valley gave more than enough earlier. Two senseless habits it had were fixed by changing what it can see, not a number. Once fixed it lives better, but in that world it does not live longer, and there one of our bets failed.

Finally we compare three creatures that feel the same and differ only in how they combine what they feel to decide: by adding it up, by how far each dimension is from its target, or with the engine. They get almost equally far. The engine creature pushes less and lives a little longer than the one that adds. If being well means that nothing is going badly in any of the three dimensions, its village is well more of the time. If it means the sum of the three, where one good thing covers a bad one, the two cannot be told apart. We do not see that it obtains more: it spreads it better.

Everything was measured in one valley, with 114 bets written before playing, of which 90 proved right. The valley is published whole; later works rest on it and this creature.

## How to cite

Enrico, M. (2026). G-EMV: Emotion and Reason in an Agent. A Body That Lives in the Present: A Creature, Its Sister and a Valley. Zenodo. https://doi.org/10.5281/zenodo.24579960

## The series

1. Enrico, M. (2026). G-EMV: A Geometric Architecture of Homeostatic Orientation for Agents. https://doi.org/10.5281/zenodo.21026795
2. Enrico, M. (2026). G-EMV: the Hive. Instinct Suffices: a Whole Life Without Reward. https://doi.org/10.5281/zenodo.21994358
3. Enrico, M. (2026). G-EMV: the Pack. Care Without Reward in a World That Pays for Killing. https://doi.org/10.5281/zenodo.22713650
4. Enrico, M. (2026). G-EMV: Emotion and Reason in an Agent. When Thinking Is Needed. https://doi.org/10.5281/zenodo.22844274 ([`../paper4`](../paper4))
5. Enrico, M. (2026). G-EMV: Emotion and Reason in an Agent. Curiosity, Trust and Commitment. https://doi.org/10.5281/zenodo.23035785 ([`../paper5`](../paper5))
6. Enrico, M., and Sklar, A. (2026). G-EMV: Emotion and Reason in an Agent. Helping Without Commanding. https://doi.org/10.5281/zenodo.23168539 ([`../paper6`](../paper6))
7. Enrico, M., and Sklar, A. (2026). G-EMV: Emotion and Reason in an Agent. Learning by Living: A Creature, Its Sister and a Reason That Lies. https://doi.org/10.5281/zenodo.23674082 ([`../paper7`](../paper7))
8. This work.

## License

Code: MIT License (see LICENSE at the repository root). Paper: CC BY 4.0, as deposited on Zenodo.

## Contact

Manel Enrico — manelenrico@gmail.com — ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)
