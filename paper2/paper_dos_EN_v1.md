# G-EMV: the Hive. Instinct Suffices: a Whole Life Without Reward

Manel Enrico
*Independent Researcher, Barcelona*
ORCID: 0009-0008-1732-6310
*Preprint, version 1, 2026*

Second part of a story in three: the engine [1], the hive (this work), the pack (the next).

**The world and the question.** This work is the second part of a story in three parts. The
first, the engine, published G-EMV: a geometry of what matters, three domains of life, six
forces, one distance to descend, defined before touching any world, with no learning. It left
open the question that matters: can that geometry, alone, orient an agent in a world its author
did not design? This work answers it by building an agent for machina_1, the competitive
environment of Cogs vs Clips (Softmax) [2], where a team of eight agents mines resources,
supplies a common pantry, manufactures equipment and aligns junctions, defending what is
aligned from a rival force governed by the game itself: periodic events, emanating from static
enemy ships, that disconnect our junctions, returning them to gray, and claim the gray ones for
the rival side. The team's score accumulates per tick, it is the average number of junctions
held aligned across the whole life: what scores is holding, not just conquering. The agent
carries no reward function, does not train, and contains no scripted behaviors: its entire life
emanates from the descent of the distance that the published model defines. And the third part
stands announced, the pack: what changes when these agents, who cooperate without knowing each
other, begin to recognize one another.

**The animal, said once.** If an image were needed, it would be that of the social insects: a
hive. Eight bodies with the same genes of value, the same table of constants: identical
targets, identical weights, identical sensitivities, cooperating without knowing each other,
with no names, no faces, no census, sustained by a common notice board with no author. Calling
it an animal is only that, an image, and this is the only time this text uses it. From here on,
the agent.

**The map of the work.** Section 1 summarizes the published model: only the pieces the rest of
the work uses. Section 2 presents the architecture, the layer that translates the world into
forces, and the machinery that executes the descent. Section 3, the method by which everything
was measured. Section 4 shows the adult agent: its complete life, its numbers. Section 5
studies the team's communication, and what happens when it is switched off. Section 6 tells of
the two campaigns to trim its thinking, and why both failed. Section 7 places the work in its
family, and Section 8 draws its frontiers, each with its door.

---

## 1. The model, in two pages

The agent of this work is oriented by G-EMV, a published homeostatic model
(DOI 10.5281/zenodo.21026795). This section does not re-expound that work: it summarizes only
the pieces the following sections use, and refers to the published text for everything else.
The agent uses the constitutive pieces of the model, the six forces, the homeostatic distance,
gradient descent. The published work also demonstrates several phenomena that derive from those
pieces: that losses weigh more than gains, that the sated stops listening to its own domain,
and others. This work does not demonstrate any of them again, nor does it explain any result
by leaning on them. They are there, operating, because the engine that produces them is the
same, wherever this engine runs, losses will keep weighing more than gains. But no conclusion
in the pages that follow rests on those phenomena existing, and none would fall if they did
not: what is claimed here stands only on what is measured here. Where the agent's behavior
shows a relative of those phenomena, for instance, the satisfied agent that stops tending its
pantry, and the mechanism that had to be added to correct it, in Section 2, the concrete
mechanics will be told, without leaning on the model's taxonomy.

**The state: six forces over three viability domains.** The agent's internal state is defined
over three axes, each corresponding to a viability domain: the physical (F), the resource (R)
and the social/relational (S). Each domain is governed by two opposing forces that can vary
independently: one of gain (f⁺) and one of loss (f⁻), both of non-negative magnitude. The
state is the sextet

S = (f⁺_F, f⁻_F, f⁺_R, f⁻_R, f⁺_S, f⁻_S),  f± ≥ 0.

From the composition of the two forces of an axis, two quantities derive: the position (their
difference), which indicates which way the axis leans, and the tension (their sum), which
indicates its total load. Two states with identical position can differ in their internal
load; that dissociability is the central structural property of the model. This work presents
no results about it, none of the experiments that follow puts it to the test, but it operates
in every evaluation: two agents with the same leaning can be one serene and the other loaded,
both forces low, or both high, and the distance that governs the agent distinguishes those two
states, because it combines both quantities, not just the position.

**The appraisal lies outside the model; this work builds it.** The published core does not
determine the value of each force at each instant: it takes it as input from an evaluation
layer (the perception, or appraisal) that the model declares external and does not formalize.
That is exactly the coupling point between the two works. The architecture of Section 2 does
two things: it builds the appraisal layer the model declared external, the projection of the
game world onto the six forces, and it assembles the machinery needed to execute the descent
of d in a world with space, time and other agents: navigation, memory, commitments. That
machinery includes rules of persistence and priority among plans, which discipline when the
descent is re-arbitrated without altering what is valued; each one was born as a correction to
a measured pathology of pure descent in a spatial world, and Section 2 lists them one by one
with their motivation. No piece of the architecture introduces a second criterion of value:
what matters is fixed by the published model; what counts as gain or loss in machina_1 is
fixed by the appraisal described here.

**The homeostatic distance and gradient descent.** All the pieces of the model converge on the
homeostatic distance d, which measures how far the agent's state strays from its reference
configuration (the position and tension targets of each axis); it combines the position
deviation, the tension deviation and the coupling between axes, in compact form,
d = √(d_pos + d_ten + coupling), where each term aggregates its squares and internal weights;
the literal specification is in Appendix A of the published work. Said plainly: d measures how
far the agent is from being entirely well, and lowering it is all the agent ever does. The
behavior is gradient descent: at each tick, each step of the game's clock, the agent evaluates
the actions within its reach and executes the one that most reduces d. There is no other
criterion of value in this entire work; there are, in the machinery that executes the descent,
rules of persistence and priority among plans, which Section 2 declares. One consequence of
the form of d, squares under a root, is worth retaining from the start. Since every deviation
enters squared, being far hurts disproportionately: twice as far, more than twice the pain.
And that is why the same relief is not always worth the same: discounted against a large
deviation, it erases more pain than against a small one. Said with an example: eating is worth
more with the body at the brink than with the stomach half full, not because anyone decided
it, but because the formula produces it. The detail is not decorative: when two desires
compete, in Section 2, it is this curvature that will decide the duels.

**Decentering and proactivity.** The model's equilibrium is not neutrality: the position
targets are positive and, since an axis's tension cannot be smaller than the absolute value of
its position, the system's rest lies below those targets (the decentering, or gap). The
operative consequence for this work is direct: d is not zero even with all three positions at
their targets (1.250 in the reference profile). That residue must not be read as perpetual
malaise, but as structural appetite: even at its best, any opportunity of gain reduces some of
the agent's d, so it always has reasons to seek one. An agent whose equilibrium were reachable
would become, upon reaching it, indifferent to every prize; the agent of this work cannot
become indifferent, by construction. Its disposition to act is neither programmed nor
rewarded: it is structural. It is that property, and not a reward function, that
sets in motion everything Sections 4 and 5 measure.

**No learning.** The position and tension targets, the sensitivities, the per-domain weights
and the system's limits are constants of the model: nothing adjusts with experience, there are
no trained parameters and no reward function to optimize. When this work says zero training,
it says it in this literal sense: the geometry is a priori and remains fixed throughout the
entire work.

**The engine, frozen.** The model runs as published code: `motor/model.py`, md5
`1e511978c251130e95169ebf8443efa1`, identical from the first experiment to the last. The
agent's layer imports the engine's constants (targets, weights, sensitivities); it does not
copy them, so no second source of truth exists that could diverge. The claim "the engine was
not touched" is not declarative: the md5 is verified at every custody gate of the method
(Section 3), and all the evidence of this work, including the score, which is computed from
those same imported constants (Section 4), comes out of that engine and no other.

---

## 2. The architecture

### Block A, the appraisal

Section 1 left the contract between the two works signed. The model sets the form: the three
domains, the six forces, the distance. And it declares external the layer that decides what
counts as gain or as loss in a concrete world. This block describes that layer for machina_1.
First, the two currencies in which the forces operate. Then, the catalog of forces with their
sizes. At the end, how they compete.

All numbers come from the constants imported from the engine and from the appraisal layer. The
computation profile is the reference one, that of the control agent, and three families of
constants define it. The position targets, which way each axis wants to lean: (1; 2; 0.8) for
F, R and S. The per-domain weights, how much each axis counts within the total distance:
(1.0; 1.0; 1.40). The social weight deserves a line of its own: it is set at 1.40, double the
published engine's default, a calibration choice of this layer, baked into the configuration
of every run in this work, and declared here. And the sensitivities, how much each axis is
moved by what happens in the world: (0.30; 0.15; 0.10).

**The two currencies.** The appraisal feeds the engine through two distinct channels. The
first are the standing forces, which come in two signs: the pains and the bonuses. A standing
force describes a condition of the agent, life running low, energy spent, held territory that
consoles, and it points to no place: it pushes, or relieves, from within, wherever the remedy
may be. Its size is measured in Δd: how much it sinks the distance d of Section 1, the measure
of how far the agent is from being entirely well, relative to the healthy agent.

The second channel are the directed pulls: the gains with a place. The difference with the
bonus is not in the sign, both play in favor, but in the arrow: a pull points to a site in the
world. A winnable junction, an extractor, the hub awaiting its deposit. Its value is
discounted from d, but attenuated by distance: value·0.85^dist. We call that decay the radius
of desire. Every gain halves in value every ~4.3 cells. An opportunity worth 2.40 is worth
1.06 at five cells and 0.34 at twelve.

