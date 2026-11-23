---
name: event-storming
description: "Use when the user describes a project and wants it analyzed with a text-based Event Storming session: fill in missing information through targeted questions, map the flow as tables, then surface gaps, conflicts between rules, future risks, a required feature list, and an estimated domain directory layout for development. Use for English requests; for Korean requests use the event-storming-ko skill."
license: MIT
metadata:
  author: "Jinhan Han (pathcraft - Path Creator)"
  version: "1.0.0"
  language: "en"
---

# Event Storming (Text Edition)

## Purpose
Lay out the project the user describes, in order, centered on **"what happened"**.
Drawing a diagram is not the goal. The goal is to **find what is missing, which rules collide, and which problems may appear later, and organize them into tables ahead of time.**
Based on that result, **combine the features that already exist and the features newly required into a single list**,
and finally build an **estimated domain directory table** to be used in actual development.

## Principles
- Start from **things that actually happened**, not from features, screens, or database tables.
- Avoid jargon. Use only the words defined in [Terms] below.
- Deliver results as **tables**, not diagrams.
- **Follow the rules (counts, formats, criteria) of every step.** If a rule cannot be met, record that fact in the issue table.
- Record **only issues produced by the checking procedures.** Never invent issues to fill a quota.
- Every example in this skill exists **only to show the notation** and has nothing to do with the input project. Do not reuse example names, structures, or content in the result; take content **only from the input**.

## Terms
| Term used in this skill | Meaning | How to write it |
|---|---|---|
| Event | Something that actually happened in the business | Past tense. "Order was placed" |
| Action | The request that caused an event | Imperative. "Place order" |
| User type | The person or role performing an action | "Buyer", "Seller", "Inspector" |
| Auto rule | A rule that automatically triggers the next action when an event happens | `When A happens → do B` |
| Viewed info | Information a user checks before taking an action | "Cart screen", "Order history" |
| External service | A service we connect to instead of building ourselves | Payment, shipping, identity verification, SMS |
| Turning point | An event at which the flow moves into a clearly different stage | "Order was confirmed", "Item was shipped" |
| Rule group | A unit that receives actions, keeps its rules, and produces events | "Order", "Inventory" |
| Guaranteed rule | A condition a rule group guarantees will never be broken | "Stock can never go below 0" |
| State | A stage a rule group passes through | "Draft", "Published", "Deleted" |
| Business area | A business scope in which the same word always means the same thing | "Sales", "Delivery", "Settlement" |
| Request | (Step 5) Something one side sends to another saying "please do this". The name for an action of the flow table when it crosses between domains | "Reserve this quantity" |
| Response activity | (Step 5) What the receiving side does in reaction to a request | Check, change, request another domain, notify, reply |
| Domain | (Step 5) A unit that groups similar responsibilities and becomes an actual development folder | Written as an English directory name |

---

## Step 1. Project Question List
Before starting Event Storming, collect information with the questionnaire below.
- Fill in items the user's description already answers, and ask **only the empty items**, all at once.
- If the user says "just go ahead" or answers cannot be obtained, fill items with your best guess, prefix the answer with `(Assumption)`, and proceed.
- "Unknown" is an acceptable answer. Every "Unknown" item is raised again as a confirmation question in the issue table.

### Questionnaire
**1. What kind of app is it?**
- Who suffers from what inconvenience, and how does this app solve it? (one sentence)
- How does it make money? Who pays whom, and when?

**2. Who uses it?**
- What types of users does it have? (e.g., buyer, seller)
- For each user type:
  - What they can do / what they must not do
  - What they gain from this app
  - The moment they think "if this works, I'm satisfied"
  - The situation that troubles them the most

**3. In what order is it used? (per user type)**
- 1–3 representative flows, from start to finish, in order (e.g., apply → confirm → pay → receive)
- Is each step done by a person or automatically?
- Features users use outside the representative flows (e.g., save to wishlist, write a review, send an inquiry, edit my profile)

**4. What information is exchanged?**
- Information the user enters
- Information the user sees or receives as notifications

**5. How much is it used?**
- Roughly how many people use it? (now / expected in one year)

**6. Rules**
- "If ~, then ~" rules
- Steps that require someone's confirmation or approval
- Cancellation and refund rules

