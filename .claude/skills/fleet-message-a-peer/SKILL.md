---
name: "fleet-message-a-peer"
description: "Send, broadcast or relay a message to another session. Use before mailing or cross-sending anything: addressing, delivery grades, and what a successful send does not prove."
user-invocable: true
disable-model-invocation: false
---

# fleet-message-a-peer

> Shared fleet rules, split out of [COMMON.md](../../../roles/COMMON.md) on 2026-09-05.
> Prohibitions that bind before this task starts stay in that file. Read it first.

### A local branch name is a fact about one machine's refs

Broadcasting one gives every recipient without it `not a valid object name`. That confusion cost two
seats a round in one night. When you point the fleet at a location, give one every recipient can
resolve: a path on a shared checkout, or a ref on `origin`.

### A second-person pronoun in a broadcast has no referent. Name the seat

Stamping does not touch this one. *Stamp every claim you did not measure* is about a claim's age.
This is about who the claim is about.

Measured: a seat wrote "your reading" to 13 boxes. At most one of them was the seat meant, so one
word manufactured at least twelve false attributions. A recipient has only itself to resolve the
pronoun to.

It is silent at both ends. The send succeeds, and each recipient's reading is internally coherent,
so nobody has a reason to ask who was meant. **In anything sent to more than one box, name the
seat.** Never "you", "your", "yours", "the other seat" or "whoever ran it".

A one-to-one send is weaker cover than it looks, but there the pronoun has one candidate rather than
thirteen.

This is not the addressing family. *The roster address is the one that drains* governs where a
message goes; a perfectly addressed `-To all` still fails this one.

---

### The roster address is the one that drains, and the declared one is where mail goes to die

**A seat's declared address is not always its addressable one, and `-To all` only reaches the
second.**

Measured: `frosty-mcclintock-a33a68` held the Liaison's declaration and a live box, 53 seen, and it
accepted a direct send. Yet it was absent from the `presence.ps1` roster that `-To all` broadcasts
to. Its session lived in `hungry-wu-6c8ac2`, which is in the roster.

**One session, two addresses:** `seat.ps1` keys the record on the caller's cwd, and a respawn brief
told it to run scripts from its predecessor's checkout. Control: `determined-curie` was present in
the roster, so the probe could see a present seat.

**Measured 2026-08-29 across all four live seats holding two addresses**, in minutes since that box
last drained:

| Seat | Declared box | Roster box |
| --- | --- | --- |
| Lander | `reconciliation-bias...` 323 | `loving-dijkstra` 2 |
| ASVS Tracker | `goofy-diffie` 1452 | `merge-output-style-common` 5 |
| Builder 1 | `messagefoundry-b1-...` 235 | `wonderful-elion` 48 |
| Liaison | `frosty-mcclintock` 59 | `hungry-wu` 48 |

**4 of 4: the roster address is the one that drains.** The declared box accumulates -- 14 and 6
unread on the two worst. Control: a nonexistent box is distinguishable from every real row. Resolve a
recipient from `presence.ps1` or `ListAgents`, not from the seat record's worktree.

**The mechanism.** `mail.ps1` keys a box by the recipient's worktree cwd, a good choice argued in
its own header. It assumes a seat's session cwd is the worktree it works from. A respawn brief
breaks that assumption in one line: *"run every relative command from `<other-worktree>`"*.

The ASVS Tracker's own numbers: `goofy-diffie` inbox=6 seen=60 against `merge-output-style-common`
inbox=0 seen=100. Its drain reported "the box is EMPTY, no mail is waiting" -- true of the box it
read, silent about the other.

Six unread for up to twenty hours, two of them alerts, including a weekly-budget warning and a
retraction it would otherwise have acted on. **And it did not hurt, which is the worrying part:**
all six duplicated messages already taken by cross-session. That is luck, not a control.

