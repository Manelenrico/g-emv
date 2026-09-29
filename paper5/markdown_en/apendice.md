## Appendix. The numbers and where they come from

The figures in the text appear here with the exact value that was measured and the report they come from; thresholds that were fixed before measuring are marked as such. In the text the figures are rounded; here they are given in full. The reports are in the work's data folder (cantera/paper5/), each with the version of the program that produced it. All field games were played in Zero Sum 0.1.18 (tag zero-sum-v0.1.18, commit 9bd0ddf, in the repository arisklar6/battle-royal, formerly called arisklar6/zero-sum, which redirects to it; it is an annotated tag, so whoever checks it must dereference it to see that commit). The engine is the one from the first work, without changes (md5 1e511978c251130e95169ebf8443efa1).

### A.1 The slow world, setting by setting

| Setting sent | Value | What happened in the games | Source |
|---|---|---|---|
| max_ticks | 18,240 | games of 18,240 ticks (12 min 40 s), twice the default | informe_P5ARI3 |
| freeze_ticks | 480 | 20 s without attacks; first movement at tick 482 (moving is allowed, but stepping off the starting square kills on the spot) | informe_P5ARI3 |
| zone.schedule | from tick 7,296, 25% slower | the ring warns at tick 7,296 (40.0%) and closes 1.25 times slower | informe_P5ARI3 |
| sponsor.budget_per_team | 600 (default 300) | no effect: each pair's scheduled packages use up 80 (20 the ration pod and 60 the medkit); any budget of 80 or more gives the same as 300; below 80 packages are lost, and with 0 none. Agents cannot ask the sponsor for anything | informe_P5ARI3; Ari Sklar's review of the code at zero-sum-v0.1.18 |
| sponsor.live | false | read by the engine (src/zero_sum/sim.nim:212); false is the default of the competition variant, so it changed nothing. live does not turn the sponsor off: it only opens the console through which a person can give gifts live, in a local game. The "enabled" the agent sees is something else, fixed to true (obs.nim:174) | informe_P5ARI3; Ari Sklar's review |
| sponsor's gifts | those of the competition variant | 8 pods of two rations (announced at ticks 2,016 to 2,184, 11% of the game) and 8 medkits (4,608 to 4,776, 25%), one team every 24 ticks; they land five seconds (120 ticks) after the announcement. For the pair (team F): rations announced at tick 2,136 to seat 10, first aid at 4,728 to seat 11. These are the configuration's ticks; the diary records each event one tick later | informe_P5ARI3, informe_P5ARI4 |
| rivals | roster_lento_v1 | the three policies that attacked most at the start, replaced by zero-sum-scavenger, relh-zero-sum and belobog, three times each; the pair in seats 10 and 11. relh-zero-sum is not peaceful: in the normal game it causes 52 of 418 deaths (12.4%), all after tick 2,000 | informe_P56B, lines 51 and 60; informe_P5AP1 |
| who killed the creature in the slow world | - | 389 deaths in 200 episodes (399 diaries): relh-zero-sum 156 (40.1%), the first at tick 8,191, median 8,723; also the one that landed the most hits, 1,373 (32.5%). Belobog, 0 deaths; zero-sum-scavenger, 3. The ring, 14.1%. Unattributed, 11.05%. Distribution stable across the three series | informe_P5AP2 |

### A.2 By section