The consequence for behavior is direct. Pains and bonuses operate from within and do not fade
with remoteness, the pain pushes to leave the bad state; the bonus rewards staying in the good
one. Gains pull from outside and weaken with it.

**The catalog of forces.** The table summarizes the forces of the final agent. For each: its
axis, its type and its maximum size (the Δd from the healthy state).

| Force | Axis | Type | Maximum size |
|---|---|---|---|
| Body (life) | F | standing pain | Δd 3.78, the strongest in the system |
| Personal energy | R | standing pain | Δd 3.61 |
| Heart deficit | R | standing pain | Δd 1.641 (weight 2.40; target 5; grows quadratically with scarcity) |
| Territorial (score) | R | standing pain | Δd 1.641 |
| Territorial bonus (holding junctions relieves) | S | standing bonus | Δd ≈ −0.39 |
| Supply engine (two faces: deposit / mining) | S | directed pull | 2.40·ceiling·0.85^dist |
| Conquest opportunity | R+S | directed pull | 1.386·0.85^dist |
| Exploration (toward the map's untracked frontier) | R | directed pull | 0.48·0.85^dist |

Three notes keep the table honest. The scarcity of the common pantry is not a standing force:
it lives as the two faces of the supply engine, and its history, there was a time when it was
counted twice, is told in Block D. The heart deficit, by contrast, is personal hunger and
always observable: the agent counts what it carries, with no pantry memory. And its reverse,
wealth, is declared in the signed table but inert: the engine's saturation already makes
abundance move nothing. Wealth that does not relieve does not attract, the same lesson that
closes Block D. And the exploration row runs in the engine under an inherited label, forage,
on the F axis, doubly misleading: it seeks no food, which does not exist in machina_1, and the
reserve it grazes while exploring belongs to resources, not to the body. The table names it by
what the force does: pulling, weakly, toward the least-seen tile of the map.

The eight agents of the team run this same profile. A table of eight temperaments exists,
per-agent weight variations, implemented and switched off: it stays outside the agent of this
work.

The size hierarchy is not decorative. The body (3.78) and the energy (3.61) dominate the
catalog. The gains live far below, and further still once distance is discounted. That is why
survival rules without any rule decreeing it: it rules by size.

**The currency of comparison.** When two acts compete, the common yardstick is Δd in the
state: how much d each act lowers, computed in the agent's present situation. And here the
curvature Section 1 asked to retain returns, working, that of the squares: since every
deviation weighs squared, the same relief discounts more pain the deeper the well already is.
The practical consequence deserves saying slowly: the sizes in the table are not fixed prices,
they are ceilings. The body's Δd 3.78 is what that pain can come to move with the agent at the
brink of death; with the body at half, the same force moves less; with the body full, almost
nothing. No force is ever worth the same: each one is worth, at each tick, what the agent's
state lets it be worth. The table orders the catalog; the duels are settled by the state, tick
by tick.

**The arbitration, in one case to the digit.** Scenario E5 pits the two extreme temptations
against each other. An agent with its energy nearly spent. And in sight, a winnable gray
junction. In that state, the body's marginal is worth 4.574 and the conquest 2.934. The body
wins by 1.56×. There is no "survive first" rule in the appraisal. There is a pain that, in
that state, weighs more. In an easier state, the same junction would win. That is how the
whole evaluation layer arbitrates. Priority, where it exists as a written rule, lives in the
execution machinery (Block C). Never here.

### Block B, navigation and memory

Gradient descent is a one-step rule: execute the action that most reduces d. In a world with
walls and distances, that rule needs machinery. One must know how many real steps away each
thing is. One must remember what left the field of view. And one must hold a course when the
target is far. This block describes that machinery. None of its pieces changes what is valued.
All of them operate on the measurement of distance and on the execution of the step. And
distance was already in the formula: the pull decays with it. Navigating better is not wanting
differently. It is measuring farness better.

**The window and the planner.** The agent perceives an egocentric window of 13×13 cells:
radius 6 around itself, with the actual visibility within the frame close to a disc, the
corners of the square are not revealed. The window belongs to the environment; over it, this
layer applies a lock to its social channel: what falls within one's own sight is not accepted
on hearsay. Over it, the agent plans by dynamic programming. It expands the actions within
reach, evaluates each resulting state with the engine, and executes the first step of the best
path. It is a minimizer of present distance: it does not accept getting slightly worse now to
get better later.
That myopia has measured consequences, and they reappear throughout the work. The plateau: all
nearby paths are worth the same and the choice oscillates. The jam against the wall. And the
pocket whose exit demands moving away first. The pieces of this block are the cures for those
pathologies, one by one.

**The geodesic distance.** The distance that matters to a body is not the straight line: it is
the walkable one. Over the known map, the agent computes the real distance on foot to every
cell. We call that computation the geodesic field. Gains, tie-breaks and routes feed on that
field, not on the straight line. With the unknown, the principle is optimistic: the unseen is
assumed walkable. Thus ignorance does not imprison. The alternative, assuming wall where one
has not looked, would leave the agent captive of its own ignorance.

**The memory.** Outside the window, the world does not vanish. Memory retains positions: the
extractors, the junctions, the hub. And the deletion rule is strict: it only deletes what has
been genuinely refuted. To genuinely refute is to return to the place, have it within sight
range, and find it absent. Leaving one's sight refutes nothing. This rule was born from a
measured false refutation: a well given up as vanished only because it sat at the window's
edge, occluded, without truly being in sight.

Recollection also has two clocks. Position does not age. State does: confidence in what is
remembered decays with time, and with it the height of the pull toward it.

Two exceptions, each with its dead. The hub is never forgotten: an agent died with no home to
return to because its memory of the hub had expired. And walls are remembered apart, without
decay: a registry that vetoes stepping into known solid. To this layer also belongs the strict
reading of territory: home is one's own territory only. The previous criterion asked only
whether a cell had an owner, without looking at whose it was, and for a badly wounded agent,
the enemy front passed for home. One went there to heal, and died. Since then, the question is
whose.

**The open horizon.** Sometimes the target lies beyond the planner's reach. The piece the
final agent carries for that is the global geodesic: the field of walkable distances is
computed over the entire known map, not just over the window. A hub thirty or fifty cells away
already creates gradient by itself. It is the piece the dying agent's return uses (Block C).

There was an earlier piece for the same problem: the proximate goal. When the distant target
created no gradient, it relocated the attraction to an intermediate point along the path,
within reach, which inherited the target's value. It cured a measured immobility: a loaded
agent went from 466 ticks standing still to 3. And it stayed out of the final agent,
superseded: with the global geodesic, the flat landscape it cured no longer exists. It is
named because it teaches a pattern of the house: pieces retire too, and they retire with their
number.

**The real limit, declared.** Navigation was closed twice by stopping rule. The bottleneck
that remained is not navigating: it is discovering. The agent only pursues what has at some
point entered its sight. There is no imperative of exploration in the catalog, only a residue:
a pull toward the untracked frontier, the weakest in the table, almost always eclipsed by any
desire with a name. Nothing turns not-knowing into a push that commands. In the eight-agent
examination, only one ever saw the junction four cells from the hub. The others had it forever
out of reach. That limit is structural, and it is taken up again in the frontiers section,
where the door that would open it is also drawn: treating ignorance itself as a pain. One of
its answers is that another tells you what you did not see: communication
between agents. That piece, the town crier, is extended perception. It introduces no new
value: it widens what the appraisal can translate.

### Block C, the commitments

Section 1 left a promise pending. The agent carries a few written rules, and what was promised
was to list them all, each with the measured problem that made it necessary, and to show that
none of them decides what matters: only the balance of forces decides that. This block keeps
that promise. All the rules that follow are of the same kind, rules of constancy: when to hold
a plan and when to let it go, and each one exists because its absence killed someone or left
someone pinned. And it is worth saying clearly where they come from: intuition proposed more
than one, proposing is intuition's trade, but none stayed by intuition: those stayed that the
bench confirmed, and with the letter the measurement gave them.

**Why constancy is needed.** The agent, as Block A left it, decides from scratch at every
tick: it looks at the world, weighs its forces, and does what most reduces its distance d.
That has an enormous virtue, it is never captive to an old plan, and a defect that only shows
in practice: when two options are worth nearly the same, the agent hesitates. And since at the
next tick it decides from scratch again, it can hesitate forever. The case that portrayed it:
an agent loaded with ore, alone, pressed against the door of its own home, one step from
delivering. For its computation, stepping north or stepping south was worth exactly the same,
and it spent its life alternating north, south, north, south, in front of its door, never
entering. It was not broken: it was perfectly undecided.

The cure is the commitment: when the agent chooses a plan, it writes it down and executes it
to the end without re-arguing it at every step. But with one proviso learned the hard way,
because the project also tried the opposite, freezing decisions altogether, and found that
frozen habits build their own traps (that result has its own section, further on). Neither
arguing everything at every tick, nor never arguing anything: plans that hold, with priced
reasons to break. That is what this block is: four commitments, each with its trigger, its
reasons for rupture, and the corpse or the jam that justifies it.

**How a commitment executes.** All four share the same mechanics. The plan is a route: the
list of steps toward the target, computed over the map of walkable distances Block B
presented, always by the step that brings it closest. And the last step of every route is
contact: in this world, things are done by touching them, ore is mined by bumping into the
extractor, delivery is made by bumping into the home. If no known path exists, the route comes
back empty and there is no commitment: the machinery does not invent paths it cannot see.

**The delivery commitment.** It fires when the agent carries the full lot, five units, and the
common pantry needs material. It is, no more and no less, the "deposit" face of Block D's
economic engine, with constancy added. What breaks it? Four reasons, written: that the world
rejects the step (someone occupies the cell, an unknown wall); that the opportunity truly
vanishes; that the body's pain grows; or that a clearly better target appears, and "clearly"
has a number: worth at least one and a half times more. The number is a declared constant, not
a sought optimum: nobody swept its neighbors, and what the bench confirmed is the whole rule
with that threshold inside. Merely better is not enough, because two similar targets taking
turns are another form of the infinite doubt.

**The mining commitment.** It fires when the agent goes with its pocket to fill and there is
an extractor to pursue, seen now or remembered. Its rupture rule is the finest of the four,
and it distinguishes two things that look alike: changing material and changing well. If the
economy comes to need another material, the pantry already has silicon, now carbon is missing,
the old plan is surplus and is dropped: obeying the pantry is the journey's meaning. But if
another well of the same material appears, a little closer, the plan is not dropped. The
difference has history: an agent spent its life orbiting between two equivalent silicon wells,
halfway from both, switching favorites every tick without touching either. With the rule, the
orbit becomes a straight line to the chosen well.

**The conquest commitment.** It fires when the agent goes equipped, the aligner, the tool for
aligning junctions, and a heart, the ammunition each alignment spends, both manufactured in
the common pantry from what the team mines, and there is a junction to take. It is broken by
the world's rejection, by the body's pain, or by the junction already being ours, including
one a teammate took first, because the goal was for it to be ours, not to take it oneself. It
is not broken by another junction appearing closer, nor by the rival capturing the chosen one:
the journey continues. Its founding story is Block D's: the perfectly equipped porters who
reached the junctions and did not enter, 226 contacts, zero conquests. With this commitment
active, on its first trial, the porter went, entered and spent its ammunition. It was the
behavior the system had never produced.

There is also an order among the three: delivery, mining, conquest, they are evaluated in that
order, and the first to fire takes the plan. That order ensures, with no new rule, that a
loaded agent does not get distracted conquering: what is carried gets delivered first. Supply
comes before trade, by order of evaluation, not by decree.

**Home's door.** When the life reserve falls below the threshold, the body's pain outweighs
everything else. Up to here the balance decides, as always. But the route home that is then
committed has a property unique in the whole system, and it must be said plainly: it is
unbreakable, it is exchanged for nothing. Not pain, not an opportunity however good. Only the
fact of reaching home ends it, or the world rejecting it: the attempted step not happening
because another body occupies the cell or an unknown wall closes it. In that case the agent
has not changed its mind, it is the path that no longer exists, and it is recomputed toward
home, to the same destination.

This is the only rule of the agent that decides by writ and not by weight, and that is why it
takes the longest paragraph of the block: exceptions are paid for in detail. Its motivation is
ten deaths. In the long runs of an earlier era ten agents died, and the autopsy found the same
mechanism in all of them. The alarm rang in time in all ten, the agent knew it had to return.
But the return journey, decided tick by tick with home out of sight, advanced in stumbles:
where a firm course closes one cell per tick, they closed between zero and 0.67. And while
they hesitated, they bled, one unit of life per tick in no-man's-land, and double that (1.96,
measured) in enemy territory. They died six, twelve cells from their door. The balance had
been right about what mattered; what failed was the constancy of the journey. The written rule
guarantees exactly that: that the most important journey of all is not re-argued at every
corner.

