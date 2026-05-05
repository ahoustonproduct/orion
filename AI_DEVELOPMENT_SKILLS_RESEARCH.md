# AI Development Skills Research for Orion

Date: 2026-05-05

## Purpose

This paper summarizes GitHub research into skill files, agent guidance, vibe-coding
workflows, full-stack development guidance, code auditing, security auditing,
frontend/backend practice, and design-system guidance. The goal is to decide what would
actually help Orion move faster while raising the engineering bar.

Orion's current priority is the Core Analytics rebuild for WashU MSBA Financial
Technology Analytics preparation. The useful skill stack should therefore help with four
things:

- preserving product decisions across sessions
- rebuilding curriculum from a finance-first viewpoint
- shipping Next.js plus FastAPI changes with fewer regressions
- auditing UI, backend, and security before the app grows more complex

## Executive Findings

The best GitHub material does not point to one giant "vibe coding" prompt. It points to
a layered operating system for agentic development:

1. A project instruction file, usually `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or
   `.github/copilot-instructions.md`, so agents can reliably find repo context,
   commands, coding standards, and product constraints.
2. A `DESIGN.md` file that gives agents a concrete visual language: color roles,
   typography, component rules, layout principles, responsive behavior, and do/don't
   guardrails.
3. Small role-based skills for distinct jobs: product framing, engineering plan review,
   frontend design review, backend contract review, security audit, QA, release
   documentation, and post-change regression review.
4. Mechanical verification tools: tests, linting, browser QA, CodeQL, Semgrep, Bandit,
   Gitleaks, and OWASP checklists.
5. A project-specific curriculum skill, because Orion is not a generic CRUD app. It is a
   local study system for finance-first analytics learning.

The main recommendation is not to install every impressive-looking skill pack. We should
create a small Orion-native stack, then selectively borrow patterns from the strongest
public repositories.

## What I Found

### 1. Vibe Coding Needs Guardrails

The GitHub vibe-coding ecosystem is energetic, but the serious guidance converges on the
same point: natural language can accelerate software creation, but humans still need to
own judgment, testing, and feedback.

The `roboco-io/awesome-vibecoding` guide lists key principles including context
management, responsibility boundaries, trust-building, and iterative testing. Its
framing is useful because it treats AI-generated code as something to verify with tests
and feedback, not as magic output. The `cpjet64/vibecoding` repository also recommends a
reading path that includes AI collaboration, prompt engineering, and quality assurance
for AI-generated code.

Benefit for Orion:

- gives us permission to move quickly without pretending speed is enough
- encourages short, explicit briefs before code changes
- makes review and QA part of the normal workflow

How we would use it:

- every significant Orion change starts from a short product/engineering brief
- every implementation ends with targeted tests or a clear note about what could not be
  tested
- "vibe" becomes product intent plus verification, not loose improvisation

Relevant sources:

- [roboco-io/awesome-vibecoding](https://github.com/roboco-io/awesome-vibecoding)
- [cpjet64/vibecoding](https://github.com/cpjet64/vibecoding)
- [taskade/awesome-vibe-coding](https://github.com/taskade/awesome-vibe-coding)

### 2. AGENTS.md Is The Strongest General Project Guide Pattern

The `agentsmd/agents.md` repository describes `AGENTS.md` as a simple open format for
guiding coding agents, essentially a README for agents. Its examples include development
environment tips, testing instructions, linting, and PR instructions. GitHub's Copilot
documentation now also recognizes repository custom instructions, path-specific
instructions, and agent instructions such as `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.

Benefit for Orion:

- fewer repeated handoffs about product decisions
- fewer mistaken commands, ports, and test assumptions
- better continuity across Codex, Claude, Copilot, Gemini, or future agents

How we would use it:

- create a root `AGENTS.md`
- include the current Orion product decisions: single local user, Core Analytics first,
  finance-first examples, no streaks, Python/pandas first, Excel supporting
- include exact frontend/backend commands and known ports
- include "Questions for Hack" as a reporting convention
- include rules for not reintroducing YouTube generation into the app

Recommended Orion file:

- `AGENTS.md`

Relevant sources:

- [agentsmd/agents.md](https://github.com/agentsmd/agents.md)
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)

### 3. Skills Should Be Small And Progressive

The Anthropic Claude Code plugin development examples are useful even when we are
working in Codex, because the skill structure is similar: `SKILL.md` should stay lean,
with deeper materials moved into `references/`, reusable scripts in `scripts/`, and
output templates in `assets/`. This is the right pattern for Orion because our biggest
risk is context bloat.

Benefit for Orion:

