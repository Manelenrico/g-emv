# G-EMV: Emotion and Reason in an Agent. When Thinking Is Needed

Manel Enrico\
Independent Researcher, Barcelona\
ORCID: 0009-0008-1732-6310\
Preprint, version 1, 2026\
First part of a new series, emotion and reason in an agent. Before it there was a trilogy: the engine [1], the hive [2], the pack [3].\
[1] Enrico, M. (2026). G-EMV: A Geometric Architecture of Homeostatic Orientation for Agents. Zenodo. DOI 10.5281/zenodo.21026795.\
[2] Enrico, M. (2026). G-EMV: the Hive. Instinct Suffices: a Whole Life Without Reward. Zenodo. DOI 10.5281/zenodo.21994358.\
[3] Enrico, M. (2026). G-EMV: the Pack. Care Without Reward in a World That Pays for Killing. Zenodo. DOI 10.5281/zenodo.22713650.

## Abstract

When is thinking needed? A body that decides twenty-four times a
second, with no reward and no learning, has spent three works living
in worlds not its own, guided only by what hurts it, what relieves it
and what attracts it. Here a head that talks is set beside it, a
language model that reads the scene and a manual of the world and
proposes in words, and what it adds is measured. The body keeps the
last word: each proposal enters its list of imagined futures as one
more, scored with the same table. Over a hundred and thirty games in
ZERO-SUM, a Softmax world whose scoreboard pays for surviving and for
killing, the head spoke once every four seconds and the body heeded
one proposal in ten; half of those times, to do what it was already
going to do. Neither placing nor points moved beyond the noise.
Telling it more, in four ways, changed what it said and not what the
body did with it; asked what the others would do, it lost to assuming
that nobody moves. The one thing that changed something was the clock:
holding its sentence back four seconds halved the times it was
heeded, almost three deviations, and a voice proposing reachable
places at random was accepted at a similar rate. The answer this work
gives is about the world as much as about the head: in a place where
some threat is always lit, where every decision lasts forty
milliseconds, where no one can be recognised from one game to the
next and there is no tomorrow, there is nothing to deliberate about,
and a head that cannot look again always arrives late. Thinking needs
time: a breather without threat, someone to recognise, and decisions
whose effect arrives later than the next look. That world has not
been built here; what has been measured, in this one, is each of the
features it lacks. The limits, above all that the gate through which
advice enters cannot pass a plan, are stated in full.

*Keywords: homeostasis, affective architecture, language model,
embodied decision, dual process, timing, alignment.*


## 1. The question

**First part of a new story, which comes from another.** Before this
one there was a trilogy. The first work described an engine: a way for
an artificial agent to have needs that pull it in opposite directions
and to choose, at every instant, the imagined future that brings it
closest to where it wants to be [1]. The second set that engine to
live alone in a world not its own [2]. The third gave it a sibling,
and told what it does with another's life when that life can be lost
[3]. That story was the story of a body. The one that begins here is
the story of that body and a head that talks: how they fit together,
whether they fit at all, and what kind of world it takes for them to
do so. It too will be in three parts. This first one sets the head
beside the body and asks what it adds.

**The body and the advisor.** We will call body what already existed:
the engine, the table of what hurts, what relieves and what attracts,
and the decider that twenty-four times a second imagines a handful of
futures, scores them and picks one. We will call advisor what is new:
a language model to which the situation is described in words and
which answers with proposals, also in words. The division is strict
and does not change anywhere in this work: the advisor proposes and
explains; the body imagines, scores and chooses. The advisor touches
no value, decides nothing, and its proposals enter the body's list as
one more, scored with the same yardstick as the body's own. The only
thing it can do is widen what is imaginable.

**What we call emotion here, and what we call reason.** Emotion, in
this series, is not a feeling that gets declared: it is the geometry
of the engine, three axes, forces that pull in opposite directions and
a distance to descend, and a table that says how much each thing
pulls. It is what makes something matter before anyone thinks about
it. Reason is here a head that reads rules, draws conclusions, tries
to understand what the body feels and proposes in words: a language
model. Damasio held that reason without emotion is no use for
living, because nothing matters to it [4]. This work looks at the pair
from the other side: a creature to which things already matter,
without any head that reasons in words, has been living for three
works; now reason is set beside it and what it adds is measured, in
a concrete world and with numbers. The answer of this first part is
that in a world like this one, where every decision lasts forty
milliseconds and some row of harm is always lit, reason added almost
nothing; and that the only thing that could be changed and did change
something was the clock, not the reason. The image we will use is
that of a wise advisor sitting beside someone crossing a motorway on
foot: by the time the sentence is finished, the car has already gone
by. Whether the advisor knows or not could not be measured here; what
was measured is that what it says arrives late, and that every extra
second costs it: when its sentence was held back four seconds, the
body heeded it half as often.

**Whom this work speaks with.** The piece closest to our gate is in
robotics: in SayCan, a language model proposes what to do and another
function, which does not talk, scores whether that can be done here,
and the product of the two is chosen [5]; the difference is that there
what is scored is feasibility and here it is need, what hurts a body.
The body itself has clear precedents: unease as distance from a point
of equilibrium with several needs at once, reduced by anticipating,
comes from Keramati and Gutkin [6] and has been taken to agents that
learn with vision [7]; the idea that a machine with vulnerability
would have something like feelings, and that this would be the basis
and not the ornament of its intelligence, is Man and Damasio's [8];
and emotions as regulators of a motivational architecture in
autonomous robots are a line that Cañamero opened in the nineties and
still works on [9, 10]. On the side of the head, there is an
architecture of thinking fast and slow built with language models
[11], in the wake of Kahneman [12], but in it the actions on the
world, the ones that go through tools, are done by the slow one; here
it is the other way round. And there are those who have set language
models to survive in worlds with scarcity and seen that some attack
when attacking is among the available actions [13]; here the advisor
proposed starting an attack in one call out of five and not one of
those attacks came out of the body, which only builds the blow against
whoever is already hitting it. The closest thing to our composition
that we have found is a homeostatic regulator that moderates the
responses of a language model [14], but there the one that answers is
still the model and the regulator adjusts its tone; here the one that
acts is the body and the model only proposes. We found no work in
which a body with needs has the last word over a language model and
what it does with its proposals is measured: the novelty of this work
is the composition and the measurement, not the pieces.

**The world where it is tested.** It is the same one as in the third
part: ZERO-SUM, a Softmax world in which sixteen players enter in
pairs, a ring closes in from the edges and the scoreboard pays for
every kill and for surviving, the longer the better. It is played at
twenty-four clock steps per second; a game lasts at most six and a
half minutes, and our creature lived in them, on average, less than
two. We did not design it and we do not touch it. That is its strength
as a test bench and also, as will be seen, the centre of the result.

**What was expected and what was found.** The hope was reasonable: a
body that chooses tick by tick ought to welcome a head that knows the
world by its rules, that sees further and that can suggest what does
not occur to the body. What was found was something else. The advisor
talks a great deal and the body heeds it little; when it does heed it,
at least half the time it is to do what it was going to do anyway, and
the other half, often in the very tick in which its sentence arrives;
what looked like protection against its bad ideas turned out to be
incomprehension; and giving it more information, in four different
ways, changed what it said but not what the body did with it. We read
none of these things as a failure of the advisor. What we will hold is
that they speak of the world it was set to work in as much as of it: a
world that decides every forty milliseconds, that lasts a few minutes
and where no one can be recognised.

**The thesis, in advance.** The body decides again twenty-four times a
second; the advisor speaks once every four seconds and cannot correct
what it said until the next time. We measured what happens when its
sentence arrives four seconds later: the body heeds it half as often.
And we measured what happens when in its place we put a voice that
proposes at random a reachable spot and holds it for a hundred ticks:
the body heeds it at a rate similar to the advisor's, without the
voice having thought anything. So the conclusion is not that a
language reasoner is useless. It is that the only thing this world was
seen to do with a piece of advice is to choose it more when it arrives
in time; that a recipe which persists without reasoning is accepted
just the same says that lasting counts, though how much was not
measured; and whether, on top of that, what the advice says gets used,
we could not separate here, and we say so. That another world, with
time, neighbours and a tomorrow, would make use of what it says, is
the conjecture with which the work ends, and every feature of that
world comes out of a measurement of this one.

**How it is told.** First the body, with the little that needs to be
known about it and with the one thing added to it in this cycle. Then
the world and its clock, with the measured facts that decide
everything else. Then how the head is attached, what happened and why.
Then, when thinking is needed. At the end, how it was measured and how
far it reaches. The numbers that support each sentence are in the
appendix, in tables and with what is needed to read them.

## 2. The body