The cure is completed with a detail of prudence: the threshold that triggers the return is not
fixed, in enemy territory it doubles (from 25 to 50 units of reserve), because there one
bleeds double, and the factor comes from that measured bleeding, not from the eye. With the
ten dead set as judges on paper, the rule saves nine. The tenth was 54 cells from home,
deep in enemy territory: it needed more life than fit in its body, and no return rule saves
it, its failing was having gone so far, which is another corner of the design and is so named.

**The conflict that dissolves itself.** With four commitments coexisting, clashes are to be
expected. The case that seemed inevitable: a loaded agent, committed to deliver, that begins
bleeding out on its way home. Which rules, delivery or survival? The answer turned out to be
that the question is badly posed: the two destinations do not compete because they are nested.
Survival asks for home, one's own zone, where the body regenerates, and delivery asks for the
hub, which lives inside it. The dying, loaded agent makes a single journey, under the
protection of the unbreakable route: on crossing the door it is already healing, and on
reaching the hub, if still loaded, it delivers. No tie-breaking rule had to be written, and
from there a principle that governs the whole design: where geometry dissolves the conflict,
no rule is written. Rules are for the conflicts geometry does not dissolve, and those turned
out to be very few.

**What no rule touches.** To close the block it is worth saying calmly what these four rules
do *not* do, because there lies the point Section 1 promised to defend.

The agent has two systems working together, and they do different jobs. The first is Block A's
balance: the forces with their sizes, weighing against one another at every tick. The balance
answers the question "what matters most right now?", and it answers with numbers, comparing
how much each option would relieve. The second system are the rules of this block, and they
answer another question: "what the balance already chose, with how much constancy is it
pursued?".

Section 1's promise was that the rules never invade the balance's ground. And it can be
verified rule by rule: none of the four changes the size of a force, nor the weight of a
domain, nor the value of an opportunity. None says "this matters more than the balance
believes". All of them operate on something else: the route already chosen, and the reasons to
abandon it or not.

An example with numbers lays it in plain view, and the numbers come from Block A, from the
test scenario presented there: an agent with its energy nearly spent that sees, within reach,
a junction ready to conquer. The maximum temptation at the worst moment. Who decides? The
balance, alone: recovering energy would relieve its distance by 4.574; the conquest, by 2.934.
The body wins, by number, 1.56 times more, with no rule having intervened. If the same agent
were rested, the numbers would come out reversed and the junction would win, with the same
rules asleep. The rules of this block only wake *afterwards*: once the balance chooses, they
protect the journey toward what was chosen.

That division of labor, value set by the balance, discipline set by the rules, is Section 1's
bridge sentence, kept: in the entire agent there is no criterion of what matters other than
the published geometry.

### Block D, the economic constitution

The world's economy demands a complete chain. Four elements must be mined, carbon, oxygen,
silicon and germanium. They must be carried to the hub, the home, the common pantry. With
them, the hub manufactures the equipment. The game offers a catalog of manufacturable
equipment wider than what this agent uses: from that catalog, the agent manufactures and
employs only two pieces, the aligner, the aligning tool, and the hearts, the ammunition,
because they suffice to close the entire cycle. The four elements are not equipment: they are
the raw material everything else consumes. With the aligner and one heart, an agent can align
a junction: that is conquering, and that is what scores. This block tells how the agent
governs that chain. And it also tells its history, because the final constitution was not
designed in one piece: it was earned through forensics.

**The supply engine.** The pantry speaks through a single channel: the supply engine. It has
two faces and never both at once. If the agent goes loaded with the lot, the face says: to the
hub, to deposit. If it goes empty and the pantry lacks something, the face says: go mine what
is missing, the
most needed element, not the nearest. The force of this channel is not fixed. It carries a
continuous ceiling: its height drops as the body's pain rises. A healthy agent supplies
eagerly. An aching one, less and less, until the body rules. There is no switch: it is a
slope.

That form deserves a name and an explanation, because it repeats three times in the agent. The
idea: instead of a yes-or-no gate, "if this happens, stop wanting that", the desire is
multiplied by a continuous factor: a dial between zero and one that slides with the state. The
supply engine carries the first: its ceiling drops as the body's pain rises, the healthy agent
supplies eagerly; the aching one, less and less, until the body rules. The equipment cushion,
which appears further down, carries the second: the trade's spending brakes as the pantry
nears the vital minimum. And the force of returning home carries the third: it grows as the
life reserve falls. We call them the three sisters. The lesson that begot them was paid for
with benches in its day: yes-or-no switches fail on both sides. If the switch cuts desire at a
stroke, it crushes, the worker who crosses the threshold drops the task half done, even one
step from finishing. If it lets desire through whole until the cut, it wanders, chasing at
full force, until the last instant, what it should hardly touch anymore. The slope does what
the gate cannot: desire weakens little by little as the state tightens, and behavior turns
smoothly instead of snapping.

**The limbo of the sated.** The first version of the pantry had a fine disease. When the hub
reached just enough to manufacture the vital, one unit of oxygen, three of carbon, one of
germanium and one of silicon, it declared itself satisfied. No pain sounded. Nobody mined,
nobody deposited, and the pantry froze at the exact point where the failure caught it.
Measured: the hub frozen at [3,3,3,3] in the forensic run, the trade dead, the score at zero.
We call it the limbo of the sated. And it is worth saying what it is: the operative relative
of the saturation blindness the published model demonstrates as a phenomenon. Whoever feels
well stops listening to its own domain, the axis, of Section 1's three, that it already has
satisfied. There it was a theorem with ablations; here it was a disease with a corpse.

**The breathing band.** The cure was two slopes. Below the slack, the vital level plus the
equipment's cost: [1,3,1,1] plus [1,3,1,1], the slack [2,6,2,2], supply pushes: the pantry
asks until it has margin, not just until the minimum. Above the vital, the trade may spend,
but with a continuous cushion that brakes spending as it nears the minimum. Between the two
slopes, the pantry breathes: it fills, it spends, it refills. No limbo, because below the
slack there is always push. No drain, because spending brakes itself before touching the
vital.