- a skill can activate only when relevant
- detailed checklists do not flood every session
- validation scripts can be reused instead of retyped

How we would use it:

- keep each Orion skill under a narrow trigger
- put long checklists in `references/`
- create scripts only for safe deterministic checks, not for hidden behavior
- avoid huge "do everything" skills

Recommended Orion structure:

```text
.claude/skills/
  orion-core-analytics/
    SKILL.md
    references/
      statistics-for-fintech-decisions.md
      lesson-schema.md
  orion-security-audit/
    SKILL.md
    references/
      owasp-api-checklist.md
      local-app-threat-model.md
```

Relevant sources:

- [Anthropic Claude Code](https://github.com/anthropics/claude-code)

### 4. Gstack Is A Useful Role Model, Not Something To Copy Blindly

Garry Tan's `gstack` is the most complete role-based AI engineering workflow I found.
Its docs list specialists for office-hours product framing, CEO review, engineering
review, design review, QA, security, release, benchmarking, docs, and memory. The
important lesson is the sequence: think, plan, build, review, test, ship, reflect.

Benefit for Orion:

- shows a working model for a "virtual product team"
- gives us role names and review gates worth adapting
- reinforces that QA and release docs are separate jobs

How we would use it:

- adapt the workflow, not necessarily install the entire pack
- create Orion-native equivalents for product, engineering, design, QA, security, and
  docs
- keep Hack in the decision loop for product taste and scope

External skill candidates to inspect later:

- gstack `plan-eng-review`, `review`, `qa`, `cso`, `document-release`
- Arc `audit`, `review`, `implement`, `design`, `document`, `testing`
- TDD-oriented skills from `glebis/claude-skills`

Risks:

- large external skill packs may include scripts, hooks, or assumptions that do not fit
  Orion
- some skills are opinionated for teams, cloud apps, or deployment workflows that Orion
  does not need yet
- install only after security review

Relevant sources:

- [garrytan/gstack skills](https://github.com/garrytan/gstack/blob/main/docs/skills.md)
- [howells/arc](https://github.com/howells/arc)
- [glebis/claude-skills](https://github.com/glebis/claude-skills)

### 5. DESIGN.md Is A Strong Pattern For Agentic Frontend Work

The `DESIGN.md` ecosystem is young but useful. `VoltAgent/awesome-design-md` frames
`DESIGN.md` as a plain-text design-system document for AI agents. Its examples capture
visual theme, color roles, typography, components, layout, elevation, do/don't rules,
responsive behavior, and prompt guidance.

Important caveat: many public `DESIGN.md` files are community-extracted or inspired by
public websites. They are not necessarily official company design files. For Orion, the
correct move is to create an original Orion `DESIGN.md`, using public examples as
structure inspiration, not brand copying.

Benefit for Orion:

- makes the UI more consistent
- prevents random one-off design choices
- lets frontend changes preserve a study-app identity
- helps us avoid generic AI-looking dashboards

How we would use it:

- create `DESIGN.md` at the repo root
- define Orion as a calm, finance-learning workspace, not a marketing landing page
- define accessible colors, type scale, components, empty states, dashboards, lesson
  cards, quiz states, and notebook module states
- include rules for dense but readable study interfaces
- include responsive behavior for dashboard, curriculum, lesson, progress, notebooks,
  and quiz pages

Recommended Orion file:

- `DESIGN.md`

Useful design references:

- `VoltAgent/awesome-design-md` for file structure
- fintech-inspired examples such as Stripe, Coinbase, Wise, and Mastercard only as
  mood-board input
- Orion should remain original and tailored to a local learner

Relevant source:

- [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

### 6. Security Auditing Should Combine Checklists And Scanners

Security material on GitHub is mature. OWASP ASVS provides application security
requirements. OWASP API Security focuses on risks in APIs. OWASP Cheat Sheet Series
gives practical guidance by topic. CodeQL provides semantic code scanning. Trail of Bits
publishes Semgrep rules used in security audits. Bandit scans Python ASTs for common
security issues. Gitleaks detects committed secrets.

Benefit for Orion:

- catches risks before we accidentally normalize them
- especially relevant because Orion has a Python execution route and AI routes
- protects local secrets, API keys, and future imported curriculum data

How we would use it:

- create an Orion security-audit skill that checks changed files against:
  - OWASP API risk areas for FastAPI routes
  - ASVS basics for input validation, secrets, access control, logging, and error
    handling
  - Bandit for Python code
  - Gitleaks for secrets
  - Semgrep for higher-signal static patterns
  - CodeQL later if/when the repo is pushed to GitHub Actions
- require extra review when touching:
  - `backend/routes/execute.py`
  - `backend/routes/ai.py`
  - notebook import/storage code
  - env/config handling
  - markdown rendering and sanitization

Recommended Orion skill:

- `.claude/skills/orion-security-audit/SKILL.md`

Relevant sources:

- [OWASP ASVS](https://github.com/OWASP/ASVS)
- [OWASP API Security](https://github.com/OWASP/API-Security)
- [OWASP Cheat Sheet Series](https://github.com/OWASP/CheatSheetSeries)
- [github/codeql-action](https://github.com/github/codeql-action)
- [trailofbits/semgrep-rules](https://github.com/trailofbits/semgrep-rules)
- [PyCQA/bandit](https://github.com/PyCQA/bandit)
- [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks)

### 7. Orion Already Has Useful Skills, But They Need Curation

The repo already tracks these skills:

- `.claude/skills/data-storytelling`
- `.claude/skills/e2e-testing`
- `.claude/skills/error-handling-patterns`
- `.claude/skills/fastapi-pro`
- `.claude/skills/kpi-dashboard-design`
- `.claude/skills/nextjs-app-router-patterns`
- `.claude/skills/python-testing-patterns`
- `.claude/skills/react-component-performance`
- `.claude/skills/react-state-management`

They are a good starting inventory. The most directly useful for Orion right now are:

- `nextjs-app-router-patterns`
- `fastapi-pro`
- `python-testing-patterns`
- `e2e-testing`
- `data-storytelling`
- `kpi-dashboard-design`

Concerns:

- several are broad community skills rather than Orion-specific
- at least two have `risk: unknown`
- some content has encoding artifacts, suggesting they were imported mechanically
- none encode the Core Analytics product contract or finance-first curriculum direction

Recommendation:

- keep them for now
- do not add a large pile of new generic skills
- add a thin Orion-specific layer above them
- later, audit and tighten the existing skill descriptions so they trigger only when
  useful

## Recommended Orion Skill Stack

### 1. Orion Operating Manual

File:

- `AGENTS.md`

Benefit:

- keeps product decisions and dev commands stable across agent sessions

How we would use it:

- every agent reads it before major work
- includes product decisions, commands, testing, ports, "no YouTube generation in app",
  and "no streak mechanics"

Priority:

- highest

### 2. Orion Design System

File:

- `DESIGN.md`

Benefit:

- gives frontend work a consistent visual system

How we would use it:

- use before dashboard, curriculum, progress, notebooks, lesson, and quiz UI changes
- define visual rules for finance-learning dashboards and polished deliverables

Priority:

- highest for frontend rebuild work

### 3. Core Analytics Curriculum Builder

File:

- `.claude/skills/orion-core-analytics/SKILL.md`

Benefit:

- converts generic curriculum changes into finance-first, WashU MSBA-aligned learning
  modules

How we would use it:

- build modules, drills, quizzes, and projects from the learner profile
- enforce Python/pandas first and Excel supporting
- require short daily drills, adaptive recommendations, review of misses, and polished
  deliverables

Priority:

- highest for the next product phase

### 4. Statistics For Fintech Decisions

File:

- `.claude/skills/orion-statistics-for-fintech-decisions/SKILL.md`

Benefit:

- focuses the first serious rebuild on shaky statistics through fintech examples

How we would use it:

- build lessons around A/B testing, conversion, underwriting, default rates, fraud,
  volatility, model error, confidence intervals, and decision risk
- pair concepts with small pandas tasks
- generate beginner-friendly explanations and short drills

Priority:

- highest for the first curriculum rebuild

### 5. Full-Stack Feature Planner

File:

- `.claude/skills/orion-full-stack-feature-plan/SKILL.md`

Benefit:

- turns product intent into frontend, backend, data, state, and test changes before
  coding

How we would use it:

- use when a change touches both `frontend` and `backend`
- produce a compact plan with affected routes/components/models/tests
- keep "Questions for Hack" at the end

Priority:

- high

### 6. Frontend UX Auditor

File:

- `.claude/skills/orion-frontend-ux-audit/SKILL.md`

Benefit:

- catches layout, copy, responsiveness, state, and interaction problems that lint cannot
  see

How we would use it:

- run after meaningful UI changes
- use browser screenshots and real navigation
- check dashboard density, mobile fit, accessible contrast, empty states, text overflow,
  and whether the page feels like a serious study tool

Priority:

- high

### 7. Backend Contract Auditor

File:

- `.claude/skills/orion-backend-contract-audit/SKILL.md`

Benefit:

- protects API and data behavior as notebooks, lessons, progress, mastery, quiz, and
  review logic evolve

How we would use it:

- inspect FastAPI routes, Pydantic/SQLAlchemy models, response schemas, and frontend API
  client assumptions
- require tests for changed behavior
- watch for stale contract drift between frontend and backend

Priority:

- high

### 8. Security Auditor

File:

- `.claude/skills/orion-security-audit/SKILL.md`

Benefit:

- gives local app development a practical security review loop

How we would use it:

- run when backend routes, execution sandbox, AI calls, imports, storage, markdown
  rendering, or env handling change
- combine OWASP review with Bandit, Gitleaks, Semgrep, and eventually CodeQL

Priority:

- high

### 9. Code Review And Regression Auditor

File:

- `.claude/skills/orion-code-review/SKILL.md`

Benefit:

- catches behavior regressions and missing tests before we stack more curriculum changes
  on top

How we would use it:

- review current diff before each handoff
- lead with concrete findings
- verify tests and note untested risk

Priority:

- high

### 10. Documentation Release Writer

File:

- `.claude/skills/orion-doc-release/SKILL.md`

Benefit:

- keeps product contracts and app docs from drifting behind code

How we would use it:

- after product changes, update product contracts, implementation notes, and report
  decisions
- preserve "Questions for Hack" at the end of reports

Priority:

- medium

## Recommended Workflow For Orion

For curriculum/product work:

1. Read `AGENTS.md`, `CORE_ANALYTICS_PRODUCT_CONTRACT.md`, and
   `NOTEBOOK_PRODUCT_CONTRACT.md`.
2. Use `orion-core-analytics` or `orion-statistics-for-fintech-decisions`.
3. Produce a short implementation plan.
4. Implement frontend/backend/content changes.
5. Run focused backend tests and frontend lint.
6. Use `orion-code-review` for diff review.
7. Use `orion-frontend-ux-audit` if UI changed.
8. Use `orion-security-audit` if backend, execution, AI, import, storage, or markdown
   changed.
9. Update docs with `orion-doc-release`.
10. End reports with "Questions for Hack".

For normal full-stack features:

1. Use `orion-full-stack-feature-plan`.
2. Implement with existing `nextjs-app-router-patterns`, `fastapi-pro`, and
   `python-testing-patterns` only as needed.
3. Verify with lint/tests.
4. Review diff.
5. Update docs if the product contract changed.

## External Skills To Consider Later

### Gstack

Use as inspiration first. Consider installing only after vetting scripts, hooks, and
assumptions.

Best borrowed ideas:

- product office-hours
- engineering plan review
- design review
- QA
- security officer
- document release

### Arc

Worth further evaluation because it groups audit, review, implement, design, document,
and testing workflows. Best considered after we have Orion's own `AGENTS.md` and
`DESIGN.md`.

### Glebis Claude Skills

Useful to study for TDD and context-building patterns. I would not install broadly until
we identify one specific workflow gap.

### Design.md Collections

Use as references, not imports. Orion needs its own original design system.

## Security Notes For Skill Installation

Skills and plugins are executable context. Some include scripts, hooks, settings,
browser automation, or external service assumptions. Before installing external packs:

- read every `SKILL.md`
- inspect `scripts/`, `hooks/`, and settings files
- avoid automatic session-start hooks unless they are clearly safe
- reject hardcoded paths, hidden network calls, and destructive commands
- prefer prompt-only skills until trust is established
- keep installed skills minimal

The Anthropic hook-development guidance is especially relevant: validate inputs, check
paths, quote variables, set timeouts, and avoid trusting user input in command hooks.

## First Implementation Recommendation

The next best move is:

1. Create `AGENTS.md` for Orion.
2. Create `DESIGN.md` for Orion.
3. Create one curriculum skill: `orion-statistics-for-fintech-decisions`.
4. Create one audit skill: `orion-code-review`.
5. Start the Core Analytics rebuild with Statistics for Fintech Decisions, supported by
   Python/pandas.

This keeps the stack small while giving Orion durable memory, design consistency,
curriculum focus, and review discipline.

## Questions for Hack

- Should I create `AGENTS.md` and `DESIGN.md` next, or start directly with the
  `orion-statistics-for-fintech-decisions` skill?
- For Orion's visual direction, should it feel more like a calm academic finance
  workspace, a fintech analyst dashboard, or a polished personal study cockpit?
- Do you want external skill packs like gstack installed after vetting, or should we
  build only Orion-native skills for now?
- Should security auditing become a required step only for backend/execution changes, or
  for every meaningful diff?
