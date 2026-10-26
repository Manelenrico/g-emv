# Paper seven: G-EMV: Emotion and Reason in an Agent. Learning by Living: A Creature, Its Sister and a Reason That Lies

Fourth part of the series on emotion and reason in an agent. The first part ([`../paper4`](../paper4)) placed a head that talks beside a body that feels; the second ([`../paper5`](../paper5)) gave the world time and built a wide door, trust and curiosity; the third ([`../paper6`](../paper6)) asked whether reason can help a pair of creatures without commanding them. This one asks whether a creature that is born without knowing what the things of its world do can find out by living, guided by what it feels, with a sister that tells it what she has lived and a reason that can lie. Before that series there was a trilogy: the engine, the hive, the pack.

**Status:** preprint, version 1, 2026. DOI pending.

## Authors

- Manel Enrico, Independent Researcher, Barcelona. ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)
- Ari Sklar, Independent Researcher, Los Angeles. ORCID [0009-0000-8005-4524](https://orcid.org/0009-0000-8005-4524)

## What is here

- `GEMV_paper7_EN.pdf`: the English version of the paper.
- `GEMV_paper7_ES.pdf`: the Spanish version, laid out like the English one.
- `paper7_EN.md`: markdown source of the English version.
- `paper7_ES.md`: markdown source of the Spanish version.
- `fig/`: the figures, in English and in Spanish (`fig2_1`, `fig_llegadas` and `fig_confianza`, with `_en` and `_es` suffixes; `fig5_1_miente.png` and `fig5_1_honesta.png`, the two frames of figure 5.3, have no text and are the same in both languages).
- `code/`: the code, in its repository paths. First, the frozen code of paper seven, the 118 files that `code/CONGELADO_P7.md` lists with path, md5 and why each one is there: the 58 files the image of the final field loads (the engine, `motor/model.py`, md5 `1e511978c251130e95169ebf8443efa1`, unchanged since paper one; the planner; the body, `paintball/alma/`; the pieces inherited from papers five and six; and the pieces of this paper: the emotional memory, curiosity, the different way of perceiving threat, what the sisters tell each other, the night reason, the trust in it, the lie and the frozen trust), 47 files the image copies and does not load (the pieces and entry points of the earlier fields, the smoke tests that run when the image is built, the still rival), and the 13 recipes of the images of the fields this paper reports. At its end, `CONGELADO_P7.md` compares every md5 that a seal names with the file today. Second, the measurement and analysis code, which is not frozen (262 files): the analysis, bench, power, local-world and report programs of paper seven, the program that draws the figures (`cantera/paper7/figuras/hace_figuras_P7.py`) and what those programs import. `code/CHECKSUMS_code.md` gives the md5 of every file, in its source and here.
- `reports/`: the 73 reports of this paper (`informe_P7_0.md` to `informe_P7_67_campo.md`, in Spanish, one per experiment or bench, with the world's data in `informe_P7_mundo.md`), the report of the figures (`informe_P7_figuras.md`) and the external review (`informe_P7_revision_externa.md`), with the scripts that recompute each of its numbers and their outputs (`revision_externa/`). Every number in the appendix names the report it comes from.
- `seals/`: the seals (22 `SELLO_P7_*.md`), each written before the field or bench it seals was played, with their amendments written in the same file (P7-67 has four); the register of the final field (`REGISTRO_P7_67.md`); the results of the seal checks (`P7_*_sello.json`, `P7_*_sello_resultado.json`) and the seeds of the fields (`semillas_P7_*.json`).
- `data/`: the 248 JSON files the reports, the seals and the paper name (measures, power calculations, per-game and per-creature summaries, bench results), those under 10 MiB: `data/paper7/` (245; and `data/paper7/figuras/`, 1, the values behind the figures), `data/paper5/` (1), `data/paper6/` (1).
- `diaries/`: the manifest of the recorded games and of the creatures' notebooks, `DIARIOS_P7_MANIFIESTO.md` (folder, name, size, md5 and where each file is kept) and the same table as `diaries_manifest.csv`.

## What is not here

The diaries themselves, the recorded games (30702 files in the manifest, 96.98 GiB: 2590 diaries, one `.art.log` per creature per game, 5649 artifacts the platform returned, 5603 notebooks, one per creature per day, which carry its memory from one day to the next, 2732 answers of the platform to the game requests, and 14128 other files), are not in the repository because of their size. Their md5, one by one, is in `diaries/`, so anyone who holds them can verify they are the same. **They are available from the authors on request.**

4 JSON files that the reports name are over 10 MiB and are not included: `P7_18_escenas.json` (18.1 MiB), `P7_37_momentos.json` (28.4 MiB), `P7_40_cadena.json` (30.9 MiB), `P7_40_momentos.json` (14.2 MiB); their md5 is in the manifest.

`code/` holds the frozen code and the measurement code, and not everything the reports name. Left out, and why:

- The launchers and what drives them (24 `lanza_*.py`, 7 `orquesta_*.py`, 5 `reintenta_*.py`): they only work with the platform's client and the credentials of the account, which are not included. The recipes of the images and the seeds are in `code/` and `seals/`.
- Credentials of any kind: no `.env` file, no key, no token. Some programs (the night reason) read a key from the environment or from a local `.env` file; the file is not here.
- Any `model.py` other than the published one: there is only `code/motor/model.py`, md5 `1e511978c251130e95169ebf8443efa1`.
- Housekeeping and display programs the reports name: copies to the external disk and clean-ups (11), smoke tests (3), GIF makers (6), and the piece that removes e-mail addresses from the platform's answers before they are saved. The reports describe them.

## Declared redactions

Some copies differ from the originals by a declared redaction, and nothing else:

- `code/`: none. `code/CHECKSUMS_code.md` shows the md5 of the source and of the copy for every code file.
- `data/`: 3 files (e-mail addresses emptied; the user id of the platform account emptied).
- `reports/`: none.
- `seals/`: none.
- `diaries/`: none.
- `paper7_EN.md`, `paper7_ES.md`, the PDFs and `fig/`: none; the sources are the texts of the paper byte for byte.

## Abstract

This work asks whether an artificial creature that is born without knowing what the things in its world do can find out by living, guided by what it feels. The creature is a body that seeks its own balance between needs that pull in opposite directions, with no reward and no training. Now it remembers from one day to the next, and each memory keeps what happened, in what situation, how it felt and what it was doing.

Alone, it discovers what acts quickly and can be seen, like a medkit, and we did not see it fall behind the creature that is born knowing. It struggles with what heals little, and it does not see what acts by its absence. We compared its curiosity with a coin that chose at random what to try, placed in the same body, and we found no difference; our reading is that, in a world with danger, when to try weighs more than what to try, and that is decided by the body, which was the same in both. With a sister who tells it what she has lived, the two end up believing the same things, the one who has lived less herself learns more from her sister, and we did not see anything false spread. With a reason, a language model that reads the diary of its day each night and makes it proposals, the creature does not obey: the proposal adds a little attraction to something the body already knows how to do, and trust in the reason is earned by comparing what was promised with what was lived, separately in each dimension: one trust for what the reason says about the body, another for resources and another for the bond. That trust ends up high after the proposals that were true and low after the false ones, even though the body does not know which are which: it only judges what it lives. We also tested lies that we ourselves put into the proposals on purpose. Faced with one that led it to an empty place, the creature stopped following it as its trust fell; with its trust frozen, it kept going until the last day. Counted as we sealed it, the effect is clear; counted in the strictest way, it keeps its direction but sits at the limit. A lie the body does not follow all the way to the end is never uncovered.

Everything was measured in a single game world, with the predictions written down before playing.

## How to cite

Enrico, M., and Sklar, A. (2026). G-EMV: Emotion and Reason in an Agent. Learning by Living: A Creature, Its Sister and a Reason That Lies. Preprint, version 1. DOI pending.

## The series

1. Enrico, M. (2026). G-EMV: A Geometric Architecture of Homeostatic Orientation for Agents. https://doi.org/10.5281/zenodo.21026795
2. Enrico, M. (2026). G-EMV: the Hive. Instinct Suffices: a Whole Life Without Reward. https://doi.org/10.5281/zenodo.21994358
3. Enrico, M. (2026). G-EMV: the Pack. Care Without Reward in a World That Pays for Killing. https://doi.org/10.5281/zenodo.22713650
4. Enrico, M. (2026). G-EMV: Emotion and Reason in an Agent. When Thinking Is Needed. https://doi.org/10.5281/zenodo.22844274 ([`../paper4`](../paper4))
5. Enrico, M. (2026). G-EMV: Emotion and Reason in an Agent. Curiosity, Trust and Commitment. https://doi.org/10.5281/zenodo.23035785 ([`../paper5`](../paper5))
6. Enrico, M., and Sklar, A. (2026). G-EMV: Emotion and Reason in an Agent. Helping Without Commanding. https://doi.org/10.5281/zenodo.23168539 ([`../paper6`](../paper6))
7. This work.

## License

Code: MIT License (see LICENSE at the repository root). Paper: CC BY 4.0, as deposited on Zenodo.

## Contact

Manel Enrico — manelenrico@gmail.com — ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)

Ari Sklar — ORCID [0009-0000-8005-4524](https://orcid.org/0009-0000-8005-4524)