**7. Connections to other services**
- External services that must be connected (payment, shipping, identity verification, SMS, etc.)

### Step 1 Output
| Item | Answer |
|---|---|

---

## Step 2. Run Event Storming (10 sub-steps)
Cover the questionnaire's **representative flows in depth** and **additional features lightly** (2-1, 2-2, and 2-5 only).
Keep the order below, and satisfy each sub-step's **rule** before moving to the next.

| Sub-step | What to do | Rule | Easy to miss |
|---|---|---|---|
| 2-1 Collect events | Write down events from the questionnaire, in no particular order | **30–60 events** in total. All in past tense | Events from internal staff and automated processing, not just users |
| 2-2 Sort by time | Arrange events in order and separate the **normal flow** from **failure/alternative flows** | If one event has several names, **merge them into one** and record it in the issue table | Places where the flow breaks off midway |
| 2-3 Mark problem spots | Record problems in the issue table as soon as you see them | Check four things: **term conflicts, unclear rules, work without an owner, money/legal risks** | Items left as "Unknown" in the questionnaire |
| 2-4 Find turning points | Pick the events that change the stage of the flow and split it into sections | **3–7 turning points** | Whether each turning point has a failure/cancellation flow |
| 2-5 Actions and user types | For each event, attach **who + which action** produced it | Every event must have either a user type or an auto rule attached | Actions whose permission is unclear |
| 2-6 Auto rules | Attach rules in which an event automatically triggers the next action | Fixed format: `When A happens → do B` / with a condition: `When A happens and [condition] → do B` | Events with no next action |
| 2-7 Viewed info | Attach the information a person checks before acting | **At least 1** per action performed by a person | Information needed for a decision but not shown |
| 2-8 External services | Mark actions and events that touch an external service | For each connection point, write **what is sent and what is received** | No response, or an unexpected result |
| 2-9 Rule groups | Group into units that receive actions and produce events | For each group, write **at least 1 guaranteed rule** and a **state list**. If no guaranteed rule can be written, it is not a group: merge it into another group or turn it into viewed info | One rule kept jointly by several groups |
| 2-10 Split business areas | Split rule groups into business areas | Draw a boundary only when **at least one** of three criteria applies: ① a turning point ② a word changes meaning ③ the main user type changes | The same word used with different meanings in different areas |

### Flow Table (results of 2-1 to 2-8)
| Section | Flow | User type | Action | Event | Auto rule | Viewed info | External service |
|---|---|---|---|---|---|---|---|

- **Section**: The sections split in 2-4. Mark turning-point events with ★.
- **Flow**: `Normal` / `Failure/Alternative` / `Additional feature`
- Leave cells empty when nothing applies.
- If there are more than 40 events, **split the table by section**.

### Rule Group Table (result of 2-9)
| Rule group | Actions received | Events produced | Guaranteed rules | States |
|---|---|---|---|---|

### Business Area Table (result of 2-10)
| Business area | Rule groups included | Split criteria (①②③) | Events announced to other areas |
|---|---|---|---|

---

## Step 3. Find Issues (the core of this skill)
Perform all four checks **in order**. Each check looks from a different angle, so skip none of them.
Also review the issues recorded in 2-3 and the "Easy to miss" column of every sub-step table.

### 3-1. Event Check (when a single event goes wrong)
Ask these for every event in the representative flows.
- What if this event **does not happen**? (failure, interruption)
- What if it **happens twice**? (duplicate request, duplicate payment)
- What if it **happens late**? (delay, deadline exceeded)
- What if its **order changes**? (a cancellation arrives before the payment)
- What if **two people do it at the same time**? (two buyers purchase the last item simultaneously)
- What if it **must be undone**? (cancellation, refund, return)
- Can **someone who must not do it** do it? (permission)

### 3-2. State Check (when states and actions do not match)
Pick **up to 3** rule groups that have 3 or more states, focusing on the representative flows, and build the table below for each.
Rows are states; columns are **every action that touches that group** (including actions of other groups — for example, likes, comments, and reports that touch a "Post").
Fill cells with `Allowed` / `Blocked` / `?`. Use `?` when the input does not provide the answer, and **raise every `?` in the issue table.**

| State \ Action | Action A | Action B | Action C |
|---|---|---|---|
| State 1 | Allowed | Blocked | ? |