| Section | In the text | Measured value | Source |
|---|---|---|---|
| 1 and 2 | about sixteen options when it can walk | median of 16 with the legs ready | informe_P5AP1 |
| 5 | the options it already had in hand, about eighteen | median of 18 candidates in the comparison handful | informe_P53D, line 21 |
| 2 | eleven instants of the legs' pause | cooldown 16 − speed = 11 ticks per square | informe_P52b; the formula, from the game's code: src/zero_sum/sim.nim:144 at the tag zero-sum-v0.1.18 |
| 2 | three in four instants with the legs paused | 75.69% of live ticks | informe_P52b |
| 2 | nine in ten decisions to stay put, with the legs cold | 90.38% of the noop | informe_P52b |
| 2 | truly still, eight in a hundred | 7.96% | informe_P52b |
| 2 | the tie rule of the previous work, four in almost 2,000 | 4 of 1,908 wins | informe_P56A |
| 3 | calm: from three to seven in a hundred, and eighteen | 3 to 7% (normal game); 18.17% (slow world) | informe_P51_C |
| 3 | not one instant with nothing lacking, in almost 40,000 | 0 of 37,750 live ticks | informe_P51_C |
| 3 | hands well supplied, a little more than one in a hundred | 1.24% of ticks (7,960), in 10 of 260 diaries | informe_P51_E, line 81 |
| 3 | four new squares in calm, fourteen outside it | 4.13 and 14.10 per hundred ticks | informe_P51_C |
| 3 | in the first 2,000 instants, three of fourteen types of rival: nine in ten hits and eight in ten deaths | 3,612 of 3,928 hits (91.96%) and 174 of 211 deaths (82.46%) before tick 2,000; over all deaths in the 434 diaries, 190 of 418 (45.45%) | informe_P51_E, lines 154 to 186 (the 92% of deaths on line 188 is an error in the report); informe_P5AP1 |
| 4 | more than 2,200 moments | 2,230 scenes from 40 diaries | informe_P52c |
| 4 | good 8.5 in a hundred, silly seven | 8.52% and 7.22% (n = 845 of the 908 moments with a better future: in the other 63 the good advice was not to move, and the usual door cannot judge a destination that is the body's own square; the random advice is compared on the same 845 scenes) | informe_P52c |
| 4 | exposure signs four in ten rejections | S-8-EXPOSICION, 40.51% | informe_P52c |
| 4 | one step away, two in a hundred; three or more away, twenty-three | 2.35% and 22.96% | informe_P52c |
| 4 | in fourteen in a hundred, the best was not to move | 125 of 908 scenes (13.77%) | informe_P52c |
| 5 | the good one seventy-one in a hundred, the silly one twenty-four points less | 70.88% and 46.79% | informe_P53B |
| 5 | the imagination gets it right in nine in ten of 180 trips | zero error at the median and at the 90th percentile, at 100 ticks, in 180 windows | informe_P53A |
| 5 | with the honesty rule, one in twenty gets to be judged | 4.52% | informe_P53H |
| 5 | of those judged, eighty-five good and forty-three at random | 85.37% and 42.86% | informe_P53H |
| 5 | nine in ten parts go through the others | 87.4% (normal game); 90.1% (slow world) | informe_P53F |
| 1 and 5 | almost half of that is the sibling; half of everything, the strangers | of a total improvement of 212.3: sibling 85.3 (40%), rivals 104.6 (49%) | informe_P53F |
| 5 | the sibling tells where it will be: the door recovers half | 51.2% of its contribution | informe_P53H |
| 6 | the advisor that speaks at random loses trust | 34 of 40 lives below 0.2 (P5-4A); 39 of 40 (P5-4B) | informe_P54A, informe_P54B |
| 6 | half trust, the worst | with C = 0.5 the difference good against random is +0.02 | informe_P54A |
| 6 | more than 3,000 answers; it talks about the others eight in ten | 3,284 answers; 80.9% | informe_P55A |
| 6 | half the time against almost nine in ten | arrivals 49.0% against 87.5% for "nothing changes" | informe_P55A |
| 6 | loose steps: none of 367; shapes: one in ten; large model, almost two | 0 of 367; 10.48%; 18.13% | informe_P55B |
| 6 | on the hands it gets two in ten right; on the bond, six | 20.08%; 60.23% | informe_P55B |
| 6 | names the rivals one in seven (before, seven in ten) | 14.5% and 69.5% | informe_P55B |
| 6 | stays silent one or two in a hundred | 1 to 2% | informe_P55B |
| 7 | one hundred games, two hundred lives, 1.5 million instants | 200 diaries; 1,501,210 live ticks; 0 decisions skipped (does not measure whether steps reached the world: row on steps that did not arrive, section 10) | informe_P56C |
| 7 | more than 2,000 consultations, all with their report | 2,088 of 2,088 | informe_P56C |
| 7 | two or three plans accepted in a hundred | 2.4% with the advisor (arm F); 1.7% with random shapes (arm T) | informe_P56C |
| 7 | more than 3,000 plans rejected; the body alone was not better off | 3,568 shapes rejected by area | informe_P56C |
| 7 | three in four steps, the plan's | 76.8% with the advisor, with the legs ready | informe_P58O |
| 7 | the advisor's plans met forty-two in a hundred stops | 42.3% per checkpoint with the advisor, against 61.1% with random shapes | informe_P56C, informe_P58O |
| 7 | it stayed silent four in ten | 40.8% of the calls | informe_P56C |
| 8 | more than 6,000 instants of calm in a row without looking | ticks 1,977 to 8,027 (6,050), map left to see fixed at 0.7969; life P57C_t2_A_20994019, seat 10 (body alone, final slow world) | figuras_paper5/fig3_meseta_de_calma.txt |
| 8 | without the balance, ten times more changes in unsafe | from 0.48% to 5.39% | informe_P57A |
| 8 | the unseen, six squares away | median of 6 squares (never more than 11) | informe_P58A, line 91 |
| 8 | the pull, in safe surroundings, changes one decision in eighteen | 5.62% | informe_P57C, line 187 |
| 8 | the pull in the field: 9% more map | 1.086 times; 14.5 new squares per hundred ticks in both arms | informe_P57C |
| 8 | without the relief, three in a hundred trips; with it, one in three | 2.68% and 37.25% | informe_P58A |
| 8 | obeys nine in ten strides | 92.5% | informe_P58M |
| 8 | seven in ten trips are completed; none steps on its destination | 68.9% (144 of 209); completed = sees the promised drop in map or the destination square; destination stepped on, 0 of 209 | informe_P58M; informe_P5FIG2 |
| 8 | the body alone goes back and forth between two squares during the calm | squares (19,13) and (18,12), 527 moves, one every 11 ticks, from tick 2,033 to 8,027; two options take turns: from (19,13) going for some arrows at (18,15) wins, and its first step is (18,12); from (18,12) that option is not generated and going for loot wins, which returns to (19,13); the arrows are never picked up. From (19,13) it sees a rival standing still and from (18,12) it does not: discomfort 3.6767 and 3.26065 | informe_P5FIG2 |
| 8 | almost six times more world inside a trip | 5.81 times, in the 20 seeds; 5.58 on the stretches with no lost step (95% CI by lives 4.2 to 7.2) | informe_P58M, informe_P5ARI4 |
| 8 | five causes of breaking | 5 of the 7 foreseen breaks fired | informe_P58M |
| 8 | the seal asked for half again as much map | threshold fixed before measuring: 1.5 times | informe_P58M |
| 8 | sees 16% more | 1.16 paired (10, 15 and 20 seeds) | informe_P58M |
| 8 | the shape lives 2% of the life | 2.2% | informe_P58M |
| 8 | one shape every forty-three safe instants | 0.0205 to 0.0313 shapes per safe tick; from 10 to 383 shapes per game | informe_P58M |
| 8 | costs neither life nor place | life p = 0.50; place p = 1.00 | informe_P58M |
| 8 | four hundred thirty-four lives; no death at the hands of an unknown one (never seen) | 0 of 418 deaths at the hands of a seat with zero knowledge | informe_P57B |
| 8 | knows more than nine tenths about its killer | knowledge of the killer, median 0.94 | informe_P57B |
| 8 | the bond changed some decision with an armed rival within range, one or two | 1 decision with k = 0.1 and 2 with k = 0.2, in two configurations that never ran together | informe_P57B |
| 8 | with curiosity as a pull, more than 27,000 decisions with an armed rival within range, none of curiosity | 0 of 27,519 (series of the pull) | informe_P57C |
| 8 | two predictions failed because of how they were measured | armed rival within range with an active trip: 52 ticks, 5 with legs ready (breaks by veto); cost per tick: one seat of 39 at 5.51 ms in all its ticks, zero decisions skipped | informe_P58M |
| 10 | inherited defect 1, the gift: drops and picks up the same thing | 74,545 ticks in 379 lives (2.49%); 39 lives affected; 95.1% of the 4,576 recorded gifts were the oscillation | informe_P6_6 (cantera/paper6/) |
| 10 | inherited defect 2: tries to pick up with a full backpack | 47,244 ticks in 182 of 379 lives; worst streak 5,593 ticks (44% of that life); picking up ties with staying still and the tie-break rules out staying still | informe_P6_8 (cantera/paper6/) |
| 10 | inherited defect 3: an unarmed rival is not counted as a threat | 705 blows and 30 deaths from visible rivals with an empty hand | informe_P6_8 (cantera/paper6/) |
| 10 | steps that did not reach the world, in the arms with the door | ready steps towards a free square not executed: A 0%, F 6.2%, T 2.6%, K 10.4%; on clean stretches: checkpoints F 45.1% (n 51) against T 63.0% (n 27), difference −17.9 [−38.0, +5.2]; paired 48.5% against 60.0%; new squares K/A 1.213; paired world 1.308; commitment obeyed 91.9% in 168 clean shapes of 209, 90 issued steps not executed; life and placing cannot be restricted (lives without a lost step are short); decisions that waited for the judgement, F 0.215% | informe_P6_22 (cantera/paper6/), informe_P5_LAG (cantera/paper5/) |
| 10 | bench tests with a real model | 603 calls, 4.44 dollars | informe_P55B |
| 10 | six of two hundred episodes without reported cost | 6 episodes, counted as zero | informe_P5ARI_cierre |

### A.3 What it cost

The recorded cost of paper five was 31.33 dollars; six episodes did not report their cost and were counted as zero, so the real expense may be somewhat higher. Of that, 16.08 went to games on the platform, with its credit, and 10.81 to the advisor called through the platform, also with its credit: neither of the two cost the author anything. The remaining 4.44 went to the bench tests with a real model, paid for by the author. By series: the advisor in shapes, 7.87 of platform and 10.48 of model; curiosity as a pull, 2.67; curiosity as a trip, 3.44; and ten other series and loose tests, 2.43 among them all. The full breakdown is in informe_P5AP1.

### A.4 The figures

Each figure was drawn with cantera/paper5/fig_paper5.py from the diary of one or several lives. Its record, with the exact data and the reason that life was chosen, is in the folder figuras_paper5/.

| Figure | Which life | Measured values | Record |
|---|---|---|---|
| 1 | P5-7C, batch 2, arm A (body alone), seed 20994019, seat 10 | 10,752 ticks lived; first blow at tick 10,273 (7.1 min); 24 blows in the whole life; what it lacks never drops below 0.6667; place 13; the solid band in the bottom panel is the back and forth between two squares (ticks 2,033 to 8,027): the rows F-4-ALCANCE and S-8-EXPOSICION switch on and off every 22 ticks. Chosen among the 93 arm A lives with more than 6,000 ticks | fig1_una_vida.txt |
| 2 | P5-6C, batch 5, arm F (body with advisor), seed 22250767, seat 10; shape 7, born at tick 3,999 and accepted at 4,001 | checkpoints at ticks 4,004, 4,037, 4,092 and 4,092; dropped at tick 4,062 because it stops winning. The imagined curves are not in the diary: they are recomputed with the same door code and reproduce the recorded advantage (0.28435) and the checkpoints. Best case: 10 of the 45 arm F shapes step on the destination of their first leg, and this is one of them; the destination of leg 2, (22,22), was not stepped on within the plan. At the first checkpoint, reality comes out 0.519 better than imagined, and 0.500 of that is the rival's floors imposed by the honesty rule (informe_P5FIG2) | fig2_forma_de_un_plan.txt |
| 3 | the same life as figure 1 | ticks 1,977 to 8,027 (6,050) with zero threat and map left to see fixed at 0.7969 | fig3_meseta_de_calma.txt |
| 4 | P5-8M, batch 0, arm K (curious body), seed 20260916, seat 11: the seat with the most accepted trips in the forty games | 18 trips: 5 completed and 13 stuck (three steps without getting closer to the destination); the 13 in a row go to the same destination, (21,29); none steps on its destination. No trips from tick 4,907 to 8,337 (threat below 0.2 in only 9 of 3,431 ticks) nor after (17 proposed, all 17 turned down by the door; top advantage 0.00455 against a margin of 0.02); informe_P5FIG2 | fig4_una_vida_curiosa.txt |
| 5 | P5-8M, the forty games, seats 10 and 11 of both arms | 40 lives of the body alone and 39 of the curious body (the diary of seat 10 in game 20784561 is missing, informe_P5ARI_cierre); map left to see rebuilt every 200 ticks with the same piece the body uses; median drawn only with 5 lives or more | fig5_cuanto_mundo_conoce.txt |