**The halt.** The band was taken to the bench with its criterion frozen beforehand, like
everything in this work. And the bench delivered two truths at once. The pantry truly
breathed: for the first time in the project, the hub did not freeze, three of the four
elements came in, and the trade's window opened. But the score collapsed to zero, and the
criterion said: if the score sinks, halt. It halted. The band was switched off whole and the
brake was written. The pre-declared criterion ruled over the score: it was not a defeat of the
design, it was the method's discipline executing itself, the same brake that protects every
number in this work.

**The forensics that acquitted the band.** The natural suspicion was that the band was to
blame: supplying absorbed all eight agents and nobody conquered. The score's autopsy put that
suspicion to the test: five hypotheses, four discarded with data, one confirmed. Does supply
crush the desire to conquer? No: the conquest desire won the choice 66% of the ticks. Did
geography keep them far? No: there were 226 contacts with conquerable junctions. Did they not
know them? No: some forty junctions in memory. The confirmed one was the fifth: they arrived
and did not enter. 226 contacts, zero conquests. The porters touched the door and did not
cross the threshold. The cure, therefore, was not economic: it was Block C's conquest
commitment, the
landing. With it, the final picture fits: the band on, the pantry breathing, and conquest
turned into act, 100% conversion of contacts, median score 1.705 across five runs, the whole
team alive, all four elements in the hub, residual exploration at zero.

**What stayed out, declared.** The final constitution is also defined by what it keeps off.
The pantry as a standing social force stayed off: scarcity lives in the supply engine, and
keeping both was counting the same hunger twice. Heart manufacturing stayed in the drawer,
with its measured reason: the birth cradle brings eight hearts and the spending of those runs
was two to four per run, with ammunition unspent, making more is not due; first one learns to
shoot. From that wait comes the era's maxim: land before you manufacture. And an amendment to
the engine's order was also parked with its number in front: only 8.8% of the conquest desire
was being crushed by supply, that was not the bottleneck.

**The era's principle.** Two distinct defeats, the heart that drained the pantry without ever
equipping, and the cushion alone that froze in the limbo, wrote the same lesson: desire that
cannot be consummated does not sate. A force without its full chain behind it produces no
behavior: it produces stampedes or paralysis. The final constitution is that: every desire
with its entire chain, from the missing element to the bump that delivers it, from equipment
in hand to the aligned junction.

### Block E, what there is not

The previous blocks told what the agent carries: its forces, its navigation, its commitments,
its economy. This last block tells the opposite, what the agent does not carry, because in a
work like this the absences say as much as the pieces: each missing thing is a decision taken
on purpose, not an oversight, and several of those absences are exactly what the experiment
wants to put to the test. The list, one by one.

**There is no learning.** Nothing in the agent adjusts with experience. The targets of each
domain, the weights, the sensitivities, the sizes of the forces: everything is constant from
the first tick to the last, and from the first run to the last. The agent at the end of the
work is exactly the one from the beginning, it has not improved, it has not adapted, it
remembers nothing of previous lives. What changes between runs is what it knows of the world
(its map), never what it cares about. Section 1 said it of the model: its constants do not
change. Here it is said of everything else. Neither does the layer that translates the world
learn, the appraisal's weights and thresholds are fixed, nor the rules of constancy, their
margins are the same on the first day and the last. The whole ensemble, model, translation and
rules, is as fixed as its parts.

**There is no reward function.** In the usual technique of agents, a reward function is a
point counter the system tries to maximize: do this, add; do that, subtract, and the entire
behavior is molded chasing that number. Here that counter does not exist. The game's score,
the tally machina_1 keeps for each team, enters the agent through no channel: no force looks
at it, no rule mentions it. The agent does not know it scores. It aligns junctions because
territory hurts and opportunity attracts, because doing so reduces its distance, and the score
rises as an external consequence, just as the bee does not know it pollinates. When the
results section measures the score, it will be measuring an effect of the behavior, not its
objective.

**There is no network and no learned policy.** Neither is there, under the hood, a neural
network, the fabric of millions of numbers tuned by training that governs most of today's
agents. The one that decides is Block B's planner: it unfolds the options within reach, hands
them to the published engine to evaluate, and executes the best. Zero trained parameters, zero
practice episodes. The entire policy, everything the agent can come to do and why, fits in a
file of readable rules, and every rule has its motivation written in this
section. It can be audited with the eyes, something no network allows.

**There are no written goal-behaviors.** No line of the agent says "in situation X, pursue Y".
There is no script of behaviors, go mine at the start, come back if attacked, like the one a
videogame character would carry. Destinations are always set by the descent of the distance:
what to mine is said by the material the pantry lacks, when to return is said by the pain,
which junction to take is said by the best-weighed opportunity. What is written was told in
Blocks B and C, memory rules and constancy rules, and it has already been shown which side
they are on: they discipline the journey; they do not choose the destination.

**It brings nothing written down from home.** The agent arrives in machina_1 knowing nothing
of the world beforehand: not the names of things, not the recipes, not the numbers. Everything
it needs it reads from the world itself upon arrival. The names, what the resources, the
junctions, the equipment are called, it takes from the match configuration. The manufacturing
recipes it reads from the game, and from them it computes how much the pantry needs: nobody
chose those quantities by hand. And the model's constants are imported from the published
engine, the first work's model.py, rather than copied: no second copy of the numbers exists
that could drift from the published one unnoticed. It is a property of construction, and it is
stated as such, the experiment has not been run: if machina_1 dawned with other names, the
agent would read them at startup just as it read today's, because names never meant anything
to it, they are labels from which it hangs its desires, and with other recipes it would
recompute the quantities. Nothing travels hidden inside it.

**There is no exploration worthy of the name.** Block B left it said with its nuance: in the
catalog lives a residue, the weakest pull in the table, toward the untracked frontier, but no
imperative: the agent's ignorance does not hurt it. It pursues what it saw or what it was
told; what never entered its sight nor the board barely exists for it. It is the measured
frontier of this architecture, and it is taken up again in the limits section.

**There is no representation of the other.** Teammates exist for the agent as bodies occupying
cells and as notices on the common board, never as individuals. There is no census, no memory
of who said what, no identities. All the cooperation this work shows, the shared map, the life
saved, the junctions a teammate takes first, happens without anyone knowing who anyone is.
That absence is not an oversight: it is the experiment. And where anonymity ends, the next
work begins.

What remains, when all of that is missing, is exactly what this work wants to measure: a
published geometry of what matters, a layer that translates the world into that geometry, and
the minimal cures execution demanded. The sections that follow measure what that agent, thus
bare, does.

---

## 3. The method

A long project has an enemy that is not the world: it is the author himself. Results always
admit a favorable explanation if sought after seeing them, and a system that gets touched
along the way can end up proving things about itself rather than about what it intended. This
section describes the three habits with which this work defended itself from that.

**The first: the engine is not touched, and this is checked.** The published model runs here
as frozen code. Its fingerprint, the md5: a mathematical digest of the file, such that if a
single letter of the code changed, the whole fingerprint would change, is verified before
every experiment, and it is the same from the first run to the last:
`1e511978c251130e95169ebf8443efa1`. It is further checked
that the system being executed contains exactly the code the experiment claims to test. These
are not gestures of ceremony: they are the condition for a result to enter this work. Without
them, the claim "this is done by the published model" would be a promise instead of a fact.

**The second: criteria are written before looking.** Every experiment in this work is declared
in writing before it runs: what is changed, what is measured, and, crucially, which outcome
will count as success and which as failure, with numbers. Then it runs, it is read, and it is
obeyed. The order is everything: whoever sets the bar after seeing the jump always clears it.

Two words the work uses constantly deserve fixing here. A run is a complete match: the eight
agents released into the world for a fixed number of steps, ticks, in the game's tongue, until
the end. And the baseline is the reference configuration against which everything else is
compared, the agent with its stable stack, so that every claim of the type "this piece does X"
is always a measured difference between the baseline and a run identical except for the piece
in question. Hence the procedure the results sections use again and again: to know what
something does, switch it off and compare.

Criteria, moreover, are only corrected forward. When experience shows a bar was measuring
badly, it is re-declared in writing for future experiments, but the verdict it dictated,
including an unjust halt, stays in the record as is. A criterion is corrected for the future;
never for the past.

**The third: measure whole lives, not instants.** That a piece is switched on does not prove
it does anything. What counts is its effect tallied over the agent's complete life: how many
times it acted, what changed in behavior, what happened when switched off. A switch turned on
is not a result.

That habit brought the most uncomfortable methodological finding of the work, and it deserves
telling in full because it explains how every number in the following sections is read. At
first, scoring was believed deterministic: two identical runs gave exactly the same result. It
had been verified, and it was true, but in short runs. Measured over whole lives, the opposite
appeared: the same configuration, run three times, gave 1.705, 2.322 and 2.785. No new piece
was breaking it; the horizon was. In short runs almost nothing has scored yet and a minuscule
difference at the start has had no time to propagate; over a whole life it has. The
divergence's starting point was even located in a pair of extreme runs: the first different
action occurred at tick 13, and that tiny fork came to decide, nearly two hundred ticks later,
whether an agent reached a junction in time or not.

