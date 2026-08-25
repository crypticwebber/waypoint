COURSE = {
    "title": "UX Design Foundations",
    "description": (
        "Learn how to research real user needs, structure information "
        "clearly, and design interfaces that people can actually use without "
        "a manual -- the foundational thinking behind every good product, "
        "regardless of which design tool you use."
    ),
    "category": "Design",
    "tags": ["ux research", "usability", "information architecture", "wireframing", "accessibility"],
    "level": "beginner",
    "duration_hours": 8,
    "color": "#B4507A",
    "project_brief": (
        "Pick a real app or website you use regularly and find one genuine "
        "usability problem in it. Conduct (or simulate, if needed) three "
        "quick user interviews about that flow, write up your findings, and "
        "produce a low-fidelity wireframe of your redesigned solution with a "
        "short rationale for each change, tied directly back to something a "
        "user said."
    ),
    "modules": [
        {
            "title": "Understanding real user needs",
            "description": "Why design starts with research, not with a blank canvas.",
            "lessons": [
                {
                    "title": "Design is not decoration",
                    "estimated_minutes": 13,
                    "content": """A common misconception, especially for people new to the field, is that UX
design means "making things look nice." Visual polish matters, but it's the
last layer applied to a decision that's already been made about *what* the
interface needs to do and *how* it should be structured. Good UX design is
fundamentally about reducing the gap between what a user is trying to
accomplish and what the interface asks them to do to accomplish it.

That gap shows up as friction: a form that asks for information in an
order that doesn't match how the user thinks about the task, an error
message that describes what went wrong in technical terms the user can't
act on, a critical action buried three menus deep because it wasn't used
often *during development*, even though it turns out to be used constantly
by real users. None of these are visual problems -- they're structural
ones, and no amount of better colors or typography fixes them.

The core discipline this course builds is: before proposing a solution,
understand the problem from the user's actual perspective, not from
assumptions about what they probably want. This sounds obvious stated
plainly, but it's the single most commonly skipped step under deadline
pressure -- it's much faster to jump straight to "here's my redesign" than
to first ask "what is actually going wrong for the person using this, and
why?"

Every lesson in this module works toward one practical skill: turning
"I think users want X" into "I have evidence users need X, and here's what
they told me or showed me that proves it." That evidence is what separates
a defensible design decision from a guess that happens to look
professional.""",
                },
                {
                    "title": "User interviews and finding real problems",
                    "estimated_minutes": 15,
                    "content": """A user interview is a structured conversation aimed at understanding how
someone actually behaves and thinks, not what they'd hypothetically say
they want. The single most important skill in conducting one well is
resisting the urge to ask leading questions -- questions that suggest the
answer you're hoping for.

Compare these two: "Don't you find this checkout flow confusing?" versus
"Walk me through the last time you bought something online -- what
happened?" The first invites agreement regardless of the person's actual
experience (most people will politely agree that *something* was
confusing, if only to be helpful). The second asks for a real, specific
story, which is far more likely to surface genuine friction the person
actually experienced, described in their own words rather than yours.

A few concrete habits make interviews substantially more useful:

- **Ask about specific past behavior, not hypothetical future behavior.**
  "What did you do the last time X happened?" produces far more reliable
  information than "What would you do if X happened?" -- people are
  notoriously bad at accurately predicting their own future behavior, even
  with the best intentions.
- **Follow up with "why" and "tell me more about that."** The first answer
  is often surface-level; the second or third follow-up is where the real
  insight usually shows up.
- **Watch for what people do, not just what they say**, whenever you can
  observe them actually using something -- people frequently describe their
  intended behavior inaccurately, not out of dishonesty, but because a lot
  of real usage is habitual and not something people consciously notice
  themselves doing.

The output of good interviews isn't a list of feature requests -- it's a
clear, specific understanding of a *problem*: what the person was trying to
do, what got in their way, and what it cost them (time, frustration, a
mistake, giving up entirely). That problem statement is what the rest of
the design process should trace back to.""",
                },
                {
                    "title": "Turning research into a clear problem statement",
                    "estimated_minutes": 13,
                    "content": """Raw interview notes -- however good the interviews were -- aren't
directly actionable. The bridge between research and design is
**synthesis**: distilling scattered observations into a small number of
clear, specific problem statements that a design solution can actually be
measured against.

A weak problem statement is vague enough to justify almost any design
decision: "Users find the checkout confusing." A strong one is specific
enough to be falsifiable and to point toward what actually needs to change:
"Users don't notice the 'apply discount code' field because it's visually
identical to the (unused) 'gift card' field above it, so they assume
there's no way to apply a discount and either abandon the purchase or
contact support." The second version tells you exactly what a successful
redesign has to fix, and exactly how you'd know if it worked.

A useful format for this is the **"How Might We" (HMW)** reframe, which
turns a problem into a direction for solutions without prematurely
committing to one specific answer: "How might we make the discount field
clearly distinguishable from other fields at the moment a user is deciding
whether they have a code to apply?" This is deliberately more open than
"add a bigger label to the discount field" -- it leaves room for solutions
you haven't thought of yet (maybe the real fix is reordering the fields,
not relabeling them), while still being anchored tightly to the specific,
evidenced problem.

Grouping similar observations across multiple interviews (a lightweight
form of **affinity mapping** -- literally clustering sticky notes or
bullet points that describe the same underlying issue) is what turns three
individual people's complaints into a pattern worth designing around,
versus one person's idiosyncratic preference that doesn't generalize. A
problem only one person mentioned might still be real, but it's much
weaker evidence than the same complaint surfacing independently across
several people who don't know each other.""",
                },
            ],
            "quiz": {
                "title": "Understanding User Needs Check",
                "questions": [
                    {
                        "question_text": "What's the main problem with a question like 'Don't you find this confusing?'",
                        "options": [
                            "It's grammatically incorrect",
                            "It's a leading question that invites agreement regardless of the person's real experience",
                            "It's too short",
                            "There's no real problem with it",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why ask about specific past behavior instead of hypothetical future behavior?",
                        "options": [
                            "Past behavior is more polite to ask about",
                            "People are notoriously unreliable at predicting their own future behavior",
                            "It takes less time to answer",
                            "There's no real difference",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What makes a problem statement 'strong' rather than 'weak'?",
                        "options": [
                            "It's phrased politely",
                            "It's specific enough to point toward what actually needs to change and be falsifiable",
                            "It's as short as possible",
                            "It includes a proposed visual design",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why does a 'How Might We' statement avoid naming one specific solution?",
                        "options": [
                            "It's just a stylistic convention with no purpose",
                            "It keeps the framing open to solutions not yet considered, while staying anchored to the evidenced problem",
                            "HMW statements are only used for visual design, not UX",
                            "It's required by usability testing standards",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "Structuring information and flows",
            "description": "Information architecture, navigation, and designing for how people actually think.",
            "lessons": [
                {
                    "title": "Information architecture: organizing so people can find things",
                    "estimated_minutes": 14,
                    "content": """**Information architecture (IA)** is the structural skeleton of a product:
how content and features are categorized, labeled, and connected, so a
user can predict where to find something without having to search
randomly. Good IA is invisible when it works -- nobody praises a website
for having a well-organized navigation menu -- and glaringly obvious the
moment it fails, when a user gives up looking for a feature that
technically exists somewhere in the product.

A core technique for building IA around how users actually think, rather
than how the engineering team organized the codebase, is **card sorting**:
give participants a set of content items (written on individual cards) and
ask them to group them into categories that make sense to them, then name
those categories in their own words. The categories people naturally
produce are often meaningfully different from how a product's internal
teams think about the same content -- and it's the user's mental model,
not the org chart, that the navigation should reflect.

A closely related concept is the **information scent**: the cues (labels,
icons, descriptions) that tell a user whether following a particular link
or button is likely to get them closer to their goal. A navigation label
like "Solutions" carries almost no information scent -- it could mean
anything -- while "Pricing" or "Integrations" tells a user exactly what
they'll find, letting them navigate confidently instead of clicking around
tentatively to explore.

Two structural patterns worth knowing explicitly: a **hierarchical**
structure (categories nested inside categories, like a file system) works
well when content naturally has a clear "parent/child" relationship, while
a **flat** structure (everything one level deep, distinguished mainly by
filtering and search) works better when items don't cleanly nest, or when
users are more likely to arrive at a specific item directly (via search or
a link) than to browse down through a hierarchy to find it.""",
                },
                {
                    "title": "Designing flows: reducing steps and decision points",
                    "estimated_minutes": 15,
                    "content": """A **user flow** maps the sequence of steps someone takes to complete a
task -- signing up, checking out, resetting a password -- and mapping it
explicitly, before designing individual screens, is what reveals
unnecessary friction that's easy to miss when you're only looking at one
screen at a time.

Two related principles guide most flow improvements. **Reduce the number
of steps** required to complete a task, because every additional step is
another point where a user might get confused, distracted, or simply give
up (this is measurable, and well-documented across countless checkout-flow
studies: each additional required field or page in an e-commerce checkout
correlates with measurably higher abandonment). **Reduce the number of
decisions** at each step -- a single, clear primary action per screen is
far easier to act on than five equally-weighted options competing for
attention, even if the underlying number of steps stays the same.

A concrete example: a multi-page signup flow that asks for email,
password, full name, phone number, company name, and job title *before*
letting someone see any value from the product delays the moment a user
experiences why they signed up in the first place. Asking only for email
and password up front, and deferring the rest to an optional profile step
*after* the user has already seen value, is a common and effective
pattern -- it front-loads the minimum necessary friction and defers
everything else.

Not every flow should be minimized blindly, though -- this is a case where
context matters more than the general rule. A flow with real
consequences (deleting an account, making a payment, submitting a legal
document) often *should* include an explicit confirmation step, even
though that technically adds friction -- the cost of an accidental
irreversible action is usually far higher than the small cost of one extra
click to confirm. The actual design skill is judging, case by case, when
friction is protecting the user from a costly mistake and when it's just
getting in their way for no real benefit.""",
                },
                {
                    "title": "Wireframing: designing structure before visuals",
                    "estimated_minutes": 13,
                    "content": """A **wireframe** is a deliberately low-fidelity layout -- boxes, rough
placeholders for text and images, no color or final typography -- used to
work out structure and hierarchy before investing time in visual polish. It
forces a genuinely useful constraint: without color, imagery, or
typography to lean on, a wireframe has to communicate hierarchy and flow
through structure alone -- size, placement, and spacing -- which is exactly
the layer of design most likely to get glossed over if you start with a
polished visual mockup instead.

Low fidelity is a *feature*, not a limitation, especially early on. A
rough, hand-drawn or grayscale wireframe invites feedback on the actual
structural decisions ("should this button be above or below the form?"),
whereas showing a polished, colorful mockup at the same stage tends to
pull feedback toward surface details ("I don't love that shade of blue")
that don't matter yet and can derail a conversation that should still be
about structure.

A useful discipline when wireframing: for every element you place, be able
to answer "what is this for, and why does it need to be here?" A wireframe
padded with decorative elements that don't serve the user's task defeats
the purpose of working in low fidelity in the first place -- the whole
point is to see the actual information hierarchy clearly, uncluttered by
anything not yet earning its place on the screen.

Visual hierarchy in a wireframe is communicated through a small set of
tools: **size** (bigger elements draw attention first), **position**
(top-left is typically scanned first in left-to-right reading cultures),
**spacing** (grouping related elements closer together, and separating
unrelated ones with more space, is often called "proximity" and is one of
the most powerful, least appreciated tools in interface design), and
**contrast** (a single prominent element stands out far more clearly
against a quiet background than one competing against five other equally
loud elements). These four tools, used deliberately, do most of the work
of guiding a user's eye through a screen in the order that actually matches
their task -- long before a single color or font choice enters the
picture.""",
                },
            ],
            "quiz": {
                "title": "Structuring Information & Flows Check",
                "questions": [
                    {
                        "question_text": "What is card sorting primarily used for?",
                        "options": [
                            "Testing color palettes",
                            "Discovering how users naturally group and label content, to inform navigation structure",
                            "Measuring page load speed",
                            "Writing marketing copy",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What does 'information scent' refer to?",
                        "options": [
                            "The literal smell of printed materials",
                            "How clearly a label or link communicates what a user will find if they follow it",
                            "The font used in navigation menus",
                            "The loading speed of a page",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "When should a flow deliberately keep an extra confirmation step rather than minimizing steps?",
                        "options": [
                            "Never -- fewer steps is always better",
                            "When the action has real, costly, or irreversible consequences, like deleting an account",
                            "Only on the homepage",
                            "Only for logged-out users",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why is low visual fidelity considered a feature of wireframing, not a limitation?",
                        "options": [
                            "It's faster to produce, which is the only reason",
                            "It keeps feedback focused on structure and hierarchy rather than surface details like color",
                            "Low fidelity wireframes are required by law in some countries",
                            "It has no real benefit, it's just a habit",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
        {
            "title": "Usability and accessibility",
            "description": "Testing whether a design actually works, and designing for everyone who might use it.",
            "lessons": [
                {
                    "title": "Usability testing: watching real people try to use it",
                    "estimated_minutes": 15,
                    "content": """A **usability test** asks a real person (ideally someone matching your
actual target user) to attempt specific tasks using your design, while you
observe -- not help, not explain, just watch and take notes. The goal isn't
to confirm the design works; it's to find out, honestly, where it doesn't,
which means the test only produces useful information if you resist the
urge to jump in and clarify the moment someone looks confused.

A well-run session follows a simple structure: give the participant a
realistic task ("find a beginner-level course about web development and
enroll in it"), not instructions ("click the search bar, then type..."),
because instructions test whether the person can follow directions, not
whether the interface itself is usable without them. Ask them to **think
aloud** as they go -- narrating what they're looking at, what they expect
to happen, and what confuses them -- which surfaces the *reasoning* behind
a mistake, not just the fact that a mistake happened.

The most important, and most frequently violated, rule of moderating a
usability test: don't help. If a participant is stuck, that's exactly the
data you came for -- the instinct to jump in and explain is strong,
especially when you designed the thing yourself and know exactly what
they're missing, but doing so erases the most valuable signal the whole
session was meant to produce. If a participant *does* get stuck badly
enough that the session can't continue, note exactly where and why before
moving on, rather than quietly rescuing them and pretending it went
smoothly.

Even a small number of participants surfaces real, often surprising
problems -- a commonly cited finding in usability research is that around
five participants tend to reveal the majority of a design's major usability
issues, because the same structural problems tend to trip up most people
in similar ways. This makes usability testing genuinely feasible even on a
small project or a tight timeline -- it doesn't require the sample sizes a
formal research study would.""",
                },
                {
                    "title": "Reading usability results without fooling yourself",
                    "estimated_minutes": 13,
                    "content": """It's tempting to explain away results that don't confirm what you already
believed about your design -- "that participant just wasn't paying
attention," "a real user wouldn't make that mistake." This instinct,
however understandable, undermines the entire point of testing, and it's
worth naming explicitly as a bias to actively guard against: if multiple
participants independently stumble on the same thing, the design is the
more likely explanation, not the participants.

A useful discipline is distinguishing between two very different kinds of
findings. A **usability problem** is something that gets in the way of
completing a task -- a button a participant couldn't find, a label they
misunderstood, a step they skipped because it wasn't visible. A
**preference** is something a participant said they'd personally like
differently, without it actually blocking task completion -- "I'd prefer
this button was green." Preferences are worth noting, but they don't carry
the same weight as an observed usability problem, and conflating the two
leads to redesigning around one person's taste while missing a real,
task-blocking issue a different participant hit.

Severity matters more than raw count. One participant failing to complete
a core task entirely is a more urgent finding than three participants
mentioning a minor visual annoyance that didn't stop them from finishing.
A simple, defensible severity scale -- something like "blocks task
completion," "causes a significant delay or visible frustration but is
eventually overcome," and "minor annoyance, no real impact on the
outcome" -- keeps a findings write-up honest and prioritized, instead of
treating every observation as equally important.

The output that actually changes a design isn't a list of every single
observation -- it's a small, prioritized set of specific, evidenced
problems, each traceable back to what a participant actually did or said,
in the same way a strong problem statement traces back to research rather
than assumption.""",
                },
                {
                    "title": "Designing for everyone: accessibility fundamentals",
                    "estimated_minutes": 14,
                    "content": """Accessibility means designing so people with a wide range of abilities --
visual, motor, auditory, cognitive -- can actually use what you've built,
not as an afterthought bolted on at the end, but as a constraint considered
alongside every other design decision from the start.

**Color contrast** is one of the most common and most avoidable failures:
light gray text on a white background might look clean and minimal, but
it's genuinely unreadable for many users with low vision, and difficult
even for users with typical vision in bright ambient light. The Web
Content Accessibility Guidelines (WCAG) define specific minimum contrast
ratios between text and its background for exactly this reason, and
checking a color pairing against them takes seconds with a free contrast
checker tool.

**Keyboard navigation** matters because not everyone uses a mouse or
touchscreen -- some users navigate entirely via keyboard, whether due to a
motor impairment, a screen reader, or simple personal preference. Every
interactive element (buttons, links, form fields) needs to be reachable
and operable via `Tab` and `Enter`/`Space` alone, with a clearly **visible
focus state** so a keyboard user can always see which element is currently
selected -- removing the default focus outline for aesthetic reasons
without providing a visible replacement is a common and serious
accessibility failure, not a minor cosmetic choice.

**Alt text** on images gives users of screen readers (which read a page's
content aloud) a text description of visual content they can't see
directly. Good alt text is specific and functional -- describing what the
image actually conveys in this context (`"Bar chart showing enrollment
tripled between January and March"`) rather than generic or absent
(`"image"` or an empty `alt=""` on an image that carries real information,
though an empty `alt=""` is correct for a purely decorative image that
conveys nothing).

These aren't a separate, optional "accessibility phase" tacked onto a
finished design -- they're the same underlying discipline this whole course
has built toward, just extended to more people: understand who's actually
trying to use what you're building, and reduce every unnecessary bit of
friction in their way.""",
                },
            ],
            "quiz": {
                "title": "Usability & Accessibility Check",
                "questions": [
                    {
                        "question_text": "Why should a usability test moderator avoid helping a stuck participant?",
                        "options": [
                            "It's considered rude in a professional setting",
                            "The moment of being stuck is exactly the data the test is meant to reveal",
                            "It takes too much time",
                            "Participants get upset if helped",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "What's the key difference between a 'usability problem' and a 'preference' in test findings?",
                        "options": [
                            "There's no meaningful difference",
                            "A usability problem blocks task completion; a preference is a stated taste that doesn't block the task",
                            "Preferences are always more important",
                            "Usability problems only apply to visual design",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "Why is removing the default keyboard focus outline without a replacement a serious accessibility issue?",
                        "options": [
                            "It slightly slows down page load",
                            "Keyboard-only users lose the ability to see which element is currently selected",
                            "It's purely a stylistic preference with no functional impact",
                            "It only affects mouse users",
                        ],
                        "correct_index": 1,
                    },
                    {
                        "question_text": "When is an empty alt=\"\" the correct choice for an image?",
                        "options": [
                            "Never -- every image needs descriptive alt text",
                            "For a purely decorative image that conveys no real information",
                            "Only for the site logo",
                            "Whenever the image is large",
                        ],
                        "correct_index": 1,
                    },
                ],
            },
        },
    ],
}
