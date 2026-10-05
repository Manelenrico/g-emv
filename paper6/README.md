# Paper six: G-EMV: Emotion and Reason in an Agent. Helping Without Commanding

Third part of the series on emotion and reason in an agent. The first part ([`../paper4`](../paper4)) placed a head that talks beside a body that feels; the second ([`../paper5`](../paper5)) gave the world time and built a wide door, trust and curiosity. This one asks whether reason can help a pair of creatures without commanding them. Before that series there was a trilogy: the engine, the hive, the pack.

**Status:** preprint, version 1, 2026. DOI pending.

## Authors

- Manel Enrico, Independent Researcher, Barcelona. ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)
- Ari Sklar, Independent Researcher, Los Angeles. ORCID [0009-0000-8005-4524](https://orcid.org/0009-0000-8005-4524). This work was done while the author was a contractor at Softmax.

## What is here

- `GEMV_paper6_EN.pdf`: the English version of the paper.
- `GEMV_paper6_ES.pdf`: the Spanish version, laid out like the English one.
- `paper6_EN.md`: markdown source of the English version.
- `paper6_ES.md`: markdown source of the Spanish version.
- `fig/`: the five figures, in English and in Spanish (`fig1` to `fig5`, with `_en` and `_es` suffixes).
- `code/`: the frozen code of paper six, exactly the files that `code/CONGELADO_P6.md` lists with path and md5, in their repository paths: the 32 files of the body of the pair (arm A4, frozen in P6-12): the engine (`motor/model.py`, md5 `1e511978c251130e95169ebf8443efa1`, unchanged since paper one), the planner (`planificador/`), the body (`paintball/alma/`), the pieces inherited from paper five (`cantera/paper5/`) and the pieces of this paper (`cantera/paper6/`: the report between siblings and its listener, the feeling of distance, the empty-handed threat, the fixes); and the 2 files of the image and the world (`Dockerfile.pareja11`, `roster_lento_v2_PROPUESTA.json`). `code/CHECKSUMS_code.md` gives the md5 of each file in the frozen list and in this copy (34 files; 0 with a redaction).
- `reports/`: the 31 reports of this paper (`informe_P6_0.md` to `informe_P6_30.md`, in Spanish), one per experiment; every number in the appendix names the report it comes from. Also the two checks of the appendix against its sources (`P6_FIN1_comprobacion.md`, `P6_FIN2_respuestas.md`).
- `data/`: the 411 JSON files those reports were written from (measures, requests, per-game summaries, bench results), those under 10 MiB: `data/paper6/` (375; and `data/paper6/P6_30/`, 27, the working folder of the last report), `data/paper5/` (6) and `data/paper4/` (3), the last two being files of the earlier papers that these reports use.
- `diaries/`: the manifest of the recorded games, `DIARIOS_P6_MANIFIESTO.md` (series, name, size and md5 of each file) and the same table as `diaries_manifest.csv`.

## What is not here

The diaries themselves, the recorded games (1346 files in the manifest, 22.05 GiB: 664 diaries, one `.art.log` per creature per game, plus the artifacts the platform returned, the raw outputs of the reasoner and a few other large files), are not in the repository because of their size. Their md5, one by one, is in `diaries/`, so anyone who holds them can verify they are the same. **They are available from the authors on request.**

3 JSON files that the reports name are over 10 MiB and are not included: `P6_14_planes.json` (22.2 MiB), `P6_15_planes.json` (35.7 MiB), `P6_2_bruto.json` (38.2 MiB).

`code/` is the frozen list and nothing else. The pieces built on top of the frozen body for the later arms of the paper (A5 to A8: the rule-based advisor, the door, the commitment, the reasoner) and the measurement, bench and launch scripts are not in `CONGELADO_P6.md` and are not in this folder; the reports describe them. No launcher is included: playing a game needs the platform's client and credentials, which are not here either.

## Declared redactions

Some copies differ from the originals by a declared redaction, and nothing else:

- `code/`: none. `code/CHECKSUMS_code.md` shows the md5 of the source and of the copy for every code file.
- `data/`: in 193 files (the answers of the platform to the game requests) the e-mail address and the user id of the platform account that requested the games were emptied; in 20 files personal file-system paths (the repository root and session scratch folders) were replaced by `<repo>`, `<scratch>` or `<home>`; in 1 file (the manifest of the world, from paper five) the `owner` field, a third party's e-mail address, was emptied.
- `reports/`: in `informe_P6_1.md` the e-mail addresses of third parties were removed.
- `diaries/`: no redaction.

## Abstract (short)

This work asks whether reason can help a pair of artificial creatures without commanding them. Each creature is a body that seeks its own balance among needs that pull in opposite directions, with no reward to chase and no training; each one has its own reasoner, which proposes plans, and the body judges them and decides.

When the siblings start telling each other what they see, they drift apart, because the voice takes the place of closeness; a feeling that hurts when the sibling is too far away gives the pair back its shape. In the fire at the end of the game, a rule-based advisor that answers instantly, an honest imagination of oneself, a plan to go and stay and a proportionate way of letting it go make the pair spend less time burning, a result replicated over 40 seeds. A language model has its proposals accepted as often as the rule-based advisor, but it arrives late: in the field we detected neither an improvement nor a worsening. We also measured the cost of obeying: the plan holds the body back a great deal, no plan is dropped because of what has been endured, and once it ends the body goes back to deciding as before.

The lesson is that the unpredictable lies in the others, and that our way of foreseeing them is not enough; learning from experience is the next step. Everything was measured in a single world, private and with chosen rivals.

## How to cite

Enrico, M., and Sklar, A. (2026). G-EMV: Emotion and Reason in an Agent. Helping Without Commanding. Preprint, version 1. DOI pending.

## The series

1. Enrico, M. (2026). G-EMV: A Geometric Architecture of Homeostatic Orientation for Agents. https://doi.org/10.5281/zenodo.21026795
2. Enrico, M. (2026). G-EMV: the Hive. Instinct Suffices: a Whole Life Without Reward. https://doi.org/10.5281/zenodo.21994358
3. Enrico, M. (2026). G-EMV: the Pack. Care Without Reward in a World That Pays for Killing. https://doi.org/10.5281/zenodo.22713650
4. Enrico, M. (2026). G-EMV: Emotion and Reason in an Agent. When Thinking Is Needed. https://doi.org/10.5281/zenodo.22844274 ([`../paper4`](../paper4))
5. Enrico, M. (2026). G-EMV: Emotion and Reason in an Agent. Curiosity, Trust and Commitment. https://doi.org/10.5281/zenodo.23035785 ([`../paper5`](../paper5))
6. This work.

## License

Code: MIT License (see LICENSE at the repository root). Paper: CC BY 4.0, as deposited on Zenodo.

## Contact

Manel Enrico — manelenrico@gmail.com — ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)

Ari Sklar — ORCID [0009-0000-8005-4524](https://orcid.org/0009-0000-8005-4524)