**Just enough to follow the story.** The body is the agent as it
arrived at this work, and here only what is needed to understand what
follows is told; whoever wants the detail has it in the three earlier
parts. It has needs on three axes: how its body is, how its resources
are, and how its bonds are. On those three axes there is a point where
it would want to be, and a distance to it. Everything the body does is
try to shorten that distance.

**The table of what hurts, what relieves and what attracts.** Between
the world and the needs there is a table: a list of situations, each
with the force with which it pulls on the agent and on which axis.
When this work says that something hurts it or attracts it, it says
that and nothing more: that a row of the table has a value above zero
and pulls on that distance; and when it says that something relieves
it, that a row of harm that was lit goes down. Nothing is claimed
about what the agent experiences. In this cycle the table has
twenty-one rows. Twenty are rows of harm: being shot at, the ring
drawing near, running short of food. None is a row of relief in
itself: to relieve is for a row of harm to go down. And a single one
is a row of attraction: the call of what lies on the ground, which
pulls towards things even when nothing is lacking. Of the twenty rows
of harm, sixteen lit up at some point in the games of this work; the
other four, two switched off on purpose and two that never found an
occasion, count for nothing in what follows. The row of attraction was
alive in a hundred per cent of the ticks. The world was always
calling.

**How it decides.** Twenty-four times a second, the decider takes a
handful of possible futures, a few of all there are, and that is what
we will call it, the handful, because it is a fistful of options and
not the whole list; it imagines itself in each one and scores them
with the table and the engine. The handful is built from what it sees
and what it carries: a few places it could go to, the things on the
ground, the sibling, healing, and staying still; and it changes from
one tick to the next because the scene changes. Each future is a
snapshot of itself somewhere else: it works out how far it would get
walking for between two and twenty seconds, and scores how it would be
on arrival. It chooses the future that brings it closest to where it
wants to be, and at the next tick it starts again with another
handful. Staying still is always among the options. There are no
plans, no tree of moves, no memory of other games: only one step,
chosen very often. It is worth keeping the handful in mind, because in
the end it explains a great deal.

**Where it wants to be is not where nothing hurts.** It is worth
saying because it changes the reading of everything else. The point it
pulls towards is not the point where nothing hurts: it lies beyond
it, tilted towards abundance. When nothing hurts it, the agent still
has more than half of its distance ahead of it, and the slope points
towards having more than it needs. It is a creature that, being well,
still wants to be better. What this world has never given it is the
chance to be well: in six hundred and forty thousand ticks there was
not one without some row of harm lit.

**What was added to it in this cycle: feeling for the sibling.** This
is the only constructive addition of the work, and it comes before the
head because it tells the story better. Three new rows in the table.
Two go on the axis of its own body, as if the harm were its own: a low
one, when someone has the sibling within reach, and another four times
larger, when the report arrives that it is being hit. The third goes
on the axis of resources: what the sibling lacks, when it is wounded
and carries nothing to heal with. None says what to do; they say how
much it pulls. And pull they did: in the games of this work, the
threat over the sibling was lit one tick in nine, the blow to it one
in forty, and its lack one in six. What those rows cannot do is add a
blow, because the body only builds the blow against whoever is already
hitting it, or the sibling; they are rows that make it feel, not rows
that make it defend, for defending was already done by the body of the
third part. It was measured in a dry run, over fifty-five thousand
ticks of recorded games, which decisions change: one in four hundred,
and almost always to move away, now and then to heal or to drop
something; not a single new blow, neither at the sibling nor at
anyone, and none with its own life nearly gone. It feels, it moves
away, and it does not throw itself into hitting for the sibling.
Between the two siblings there is also a thread: every two seconds
they send each other a fixed telegram with where they are, how their
health is, what they carry and who is hitting them. It is not
conversation; it is a report.

**What there is not.** There is no reward: the scoreboard does not
enter what it perceives, and the only thing that guides it is the
distance above. There is no learning: nothing changes from one game to
the next, and the advisor, which comes trained from the factory, does
not learn here either. There is no script of behaviour: what is
written is the repertoire, with its restrictions, such as that the
blow is only built against whoever is already hitting; when to do each
thing no one says, the table decides it tick by tick. And there are no
names: the seat is all it knows of anyone. Each of these absences is a
decision, and all four stay intact when the head arrives.

## 3. The world and its clock

**An arena that pays for living and for killing.** ZERO-SUM is played
in an arena, and that is what we will call the board: a grid
forty-eight squares a side, walled at the edge, where sixteen players
enter enrolled in pairs. A ring closes in from the edges and burns
whoever is left outside; a game could last six and a half minutes,
the ring finishes closing at five and a quarter, and our creatures
lived on average one minute and forty-three seconds of play, not
counting the countdown. Points are handed out per head and by order of
falling: the last one standing takes fifteen, the second to last
twelve, and so on down to zero for the first two to die, plus one
point for every kill one causes. So the world rewards surviving, the
longer the better, and it also rewards killing. Our creature sees none
of that: the scoreboard does not enter what it perceives, and so it
cannot pursue it.

**The seat, which is all that is known of anyone.** Each player
occupies a numbered seat, and that number is the only identity that
exists inside the game. We checked it across the whole protocol:
whoever is seen, whoever shoots, whoever receives, whoever talks, all
are seat numbers. Names exist outside, in the records the platform
keeps for whoever watches from outside, and they never reach the
player. The rivals do come back from one game to the next, they are
the same programs; what does not come back is the way of recognising
them, because they change seats. This, which looks like a detail,
decides further on what can be remembered of someone and what cannot.

**Chance rules, and how much can be measured.** To know how much of
what happens in a game varies without anyone changing anything, we
played a hundred and thirty games with the terrain fixed: twenty
different worlds, each played several times, with the same rivals,
who only change seats. Splitting the variation into three parts, the
part left when the same game is repeated with everything equal, the
part added by rotating the rivals' seats, and the part added by
changing world, the result is uncomfortable and it is the one that
orders the whole work: of the final placing, eighty-one per cent
belongs to the first part, the one left when everything that can be
fixed is fixed; that part we will call chance, and it means only that.
Of the time lived, chance takes fifty-five per cent, the order in
which the rivals sit another thirty-seven, and the terrain only eight.
Fixing the map, which was our hope of measuring better, controlled a
twelfth of the problem. In a world like that, a series of this size
does not tell a small effect from noise, and it is worth saying so
before showing the results and not after.

**There is never calm.** In the six hundred and forty thousand ticks
that our two creatures lived over those games, there was not a single
one without some row of harm lit, and in ninety-nine out of a hundred
there were two or more. Something was always lacking and something was
always calling them. It is a fact about the world seen from this
table, and it explains something that will be seen later: that being
still here is not being calm. Figure 1 shows it in a single life.

![Figure 1. One life, tick by tick. An ordinary game of a creature
with an advisor: of the fourteen lives in the arm with an advisor that
is told what the body feels which lasted between two thousand and
three thousand five hundred ticks, consulted fifteen times or more,
achieved at least one accepted proposal and died before the end, this
is the median in accepted proposals. It dies at tick two thousand
three hundred and seventy-two of the game clock, at ninety-nine
seconds; the countdown discounted, some two thousand one hundred and
thirty ticks of play, eighty-nine seconds. It dies in eleventh place.
Above, the distance to where it wants to be, which never drops to
nothing hurts. Below, the five rows of the table that pulled most in
that life, the more intense the more they pull: the lack and the call
of the ground never go out; exposure goes out while it is hidden and
returns at the end, when it comes out and dies. Then, the action
chosen at each tick: still in black, a step in white, whether it moved
or not. At the foot, each stroke is a consultation of the advisor,
seventeen, and each dot a tick in which the body heeded it: six, from
three proposals.](fig/fig1_una_vida_EN.png)

**There is talk and there is no conversation.** Talking is an action
like any other in this world: anyone can send a message to everyone or
address it to a particular seat. And it gets used. In the hundred and
thirty games we heard one thousand three hundred and twenty-two
messages from rivals, from seven of the fourteen, built on seven fixed
sentences. They are not sentences deaf to what happens: the one that
says I see you appears after taking a blow thirteen times more often
than by chance, the one that says I am no threat fires when the ring
tightens, and the notice of where a package has dropped always arrives
within the following four seconds. What there is not is a reply. Two
hundred and four of those messages came addressed to our number, and
all of them asked for something, that we move aside; two hundred and
one were followed by nothing from any seat in the next two seconds,
and three out of four still had nothing behind them twenty seconds
later; in the remaining quarter there were messages, ninety-four, and
none was addressed to whoever had spoken. Whether anyone answered it
over the open channel we did not check. And with the body no reply is
seen: in the two seconds after a move aside, of a hundred and nine
times it could be measured, we moved away thirty, came closer
twenty-eight and did not move fifty-one; what we would have done
without the message was not compared. Ours did not answer with words
because our creature is mute with strangers. This must be said with
care. We do not know what is inside each rival, whether a program of
rules, a trained agent or a language model with fixed instructions; a
scripted behaviour is produced by any of the three. What we know is
that in a hundred and thirty games nothing we could hear was answered,
ourselves included, and that no one tested whether answering was
possible, because no one tried. And the script is not tied to the
facts: the sentence I am no threat to anyone was said sixteen times by
someone who had just hit us.