The consequence was to re-found the way of measuring. Since then, no claim in this work rests
on a single run: experiments are repeated, five runs is the adopted standard, and the median
is reported, the middle value: as many runs above as below, with its range, the worst and the
best. There are measures, besides, where zero is a frequent outcome, and it is worth saying
why: scoring demands that the entire chain land inside the measured window, mine, supply,
manufacture, equip and enter, and in short horizons many runs stop one link short. For those
measures, how many of the five runs scored anything is also reported: it is what tells a
"sometimes it manages" from a "never". Earlier verdicts were not thrown away: they were
re-read honestly, and stand bounded. Those describing the working of the agent's body, that it
survived, that the pantry received its four materials, turned out identical across all runs
and remained standing without caveats. Those citing a score became what they had always been
without knowing it: a sample from a distribution.

A closing remains that completes the arc, and that this work took months to be able to write.
All that time, measurement ran on medians and ranges against a variability that was real but
of unknown cause.
The cause appeared while studying communication: the order in which the eight agents write to
the common board varies from run to run, and that order decides which news arrives first. With
the board off, three identical runs come out exactly equal. The method corrected itself twice
without breaking: first adapting to a randomness it did not understand, then naming it.

**What a number means, then, in this work.** Every value cited in the pages that follow meets
three conditions: it comes from an experiment declared before running; it was measured over
whole lives and, when the magnitude asked for it, over several runs with median and range; and
it came out of the published engine, fingerprint verified. Those failing any of these
conditions do not appear, or appear with their limit written beside them.

---

## 4. The adult agent

The two previous sections told how the agent is built and how what it does is measured. This
one tells what it does. It is the part of the biography where the protagonist is in its prime,
and it is narrated as it was lived: a first time, a cure, a horizon that stretches, another
cure, and the complete life. A reminder before starting, to avoid a natural confusion: nobody
hands out roles. There are no miners, porters or conquerors by trade, all eight run the same
profile, and who mines, who hauls or who conquers at each moment is circumstance, not caste:
the one who passes near the well, mines; the one who leaves equipped first, conquers. A note
of honesty about the figures, before starting: the verdict benches, as this work calls its
decisive experiments: the piece runs against its frozen criterion, and the outcome is obeyed,
run at five runs with their median, as the method fixed; the long-horizon reconnaissances run
at three, are reported as ranges, and are declared as what they are, reconnaissance, not
certification.

**The first time everything worked.** For months, the agent knew how to do things separately:
live, or mine, or remember, never all at once. The bench of the five cures was the day the
whole body started together: the complete team alive from beginning to end, without a single
death; the ring of wells around home held in memory instead of forgotten; the miners reaching
their wells without wandering, wandering, which had been a plague, dropped to zero; and all
four materials of the game entering the pantry, including silicon, the last link of the chain,
which had never reached home. That day one front stayed open, and the record says it without
ornament: the score was zero. The agent kept the pantry, and did not conquer. It knew how to
live; it did not yet know how to win, though that last bit deserves saying properly, because
for the agent "winning" does not exist. As the architecture left said, the score enters it
through no channel: only its distance exists, being well, nothing hurting, going toward what
attracts. What that zero signaled was not an unmet goal, because the agent has no goals to
miss: it was that one of its attractions, that of the junctions, was not reaching consummation
in the world. The problem was not of desire; it was of journey. And that is why its cure was
not giving it reasons, but constancy.

**The spending comes alive.** That is: the ammunition finally gets spent, the heart the porter
carried enters, at last, a junction. The why of that zero the architecture already told: the
porters reached the junctions and did not enter. It is worth recalling here the order of
the times: Section 2 described the finished agent, with all its pieces; this section tells
when each was born. On that day of the zero, the conquest commitment did not yet exist, it was
born precisely as the cure for this. Recall its letter: once a junction is chosen, the journey
is protected until entering and spending, and neither a closer junction nor a passing pain
interrupts it. It was taken to the bench with the new criterion, five runs and median, and the
result turned the biography around: the median score left zero, from 0 to 1.705, and every run
scored. The detail that tells it best is not the figure but the shape: before, a porter
accumulated dozens and even hundreds of contacts with junctions without entering any; with the
cure, contacts collapse to a handful, it goes, enters and spends. The conversion of contact
into conquest went from practically nothing to one hundred percent. The agent no longer
circles what it desires: it takes it.

**The horizon stretches, and uncovers a problem.** With the whole body running and conquest
alive, life was stretched to a thousand ticks to see what the agent does when time is
plentiful. Two things appeared. The first, good: conquest is not a matter of the start, the
agents conquer across the whole life, and in one run the team signed a late burst of five
junctions in a hundred and ten ticks, extending its front far beyond the cradle. The second,
bad: the long life kills. Three and four agents per run died bleeding out, far from home, on
journeys the short life had never asked of them. The recognition was clear: the adult agent's
most urgent problem was not winning more, it was not dying on the way.

**The bleeding, cured.** The answer was the dying agent's unbreakable route, Block C's home's
door, with its ten dead as motivation. Recall what it does: when the life reserve falls below
the threshold, the agent commits the route home over its complete map and does not let it go
for anything, only arriving ends it, or the world rejecting it and recomputing toward the same
destination; and in enemy territory, where one bleeds double, the alarm rings earlier. Its
bench is the most resounding of the work: deaths by bleeding dropped to zero in all three
runs, the whole team finished alive all three times, and the score, far from paying a price
for so much prudence, rose, from median 3.00 to 5.16. The reading matters more than the
number: living does not cost producing. The saved do not hide at home, they work, and they
sustain the junctions that used to be lost with their dead porter. And the symmetry that signs
it: the same agent that in the control runs died pinned thirty-eight cells from its door, with
the cure active crosses the same dangerous way back, badly wounded, in hostile territory, and
crosses the door of home. That crossing exists on video, frame by frame, drawn from the data.

**The complete life.** The final question remained: the whole life, two thousand five hundred
steps. And that horizon deserves declaring with its two legs, because it is this work's
protocol, not the game's limit: the official league runs matches of ten thousand. The
scientific leg: two thousand five hundred steps contain the agent's complete behavioral cycle,
expansion, maturity, quiescence, and its endowment economy (some eight hearts from the cradle
against a measured spending of six to nine over the complete life) is calibrated almost
exactly to that window. The material leg: an uncompiled deliberative agent costs some thirty
machine-hours per life, and the triplicate protocol at ten thousand steps would have been
unviable. The adult agent's picture, taken three times: median score 3.23, not one death in
any of the three lives, and a clean ceiling, the agent conquers its territory and sustains it,
around seven junctions, against the fifty-two enemy waves the game throws at it, and expands
no further. The score, recall, accumulates per tick, holding scores, and in one of the three
lives the arithmetic shows itself bare: nine thousand one hundred and forty-nine
junction-ticks spread over two thousand five hundred steps are 3.66, that run's exact score,
to the ten-thousandth. The ceiling is not set by time: it is set by ammunition. And there, an
elegance nobody designed on purpose: the endowment of hearts the team is born with, decided
long before knowing this datum, turns out almost exactly calibrated for the complete life, it
runs out, literally, with the last breath of the measured life. The piece for making more
stayed in the drawer with reason: its moment would be an even longer life.

This picture also leaves two seeds planted, which the price-of-thinking section harvests. The
first: the adult agent repeats itself, when young, one in three decisions is identical to one
already taken; when old, two in three. Routine emerges with nobody programming it. The second:
thinking costs it more and more, the tree of options it unfolds each tick thickens with age,
until the end, and late life is the most expensive to think. An agent that repeats more and
more and pays
more and more to deliberate: that open scissor is exactly the promise that tempted the
reflexes, and the price-of-thinking section deals with it.

**The force that never had to be written.** The adult's biography closes with an episode that
sums up the whole design. On paper, one last force was missing: the defense of territory, that
losing a junction should hurt, that the agent should rush to recover it. It was designed in
full. And before building it, the method ordered judges for it: the real thefts of the long
runs, examined tick by tick. The verdict was the best possible ending: the agent already felt
the theft. In this world, a stolen junction does not pass to the enemy, it goes gray,
ownerless. And the gray one, for the agent, already attracts: it is exactly what the conquest
commitment pursues. And it is worth saying why in this world theft never becomes a trade: the
agent never sees a junction in enemy hands as something to wrest away. Junctions, for it, come
in two states, its own, or gray and winnable, and when the rival strikes one of its own, it
does not take it: it disconnects it, and leaves it gray. Recovering it is, once again,
conquering. That is why the game's catalog includes tools of contention this agent knows by
name and never manufactured: it never lived the situation that calls for them. And the twin
condition, declared: within the measured horizon and map, no rival junction ever came within
reach, rivals at zero across twenty thousand agent-ticks; direct contention is territory
unobserved by this protocol, not an impossibility of the agent or of the game. And that is why
the record shows that every nearby theft was always recovered, alone, with no new force; the
only thing out of reach was one distant, late loss, marginal, in the match's last breath. The
missing force turned out to be implemented without knowing it, implicit in the geometry, and
was archived without spending one machine-hour. It is the elder sibling of a principle the
architecture already stated: where geometry already does the work, no force is written. The
adult agent became complete not when the last piece was added, but when it was proven
unnecessary.

---

## 5. The village: the word in the team

