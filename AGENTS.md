# AGENTS.md

This file is the operating manual for AI agents working on Orion. Read it before
making product, code, curriculum, design, security, or documentation changes.

## Product North Star

Orion is a local study app for one learner preparing for the WashU MS in Business
Analytics program, Financial Technology Analytics concentration. The first serious
curriculum rebuild is Core Analytics.

The app should help Hack earn high grades by building dependable skill in statistics,
Python, pandas, SQL, data visualization, and finance math. Lessons, examples, drills,
quizzes, and projects should use finance and fintech contexts whenever that framing is
natural.

## Current Product Decisions

- Orion is for one local user.
- Progress should follow Hack across this Windows device and the MacBook LAN URL. Use
  the stable local user key `orion_local_user` by default so `localhost`, `127.0.0.1`,
  and `http://<windows-lan-ip>:3000` do not split progress into separate browser
  profiles.
- Core Analytics comes first.
- Python and SQL are beginner level.
- Statistics is shaky and needs patient rebuilding.
- Finance/accounting basics are familiar, but formulas need rebuilding.
- Finance math should be taught from scratch.
- Teach Python/pandas first. Use Excel as a supporting skill.
- Frame curriculum from a finance/fintech viewpoint.
- Do not use streak mechanics.
- Default daily study target is 60 minutes.
- Use short daily drills, adaptive recommendations, review of misses, and polished
  deliverables.
- YouTube generation does not belong inside the running app.
- Future YouTube or external source work should happen outside Orion, then import saved
  modules later.

## Core Documents

Read these when the work touches product direction, curriculum, notebooks, or agent
process:

- `CORE_ANALYTICS_PRODUCT_CONTRACT.md`
- `NOTEBOOK_PRODUCT_CONTRACT.md`
- `AI_DEVELOPMENT_SKILLS_RESEARCH.md`
- `DESIGN.md`

Current design decision:

- Use Calm Academic Finance Workspace as the design direction.
- Preserve the existing warm stone/amber color scheme unless Hack chooses a redesign.
- Do not add mockup-only nav tabs such as `Data Lab` or `Analytics` unless the feature
  is explicitly defined and implemented.

## Repository Shape

- `backend/`: FastAPI, SQLAlchemy, curriculum routes, progress, quiz, review,
  notebooks, execution, and decision routes.
- `backend/curriculum_data/`: built-in curriculum modules.
- `backend/tests/`: backend contract tests.
- `frontend/`: Next.js App Router app.
- `frontend/components/`: reusable UI and lesson components.
- `frontend/app/`: pages and route segments.
- `.claude/skills/`: currently tracked Claude-style skills. Treat broad community
  skills as optional guidance, not binding law.
- `windows-shortcuts/`: Windows helper scripts for running Orion.

## Local Runbook

Known local URLs:

- Frontend: `http://127.0.0.1:3000`
- Backend health: `http://127.0.0.1:8000/health`
- MacBook access: use the Windows PC LAN URL printed by `Orion Start`, usually
  `http://<windows-lan-ip>:3000`.

Useful commands:

```powershell
# Start the full Windows app flow from the repo.
.\start-windows.ps1

# Install double-click desktop shortcuts.
.\windows-shortcuts\Install-Orion-Desktop-Shortcuts.ps1

# Stop Orion when launched through the desktop shortcut flow.
.\windows-shortcuts\Stop-Orion.ps1

# Frontend lint.
Set-Location frontend
npm run lint

# Frontend build.
Set-Location frontend
npm run build

# Backend contract tests.
Set-Location backend
python -m unittest discover tests
```

Use the repo's existing virtualenv, node modules, and helper scripts when they are
present. Do not introduce a new package manager or framework unless Hack explicitly
chooses that direction.

## Implementation Rules

- Prefer the repo's existing patterns over new abstractions.
- Keep edits narrowly scoped to the task.
- Do not reintroduce in-app YouTube transcript fetching or notebook generation.
- Do not reintroduce local AI model, Ollama, LoRA training, or `/orion` tutor routes.
- Do not add multi-user account management, social features, or institutional
  permissions.
- Do not add streak UI, flame-as-motivation language, streak counters, daily streak
  badges, streak recovery, or streak pressure.
- It is acceptable to show study minutes, days studied, lessons completed, review due,
  mastery, confidence, weak topics, deliverables, and attempts.
- Be careful with stars. Existing stars may remain until replaced, but new work should
  prefer mastery, confidence, completion, review, or deliverable language.
- When changing frontend and backend together, identify the route, model, API client,
  component, page, and test impact before editing.
- When changing curriculum, make the example finance-first unless an abstract example
  is genuinely clearer for a beginner.
- When removing a product feature, remove its model fields, API fields, prompts,
  frontend types, tests, UI states, copy, and docs references. Do not merely hide the
  UI or disable the entry point.
- Normal local use should feel like a desktop app: fixed ports, explicit launch,
  double-click Start/Stop shortcuts, clear plain-text errors, and no admin requirement
  except the one-time removal of old Windows services.