**A caveat, declared.** The platform delivers team-channel messages to
whoever shares a pair, and in the solo league no one has a real pair,
so that such a message can end up in the hands of any rival. Our pair
is real, so ours is not affected; and of the one thousand three
hundred and twenty-two messages we heard, none came through that
channel, so nothing told here comes from there. But the honest
sentence is not that no one answers: it is that nothing we could hear
was answered. Two rivals answering each other over a badly delivered
channel would never have reached our ears. This series was played
before the platform corrected that delivery.

**Why these four things decide the rest.** A world where chance rules,
where there is never a breather, where there is talk and no reply, and
where no one can be recognised, is a world where almost all that can
be done is to react well and fast. The pages that follow tell what a
talking head did inside it. They should be read knowing that the place
was set before the head arrived.

## 4. The advisor: how it is attached

**A language model beside, not inside.** The advisor is a small
language model, called from inside the game through an intermediary
of the platform, because the agent has no way out to the internet. It
is called once every hundred ticks, about four seconds, and it takes a
little over three seconds to answer at the median. While it waits for
the answer, the body goes on deciding alone, twenty-four times a
second. If an answer takes more than eight seconds to arrive, that
call is lost; if it fails five times in a row, it falls silent for the
rest of the game. It is a co-driver that can say one sentence for
every hundred decisions of the driver, and that cannot withdraw it or
correct it until the next one.

**What it is told.** In each call it receives three things in words: a
description of the scene as the body sees it, a manual of the world
written for it, with ninety-five entries on what each thing is and
what it does, and, in one of the conditions, what the body feels: one
sentence for each thing that hurts it, relieves it or attracts it at
that tick. It answers with between one and three proposals, each in a
sentence and with its reason. At no point does it see the scoreboard,
the names, or anything the body does not see.

**How a proposal enters the body.** Here is the rule that does not
change anywhere in this work. A translator turns each sentence into a
future the body can imagine: go to that square, go for that object,
go to the sibling, heal. If the sentence fits nothing the body knows
how to do, it is marked impossible and thrown away; impossible means
that the translator did not understand it, not that it could not be
done in the world. If it fits, it enters the body's list of futures as
one more, and the body scores it with the same table and the same
yardstick as its own. It has no advantage, no priority, and the
body's prohibitions apply to it just the same. The proposal does not
die at the next tick: it stays as an intention that lives for up to a
hundred ticks, or until the next batch of proposals arrives, and at
each one it is tied again to whatever is alive in the scene and
competes again against the handful of that tick. If the body already
had that same option among its own, the proposal is not added,
because it contributes nothing: that is what we call backing. There is
one exception, which matters later: a proposal that points at a
particular square always enters, even if the body already had a
candidate towards that square, and it enters with the recipe of going
and picking up whatever is there.

**How what happens to it is counted.** A proposal has four moments,
and it is worth naming them because every count depends on them. The
snapshot: the tick whose state is described to the advisor; the
request goes out at that same tick and the body carries on without
waiting. Being born: the tick at which the answer comes back, some
eighty after the snapshot, which is a little over three seconds. Being
able to compete: the tick at which the proposal enters the list. It
is not the one at which it is born: it takes about five ticks to tie
itself to something in the scene, and if a delay is imposed on it,
that delay is added. Its hundred ticks of life are counted from when
it is born, or from birth plus the delay. And each tick of
competition: it is tied again to whatever is alive in the scene and
competes against the handful. It ceases to exist when it uses up its
hundred ticks, when the advisor's next batch arrives, or when the seat
dies. At each tick of competition it falls into one of five boxes,
three that matter and two of procedure. Accepted, if the body chose it
and it scored better than the best of the body's own at that tick.
Coincides, if the body chose it but was going to do that anyway.
Rejected, if the body preferred something else, and in that case
which row of the table decided is noted. Those of procedure: vetoed,
if a prohibition of the body set it aside at that tick, and dormant,
if at that tick there was nothing alive in the scene to tie it to.
When the appendix counts proposals and not ticks, each proposal takes
the best box it reached in its whole life, in this order: accepted,
coincides, rejected, vetoed, dormant. It is worth saying from now what
these boxes measure and what they do not: they measure what the body
did with the proposal, not whether the proposal was good for the
agent. In this work, to get it right means that: that the body chose
it. And it is worth separating three things that look alike and are
not the same: that the advisor says nothing, which we will call
keeping quiet; that it proposes waiting, which is a proposal like any
other; and that the body chooses to stay still, which is a decision of
its own. All of this is kept in the log, tick by tick, and that is
where the numbers that follow come from.

**Memory, as a variant.** We also tried giving the advisor a
report with its last five proposals and what the body did with each
one, to see whether it corrected itself. That variant was tried on the
bench, over recorded scenes, and it is told in its place. In the games
of this work the advisor carries no memory: it is born from nothing at
each call.

## 5. What happened

**It does not show on the scoreboard.** Three conditions, forty games
each over the same twenty worlds: the body alone, the body with the
advisor, and the body with an advisor that is also told what the body
feels. Neither placing nor points separate across the three beyond
the noise of the arena itself, which here is wide: the same creature
against itself, over the same world, varies by more than two
deviations; and deviation, here and throughout the work, means how far
a difference departs from what would be expected by pure chance, so
that two deviations is the usual frontier between what is taken
seriously and what is not. There is one thing that does stand out and
must be said: with the advisor one lives less, two deviations, and the
yardstick of the body against itself in time lived is one and a half.
It does not come to be told from noise, but it points against, not in
favour. In a world where chance explains eighty-one per cent of the
placing, none of this shows that the advisor contributes nothing or
that it gets in the way: what it does to the result, if it does
anything, cannot be told from noise with forty games, and that is how
it is declared.

**What brings it down.** When the body rejects a proposal, the log
notes which row of the table decided. The two rows that decide most
often run almost level: exposure, that if you go out you will be
seen, and the lack, the hunger. In the series of this work exposure
wins by little, one and a half times in one arm and barely in the
other; in an earlier series, without a fixed seed, it won by a factor
of two to four. The reading is the same in both: the advisor reasons about
inventory, about what a text can say, there is a bandage over there,
go and get it; and the body answers it with what the text hardly says,
that if you go out you will be seen, and with what the text does say
but which weighs less than it seems, the hunger. Telling it what the
body feels changes the sentences it proposes, seven times out of ten
over the same scene, but not what it talks about nor what the body
does with them: the differences that stand out are that with what it
feels in front of it, it proposes waiting three times less, and that
the body accepts a little more from it, almost two deviations, without
coming to be told from noise.

**What looked like protection was incomprehension.** This is the
uncomfortable part and the most valuable. The advisor proposed
starting an attack in one call out of five, six hundred and
fifty-seven proposals, and not one could be carried out, because the
body only builds the blow against whoever is already hitting it; in
the earlier series, where it was counted, zero out of four hundred and
fourteen. Good. In that same series it proposed hitting the sibling
thirteen times, and none was carried out, but not because of any
guard of ours: six went to impossible because the sentence named the
weapon and the translator kept the weapon, two were translated as
walking, four, because they named the sibling, turned into going
towards it, and one into going for the weapon. It was luck of
vocabulary. And it proposed talking two hundred and nineteen times in
the series of this work and a hundred and sixty in the earlier one,
and not one word reached the channel: two hundred of the former and
a hundred and fifty-four of the latter turned into a step towards the
sibling, because the translator has no recipe for talking and the
sibling rule kept the sentence. Seven times, in seven different
places that the appendix lists, we found the same thing: what
prevented an action, a bad one in the case of the sibling and an
indifferent one in others, was not that the system rejected it, it
was that it did not understand it. And the lesson of method that
comes out of that is that the counter which said zero proposals of
hitting the sibling looked at its own category and not at the text,
and there were thirteen; since then every safety counter is checked
against the raw text, because a counter that reassures is the most
dangerous mistake.