The eight agents of the team share a single social piece: the town crier. It is a common
notice board. Each agent publishes on it what it sees first-hand, extractors and junctions,
with their position, and reads what the others published. There are no encounters: the board
is read from any point of the world, every tick, without crossing paths or approaching, like a
network to which all eight are always connected. Crossing another on the way adds nothing:
there is no channel of encounter, everything, absolutely everything, passes through the board.
And the heard weighs less than the seen: others' notices enter memory with discounted
confidence. Communication there is, and abundant: the agents tell each other things millions
of times per life, this is here, that is there. What there is not is language in the
linguistic sense: notices are facts with a fixed format, what and where, not symbols whose
meaning must be interpreted. With this channel one cannot lie, nor qualify, nor ask: only
state. There is no learned protocol: nobody negotiates what to publish. And there is no
author: the notice does not say who posted it. The agents do not know one another; they share
a map, not a society. This chapter measures what that piece does in the complete agent, with
the method of the whole work: to know what a piece does, switch it off and compare the life
with it and without it. And the criteria of success or failure are written, with numbers,
before seeing any result, the full doctrine is told in the method section.

**The channel's anatomy: almost all repetition, and yet it sustains the map.** Two numbers
define the channel, and together they look like a contradiction. First: it is a deluge of
repetition. The universe of distinct facts that can travel is small, 1,184 in the reference
run, and
yet it gets injected millions of times: the maximum possible novelty is 0.20%; the remaining
99.8% is re-announcement of what was already said. Second: that deluge sustains the agent's
knowledge. Between 80% and 96% of each agent's map, 85% on average, came from the board, not
from its eyes. Of what travels, three quarters are extractors and the rest junctions; walls do
not travel. The agent owes most of its world to the word, not to sight. The resolution of the
apparent contradiction is the chapter's central finding, and it comes out of the two
experiments that follow: switching the channel off entirely, and removing only its repetition.

**The silence: switching the channel off.** Three complete-life runs with the board off,
against the baseline with the board on. Four findings, each with its number.

First: the harvest does not depend on the channel. The score of the three mute runs was 3.408,
all three identical, against the baseline's median of 3.23. Agents with only their eyes know
seven times less world (140 objects on average against 1,010), and harvest the same. The
explanation lies in this world's bottleneck: what limits the score is the cradle of hearts,
not information. The delimitation is declared without detours, and with its condition: for the
agent as constituted, in machina_1 and at the measured life, the protocol's two thousand five
hundred steps, everyone is born rich: the conquest ammunition comes as standard, and the
starting endowment exceeds with margin what this agent comes to spend, because the piece for
making more stayed in the drawer. Wealth is relative to desire: an agent built to maximize the
score could manufacture ammunition without rest, and for it this world would be not an
inheritance but a factory, and the channel's role could be another. The same holds for a world
where discovery were the limit: the opposite could be expected.

Second: the channel saves a life. One of the eight, the one that wanders farthest from home,
dies in all three mute runs, at the same tick in all three (t2231), and in the baseline it
lives. Its autopsy: it knew 199 objects with only its eyes against 989 with the board, it
explored forty-two cells from home, and when the alarm to return rang, its life no longer
covered the road. The social map is survival infrastructure for the one who goes far: the word
as streetlamp, not as coin, it buys no harvest; it lights the way home.

Third: the channel was the lottery. The whole work lived with a variability between identical
runs that forced measuring with medians, ranges and triplicates. With the board off, that
variability vanished completely: three mute runs give 100% identical actions, behavioral
determinism, verified action by action. With the board, 25%. The source of the randomness had
a name: the arrival order of the writes to the shared board, different in every run for
reasons alien to the agent. This re-reads the method's history without rewriting it: the
measurement criteria were correct for the system they measured, an agent with a board, and
now, besides, the variance that motivated them has a mechanism.

Fourth: the channel focuses the planner. Each tick, the planner unfolds a tree of options, the
actions within reach and their consequences, a few steps ahead, and chooses. Against
intuition, the mute agent, knowing seven times less world, unfolds a fatter tree than the
baseline's. Knowing where the target is lets you go for it; ignorance forces considering too
much. The board slims that tree by 17%.

**The lock: removing only the repetition.** If 99.8% of the traffic is re-announcement, the
temptation is obvious: an "I already know" lock. The publisher does not repeat what has not
changed; the reader does not re-note what it already knows. The lock was built, passed its
cold verifications, and fulfilled its assignment: notices fell by more than 86% and the map
was preserved. And even so it was archived, because it failed at the two prizes expected of
it.

The first prize was saving work. The opposite happened: the system came out 45% slower per
step. Repetition had a hidden function: every re-announcement is also a "this is still there",
it renews the date of the known, like the date stamps on food. Without repetition,
memories are not erased but they age: the agent trusts ever-older information less, and walks
worse routes toward stale data. Notices were saved and steps were paid. (This result is from a
single run, and is declared as such.)

The second prize was calming the randomness between runs. To understand why it did not, one
must know where the randomness came from: eight agents write to the board every tick, and the
order in which their writes arrive varies from run to run for machine reasons, alien to the
agent, like eight people dropping letters into the same mailbox, where who arrives a second
earlier changes every time. That order matters the first time each piece of news arrives:
learning of the northern extractor before the southern one, or the reverse, twists the first
decisions, and from there, whole lives diverge. The lock eliminated the repeated arrivals, but
the first arrival of each piece of news kept arriving whenever it arrived: the draw was in the
first delivery, not in the reminders. Measured: with the lock, runs coincide in 27.9% of their
actions, the same as the baseline with its 25%.

**The baseline does not change.** After the two experiments, the town crier stays on in the
agent, deluge of repetitions included. What it gives is measured: it saves the one who goes
far, keeps the map fresh, and spares the planner work, its option tree comes out 17% slimmer.
What it costs is also measured: almost all its traffic is repetition, and it is the source of
the randomness between runs. It stays on because what it gives is worth more than what it
costs, and both figures are on the table. A gift tool remains besides: if a future experiment
demands that two runs come out exactly equal, switching the board off achieves it, determinism
is one switch away, knowing already what is lost in exchange.

**An idealization, less unreal than it seems.** The channel is global by construction:
communication without cost, without distance and without encounter. For an agent in a physical
world, that is an idealization, and it deserves saying without detours. But it is not science
fiction: it is the condition our own world has built. We live connected to a network where
notices arrive on their own, wherever we are, without seeking who published them, and what
anyone publishes reaches everyone. The team's board is that condition in miniature, with its
pros and cons measured: the common map that saves the one who goes far, and the deluge of
repetition nobody asked for. Note besides that the idealization makes the results stronger,
not weaker: not even with this perfect connection did the harvest improve, the bottleneck was
elsewhere. What remains untested is local communication: that of those who cross paths, that
of the physical board in the common house consulted upon returning. It is a declared frontier
of this work, and the natural place where the anonymous hive begins to become something else.

**A convergence, offered with prudence.** There is a classic hypothesis about human language,
the gossip hypothesis, Dunbar's, according to which conversation serves above all to maintain
the social map: most of what we say is repeating what is already known, and that repetition is
not noise, it confirms currency. The lock is, without seeking it, a computational miniature of
that idea: we suppressed the communicative redundancy of a hive and the cost was measurable,
the map aged. Nothing more than the convergence is claimed: an agent without language, with a
board of facts, reproduced the lesson that repeating the known is keeping the common fresh.
The formal dialogue with that hypothesis, the citation, what it claims exactly, and where our
miniature falls short, is held in the section devoted to the literature, along with the rest
of this work's relatives.

---

## 6. The price of thinking

The adult agent's section left two seeds planted in its final picture. The agent, with age,
repeats an ever larger share of its decisions, from one in three to two in three. And thinking
costs it more and more: the tree of options it unfolds at each tick is, by an enormous margin,
almost all of its computing expense: the tree takes
practically all the thinking time, and the rest of what the mind does, evaluating the forces,
maintaining memory, computing distances, costs so little that, in the tally, it is a rounding.
And the tree thickens until the end of life, so that old age thinks several times more
expensively than youth. An agent that repeats itself ever more and pays ever more to
deliberate: the conclusion seems to write itself. If it repeats so much, remember the answer
and skip the thinking. If the tree fattens, prune it. This section tells the two campaigns
that attempted exactly that, with careful instruments, frozen criteria and all the method's
discipline, and how both ended on the same shore: there was nothing to trim. The price of
thinking was not a waste. It was the organ.

**First campaign: the reflex. The probe.** Before giving the agent reflexes, an instrument was
built to measure whether it deserved them: a shadow that accompanies the entire life noting,
in each situation already seen, "I would have answered this", deciding nothing, touching no
behavior. The shadow censused the complete adult, and its census gave two results that stand
on their own. The first: the tree confirms more than it chooses. In 97.8% of life, the options
the agent compares are worth nearly the same, deliberation ends in a "whatever" that any
reasonable answer satisfies, and the genuine decision, the one where choosing badly would
truly cost, is barely 0.3% of the ticks. The second: routine emerges with maturity. The shadow
recognized one third of the young agent's situations and three quarters of the old one's. The
reason is of life, not of program: the young one still discovers, and every day brings it new
situations; the old one already has its world made, the same wells, the same routes, the same
home, and the same world produces the same situations. Life becomes repeatable with nobody
programming the repetition.

