# Orion Code — AI Work Instructions

---

## 📖 Guidance — Read This First, Follow Throughout

This section contains standing rules and hard-won lessons about this codebase. Read it completely before writing a single line of code. Every rule here exists because a previous mistake required manual cleanup.

### 1. Visual Theme — The Non-Negotiable Design System

The entire application uses a **WashU Olin Executive** aesthetic — a premium, light interface inspired by Washington University in St. Louis's brand palette. Cream/parchment backgrounds, warm white surfaces, and deep WashU crimson accents. It must never look like a gaming app, a neon dashboard, or a generic dark mode site.

**The golden rule: NEVER hardcode color values.** Every color must come from the CSS variables defined in `frontend/app/globals.css`. Using raw hex codes, Tailwind color classes like `slate-*`, `gray-*`, `rose-*`, `blue-*`, or any other specific color name will break the theme.

**Always use these CSS variables:**

```
var(--color-background)     →  #F2ECE3  — warm cream (page background)
var(--color-surface)        →  #FFFFFF  — pure white card/panel background
var(--color-surface-2)      →  #FAF7F3  — light parchment for nested surfaces
var(--color-border)         →  #E5DDD4  — subtle tan for dividers
var(--color-accent)         →  #A01C2C  — WashU crimson (buttons, icons, active states)
var(--color-accent-hover)   →  #821624  — crimson hover state
var(--color-accent-light)   →  #C97A84  — soft crimson (progress bar current segment)
var(--color-gold)           →  #B8822A  — WashU gold (secondary accent, decorative)
var(--color-text-primary)   →  #1C1410  — main ink body text
var(--color-text-secondary) →  #5C4F45  — supporting warm stone text
var(--color-text-muted)     →  #9A8C80  — labels, placeholders, metadata
var(--color-success)        →  #166534  — deep success green
var(--color-error)          →  #991B1B  — deep error red
```

**Code editor panels (Monaco) are the ONLY dark exception.** These are intentional dark islands within the light UI:
```
Code panel background:  #14110F
Code panel surface:     #1E1A16
Code panel border:      #2C2520
Code panel text:        #F0ECE6
Code output text:       #4ADE80  (bright green — keep as-is)
```

**Typography:** Headings (`h1`, `h2`, `h3`) should use **Serif** fonts (e.g., `var(--font-serif)`) for a classic textbook feel. Body text uses a clean Sans-serif (`var(--font-sans)`).

---

### 2. Backend Stability — Python Syntax Rules

- Never nest triple-quoted strings (`"""`) inside other triple-quoted strings in Python files. This causes `SyntaxError`. Use triple single-quotes (`'''`) for any inner multi-line strings when the outer context already uses `"""`.
- After any edit to a `curriculum_data/*.py` file, verify the file parses cleanly by checking that the backend server boots without errors.
- The `__init__.py` in `backend/curriculum_data/` must export every new module you create. If you add `module6_stats.py`, you must add `from .module6_stats import MODULE_6` to `__init__.py` and include `MODULE_6` in `ALL_MODULES`.

---

### 3. TypeScript — Type Safety

- The `QuizQuestion` and `QuizQuestion2` union types in `frontend/lib/api.ts` must include every question `type` string used in curriculum data. If you add a new question type, update the type union first before writing curriculum data that uses it.
- Do not use `any` types unless absolutely unavoidable, and always leave a comment explaining why.
- Never use empty `catch {}` blocks. At minimum log the error and set a visible error state. Silent failures are the hardest bugs to diagnose.

---

### 4. Installed Skills — Use These in Your Work

Skills are pre-loaded playbooks that give you specialized expertise for recurring tasks. They live in `.claude/skills/`. Reference them by name at the start of a task.

| Skill | When to use it |
|---|---|
| `@react-state-management` | Any time you add state that needs to be shared across components — mastery scores, review queue, lesson progress, streak |
| `@react-component-performance` | Before finalizing any component that contains Monaco Editor, large lists, or frequent re-renders |
| `@e2e-testing` | When building or updating user-facing flows: lesson navigation, quiz submission, code execution |
| `@error-handling-patterns` | Every API call must have a visible error state. Apply this before any `fetch`/`axios` call |
| `@python-testing-patterns` | When adding or modifying backend routes — especially Decision Engine math and spaced repetition intervals |
| `@fastapi-pro` | When writing new FastAPI routers or modifying async patterns in the backend |
| `@kpi-dashboard-design` | When working on the Progress/Diagnostics page or any analytics visualization |
| `@data-storytelling` | When designing charts, heatmaps, or mastery visualizations |
| `@nextjs-app-router-patterns` | When creating new pages, layouts, or modifying the App Router structure |

**How to invoke:** At the start of your message, write `Use @skill-name` and the skill context will be loaded automatically.

---

### 5. Workflow — How to Work Safely