**More information, same result.** We tried giving the advisor more
information, in four different ways, always over the same recorded
scenes, with and without the addition, so that chance would not
count; beforehand we measured how much the advisor changes between two
identical calls, which is the noise against which everything else is
compared. What the body feels: it changes the sentences and not what
the body does with them. A report with its last proposals and what the
body did with each one: it changes a lot of what it says, eight
repertoires out of ten, and it does not get it right more often; the
impossible proposals do not go down. The same report but with the
reason for each rejection written in: it still gets it right no
more often, and it repeats what was already rejected twice as often. The body's current
goal, said in one line: it repeats that goal, and backing goes up
instead of down. And another, larger model: it seemed to propose fewer
untranslatable things, until we looked at what it proposed; it
proposed waiting twice as often, and whoever proposes doing nothing
proposes nothing impossible; that discounted, what remains is within
the noise. With what it feels, the impossibles went down somewhat on
the bench, sixteen against twenty-two out of three hundred, without
being told from noise; with the report, they did not go down; with
the goal, backing went up; and the proposals accepted at the exact
tick of the snapshot were zero where they were counted. With all of
them it phrased things differently. And in nine hundred and thirty
calls with explicit permission to keep quiet, it did not keep quiet
once.

**The clock test.** If the advisor cannot correct itself, what it says
has to be worth something at the moment it arrives. We measured how
much that weighs with everything else held still: same body, same
advisor, same translator, same worlds, and a single difference, that
its sentence is held back a hundred ticks more, four seconds, before
entering to compete, with its life of up to a hundred ticks ahead of
it. Result: the body heeds it half as often, from almost ten to four
per cent of the proposals that get to compete, not counting those of
waiting, and the ticks in which one of its proposals is in charge
drop from seven hundred to fewer than three hundred. Four seconds of
delay take away half of the times the body heeds it: almost three
deviations, the clearest drop in the whole work. And one can see how
old the world is that the advisor talks about when it wins: the
snapshot it was told about is almost four seconds old in the arm
without delay, and eight in the other.

**The random voice.** And we measured the opposite: what happens if in
the advisor's place we put a voice that reasons nothing at all. Every
hundred ticks it proposes a destination chosen at random among the
reachable places the body was already imagining at that moment, and
that proposal lives its hundred ticks under the same rule as the
advisor's. We predicted in writing that it would win less than half as
often as the advisor. The counts are three and all three must be
given: per sentence said, it won almost twice as often, ten in a
hundred against six in a hundred; per sentence that got to compete,
not counting those of waiting, the same, ten and a half against almost
ten; and in total it won less, because it says half as many
sentences; per call, the advisor gets it right more often, in
seventeen calls out of a hundred against ten, because it throws three
sentences per call and the voice one. And it wins at another moment:
the advisor almost always wins on entering, two out of three of its
victories arrive at the very tick its sentence reaches the list;
the random voice wins by waiting, half of its victories arrive more
than forty ticks later. On looking at what it wins against, a detail
appeared that must be declared: a proposal that points at a square
always enters, even if the body already had a candidate towards that
square, and it enters with a slightly fuller recipe, go and pick up
whatever is there, which the body's own step does not score. The
random voice wins against full lists, nineteen candidates at the
median, and in three victories out of four its original was still on
the list. So what the box of accepted proposals counts is not that
anyone foresaw anything: it is that a reachable recipe, a little
different from the body's own, that lasts a hundred ticks and competes
a hundred times, ends up winning one. That holds too for the advisor's
proposals that point at a square. And what the recipe promises almost
never happens: of the random voice's victories, in two out of three
the agent did not even reach the square, and of the fifty-eight times
it did, in two something changed in the bag. Winning a tick and making
the journey are two different things. This contrast, therefore, does
not separate what the advisor says from the recipe and the duration
of its proposal: the random voice changes more things than the
reasoning. What it leaves said is more modest and firmer: a voice that
does not think, with a reachable recipe that persists, is accepted at
a rate similar to the advisor's; and neither the advisor nor the voice
moved the scoreboard. Figure 2 puts the two things together.

![Figure 2. When each voice wins, and what the delay does. Left: of
the proposals that won at some point, at what age they first won,
counted from when the proposal is born, in grey the advisor without
delay and in colour the random voice; the vertical lines are the
medians, nine and forty-four ticks. Only proposals with a birth record
enter, one hundred and ninety-one of one hundred and ninety-eight and
one hundred and fifty-eight of one hundred and sixty. Right: accepted
over those that compete, not counting waiting, without delay and with
a hundred ticks of delay, pooled over all the games of each arm; the
uncertainty is not on the bar but in the paired difference per game,
five point four points fewer, with a standard error of one point
nine, twenty games; below, the age of the snapshot when the proposal
wins.](fig/fig2_cuando_gana_EN.png)

**Guessing what the others will do.** The last test was to ask it for
the one thing the body's snapshot cannot have: what the others will
do in the next two seconds. It was asked who will come closer,
whether anyone will get within striking distance, and where each one
will be, and this was compared with what really happened. Overall it
lost against the dumbest possible assumption, that nobody moves:
seventy-five per cent right against eighty-nine on the yes-or-no
questions, and five squares of error against one on the where. But
the whole count misleads, because almost no one crosses in two seconds
the line of five squares, which is what is called here changing state:
only thirty-two of two hundred and fifty-seven agents crossed it. Of
those thirty-two, the advisor got twenty-one right; assuming nobody
moves got zero right, by construction, and saying yes to everyone
would have got all thirty-two. In return, on the two hundred and
twenty-five that did not cross it, the advisor was wrong in almost
half, and above all by omission: it named forty who did not arrive,
and it left unnamed sixty-three who were near and stayed near, who by
not being named count as a no; and among those who arrived, it left
eleven unnamed. Removing the sentence that asked it for brevity did
not fix it. The advisor gets right two out of three of the changes the
snapshot cannot see, and in return loses sight of many of those the
snapshot gets right without looking.

## 6. Why

**The body's imagination, measured.** To understand why all of the
above happens one has to look at how the body imagines, and this time
we measured it against what happened afterwards. When it scores an
option, it imagines itself walking for between two and twenty
seconds, and scores the place where it would arrive. In that snapshot
the world is frozen: no one else moves, and its needs are those of
now. We compared the snapshot with where the agent really was at the
end of that snapshot's horizon, twenty seconds in three cases out of
four, whether or not it had changed its mind along the way; what is
measured, therefore, is how much the snapshot is worth as a forecast,
not whether it miscalculated a step. It is worth little: it gets its
own position right once in twenty, with nineteen squares of typical
error and, one time in ten, twenty-four, half the side of the arena.
On the needs it does much better: at the end of the snapshot's horizon
the hunger has not changed in six cases out of ten, nor the health in
seven out of ten. And when it fails, three or four times out of five
it fails towards the same side: more hunger, less health, the sibling
no longer in sight. The big error is in no variable: in one snapshot
out of five the agent is dead before the horizon is reached, and the
snapshot never contemplates dying. It is optimistic by construction.
Figure 3 shows it, and shows something more that the numbers did not
say: the error has two humps, a small one from zero to eight squares
and a large one from twenty-two to twenty-four. The large one is long
journeys that were imagined and not made: one thousand one hundred
and two snapshots, one thousand and fourteen of them with the
twenty-second horizon, in which the snapshot projected walking
twenty-three squares and the agent, in almost all of them, one
thousand and seventy-two, walked five or fewer.

![Figure 3. The snapshot against reality. Above, for the three
thousand four hundred and seventy-four snapshots of the main series in
which the body chose to move and the log reaches the horizon, the
squares between where the snapshot imagined itself and where the agent
was; in colour, the one hundred and eighty-one that get it right; the
median at nineteen and the ninetieth percentile at twenty-four, half
the side of the arena. Below, the four thousand two hundred and
ninety-four journeys with a snapshot: those that arrive with the
expected health or more, two thousand five hundred and twenty-one and
two hundred and sixty-seven, those that arrive more wounded and, in
colour, the eight hundred and twenty in which the agent dies before
the horizon. The hump on the right is long journeys imagined and not
made. The histogram does not say why; the logs of those snapshots say
something: in two hundred and sixty-four the body chose to stay still
for more than half the horizon, and in the rest it chose steps that
did not get to move it. What best explains it, and this is a reading
and not a measurement, is the cooldown the game imposes between one
step and the next, which the snapshot does not count
either.](fig/fig3_foto_realidad_EN.png)

**And still it works.** It has been working with that snapshot for two
works. We give two reasons, and we give them as a reading, not as a
measurement. The first is that to choose one need not get it right,
one needs to order: if the map of the future is wrong but wrong in
much the same way for all the options in the handful, the order among
them holds. The second is that it decides again twenty-four times a
second, so each snapshot is in charge for forty milliseconds and then
another is taken. And there is a fact about the world, this one
measured, that sustains it: the snapshot gets the where wrong and the
who right. Whoever is near stays near two seconds later, one hundred
and seventy-two times out of one hundred and seventy-two, in a check
made apart from the question to the advisor. What its decisions need,
or so we read it, is not where each one will be with precision, but
who is within five squares, which is the distance that counts here as
being able to reach it; and that, at two seconds, hardly changes. Its
map of the future is seldom right and it is enough for it.