**The command, and its three refutations.** With that census, the natural step: let the reflex
decide what it recognizes and reserve the tree for the new. It was built with every prudence,
the reflex only spoke on flat ground, anything doubtful always to the tree, and it failed
three times, each refuting a different hope. The first was the most instructive of the work:
two identical runs, same image, same world, same configuration, and one got pinned forever,
oscillating before its own home in a sway it never left, while the other lived a clean life.
The failure was not deterministic: it was a coin toss of machine randomness. The second
refutation tried the geographic cure, banning the reflex near home, where the sway had
appeared, and the sway simply moved: a hundred and fourteen severe loops in open field. The
failure's class was not a place. The third tried the common-sense cure, firing the reflex only
if the action brought the target closer, and neither: sixty-six loops with the target flipping
between two adjacent cells, the agent orbiting between two equivalent desires.

**The ceiling, and the finding with a name.** The question the three refutations leave on the
table is the right one: and what would happen if it worked? A reflex that gets 91% right,
ours, sounds like having almost the same agent, somewhat cheaper. It is not, for two measured
facts. The first: in this system, a different decision does not stay an anecdote, it
propagates. The method already told it with its example: a single different action at tick 13
came to decide, two hundred ticks later, whether a junction was reached in time. A reflex
answering differently from the tree in one of every twelve decisions does not produce "almost
the same life, slightly worse": it produces another life, and, benched, one that loses. The
second fact is the lethal one: the remainder the reflex misses is exactly the medicine. That
small variation of the tree at the tie, the tremor: nothing trembles in the body; the answer
trembles, was what we had spent eras cursing as noise, and it turned out to be the agent's
immunity. In a perfect tie between going north or south, whoever always answers the same
rebuilds the same tie at the next step, and repeats the sway forever; whoever some time
answers differently, gets out. The reflex, answering always the same to the same, freezes
precisely the loop's exit, which is why its benches did not yield a slightly worse agent: they
yielded agents pinned before their door until death. And where does that remainder no reflex
can get right come from? The probe measured it. It reduces every situation to a signature, the
snapshot a reflex would see: what is around, what is carried, what hurts, and when the same
snapshot reappears in life, it asks: did the tree answer the same as last time?
Only 92.65% of the time. Not because the tree throws dice, it is deterministic, but because
two moments with the same snapshot are never entirely identical underneath, and at the tie the
choice is settled by details the snapshot does not see. That 92.65% is, by construction, the
ceiling of any memory of answers: if not even the tree itself agrees with itself more than
that, no copy that looks at the snapshot can imitate it better, one cannot cache a truth that
does not exist. The reflex reached 91%: it was not bad; it was that the target did not exist.
And from there the finding that names the campaign: the coin was the mechanism. The command
was retired whole; the shadow lives on as what it always was, a measuring instrument.

**Second campaign: the scalpels.** If one cannot remember, perhaps one can trim: the tree
fattens with age, prune what goes unused. This campaign premiered its own instrument, a
reading microscope: before building any pruning, it was measured over 1.3 million real tree
expansions exactly what each candidate criterion would cut. And even so, with the prior step
in green, the three scalpels that were tried found the same thing. Committed execution, not
re-deliberating while executing an already committed plan, came out neutral to behavior, the
agent's life came out identical, decision by decision, and with no prize on the clock: the
same time per step. The why deserves its own paragraph: its defeat, as will be seen, was not
the agent's fault but the laboratory's in which it is measured. The first cone, pruning the
branches that move away from the target, had no sweet spot: at 48, at 22 and even at 4 percent
pruning, the score always fell, and its forensics found the why: the branches "moving away"
were conquest's radar, the roundabout routes toward the secondary junctions, the ones the
agent takes when the main one is served. And the second cone, the principled one, pruning only
what geodesy declares a true detour, its prior step verified in green, fell too, and its fall
wrote the final law: the thickening tree is not accumulated fat; it is reach. Late life thinks
expensively because it conquers far, and to geld the tree is to geld exactly the conquests
that demand navigating.

**Where each wall lives.** It deserves saying before adding up the defeats, because not all
have the same address. The reflex's and the cones' are walls of the agent: removing the tremor
creates the loops, gelding the tree gelds the conquest, that would happen in any world.
Committed execution's is a wall of the laboratory. This village is measured in a synchronous
world: the eight agents cross each tick together, and each step's clock is set by whoever
takes longest to decide. Picture it with robots: eight bodies in a plant where none takes its
next step until the slowest has finished deciding its own. To the eye, a waste; as a
laboratory, it is the condition that makes a whole life auditable, step by step. In an
asynchronous world, each body would go at its natural pace, whoever faces the hard would think
slowly, whoever does the easy would run light, and there the conditional savings of each head
would indeed be collected. That waiting is a choice of the method, not an imposition of the
game, the real tournament pushes, and an agent that thinks in seconds would live there like a
statue; the laboratory waits on purpose, so that a deliberative agent can live its whole life
and be audited. The price of that choice is that on the wall clock only what accelerates all
eight at once counts. And the commitment's saving exists, each agent skips the tree in a
quarter of its ticks, but it is conditional and desynchronized: all eight coincide in being
committed only two ticks in every thousand, and in a synchronous collective what does not
coincide does not add. In another world, asynchronous, single-agent, or one where compute were
billed per head, that same piece would pay. All three walls are reported; each with its
address.

**The section's thesis.** Four attempts, one reflex and three scalpels, each with its
instrument, its frozen criterion and its bench, and four defeats that, looked at with the
address in view, split like this: three belong to the agent, and one to the world in which it
is measured, this synchronous laboratory. The agent's say its deliberation is irreducible from
both flanks: it cannot be remembered, because the re-posing's variation is its immunity
against the loops; it cannot be trimmed, because the tree is its navigation. The laboratory's
says the synchronous clock pays no conditional savings, a truth of the measured team, not of
the agent that composes it. What looked like waste, the 97.8% indifference, the tie's tremor,
the thickening tree, turned out to be, piece by piece, the organ at work. It is a negative
result, and it is reported as such; but it says something positive about this architecture: in
an agent whose entire behavior emanates from a single geometry, no slack was left between
thinking and doing in which to put the scissors.

**What remains open.** Buried lies one concrete hypothesis: that of thinking less. Still open,
and another class of work, is that of thinking more cheaply: that the same tree, with the same
decisions, cost fewer machine-seconds through improvements of pure implementation. None of
this section's laws forbids it; no behavior would change. And the shadow instrument lives on,
off by default, ready to census the agent whenever a question deserves it. The frontiers
section gathers both.

---

## 7. The family

This work has two families, because it does not walk alone. The model's relatives, the
theories from which the geometry descends and with which it argues, were presented in the
engine, the first part of this series, and what is said there is not re-litigated here:
homeostatic reinforcement learning as the closest formal precursor [4], and the free-energy
and active-inference frameworks as the most ambitious neighborhood, with their similarities
and differences measured there sentence by sentence. Whoever wants that map has it in the
first work. Here are presented the relatives the agent, not the model, has earned along the
way.

**The gossip hypothesis.** The village chapter ended by offering a convergence with prudence,
and this is its formal home. The hypothesis, due to Dunbar [3], holds that human conversation
serves above all to maintain the group's social map, that most of what we say is repetition of
the already known, and that this repetition is not noise but maintenance: by repeating it, we
confirm it still holds. Our lock experiment, suppressing the communicative redundancy of a
hive and measuring the cost, works, without having sought it, as a computational miniature of
that idea: with repetition removed, the common map aged and the collective paid in steps. The
convergence is offered with its limits in view, and they are large: our board carries facts in
a fixed format, not conversation; there are no bonds to maintain nor individuals to know; and
the aging result is from a single run, declared. We do not claim the village confirms Dunbar:
we claim that a collective without language, upon losing its redundancy, exhibited the cost
the hypothesis predicts for ours. If this class of agents matures, a system this small and
auditable could serve as a measuring instrument for questions in that field. For now, it
stands as what it is: a recorded coincidence.

**The agents that maximize.** The dominant family of agents in worlds like this one is
reinforcement learning: a reward function, millions of training episodes, and a policy that
emerges optimizing the prize. This agent is of another species, it carries no reward, does not
train, and its behavior emanates from a geometry published before touching the game, and it is
worth saying with equal care what that difference claims and what it does not. Priority is not
claimed: the idea of governing agents by internal regulation instead of external prize has
lineage, the motivational architectures of the nineties [5] already governed artificial
creatures by drives and homeostasis, with survival as primary goal and no prize to maximize,
and homeostatic reinforcement itself is the formal bridge between the two families. Efficiency
is not claimed: we have not measured this agent against one trained in its same world, and
this work does not hold that it would win. What is claimed is more modest and stands entirely
on the previous sections: that the combination, fixed geometry published beforehand, zero
training, zero reward, and a complete life audited piece by piece, produces an agent that is
viable, economically competent and socially functional in a competitive world its author did
not design. The contribution is existence, demonstrated and documented, not superiority.

**Habit and deliberation.** The price-of-thinking section dialogues, without having planned
it, with a classic discussion of behavior [6]: the division of labor between a deliberative
system, slow, flexible, planning with a model of the world, and a habitual one, fast, rigid,
answering from memory. It is worth saying first where this agent stands on that
map: it does not have both systems. It is pure deliberation, a single planner that unfolds and
chooses at every tick, and the balance of forces that feeds it is not a habit: it values, it
does not remember answers. The reflex experiment was, in those terms, trying to add the
habitual system it did not have, and what was measured is that here they could not even
coexist: the frozen habit builds loops from which the deliberative one is immune by its own
variation. That is the empirical footnote this work leaves in that discussion, with the
particularity that makes it legible: the two systems shared exactly the same criterion of
value, so the failure could not come from them wanting different things, it came from
constancy itself. We do not raise it to theory; it stays where footnotes serve, within reach
of whoever works that frontier in larger systems.