Below the table, check each item on one line.
- Does every state have an action that enters it and an action that leaves it? (A state you cannot leave is an issue.)
- When the state changes, what happens to things already attached (comments, likes, notifications, public exposure)?

### 3-3. Cross Check (when two things collide)
Compare the four pairs below against each other to find contradictions. Record any contradiction found with the type `Conflict`.
| Pair compared | What to look for | Example |
|---|---|---|
| Rule ↔ Rule | Two rules that cannot be satisfied at the same time | "Exclude immediately when made private" vs "Notify followers immediately on publish" |
| Rule ↔ A user's troubling situation | Following a rule troubles some user type | "Publish instantly without approval" vs the operator's "spam flooding" |
| User type ↔ User type | One type's gain is another type's loss | The operator's ad revenue vs the reader's "ads cover the code" |
| Allowed ↔ Not allowed | Combining actions makes a forbidden thing possible | "Can edit posts" + "Ad scripts forbidden" → can scripts be inserted into the body? |

### 3-4. User Expectation Check (whether questionnaire answers are reflected in the flow)
- For each user type, does the **"satisfied moment"** exist as an event in the flow table? If not, `Missing`.
- For each user type, is there a flow that prevents or handles the **"troubling situation"**? If not, `Missing`.
- For each **"must not do"**, is there a rule or state that blocks it? If not, `Missing`.

### Issue Table
Choose a category from:
`Users/Permissions` / `Flow order` / `State` / `Failure/Cancellation` / `Time/Deadline` / `Money/Settlement` / `Information` / `External service` / `Rule` / `Terms` / `User growth`

Choose a type from:
- `Missing`: something that should exist does not
- `Conflict`: things that do not fit together
- `Ambiguous`: the meaning or criterion is unclear
- `Future risk`: fine now, but may become a problem later

Prefix the impact with a grade:
- `[High]`: loss of money or data, legal problems, or the representative flow stops
- `[Medium]`: some users or additional features do not work properly
- `[Low]`: inconvenient but has a workaround

| Step | Category | Type | Issue | Situation | When it occurs | Impact | Confirmation question |
|---|---|---|---|---|---|---|---|
| 3-1 | Failure/Cancellation | Missing | No inventory handling flow after a payment failure | When a payment fails | Right after the payment request | [High] Unsold items appear sold out | When a payment fails, when should the reserved stock be released? |

- Write **When it occurs** as a position in the flow ("right after the payment request") or an operating period ("right after launch", "as users grow", "when rules change").
- Write **Confirmation questions** so the user or business staff can answer yes/no or briefly.
- Merge issues with the same cause into one, and list every step in the Step column (e.g., `3-1, 3-2`).
- Below the issue table, write the **count per category** on one line. For a category with 0 issues, review the flow once more from that category's angle; if still none, write "Checked, none".

---

## Step 4. Organize Required Features
Using the flow table and the issue table as material, gather required features into one table. Do not invent anything new; list **only what has a basis in those two tables**.

### Where features come from
| Material | Feature extracted | Category |
|---|---|---|
| Actions performed by people in the flow table | A feature that lets them perform that action (e.g., "Place an order") | Existing |
| Viewed info in the flow table | A feature for viewing that information (e.g., "View order history") | Existing |
| Auto rules in the flow table | An automatically processed feature (e.g., "Payment completion notification") | Existing |
| Additional features from the questionnaire | Copy as is (e.g., "Save to wishlist", "View announcements") | Existing |
| Issues in the issue table | A feature that prevents or handles the issue (e.g., "Restore stock on payment failure") | New |

### Rules
- Name features as **what the user becomes able to do**, like "Do ~" or "View ~". Do not use screen or button names. Automated features may use noun phrases ("Order limit for new accounts").
- If the same feature comes from several places, merge it into one row and list every basis.
- One issue may produce several features.
- For a basis that is an event, write the event name; for an issue, write `Issue: ` followed by a short description.
- **Every issue must appear at least once as a basis in the feature table, or be listed under "Decisions that are not features" below the table.** Issues where a policy must be decided before the feature can be defined belong there.

### Required Feature Table
| Feature | Basis | User type | Category |
|---|---|---|---|
| Place an order | Order was placed | Buyer | Existing |
| Restore stock on payment failure | Issue: No inventory handling flow after a payment failure | (Automatic) | New |