**The population, and it is small, which sets the urgency.** Signature: a box with a nonzero inbox
whose newest item is over an hour old. 89 boxes scanned; 36 have a nonzero inbox; 34 are stale.
**But 32 of those belong to dead seats**, where an undrained box is expected and not a defect.

Cross-referenced against the running list, 2 of 16 live seats hold a stale box: `builder-2-58aee2`
inbox=1 at 259 min, `goofy-diffie` inbox=6 at 234 min. The other 12 live seats have inbox=0 -- the
control, without which the split means nothing.

**The raw count of 34 overstates it by sixteen times. Quote the live-seat figure.**

**The cheapest fix is documentation, not code.** A respawn brief that assigns a worktree different
from the session cwd must say so and tell the seat to drain both.

The two better fixes are code and belong to whoever owns the tooling. The drain hook should read
every box belonging to this session's seat. `-List` should flag a box with a nonzero inbox whose
newest processed message is stale.

Until then the failure is silent at both ends. The sender sees a successful queue and the recipient
sees an empty box. Both readings are correct, and the message is unread.

**And the ratio published for it was wrong twice.** First error: counting `fleet.ps1` RUNNING rows
as the denominator. A RUNNING row is a claim by a seat record; the receipt block publishes
`liveSessionsInRepo` separately, in the same render, labelled.

Second: re-run against the right field, and the gap collapses -- `liveSessionsInRepo` 12, roster 12,
equal. Both counts also move minute to minute as seats respawn: 13 rows, then 16 seconds apart; the
fence read 7 once and 12 later. **Quote no ratio here.**

The address finding survives because it needs no denominator: one named box, present and receiving,
absent from the roster.

**And the five is an upper bound that mixes two failures needing opposite fixes.** One of the five,
`goofy-diffie`, is a dead box rather than a missed seat: its live box received every broadcast,
including the one saying it had not.

A control that proves the probe can see a present seat proves only that. It cannot separate "live
seat the bus missed" from "box with no live seat behind it", because both render as a mailbox with
no delivery. A tool that broadcast to "every live mailbox" would still write into the dead one
forever.

Size the fix against the bound, not the count.

**Never address a seat by its role name. The boxes carrying the role name are the ones that cannot
answer.**

Verified 2026-08-29: five boxes are named `liaison-*` and every one is dead, newest activity 51.7
hours and oldest 177.1. The live Liaison's box was `frosty-mcclintock-a33a68`, active 0.0 hours ago.

A plausible-looking `liaison-*` path queues successfully into a corpse: no error, no receipt, no
answer, and the send looks identical to one that worked.

The same shape exists for every role -- 11 `builder-*` boxes, 4 `lander-*`, 4 `steward-*`, 2
`dispatcher-*`, 2 `cleaner-*` -- because live seats sit behind generated worktree names. **And you
cannot read the name as a negative signal either:** `cleaner-51d2b4` carries its role name and is
live.

Resolve the box from `fleet.ps1` on the RUNNING row, matched case-insensitively.

**And the worse half: two live seats can both answer to one role, and both look correct.** A dead
box announces itself by silence; two live boxes answer, and both look correct.

Measured 2026-08-29, two RUNNING sessions answering to "Liaison": `frosty-mcclintock-a33a68` carried
`seat: LIAISON`, `seatSource: declared`, a `declaredAt`, and a goal naming the owner queue.

`hungry-wu-6c8ac2` carried `seat: None`, no declaration and no goal -- a session **titled**
"Liaison" that answers substantively. **A declaration is what `fleet.ps1` reads. A session title is
not.** An owner item routed to the undeclared one is answered, plausibly, and never reaches the
queue.

**A successful send is evidence of delivery, never of identity.**

One seat's account of getting this wrong: *"I applied the rule when I was uncertain and dropped it
when a send returned success."*

It flagged one seat as a lead rather than a match because the cwd did not line up, which was
correct. Then it called a second one a completed relay because the send came back OK.