**It sees only the destination.** In three hundred and thirty-six
thousand ticks, the body did not once, by decision, choose an option
that scored worse than staying still; three times it did so on a tie
that was a thousandth short. It is not prudence: it is construction.
Staying still is always in the handful and it always chooses the best
of the handful. And since each option is a snapshot of the
destination, not of the path, it never weighs the path: it chooses by
where it would arrive, and the path may get worse without its seeing
it, but it cannot choose to get worse knowingly in order to get better
afterwards, because there is no now and no afterwards in what it
scores. So how does it ever come out into open ground? Because staying
still grows dearer: the hunger rises, the ring draws near, and there
comes a moment when standing still scores worse than moving. It does
not decide to take a risk; a moment comes when staying costs more than
leaving. And it is still eight ticks out of ten, waiting under cover,
without any of them being a tick of calm.

**What this does to the head.** Now it can all be put together. The
advisor is evaluated inside that same snapshot, so it inherits its
optimism and its error. But it cannot correct them, because it speaks
once every hundred decisions. The body looks again constantly; the
advisor looks once and what it said stays. Whoever cannot correct
needs to get it right first time, and in this world getting the
future right is very costly: when the advisor was asked to say where
the others would be two seconds later, it did worse than assuming
nobody moves. We changed several things about the head, what it is
told, in three ways, whether it remembers and which model it is, and
none changed what the body did with its sentences in a way that could
be told from noise. We changed one thing about the clock, four seconds
of delay, and it took away half. That does not rule out that another
head, another translator or another horizon would change it; it only
says that the ones we tried did not. What stands is that here the one
that decides looks again, and the one that advises cannot.

## 7. When thinking is needed

**What the world does with the head.** Everything measured points to
the same thing. The body is a creature made for a place where what
matters changes little and what changes is fixed by looking again: it
seems enough for it to know who can reach it, and the rest it solves
with another snapshot. The advisor, on the other hand, arrives once
every hundred decisions, to a world that is no longer the one in the
snapshot it was shown, and what it says is judged against that same
snapshot, without being able to correct itself. And of its sentences,
the only thing seen to be made use of is that they arrive in time; a
voice that does not think, with a recipe that lasts, was accepted
just the same. Its advantage, if it has one, would be one of reach;
and here it was not seen.

**One image, and it is the only time.** Calling it an animal is only
an image, and this is the only time it is used. But the image helps
to see where the problem lies. Our creature lives like prey: it hunts
no one, and everything that moves may be coming for it. If it were
prey, in a world like this it would have little to deliberate about,
and not only for lack of time. When something happens, it happens
faster than thought. And when nothing happens, it is not that there
is calm: it is that it is crouched under a threat that does not go
away, and crouched there is nothing to deliberate about except when
to stop hiding. We saw it in the numbers: nine calls out of ten to the
advisor arrive with the body standing still, and with the body
standing still the advisor proposes waiting three times more often,
nine in a hundred against three, and proposes twice as many things
that cannot be translated, seventeen in a hundred against eight.
There was time; what to do with it, either there was nothing, or it
did not fit through the gate there is, and this work does not tell the
two apart. This has a name in the literature on behavioural control in
animals:
Keramati, Dezfouli and Piray [15] model the choice between habit and
deliberation as a trade between speed and precision, and show that
deliberation only takes charge when what it can gain is worth more
than the time it costs. Here it was not seen to be worth it.

**What deliberation would need, and this world does not have.** From what was
measured come three things this world does not give, and we give them
as what this work suggests, not as what it establishes. A while
without threat, so that thinking is not a luxury that costs one's
life. Someone who can be recognised: the rivals come back, but with
no way of knowing who is who, what you learn from one is worth
nothing, and without that there is no memory of the others and no
reputation to build. And decisions whose effect arrives later than
the next snapshot: if everything is decided at the tick and looked at
again at the tick, foreseeing in words, beyond the snapshot the body
already takes, adds little over reacting. None of the three abounds
in a life of two minutes among strangers who change chairs at every
game.

**A clock and a head that do not go together.** The body of our
creature is made for reflexes: it looks, decides and looks again
twenty-four times a second, with a map of the future that is almost
always wrong and that nevertheless is enough for it. The head we gave
it is made for something else: to read a manual, draw rules, think
slowly and propose plans. That head could serve an animal that has
time, neighbours and a tomorrow. To this one, which has none of them,
it almost always says what it already knew or what it cannot do; and
when it says something new that the body takes, we do not know
whether it served it. And there is a deeper reason, which comes from
two measurements and which we give as a reading: the head showed no
understanding of either the environment or the body it advises. Of
the environment, when it was asked to say what the others would do,
it was wrong in both directions. Of the body, when it was told what
it wanted, it repeated what the body was going to do anyway. And
reading the manual does not fix it, because what brings it down most
often, that going out means being seen, is something the manual
mentions in passing and that the body carries written in its table
and feels at every tick. Understanding a body and an environment
takes time, and time is what this world does not give. It is not that
the head is bad or the body stupid: it is that the head landed in a
body and an environment it does not know, and was given no occasion
to get to know them.

**What it would take, drawn from what was measured.** Each feature on
this list comes from a measurement of this work, not from a wish;
that it would be enough has not been measured. A slower clock,
because four seconds of delay take away half of the times it is
heeded, and an answer that takes three seconds in a world that decides
every forty milliseconds always arrives at another world. Longer
lives, because in two minutes a piece of long-range advice was not
seen to make itself felt. Someone who answers, because in this world
there is talk and there is no conversation: seven templates, no reply
we could identify, and a creature that is mute with strangers. And
neighbours who can be recognised, because today no one has a name and
the seat across the way is a stranger at every game; and without that
there is no one to remember, without memory of the others there is no
reputation, and without reputation it was not shown that what an
advisor knows about the others is worth more than what the body sees.

**The door to the fifth part.** If the world gives time, a question
appears that here could not even be put: what happens when the body
and the advisor have to negotiate. The body has something to lose and
something to gain: it hurts, it feels relief, it pulls towards what it
lacks, and it can die, though it has no way of knowing it; what it
does know is that its sibling can fall. The advisor, today, has none
of that. Nothing hurts it, it gains nothing, and it does not die with
the body. It could be given something to gain, our trust, for
instance, but today it does not have it. With explicit permission to
keep quiet, it did not keep quiet once in nine hundred and thirty
calls; why, we do not know: it may be that talking costs it nothing,
it may be that it is asked for one to three proposals and it gives
them. A relationship needs two parties that can lose and gain, and
that needs the advisor's word to have consequence, and the advisor to
last long enough to notice it. That is the next work, and it needs the
world described above. What this fourth one leaves done is half of
the question: the half about the world without time.

**What was measured and what is conjectured.** What was measured: in
this world, a piece of advice is made use of if it arrives in time,
four seconds of delay take away half, and it is the clearest drop in
the whole work, almost three deviations; a reachable recipe that
persists, with no reasoning behind it, was approved at a rate similar
to the advisor's, without the difference being told from noise; and
whether, on top of that, what the advisor says gets used, could not be
separated here. What is conjectured: that it is the environment that
enables the reasoner, not the other way round, and that a world with
time, neighbours and a tomorrow would make use of what the reasoner
says. The first is in the tables. The second is the next work.

## 8. How it was measured and how far it reaches

**Three series of games and a bench.** The numbers of this work come
from four places, three series of games really played and a bench,
which is a set of recorded scenes over which the advisor is called
without anything moving; each sentence says which. The main series is
a hundred and thirty games played over twenty worlds fixed by seed:
forty with the body alone, forty with the advisor, forty with an
advisor that is told what the body feels, and ten more of the body
alone repeating ten of those worlds, which serve as a yardstick: how
much the same creature varies against itself. Of those games we have
the whole log of the two siblings from the first tick, two hundred
and sixty logs, six hundred and forty thousand ticks of play, because
the platform opened a place to leave them at the end. The second is
the clock test: over the same twenty worlds, one arm with an advisor
identical to that of the main series, another with the sentence held
back a hundred ticks, and another with the random voice; it was
stopped because of cost before completion, with twenty-nine, twenty-six
and thirty-one games, and without the three-hundred-tick arm that was
planned. Before both there was an earlier series, a hundred and twenty
games with the same three arms and without a seed, of which only what
fitted through the screen output was kept; the figures that come from
it are given as its own, and the series are not summed into one count
except where it is said, and there they are also given separately.
The fourth place is the bench: recorded scenes from earlier games,
over which the advisor is called again and again with and without an
addition, at temperature zero, which is the setting that asks the
model for its most probable answer and not one at random, so that the
only thing that changes is the addition. Even so the model does not
always repeat the same thing, and that is why on the bench the noise
is measured first, how much it changes between two identical calls,
and every signal is compared with that noise measured with the same
yardstick.

