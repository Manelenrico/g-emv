# Paper five: G-EMV: Emotion and Reason in an Agent. Curiosity, Trust and Commitment

Second part of the series on emotion and reason in an agent. The first part ([`../paper4`](../paper4)) placed a head that talks beside a body that feels; this one gives the world time and builds three pieces beside the body: a wide door, trust and curiosity. Before that series there was a trilogy: the engine, the hive, the pack.

**Published version (English):** Zenodo, DOI [10.5281/zenodo.23035785](https://doi.org/10.5281/zenodo.23035785). Concept DOI (all versions): [10.5281/zenodo.23035784](https://doi.org/10.5281/zenodo.23035784). Preprint, version 1, 29 September 2026. CC BY 4.0.

## What is here

- `GEMV_paper5_EN.pdf`: the English version of the paper, the one deposited in Zenodo.
- `GEMV_paper5_ES.pdf`: the Spanish version, laid out like the English one.
- `paper5_EN.md`: markdown source of the English version published in Zenodo.
- `paper5_ES.md`: markdown source of the Spanish version.
- `fig/`: the five figures, in English and in Spanish (`fig1` to `fig5`, with `_en` and `_es` suffixes).
- `code/`: the code that played and measured the paper, exactly the files listed in `code/CONGELADO.md`, in their repository paths: the engine (`motor/model.py`, md5 `1e511978c251130e95169ebf8443efa1`, unchanged since paper one), the planner (`planificador/`), the body (`paintball/alma/`), the pieces of this paper (`cantera/paper5/`: the shape of a plan, the advisor, curiosity, trust), the world presets and the bench, measurement, launch and figure scripts. `code/CHECKSUMS_code.md` gives the md5 of each file in the frozen list and in this copy (199 files; three carry a declared redaction, see below).
- `reports/paper5/`: the 66 reports of this paper (`informe_P5*.md`, in Spanish); every number in the appendix names the report it comes from. `reports/paper6/`: the 3 reports of the next work that the paper cites (P6-6, P6-8, P6-22: two inherited defects of the body and the steps the game did not execute).
- `data/`: the 133 JSON files those reports were written from (measures, requests, per-game summaries), those under 10 MiB; `data/paper5/` (and `t1_descartada/`, the discarded first batch of the advisor series), `data/paper4/` (the seed list), `data/paper6/` (the data of the three cited reports).
- `diaries/`: the manifest of the recorded games, `DIARIOS_MANIFIESTO.md` (name, size and md5 of each diary, by series) and the same table as `diaries_manifest.csv`.

## What is not here

The diaries themselves, the recorded games (1766 files, 12.01 GiB: one `.art.log` per agent per game and the artifacts the platform returned), are not in the repository because of their size. Their md5, one by one, is in `diaries/`, so anyone who holds them can verify they are the same. **They are available from the author on request.**

Three files in `code/` and six in `reports/` and `data/` differ from the frozen originals by a declared redaction, and nothing else: a third party's e-mail address in the `owner` field of the world manifest, the e-mail address and user id of the platform account that requested the games, and personal file-system paths were removed. `code/CHECKSUMS_code.md` shows the md5 of the source and of the copy for every code file. The scripts that launched games (`lanza_*.py`, `baja_*.py`, `vigila_*.py`) need the platform's client and credentials, which are not included.

## Abstract

This work observes and tests an artificial creature made of two parts. A body that feels what it lacks in three dimensions, its body, its resources and its bonds: what that body feels is what we call emotion here. And beside it a head that talks, a language model that advises it: that is reason. The question is when thinking is of use to a body like this.

To answer it we give the world time, with games twice as long, and we build three pieces. The first is a wide door: the advisor no longer proposes a step, but a whole plan with its emotional shape, what the body will feel on each leg of the way, and the body judges it with its own table. This door tells good advice from random advice, something the earlier one did not do; but, so as not to fool itself, it can only judge the small part of the good that the body is able to foresee. The second is trust, which is earned and lost with results: in the tests, an advisor that talks at random soon loses trust and stops moving the body with good news. The third is curiosity, installed as one more need of the body. As a nudge at each step it did not work. As a trip with a destination and commitment it did: while it travels, the body discovers almost six times more world per instant than when it is not traveling, without getting closer to danger; since it travels little, over the whole game it sees 16% more of the map than the body alone (31% on the stretches where no step was lost; section 10).

In a hundred games, the advisor's plans gave the body no advantage at all. Almost all the improvement in the creature's future goes through the others, and what they will do the body cannot foresee. What the work leaves is the division of roles that makes reason useful: the body says what it needs and, therefore, what is worth knowing; reason can say where to find it; and the body checks it, commits to the plan and only lets go of it if something important happens.

Everything was measured in a single world, private and with chosen neighbors, and without the creature learning from one game to the next.

## How to cite

Enrico, M. (2026). G-EMV: Emotion and Reason in an Agent. Curiosity, Trust and Commitment. Zenodo. https://doi.org/10.5281/zenodo.23035785

## The series

1. Enrico, M. (2026). G-EMV: A Geometric Architecture of Homeostatic Orientation for Agents. https://doi.org/10.5281/zenodo.21026795
2. Enrico, M. (2026). G-EMV: the Hive. Instinct Suffices: a Whole Life Without Reward. https://doi.org/10.5281/zenodo.21994358
3. Enrico, M. (2026). G-EMV: the Pack. Care Without Reward in a World That Pays for Killing. https://doi.org/10.5281/zenodo.22713650
4. Enrico, M. (2026). G-EMV: Emotion and Reason in an Agent. When Thinking Is Needed. https://doi.org/10.5281/zenodo.22844274
5. This work.

## Contact

Manel Enrico — manelenrico@gmail.com — ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)