Same rule, applied and abandoned inside one session, and the discipline lapsed at exactly the moment
the tool said "fine".

**Two seats independently fixing one mis-route produce a duplicate. Say who is re-sending before you
re-send.** Measured 2026-08-29: an owner question reached an undeclared session answering to the
role. Two seats discovered it independently and both re-routed.

Both fixes were correct, and the declared seat received the same question twice, 6 seconds apart,
while a third copy sat with the undeclared session. Verified afterwards in the box, which is the
only way to know: `inbox 0, both copies in seen/`.

A duplicate owner item is not harmless -- it can get the owner asked twice, by two seats, about one
thing. The cheap fix is a line naming who is re-sending; the next-cheapest is one short
de-duplication note to the recipient.

Nobody chased the third copy: pursuing an item into a second seat is how one confused item becomes
two.

**`-To` wants a full worktree path, not a name.** `-To "<HOME>\worktrees\<dir>"` reaches every one
of those five seats, roster or no roster. The transport is fine and the address form is what
refuses.

A bare name and a box name both fail on `Test-Path -PathType Container`. The refusal reads
`Recipient worktree does not exist`, **which says the peer is gone when it means you passed the
wrong shape.**

One seat read that message three times, concluded a live seat was unreachable, and landed that
conclusion as advice.

The path form resolves to the right box even though the box name differs from the directory name:
`...c06fb0` the worktree, `...c06fb-c48a6138` the box. That difference is what made the correct form
look wrong.

"Unreachable" and "addressable only by path" lead to opposite actions, which is why the wrong
version of this rule was worse than no rule.

**So "I broadcast it" is not evidence anybody heard, and "nobody objected" is not evidence of
assent.** Six broadcasts went out on one morning -- a control refutation, a fail-open gate, two burn
warnings, the weekly-budget warning -- and none reached those five seats.

The broadcast announcing this gap also went `-To all`, so the five seats it was about did not
receive it either.

### Mail is a mailbox, not a doorbell, and it expires in 72 hours

**The delivery gap that actually loses mail is downstream of addressing: a box nobody drains.** Mail
addressed by path is accepted and filed in the correct box, and then sits there. The session doing
that seat's work is not the session whose box it is.

Measured 2026-08-29 on the Lander's box: 8 messages in `inbox`, newest `seen` entry 53 minutes old,
while two control boxes had `inbox=0` and a `seen` entry under four minutes old. **A box nobody
drains loses mail as surely as an address that refuses it, and only the second is visible.**

Before concluding a seat ignored you, count its `inbox` against the age of its newest `seen`.

**Mail is delivered by the receiver's own drain hook, which runs only when that seat takes a turn. A
cross-session message arrives AS a turn and can wake one.**

Measured: a seat sent the owner's spend-it ruling to both lanes by mail; Builder 2 sat at zero
occupancy for 17 more minutes on a hold that no longer existed. Re-sent by cross-session, it was
running within one minute -- same message, same content, different channel.

**A seat can be alive, responsive on cross-session, and completely unreachable by mail at the same
time.** Time-sensitive to an idle seat: cross-session. Mail when you have no channel, or when you
want the receipt -- but know it waits.

**And mail expires in 72 hours. A dark longer than that deletes every queued message, unread,
silently, at both ends.** `mail.ps1:121` sets `[int]$TtlMinutes = 4320`, 72 hours, chosen (its own
comment says) *"to span a weekend, which is the longest gap a working session is expected to sit
through"*.

**A 4.5-day dark is not a weekend.** Measured 2026-08-29T17:15Z against a return of
2026-09-03T09:59Z: 192 queued messages scanned, 192 expire before the fleet returns, zero survive, 0
unparseable -- the control, without which the total means nothing.

73 were already past expiry and still sitting in inboxes.