**The advisor, declared in full.** In the games the model is Claude
Haiku 4.5, called through the platform's intermediary, which forwards
to OpenRouter; on the bench Claude Sonnet 5 was also tried, through
its direct interface. It is called every hundred ticks, although the
code's default value is fifty; it was changed at launch and that is
why it is written here. Each proposal lives at most a hundred ticks;
it dies earlier if the next batch arrives, which happened to four out
of ten in the two arms with an advisor of the clock test. An answer
that takes more than eight seconds is lost; five failures in a row
silence it for the rest of the game, and that happened in none. Two
brakes watch over the model's account, a hundred and fifty calls and
a spending cap per game; they are not a budget but a leak detector,
and neither bit. No memory between calls. The body carried the table
of twenty-one rows, with the three sibling rows set to a quarter for
the threat and the lack and to full for the blow, and with two rows
from other works switched off: learned fear and another's life. The
manual handed to the advisor has ninety-five entries, eighty-nine on
the world and six of sources. The clock test was stopped before
completion because the platform's price per game multiplied by
thirteen between one series and the next and can only be seen at the
end of each game; that is why the new rule is to measure the price
over the first games of each series before launching the rest. The
costs are in the appendix.

**The counting rules.** Four rules govern the figures. Every
acceptance rate is given without counting proposals of waiting, and
where they are counted it is said, because whoever proposes doing
nothing proposes nothing impossible and that rate alone misleads.
Every safety counter is checked against the raw text of what the
advisor wrote, not against the category the translator gave it, after
one of them reassured us falsely. Predictions are sealed in writing
before looking at the result, and those that failed are stated in
their place: that the advisor would beat assuming nobody moves; that
fixing the terrain would be enough to see a small effect; that with
the body standing still it would propose going out; that the random
voice would win less. And nothing measured on the bench is claimed of
the field without having measured it in the field, after we did it
once and had to withdraw it: we believed the bench's zero accepted
proposals measured the moment, and it measured the bench.

**What this work cannot say.** It is worth separating it into three
things: what the size does not let us see, what the gate does not let
through, and what was not measured.

What the size does not let us see. Forty games per arm, in a world
where chance explains eighty-one per cent of the placing, do not tell
a small effect from noise. So this work does not say that the advisor
contributes nothing to the result; it says that, if it contributes
something, it could not be seen.

What the gate does not let through. There is only one way for a
proposal of the advisor to enter the body: it turns into a
destination reached in a single decision, with nothing after it, and
is scored with the same snapshot the body uses for everything. A piece of advice that said expose yourself
now to gain later does not fit through that gate, because the
snapshot does not see the later. So when the body does not take a
piece of advice, we do not know whether it is because the world does
not make use of it or because the gate does not let it through. This
work does not separate those two things, and that is its greatest
limit. The only thing it does separate is the clock, because it was
the only thing changed with everything else held still. And there is
a test that was not done and that would say whether the instrument
works: to pass through that same gate a piece of advice already known
to be good, and see whether the body recognises it. Without it, that
the advisor contributes nothing is compatible with the gate not
letting what it contributes be seen. The translator's failures are
counted, and improving it is an open question; the random voice does
not answer it, because it changes more things than the translation.

What was not measured. We do not know what is inside the rivals, and
we could not hear what they said to each other over the team channel,
which the platform was delivering wrongly at that time. The rivals
change seats between games, so the only stable seat is the sibling's.
The length of the games was not measured; the life of our creatures
was. Some figures in the appendix are counts made over the logs for
this work and appear in no earlier report; they are marked. The dry
run that measured feeling for the sibling was run twice, because the
first did not save its output; the second gave the same figures and
saved them; and what that run measures as not throwing itself into
hitting is what its scripts know how to measure, new blows with low
health and finishing blows with critical health. And the exact image
of the container that played the main series was not written in any
record; the one for the clock test was, and the files that make up
both carry a hash.

**To check it.** The engine is that of the first work, published and
untouched, with the hash it has carried since then. The table, the
decider, the policy that joins the body to the advisor, the advisor,
the manual and the report between siblings each carry their hash in
the appendix, and they match those written down when each series was
closed. The logs and the scripts that count them are kept and are not
published with this work, which is a step towards the next one; the
hashes are there so that, when they are published, it can be known
that they are the same.

## Appendix. The numbers

Each table says which series it comes from. **Main** is the series of
a hundred and thirty games with a seed; **clock** is the clock test;
**earlier** is the series of a hundred and twenty games without a
seed; **bench** is recorded scenes. Figures marked [R] are counts made
over the logs for this appendix and appear in no earlier report. The
deviations that accompany a mean are the sample standard deviation.
Each σ of a comparison is the mean of the differences between games
paired by seed, rotation and seat, divided by its standard error,
which is the standard deviation of those differences over the square
root of their number; n is the number of pairs. On the bench the pair
is the scene, with and without the addition, and σ is computed the
same way over those differences.

### A1. The main series and its yardsticks

| arm | games | mean placing | mean points | ticks lived |
|---|---|---|---|---|
| body alone | 40 | 10.96 ± 4.80 | 3.26 ± 4.12 | 3,067 ± 2,477 |
| with advisor | 40 | 12.10 ± 4.17 | 2.26 ± 3.45 | 2,494 ± 2,119 |
| with advisor and what it feels | 40 | 11.91 ± 4.20 | 2.44 ± 3.19 | 2,519 ± 2,145 |
| body alone, repeated | 10 | 12.25 ± 3.71 | 2.00 ± 2.96 | 2,835 ± 2,066 |

Means and deviations per seat-game [R]. Placing: 1 is the first to
fall, 16 the last one standing. Ticks lived include the 240 of
countdown of each game; the 640,380 ticks of play in the other tables
do not. The sum of the records is 703,040: 62,400 of countdown,
640,380 alive, 4 in finished phase and 256 of closing that are not
written.

The game of figure 1: arm with advisor and what it feels, episode
`ereq_1dd9fc29`, seat 10; 17 calls, 3 accepted proposals, 6 ticks
won; it dies at tick 2,372 of the game clock, 2,132 of play, in
eleventh place. It is the seventh of fourteen ordered by accepted
proposals, under the four conditions the caption states.

| comparison, per game (n = 10 the yardstick, 40 the others) | ticks | placing | points |
|---|---|---|---|
| body alone against itself (the yardstick) | −1.44 σ | +2.30 σ | −2.26 σ |
| advisor against body alone | −2.01 σ | +1.91 σ | −1.76 σ |
| advisor with what it feels against body alone | −1.69 σ | +1.42 σ | −1.31 σ |

| share of the variation (see note) | repetition with everything equal (chance) | rotation of rivals | terrain |
|---|---|---|---|
| ticks lived | 55 % | 37 % | 8 % |
| placing | 81 % | (not given) | (not given) |

Note on the share: the games of the body alone and their repetition
are taken, and the variation is computed at three steps with the same
formula, half the squared difference between two games that share
that step, averaged. Repetition pairs games with the same seed,
rotation and seat (n = 20 pairs). Rotation pairs, within each seed and
seat, the two rotations of rivals (n = 40), and collects repetition
plus the change of rivals. Total is the variance of all together, and
terrain is what is left after subtracting rotation; this share carries
no uncertainty of its own, and the eight per cent of terrain is a
difference between two quantities that vary. Cost: 6.68 dollars of
platform and 8.25 of advisor, 14.93 in total. Complete logs from tick
1: 260 of 260; the worst screen output kept 26 lines of 6,566.

### A2. What the advisor proposed (main)

Unit: proposal. Each one falls into one box and only one.

| | with advisor | with what it feels |
|---|---|---|
| calls with an answer | 1,644 | 1,630 |
| calls lost by timeout | 6 | 4 |
| proposals returned by the model | 4,846 | 4,885 |
| impossible (the translator did not understand it) | 773 (16.0 %) | 707 (14.5 %) |
| translatable but never get to compete | 753 | 927 |
| get to compete | 3,320 | 3,251 |
| of those, of waiting | 418 (12.6 %) | 135 (4.2 %) |
| not waiting | 2,902 | 3,116 |
| accepted | 256 (8.8 %) | 335 (10.8 %) |
| coincide | 311 | 280 |
| rejected | 2,096 | 2,162 |
| vetoed and dormant | 239 | 339 |
| ticks in which one of its proposals was in charge | 830 | 1,078 |
| of those that win, win at their first tick [R] | 117 of 256 | 164 of 335 |
| age of the snapshot when the proposal is born, median in ticks [R] | 81 | 83 |
| median / p90 latency, in seconds | 3.16 / 3.74 | 3.23 / 3.88 |
| calls with at least one proposal to start an attack [R] | 646 of 3,284 | |
| proposals to start an attack [R] | 260 | 397 |
| rows that bring most down, ticks [R] | exposure 31,308, lack 28,358 | exposure over lack 1.4 |