## Curriculum Rules

Core Analytics work should map toward WashU common-core preparation:

- DAT 5561 Introduction to Python and Data Science
- DAT 5563 Data Visualization for Business Insights
- DAT 5564 Database Design and SQL
- DAT 5569 A/B Testing in Business and Social Science
- DAT 5550 Machine Learning Tools for Prediction of Business Outcomes
- DAT 5562 Text Mining
- DAT 5566 Big Data and Cloud Computing
- DAT 5567 Prescriptive Analytics
- MGT 5600 Professional Business Communication

The live Core Analytics curriculum should be treated as a suite of full mini-courses:

- Graduate Statistics for Financial Analysis: 30 lessons.
- Python Foundations for Financial Analytics: 30 lessons.
- Data Analytics with Python: 30 lessons.
- Structured Data and SQL for Financial Analytics: 30 lessons.
- Machine Learning for Financial Analytics: 30 lessons.
- Build It Yourself - Analytics Systems and Tools: 30 lessons.

Each live lesson should include a substantial Learn section, 20+ connected practice
checks, and an executable challenge. A future quality pass should deepen lessons one
by one without shrinking practice or disconnecting practice from the Learn section.

Finance and fintech contexts to prefer:

- cash flows
- returns
- loan balances
- payment behavior
- default and delinquency
- fraud
- underwriting
- portfolio weights
- risk measures
- volatility
- conversion and A/B testing
- customer transactions
- financial statements
- valuation
- options, futures, and fixed income when ready

The first full rebuild should begin with Graduate Statistics for Financial Analysis as
a 30-lesson mini-course, not a short survey. Each lesson should have a textbook-like
Learn section, 15+ connected practice drills, and a coding challenge that directly
applies the taught statistics through Python/math and financial analysis context.

Module 1 should teach statistics from the viewpoint of financial analysis. Do not
constrain it to portfolio risk, investment theory, risk modeling, or market mechanics.
Curriculum should progress gradually: each topic must explicitly build on the object,
calculation, notation, or model introduced immediately before it.

## Design Rules

Use `DESIGN.md` before significant frontend work.

Core interface expectations:

- Build the real study workflow, not a marketing landing page.
- Keep pages dense enough for repeated study use, but calm and readable.
- Use familiar icons from `lucide-react` for actions.
- Avoid visible instructional copy that explains the UI instead of doing useful work.
- Avoid one-note beige, tan, brown, dark-blue, or purple palettes.
- Avoid nested cards, oversized rounded cards, decorative blobs, and generic AI
  dashboard styling.
- Do not use a flame icon or heat language for study motivation.
- Check mobile text fit and avoid horizontal scrolling.

## Markdown Style

Markdown files should be comfortable to read inside Codex:

- Wrap prose and list items at about 88 characters.
- Avoid long raw URLs in prose. Use Markdown links with short labels.
- Use short sections and plain headings.
- Keep tables narrow. Prefer lists when a table would force horizontal scrolling.
- End reports with a `Questions for Hack` section when decisions remain.
- Use ASCII unless the file already has a reason to use Unicode.

## Testing And Verification

Run verification proportional to risk:

- Docs-only changes: read the changed file and check formatting.
- Frontend code changes: run `npm run lint`.
- Backend code changes: run `python -m unittest discover tests`.
- Full-stack contract changes: run backend tests and frontend lint.
- Visual UI changes: use browser screenshots or a real browser check when practical.
- Security-sensitive changes: run the security audit checklist below.

If a test cannot be run, say exactly why and what risk remains.

## Security Audit Policy

Security audit is required when work touches:

- `backend/routes/execute.py`
- notebook import, storage, rendering, or deletion
- markdown rendering and sanitization
- environment variables, config, secrets, or CORS
- authentication or authorization, if added later
- file paths, uploads, downloads, subprocesses, or shell execution
- database schema or raw SQL behavior

Security audit is optional for docs-only work and low-risk visual-only changes.

Practical checks:

- Look for secret leakage and unsafe `.env` handling.
- Validate user input at API boundaries.
- Keep local Python/SQL execution sandboxed away from app data.
- Avoid exposing stack traces or internal paths to the frontend.
- Keep `rehype-sanitize` or equivalent protection for rendered Markdown.
- Prefer parameterized queries and ORM-safe operations.
- Consider Bandit, Gitleaks, Semgrep, and CodeQL when the repo is ready for them.

## Existing Skills

The repo already tracks broad skills for data storytelling, E2E testing, FastAPI,
dashboard design, Next.js App Router, Python testing, React performance, and React
state management. Use them selectively when relevant, but do not let broad community
skill text override Orion's product contracts.

Do not install external packs such as gstack until Hack can vet them.

## Reporting

When finishing work, report:

- what changed
- where it changed
- what was verified
- what risk or follow-up remains
- what you noticed that Hack may not have asked about

End substantial reports with:

## Questions for Hack