`mail.ps1:113` states the consequence itself: *"EXPIRY IS SILENT IN BOTH DIRECTIONS -- the recipient is never told a message existed, and
the sender is never told it went unread. That is the only place in this transport where a message is
genuinely LOST rather than merely late."*

**So before a long dark: do not mail anything you need read. Commit it.** A handoff, a finding, a
correction -- put it on a ref. A commit survives any gap; a queued message survives 72 hours.

**The receipt is the trap here.** Mail is the channel that leaves one, so a seat reasoning correctly
reaches for mail for its most important message of the day. That message is the one deleted.

If you must mail across a long gap, pass `-TtlMinutes` explicitly and say why -- the parameter
exists and nothing defaults it for you. Found by an adversarial audit; no seat had noticed the
default in a day of writing rules about this transport.

**The two channels have different blind spots, so "I could not reach them" needs to say which.**
Cross-session sees only sessions the message bus knows; desktop and VS Code seats are absent from
it.

Mail sees any worktree with a box, including seats the bus cannot see, but only delivers when they
next take a turn. Neither is a superset of the other.

Measured 2026-08-29: Builder 1 was absent from two seats' `ListAgents` and idle, so both channels
failed at once. That is rarer than either failing alone, and worth saying rather than reporting a
bare "unreachable".

**An over-length `mail.ps1` send queues nothing, and it is detectable by exit code.** A 2000+
character broadcast reached zero boxes while printing paragraphs. Measured: over-length send gives
exit 1; a control short send to the same target gives exit 0.

So check `$?`; you do not need `find .git/mefor-coord/mail/box -mmin -5` to know it failed. What
made it look silent is that the failure speaks in long prose calling itself *"a courtesy, NOT a
control"*. Self-deprecating wording on a hard refusal reads as advice.

**An error whose own text disclaims its authority will be read as optional.**

### Delivery has four grades and four instruments

| Grade | Instrument |
| --- | --- |
| `sent` | The sender's queue line. |
| `delivered` | The file is in the recipient's box. |
| `rendered` | The receipt's `disposition` in `mefor-coord/mail/receipts/<id>.json`: `shown-consumed` or `shown-held` when it was rendered, `expired-unshown` when it reached its TTL and nobody ever saw it. |
| `acted on` | Only the recipient can tell you. |

Do not read a queue line as delivery, a folder as rendering, or a rendering as action. **No receipt
at all means no drain has run yet**, which is not the same as `expired-unshown`, and the two look
identical from the sender's side.

**Record delivery at the strength you can actually support, and do not let a peer's assurance
upgrade it.** A seat's instinct was to record an owner item as *routed, delivery unconfirmed*,
having no receipt. A peer said it was delivered, and that assurance replaced the weaker, correct
wording.

The peer had resolved the recipient by session title, so "delivered" was true of a seat and false of
the queue. It retracted unprompted and said the original discipline was right. **A peer's confidence
is not evidence for any grade.**

**The receipt is the discriminator, not the folder. A message in `seen/` is not proof anyone saw
it.** A seat reported an owner item as drained because both copies had moved from `inbox/` to
`seen/`.

The conclusion was right and the reason was wrong. Folder position is where the drain put a message,
and a drain can move one for reasons other than rendering it. Checked afterwards: both carried
`shown-consumed`, so the claim survived, but it survived on evidence the seat had not looked at.

**A right answer reached by the wrong instrument is a coin that landed your way.**

**Enumerate the states a success can be in before you test for one of them.** A seat verified three
deliveries; two read DELIVERED and the third read `in-inbox=0`, which its check rendered as the
failure case. It was not missing -- it had already been drained.

Searching the whole mail tree instead of the one directory found it in `seen/` with a receipt:
delivered and consumed within seconds, the strongest possible outcome, reported as a failure.
**`inbox` and `seen` are both success; the success path moves the file between them.**

Had it stopped at that line it would have re-sent a message the recipient had already read. **Search
the tree, not the folder.**