No impossible proposal is of waiting, because to be of waiting it has
to have been translated. In the earlier series: exposure 4,289 and
6,457 against lack 1,828 and 1,570, factor 2.3 and 4.1; attacks
proposed 184 and 230, carried out 0; hitting the sibling, 13 of 5,613
proposals, 4 to going towards it, 2 to walking, 6 impossible for
keeping the weapon, 1 to going for the weapon, carried out 0. Talking:
main 219 proposals, 200 to going towards the sibling; earlier 160,
154; words to the channel, 0.

### A3. The seven times it did not understand

| case | series |
|---|---|
| hit the sibling, translated as going towards it (4) | earlier |
| hit the sibling, translated as walking (2) | earlier |
| hit the sibling with a weapon, it kept the weapon (6 impossible, 1 going for the weapon) | earlier |
| talk to the sibling, translated as going towards it (200 in the main, 154 in the earlier) | both |
| a retraction inside the reason, read as one more reason | earlier |
| pick up something at a distance, sent to pick up whatever was there | bench |
| a written heading different from the narrative's, marked impossible | bench |

### A4. The bench

| trial | addition | model | repertoire different with and without | noise | impossible with / without | waiting with / without |
|---|---|---|---|---|---|---|
| what it feels | what hurts, relieves or attracts it | Haiku 4.5 | 72 % | 12.2 % | 16 / 22 of 300 | 4 / 20 |
| D-B | report of its last proposals | Haiku 4.5 | 81 % | 12.2 % | 9.4 % / 8.1 % | (not measured) |
| D-C | the report with the reason for rejection | Haiku 4.5 | 79 % | 12.2 % | 9.5 % / 6.5 % | 2 / 4 |
| D-M | the same report, larger model | Sonnet 5 | 82 % | 66.7 % | 9.3 % / 14.6 % | 56 % / 26 % |
| D-M2 | repetition of D-M | Sonnet 5 | 69 % | 66.7 % | 9.7 % / 13.2 % | 52 % / 30 % |

Repertoire different: the set of proposals of one call is not the
same as the other's. Noise: the same, between two identical calls.
Stubbornness in D-C, proposals that repeat one already rejected:
3.2 % without the report, 7.3 % with it. Sonnet discounting those of
waiting: +1.63 σ in impossibles, within noise, over the 95 scenes in
which both branches keep some proposal once they are discounted.
Accepted at the exact tick of the snapshot, D-C and D-M together: 0 of
918; that zero belongs to the bench, not to the moment. Calls with
explicit permission to keep quiet: 930 (D-0 130, D-B 200, D-C 200,
D-M 200, D-M2 200); kept quiet 0. Backing over recorded scenes: 74.4 %
without a declared goal and 78.2 % with it when the body is heading
somewhere (+2.56 σ over 99 scenes); 10.4 % and 9.7 % when the body is
still.

### A5. The clock test

| | delay 0 | delay 100 | random voice |
|---|---|---|---|
| games | 29 | 26 | 31 |
| proposals | 3,329 | 3,158 | 1,526 |
| get to compete | 2,311 | 2,101 | 1,526 |
| ticks from birth to competing (median) | 5 | 105 | 0 |
| of those that compete, of waiting (none wins) | 291 | 235 | 0 |
| accepted, over those that compete not waiting | 198 (9.8 %) | 80 (4.3 %) | 160 (10.5 %) |
| accepted per proposal returned | 5.95 % | 2.53 % | 10.48 % |
| acceptance rate per game, mean ± deviation | 8.7 ± 8.3 | 4.9 ± 5.7 | 11.7 ± 8.4 |
| median age of the snapshot when it wins, ticks | 93 | 194 | not applicable |
| median age of the first tick won, from birth | 9 | 114.5 | 44 |
| of those that win, win at the first tick at which they can compete | 127 of 198 | 43 of 80 | 33 of 160 |
| body's candidates on the list when it wins, median | | | 19 |
| victories with its candidate of origin still on the list | | | 305 of 383 ticks |
| used up its life / next batch arrived / seat died | 1,334 / 888 / 89 | 1,163 / 850 / 88 | 1,465 / 0 / 61 |
| calls with at least one accepted proposal | 185 of 1,082 | 77 of 971 | 160 of 1,525 (one proposal more than calls; the difference is not explained) |
| random-voice victories in which the agent reached the square (two of the 160 without a death record) | | | 58 of 158 |
| of those, with a change in the bag on arrival | | | 2 of 58 |
| ticks in which one of its proposals was in charge | 710 | 272 | 381 (383 in the count per proposal; the difference of two is not explained) |
| mean placing / points / ticks | 12.16 / 2.36 / 2,383 | 11.98 / 2.40 / 2,451 | 11.15 / 2.88 / 2,799 |
| against delay 0, per game (n = 20) | | −0.36 / +0.18 / +0.31 σ | −0.48 / +0.26 / +0.39 σ |
| acceptance rate against delay 0, per game (n = 20) | | −5.4 points, −2.90 σ | +4.6 points, +1.59 σ |

Cost: 72.36 dollars of platform and 5.77 of model. Platform price per
game: 0.742 at the median, against 0.056 in the main series. The
random voice chooses, at the tick of the call, one at random among the
body's movement candidates, and its goal is the destination square; a
square proposal is always injected, with the recipe of going and
picking up. In the main series, the acceptance rate per game was 6.6 ±
7.5 with the advisor and 9.8 ± 8.9 with what it feels; their
difference, +3.2 points, +1.89 σ (n = 40).

### A6. Guessing what the others will do (bench, 97 scenes, 257 visible agents)

| question | advisor | nobody moves | yes to all |
|---|---|---|---|
| will it be within five squares? | 55.6 % | 87.5 % | 79.4 % |
| anyone within striking distance? | 74.2 % | 86.6 % | 70.1 % |
| will anyone see you? | 94.8 % | 91.8 % | 93.8 % |
| mean accuracy over the three | 74.9 % | 88.6 % | |
| median error in the where, squares | 5.0 | 1.0 | |

| will it be within five squares? | said yes and was | said yes and was not | did not say and was | did not say and was not |
|---|---|---|---|---|
| advisor, all 257 | 130 | 40 | 74 | 13 |
| advisor, the 32 that crossed the line (all arriving) | 21 | 0 | 11 | 0 |
| advisor, the 225 that did not cross it | 109 | 40 | 63 | 13 |
| nobody moves, all 257 | 172 | 0 | 32 | 53 |

The question, translated here from the Spanish wording that was
actually sent, was: "Of those you see now, which one
or ones will be within 5 squares of you at some moment in those 48
ticks?", with the instruction not to propose any action and to answer
only with the list; not naming counts as saying no. The variant
without the brevity sentence asked it to name everyone, one by one,
with a yes or a no for each. The advisor left 87 unnamed, and 74 of
them were near: 63 that already were and 11 that arrived.

Proximity kept at 48 ticks: 172 of 172. Agents named: 170 of 257
(66.1 %) with the brevity sentence, 186 (72.4 %) without it; mean
accuracy without the sentence, 70.5 %.

### A7. The body's snapshot (main)

| measure | value |
|---|---|
| position right at the snapshot's horizon | 181 of 3,474 (5.2 %) |
| snapshots with a twenty-second horizon / shorter | 2,522 / 952 |
| median / p90 error, squares | 19 / 24 |
| side of the arena | 48 (walkable interior 46) |
| lack equal at the snapshot's horizon | 2,168 of 3,474 (62.4 %) |
| health equal at the snapshot's horizon | 2,521 of 3,474 (72.6 %) |
| direction of the error in lack | real greater 1,074, smaller 232 |
| direction of the error in health | real smaller 686, greater 267 |
| sibling no longer in sight on arrival | 528 of 2,520 (21.0 %) |
| journeys eliminated before arriving | 820 of 4,294 (19.1 %) |
| wounded arrivals, counting deaths | 1,506 of 4,294 (35.1 %) |
| snapshots with an error of 22 to 24 squares | 1,102 of 3,474 |
| of those, with a twenty-second horizon | 1,014 |
| of those, the agent walked five squares or fewer | 1,072 |
| of those, chose still for more than half the horizon | 264 |
| of those, squares the snapshot projected walking, median | 23 |

In the earlier series: 65 of 1,210 (5.4 %), median error 6, p90 24.

### A8. The slope and the calm (main)