1. **Read before writing.** Always read the existing file before editing it.
2. **Test the backend.** After Python edits, restart and confirm the server responds at `http://localhost:8001/health`.
3. **Test the frontend.** Run `npm run build` in `frontend/` to catch TypeScript errors before calling work done.
4. **Git hygiene.** Commit with a meaningful message describing what changed and why.
5. **Khan reviews your work.** Khan (Claude Code in VSCode) is the verification and quality layer in this team. Write code that is clean enough to pass a code review. Khan will catch performance issues, empty catch blocks, missing error states, and type safety gaps.

---

### 6. AI Team — Roles and Responsibilities

This project is built by a three-AI team. Understand who does what:

- **Atlas (you)** — Bulk code generation and first-pass implementation. You build features end-to-end. Speed and completeness are your priority.
- **Khan (Claude Code / VSCode)** — Verification, bug testing, performance review, security, and code quality. Khan reviews what you push. Write code you'd be comfortable defending.
- **Hermes (Gemini / Antigravity)** — Guidance, orchestration, and cross-cutting concerns. Hermes writes the Guidance you're reading now.

When in doubt about correctness, leave a `// TODO: Khan — verify this` comment. Khan will catch it in review.

---

### 7. Known Error Patterns — Do Not Repeat These

These mistakes have already been made and fixed. Do not reproduce them.

**React / Next.js**
- `"File has not been read yet"` — Never use the Write tool on a file you haven't read first. Always Read → then Write or Edit.
- Monaco Editor loaded multiple times on the same page causes visible lag. Use `dynamic(() => import(...), { ssr: false })` and memoize the component. Never render two Monaco instances in the same component tree without lazy guards.
- `wordWrap: "on"` in Monaco causes code comments to break mid-line and wrap visually. Always set `wordWrap: "off"` and `scrollbar: { horizontal: "auto" }`.
- Empty `catch {}` blocks everywhere. Every API call needs a visible error state — set state, show a message, never swallow silently.

**Python / FastAPI**
- Nested triple-quoted strings cause `SyntaxError` at startup. Use `'''` inside `"""` blocks.
- Blocking subprocess calls inside `async def` route handlers stall the entire event loop. Use `asyncio.create_subprocess_exec` or run in a thread pool with `asyncio.get_event_loop().run_in_executor`.
- The spaced repetition intervals are `[1, 3, 7, 14]` days. Do not change these without updating both the backend logic and the frontend display.

**Styling**
- Never use Tailwind color utilities (`bg-blue-500`, `text-gray-400`, etc.) directly. Always use the CSS variable classes or the custom Tailwind tokens mapped to CSS variables.
- The lesson page uses a two-column grid `grid-cols-[1fr_460px]`. The right column is the sticky `FollowAlongPanel`. Do not collapse this to single-column or move navigation outside the left column.

---

## Feature Roadmap — Implement in Order

Please resume work on the Orion Code platform. The visual aesthetics have been finalized (see Guidance above). Now expand the platform's features to rival premium Business Analytics educational software.

### Phase 1: The AI Co-Pilot & Rescue Mechanics

- **Interactive AI Sidebar** (`frontend/components/AIChatSidebar.tsx`): A slide-out chat panel next to the code editor, wired to a streaming `/api/orion/chat` endpoint in `backend/routes/ai.py`. The user can ask questions about lesson content mid-lesson.
- **Proactive Refactoring**: After a correct code submission, have Orion evaluate whether the solution is efficient. If not, stream a short tip on a cleaner approach.
- **Rescue Button**: After 3 failed challenge attempts, show a "Reveal Solution" button with a full code walkthrough so the user never gets permanently stuck.

### Phase 2: Curriculum Expansion & Data Science Sandbox

- **Data Science Library Support**: Update `backend/routes/execute.py` and `backend/requirements.txt` to allow `pandas`, `numpy`, and `scipy` in the sandboxed Python runner.
- **Statistics Module** (`backend/curriculum_data/module6_stats.py`): Teach statistical concepts for business analytics — distributions, regressions, p-values, and correlations — implemented with Pandas/NumPy.
- **SQL Module** (`backend/curriculum_data/module7_sql.py`): Teach relational database design, SELECT/WHERE/JOIN/GROUP BY, subqueries, and SQLAlchemy. The `/execute/sql` endpoint already exists in `backend/routes/execute.py`.

### Phase 3: The Full IDE & Automated Notebook

- **Multi-file Editor** (`frontend/components/MultiFileEditor.tsx`): Upgrade the Monaco editor to support multiple file tabs and update the backend runner to handle linked files — enabling real Capstone projects.
- **Smart Notebook** (`frontend/app/notebook/page.tsx`): Dynamically pull code structures the user struggled with from the SQLite database, creating an automatically generated midterm cheat-sheet.

---

Proceed with Phase 1 first. Verify the backend is bug-free and the UI strictly follows the Guidance section above before marking any phase complete.