- Sorting: place `Existing` first in business-area order, then `New` in order of the impact grade of the basis issue ([High] → [Low]).
- Below the table, write `Existing N / New N` on one line.

### Decisions that are not features
| Decision to make | Basis issue | Feature created once decided |
|---|---|---|
| Whether to allow partial refunds | Issue: No rule for cancelling only some items in a multi-item order | If allowed, "Refund some items" |

---

## Step 5. Organize the Estimated Domain Directories
Based on the results of Steps 2–4 (flow table, rule group table, business area table, required feature table), build an **estimated domain directory table** to be created in actual development.

### How to build it (work through this mentally; do not output it)
1. For each representative flow, decide **which requests travel** from the starting request to the final result (event) **first**. Decide domains later.
2. Name requests by the sender's intent ("what"), never "how".
   (Notation example: "Reserve this quantity" ✔ / "Subtract the quantity value" ✘)
3. The receiver of a request is **the side that holds the information and guaranteed rules needed to handle it**. Rule groups are the first candidates.
4. Do not pull state out and decide outside. The receiver makes the decision.
5. When crossing business areas, do not request directly; announce it with an event. The only exception is when the result must be known immediately.
6. Gather identical receivers into domains. Remove domains that receive no requests, and split domains that mix responsibilities that change for different reasons.

### Directory naming rules
- Lowercase English **singular nouns**. Use kebab-case for multiple words. If the project already has a naming convention, follow it.
  (Notation example: `invoice`, `delivery-slot`)
- Translate the **business terms from the input** into English, not technical names. Never use `service`, `manager`, `common`, `util`, `data`, or `info`.
- Paths have at most 2 levels: `<business-area>/<domain>`. If a business area contains only one domain, use just `<domain>`.
- If the same term means different things in different business areas, give it different English names.

### Estimated Domain Directory Table
The row below is a placeholder showing what goes into each cell. The actual table has one row per domain of the input project.

| Directory path | Domain (input term) | Requests received | Response activities (what it does on receiving a request) | What it knows | Guaranteed rules | Collaborating domains |
|---|---|---|---|---|---|---|
| `<business-area>/<domain>` or `<domain>` | The term used in the input | Every request this domain receives (in the sender's intent) | For each request: check, change, request another domain, notify, or reply | Information needed for its response activities | Every rule this domain keeps from breaking | Directory paths of domains it exchanges requests with |

- Prefix cells without a basis in the input with `(Assumption)`.
- Below the table, write one line each: domains that differ from the rule groups and why, and places where two domains jointly keep the same rule (if any).

---

## Step 6. Self-Check Before Output
- [ ] There are 30–60 events, all in past tense (if out of range, the reason is recorded in the issue table)
- [ ] There are 3–7 turning points
- [ ] Every event has a user type or an auto rule attached
- [ ] Every auto rule follows the `When A happens → do B` format
- [ ] Every action performed by a person has viewed info
- [ ] Every rule group has guaranteed rules and a state list
- [ ] Every business area has its split criteria (①②③) written
- [ ] All of 3-1 to 3-4 were performed
- [ ] Every `?` in the state tables is in the issue table
- [ ] Every "Unknown" item from the questionnaire is in the issue table
- [ ] Every person-performed action, viewed info, and auto rule in the flow table, and every additional feature from the questionnaire, appears in the feature table as `Existing`
- [ ] Every issue is a basis in the feature table or listed under "Decisions that are not features"
- [ ] Every representative-flow action in the flow table appears in some domain's "Requests received"
- [ ] Directory names follow the naming rules (lowercase English singular, kebab-case, no forbidden names, at most 2 levels)
- [ ] No names or content from the examples leaked into the result
- [ ] Apart from directory names, only the words defined in [Terms] were used, without jargon

If any item fails, fix it before output.

## Final Output Order
1. Questionnaire table (Step 1)
2. Flow table, rule group table, business area table (Step 2)
3. State tables (3-2)
4. Issue table (Step 3): sorted by impact grade, with the count per category below it
5. Required feature table and decisions that are not features (Step 4)
6. The 3 questions to confirm first
7. Estimated domain directory table (Step 5): output last
