# Event Storming for Claude

[한국어 README](README.ko.md)

A Claude plugin that runs a **text-based Event Storming** session on any software project you describe. Instead of drawing sticky-note diagrams, Claude asks for the information that is missing, lays out what happens in your business in time order, and then systematically hunts for gaps, conflicting rules, and risks that will hurt you later. The result is a set of tables you can hand straight to a planning or development team, ending with an estimated domain directory layout for your codebase.

## Skills

| Skill | Language | Use when |
|---|---|---|
| `event-storming` | English | You describe your project in English |
| `event-storming-ko` | Korean (한국어) | You describe your project in Korean |

Both skills follow the same procedure and produce the same tables; only the language differs.

## What you get

1. **Questionnaire table** – what Claude learned about your project, with guesses marked `(Assumption)`.
2. **Flow table** – every event in time order, with the action, user type, auto rule, viewed info, and external service behind it.
3. **Rule group and business area tables** – the units that guard your business rules, and where to draw boundaries.
4. **State tables** – which actions are allowed in which states, with every unknown raised as an issue.
5. **Issue table** – missing pieces, conflicts, ambiguities, and future risks, graded `[High]` / `[Medium]` / `[Low]`, each with a short confirmation question.
6. **Required feature table** – existing features versus newly required ones, plus policy decisions that must be made first.
7. **Top 3 questions** to confirm before anything else.
8. **Estimated domain directory table** – English directory names, the requests each domain receives, the rules it keeps, and who it collaborates with.

## Installation

**From the Claude plugin directory** (once listed): search for `event-storming` and install it.

**From this repository** in Claude Code:

```text
/plugin marketplace add Jinhan-Han-Jeremy/event-storming-skill
/plugin install event-storming@pathcraft
```

**For local testing** (from the repository root):

```bash
claude --plugin-dir .
claude plugin validate .
```

## Usage

Describe your project and ask for an Event Storming session, for example:

```text
Run an event storming session on my project: a marketplace where local bakers
sell same-day bread to nearby customers, with pickup or courier delivery.
```

Claude fills in what it already knows, asks only the missing questions in one batch, and then produces the tables above. Reply "just go ahead" to let Claude proceed with clearly marked assumptions.

## Privacy

This plugin contains only instructions (Markdown). It runs no code, makes no network requests, and collects, stores, or transmits no data. See [PRIVACY.md](PRIVACY.md).

## Development

```bash
python scripts/validate_plugin.py
python -m unittest discover -s tests
```

## License

[MIT](LICENSE) © 2026 Jinhan Han (pathcraft - Path Creator)