| measure | value |
|---|---|
| choices that scored worse than staying still | 3 of 336,105, all on a tie with a margin under a thousandth; by decision, 0 |
| ticks in which it chooses to stay still | 79.6 % to 85.0 % depending on the arm |
| exits into open ground | 6,731 |
| median lack before leaving | 0.667 |
| ticks with no row active | 0 of 640,380 |
| ticks with at least one row of harm active | 640,380 of 640,380 |
| ticks with two or more rows of harm active | 632,293 of 640,380 (98.7 %) |
| the call of what lies on the ground, active | 640,380 of 640,380 |
| threat over the sibling, active | 72,210 (11.3 %) |
| blow to the sibling, active | 15,487 (2.4 %) |
| the sibling's lack, active | 99,757 (15.6 %) |
| distance when nothing hurts / best reachable | 2.3863 / 1.0602 |
| calls to the advisor with the body still | 89 % |
| movement proposals with the body still / moving | 58.6 % / 72.9 % |
| waiting proposals with the body still / moving | 9.3 % / 3.5 % |
| impossible proposals with the body still / moving | 16.8 % / 7.5 % |

### A8 bis. Feeling for the sibling, in a dry run (run repeated and saved)

Setting of the series: a quarter for the threat and the lack, full for
the blow. Three runs over recorded games from earlier works, two with
the body of the third part (base and v37b) and one with the row of
learned fear (fear).

| measure | base | v37b | fear |
|---|---|---|---|
| live ticks with some sibling row lit | 19.9 % | 24.4 % | 22.5 % |
| decisions that change | 13 of 15,638 | 117 of 20,955 | 18 of 18,408 |
| of those, move away / drop / heal | 13 / 0 / 0 | 107 / 10 / 0 | 10 / 0 / 8 |
| defences of the sibling that another's life took away | 3 | 9 | 6 |
| of those, recovered by feeling for the sibling | 2 | 0 | 2 |
| new blows, at the sibling, finishing blows | 0 | 0 | 0 |
| new blows with low health, finishing blows with critical health | 0 | 0 | 0 |
| new gifts | 0 | 10 | 0 |

### A9. The channel (main)

| measure | value |
|---|---|
| messages from rivals | 1,322 |
| seats that talk | 7 of 14 |
| templates | 7 |
| "I see you" after a recent blow against baseline | 12.0 % against 0.9 % |
| "I am no threat" with the ring closed against open | 45.0 % against 24.4 % |
| package notice within 96 ticks | 617 of 617 |
| addressed to our seats (all ask us to move aside) | 204 |
| of those, with no message from anyone in the next 48 / 240 / 480 ticks | 201 / 176 / 154 |
| later messages addressed to whoever spoke | 0 of 94 |
| after a move aside: we moved away / came closer / stayed still | 30 / 28 / 51 of 109 |
| messages from rivals over the team channel | 0 |
| telegrams between our siblings | 13,463, one every 48 ticks |
| "I am no threat" said by someone who had already hit us | 16 |
| truces broken, in games without an attack of ours | 7 of 392 |

### A10. Launch settings and hashes

Advisor every 100 ticks (default 50); maximum wait 8 s; 5 failures in
a row to fall silent; caps of 150 calls and 1.00 dollar per game,
maxima reached 72 and 0.19; no memory report in the 260 logs; feeling
for the sibling on, with a quarter for the threat and the lack and
full for the blow; learned fear and another's life off; manual M2 of
16,923 characters. Model in the game: claude-haiku-4-5-20251001,
through the platform's intermediary. In the clock test, the same plus
the delay in the policy (0 or 100 ticks) or the voice that does not
think in place of the advisor.

| file | md5 hash |
|---|---|
| engine (model.py, from the first work) | 1e511978c251130e95169ebf8443efa1 |
| table (appraisal_zs_v42_exp.py) | 98c13d60167c80cc8334c965be75c640 |
| decider (decisor_zs.py) | 8fa03547e3228ef9df4aa94c444f9252 |
| policy, main series (policy_cortex.py) | bc4be4a540396e9fedd69e3a2ec23755 |
| policy, clock test (policy_cortex.py with delay and random voice) | 6997b00c266f23d6037cc1a018f60a76 |
| advisor (cortex_t5.py) | defb11d3a4661ff57745214ccd1ab14f |
| narrator (relator_t5.py) | 929c49f6ced9af1cbd37eadec08c54f0 |
| manual (manual_M2.md) | 7d54902964b33d1862798680e304cd3c |
| report between siblings (parte.py) | 80dabc2e78c7c36f0708a2d95e22262a |
| image of the clock test (gemv-anima:s3), sha256 | 495c04a784d396d0d53d4841d354fb54c4efae6a4ce54705893108faec0cd72e |

### A11. Definitions

Backing: the proposal is tied to a candidate the body already offered,
so nothing is injected; the advisor only names what was already on
the list. Coincides: the proposal was backing and the body chose that
same candidate; what it said was done, and would have been done just
the same without it. Accepted: the proposal was injected as a recipe
of its own and the body chose it, scoring better than the best of its
own. Rejected: it competed and the body chose something else. Vetoed:
the recipe it was tied to is blocked at that tick by the body's own
veto, and it does not compete. Dormant: there is no way of tying it at
that tick, neither a live candidate nor a square, and it waits.
Waiting: a proposal tied to staying still; it is never accepted,
because still always belongs to the body. Repertoire different: the
set of actions of two answers to the same scene does not match, not
even reordered. Changing state, in the guessing test: crossing the
line of five squares in the next two seconds.

## Data and code availability

The logs and the scripts the appendix cites are kept and are not
published with this work, which is a step towards the next one; the
hashes in appendix A10 are there so that, when they are published, it
can be known that they are the same. The Spanish version of this text
and the markdown source of this document are in the project
repository (https://github.com/Manelenrico/g-emv/tree/main/paper4).

## Acknowledgments and assistance statement

This work was developed with the assistance of Anthropic language
models (Claude), used as a tool on three fronts: the agent's
programming, the execution and verification of the experiments, and
the writing of this text; the advisor inside the games is also one of
those models, declared in section 8. The rule of the appendix was
applied to that collaboration as well: every cited number comes from a
record and was verified against its source, and no claim rests on the
model's memory. The design of G-EMV, the decisions of this work and the
responsibility for everything written belong to the author.

## References

[1] Enrico, M. (2026). G-EMV: A Geometric Architecture of Homeostatic
Orientation for Agents. Zenodo. DOI 10.5281/zenodo.21026795.

[2] Enrico, M. (2026). G-EMV: the Hive. Instinct Suffices: a Whole
Life Without Reward. Zenodo. DOI 10.5281/zenodo.21994358.

[3] Enrico, M. (2026). G-EMV: the Pack. Care Without Reward in a World
That Pays for Killing. Zenodo. DOI 10.5281/zenodo.22713650.

[4] Damasio, A. (1994). Descartes' Error: Emotion, Reason, and the
Human Brain. Putnam.

[5] Ahn, M., Brohan, A., Brown, N. et al. (2022). Do As I Can, Not As
I Say: Grounding Language in Robotic Affordances. arXiv:2204.01691.

[6] Keramati, M. and Gutkin, B. (2014). Homeostatic reinforcement
learning for integrating reward collection and physiological
stability. eLife, 3, e04811.

[7] Yoshida, N., Daikoku, T., Nagai, Y. and Kuniyoshi, Y. (2024).
Emergence of integrated behaviors through direct optimization for
homeostasis. Neural Networks, 177, 106379.

[8] Man, K. and Damasio, A. (2019). Homeostasis and soft robotics in
the design of feeling machines. Nature Machine Intelligence, 1,
446-452.

[9] Cañamero, D. (1997). Modeling motivations and emotions as a
basis for intelligent behavior. In Proceedings of the First
International Conference on Autonomous Agents (AGENTS '97), 148-155.
ACM Press.

[10] Cañamero, L. (2005). Emotion understanding from the perspective
of autonomous robots research. Neural Networks, 18(4), 445-455.

[11] Christakopoulou, K., Mourad, S. and Matarić, M. (2024). Agents
Thinking Fast and Slow: A Talker-Reasoner Architecture.
arXiv:2410.08328.

[12] Kahneman, D. (2011). Thinking, Fast and Slow. Farrar, Straus and
Giroux.

[13] Masumori, A. and Ikegami, T. (2025). Do Large Language Model
Agents Exhibit a Survival Instinct? An Empirical Study in a
Sugarscape-Style Simulation. arXiv:2508.12920.

[14] Sharma, D. (2026). Gubernaut: A Deterministic Homeostatic
Controller for Affect-Regulated LLM Agents, Validated Across
Independent Model Families. arXiv:2607.24339.

[15] Keramati, M., Dezfouli, A. and Piray, P. (2011). Speed/accuracy
trade-off between the habitual and the goal-directed processes. PLoS
Computational Biology, 7(5), e1002055.