**The map, closed.** This work's family, said in one sentence: it descends, on the model's
side, from homeostatic reinforcement and the motivational architectures; it coexists with
reinforcement learning as a distinct species, if a name had to be given: a homeostatic agent
of published geometry and zero training, without competing with it; and it touches, without
having sought them, two neighboring discussions, the evolution of language and habit versus
deliberation. It is a small family, and it fits whole on this page.

---

## 8. The frontiers

This last section is the map of the agent's limits. Every limit is measured, has its why in
the architecture, and several carry their door declared, where one would exit, if one wished
to exit.

**It barely explores.** It is the deepest frontier, and now it is said with its measured
nuance: the catalog carries a residual pull toward the untracked frontier, the weakest in the
table, almost always eclipsed by any desire with a name, but no imperative. Exploration exists
as residual force, not as mandate: the agent pursues what it saw or what it was told, and what
never entered its sight nor the board barely exists for it. In the eight-agent examination, a
junction four cells from home went unseen by seven of them across entire lives. Adding a
curiosity force is easy to say and demanding to do, it would be the first force answering
neither a pain nor a present opportunity. It could be imagined another way, and it is worth
leaving said: treating ignorance itself as a pain, information as one more resource, whose
lack hurts in the resource domain, which is where a resource lives. That form speaks the
model's grammar as it stands, three domains, and no new one, and the pending work belongs to
this layer: giving that pain a height and setting it to compete in the catalog. The door
stands declared and closed.

**It knows no one.** All the agent's social life happens in anonymity: bodies occupying cells,
notices with no author. There is no census of individuals, no memory of who said what, no
possibility of treating the one who helps differently from the one who hinders. This work
showed how much cooperation fits inside that anonymity, the common map, the life saved, the
junction a teammate takes first, and precisely for that it leaves measured the baseline of the
next question: what does the representation of the other add to a collectivity that already
works without it. That question is another work, and it begins where this one ends.

**It has lived in a single world.** All of this work's results are from machina_1, and several
carry the condition worn in the sentence: the harvest does not depend on the channel *in a
world where ammunition comes as standard*; the synchronous clock pays no conditional savings
*in this laboratory*. Nothing has been measured in another game, with another economy, with
another census of agents. The architecture, the translation layer plus the constancy rules, is
written to be ported; portability, however, is a promise without a bench, and here what was
not measured is not claimed.

**It knows how to return, but not how not to go.** The return cure left deaths by bleeding at
zero, and it also left, named, its residue: the case of the agent that pushed so deep into
hostile territory that no return rule could save it, because it needed more life than fits in
a body. The return is solved; the prudence of not pushing so deep, not. It is a small corner,
one case in ten in its day, a marginal loss in the complete life, and it stands declared as
what it is: the only death this design does not yet know how to prevent.

**It has a ceiling, and it is its own.** The adult agent sustains around seven junctions
against the constant siege, and expands no further: its cradle ammunition runs out with the
life. The piece for making more exists and stayed in the drawer with its measured reason, its
moment would be a life longer than the measured one, which the game, in fact, offers: it was
this work's protocol that bounded the window. The extrapolation to the league horizon is
arithmetic and is declared: at ten thousand steps, the cradle endowment is insufficient, the
siege would demand on the order of twenty-five to thirty-five reconquests, and the agent would
not die: it would go bankrupt. Heart manufacturing, existing in the world, absent from its
repertoire, is the piece that horizon would demand, and it stays in the drawer with its
condition quantified. Just like the eight temperaments, implemented and switched off: this
work's team is a team of equals, and the question of what the variety of characters does
remains intact, its table ready.

Lives, besides, were not only counted: they were watched. A replay viewer built from the logs
themselves allowed the whole median run to be reviewed visually, and the most striking case, an
agent still for about three quarters of its life, next to home, turned out to be exactly what
the design predicts: documented satiety, the desire engine silent since tick 157, no task
pending, healthy and at home. Rest, not a jam: across the eight agents not a single case of a
desire failing to land was found. The viewer remains as audit material alongside the rest of
the evidence.

**It thinks expensively, and that is no longer a frontier: it is a result.** The
price-of-thinking section buried the hypothesis of thinking less, from both flanks, with four
measurements. That of thinking more cheaply, the same tree, the same decisions, fewer
machine-seconds, was tried afterwards, and it left one piece and one wall. The piece: reusing
a reading job the cycle itself did and discarded bought 9.5% of speed with the agent's life
identical tick by tick, not one number in this work moves. The wall: it was measured whether a
faster machinery could execute the same computation with exact fidelity, and it cannot, in one
of every two thousand five hundred inputs, the last bit differs. The published reference lives
in its machinery; truly accelerating it would demand re-founding it, another reference,
another baseline, another work, and that door stands declared and closed. And a second door
remains, which the price-of-thinking section left drawn: one of the four walls belonged to the
laboratory, not to the agent. In an asynchronous world, or one where compute were billed per
head, the conditional saving of committed execution, which here does not add because the clock
is set by the slowest, would indeed pay. Thinking more cheaply has, then, two roads: better
plumbing in this world, or another world. And a tool remains in the code, worth explaining
because it will be used again: the shadow instrument the price-of-thinking section presented.
It is an observer that accompanies a run taking notes, at each situation it writes down what a
reflex would have answered, how much the agent repeats itself, where it hesitates, deciding
nothing and touching not a single action. Off, its default state, the agent is exactly the
usual one. On, the life does not change either: it merely gets censused. If a future question
needs that census, the instrument is ready, it is switched on, measured, and switched off
again.

**The word travels free.** This work's board is global: no cost, no distance, no encounter.
The village chapter declared it an idealization and measured what it gives and what it costs.
Local communication, that of one crossing another, that of the physical board at home
consulted upon returning, remains untested, and it is the frontier where this work's social
side and the question of the other touch: encounters are, among other things, the occasion to
learn who is
who.

**The closing.** The biography stands delivered: a published geometry, a body executing it in
a hostile world, a method with its criteria written before looking, and this map of limits
with every door in view. And it is worth saying slowly why the map closes the work instead of
shrinking it. What the agent does was measured in the central sections: it lives, supplies,
conquers and cooperates, with no prize to chase, no training to mold it, no rules but those
declared one by one. What it does not do was measured here with the same instruments: it
barely explores, it knows no one, it has lived in no other world. A result without its limits
forces the reader to guess them, and the guessed always tends to be more generous than the
measured. A result with its limits says exactly what is claimed, how far, and what remains to
be won. That is why the two halves do not subtract: they need each other. What this agent does
and what it does not do, together, are the work.

---

## Figures

**Figure 1 (GIF).** The crossing into own territory. The same agent that in the control runs died
bleeding out thirty-eight cells from its home, with the unbreakable route active returns badly
wounded —its life falling to twenty-two— and at tick 923 crosses into its own territory, where it
regenerates to full. The nuance the image fixes: the cure heals on stepping onto its own ground,
some twenty-one cells from the hub, not on touching the hub. Frame by frame, generated from the run's data.

**Figure 2 (GIF).** The landing. An equipped porter reaches a junction, enters and spends its
ammunition, the behavior the system never produced until the conquest commitment.

**Figure 3 (GIF).** The one that wanders far, in the mute run. With the board off, the agent
that explores far from home with only its eyes starts back late: its return alarm fires at
t2210, twenty-one ticks before its death, 42 cells from home, in rival territory, draining
around 2 life per tick. It closed 19 cells and died at t2231, some 23 from home, still outside
its territory: halfway, not at the threshold. The alarm rang when no life was left to answer
it, the life the channel, switched on, saves. Identical in all three mute runs, which are
deterministic.

*The three GIFs accompany this document as supplementary material.*

## Acknowledgments and assistance statement

This work was developed with the assistance of Anthropic language models (Claude), used as a
tool on three fronts: the agent's mathematics and programming, the execution and verification
of the experiments, and the writing of this text. The method of Section 3 was applied to that
collaboration as well: every cited number comes from a results file and was verified against
its source, and no claim rests on the model's memory. The design of G-EMV, the decisions of
this work and the responsibility for everything written belong to the author.

## References

[1] Enrico, M. (2026). *G-EMV: A Geometric Architecture of Homeostatic Orientation for
Agents.* Zenodo. DOI 10.5281/zenodo.21026795. (The engine: first part of this series.)

[2] Softmax. *Cogs vs Clips* (Coworld / CoGames), multi-agent environment of the Alignment
League Benchmark. https://softmax.com, code: https://github.com/Metta-AI/coworld-cogs-vs-clips

[3] Dunbar, R. I. M. (1996). *Grooming, Gossip and the Evolution of Language.* Harvard
University Press.

[4] Keramati, M., & Gutkin, B. (2014). Homeostatic reinforcement learning for integrating
reward collection and physiological stability. *eLife*, 3:e04811. DOI 10.7554/eLife.04811.
(Antecedent: Keramati & Gutkin, NIPS 2011.)

[5] Cañamero, D. (1997). Modeling motivations and emotions as a basis for intelligent
behavior. *Proceedings of the First International Conference on Autonomous Agents*, ACM Press.

[6] Daw, N. D., Niv, Y., & Dayan, P. (2005). Uncertainty-based competition between prefrontal
and dorsolateral striatal systems for behavioral control. *Nature Neuroscience*, 8(12),
1704–1711. DOI 10.1038/nn1560.
