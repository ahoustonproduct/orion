# Orion Code — AI Work Instructions

---

## 📖 Guidance — Read This First, Follow Throughout

This section contains standing rules and hard-won lessons about this codebase. Read it completely before writing a single line of code. Every rule here exists because a previous mistake required manual cleanup.

### 1. Visual Theme — The Non-Negotiable Design System

The entire application uses a **"Night Mode Digital Reader"** aesthetic — a warm, textbook-like dark interface with charcoal browns and amber gold. It is intentionally calm and print-like, not flashy. It must never look like a gaming app, a neon dashboard, or a generic "dark mode" site.

**The golden rule: NEVER hardcode color values.** Every color must come from the CSS variables defined in `frontend/app/globals.css`. Using raw hex codes, Tailwind color classes like `slate-*`, `gray-*`, `rose-*`, `blue-*`, or any other specific color name will break the theme.

**Always use these CSS variables:**

```
var(--color-background)     →  #1C1917  — deep warm charcoal (page background)
var(--color-surface)        →  #292524  — card/panel background
var(--color-surface-2)      →  #35312C  — raised/nested surfaces
var(--color-border)         →  #44403C  — all borders and dividers
var(--color-accent)         →  #D97706  — primary amber (buttons, icons, links)
var(--color-accent-hover)   →  #B45309  — darker amber for hover states
var(--color-accent-light)   →  #F59E0B  — lighter amber for highlights
var(--color-text-primary)   →  #E7E5E4  — main body text
var(--color-text-secondary) →  #A8A29E  — supporting/caption text
var(--color-text-muted)     →  #78716C  — labels, placeholders, metadata
var(--color-success)        →  #65A30D  — success states (green)
var(--color-error)          →  #DC2626  — error states (red)
```

**Lesson learned the hard way:** A previous AI added `AIChatSidebar.tsx`, `QuickLookCard.tsx`, and `MultiFileEditor.tsx` using hardcoded cold navy hex values (`#0f0f1a`, `#1a1a2e`, `#2d2d4a`) and neon cyan (`#06b6d4`). This broke the warm, textbook aesthetic entirely and had to be manually corrected. Do not repeat this mistake.

### 2. Backend Stability — Python Syntax Rules

- Never nest triple-quoted strings (`"""`) inside other triple-quoted strings in Python files. This causes `SyntaxError`. Use triple single-quotes (`'''`) for any inner multi-line strings when the outer context already uses `"""`.
- After any edit to a `curriculum_data/*.py` file, verify the file parses cleanly by checking that the backend server boots without errors.
- The `__init__.py` in `backend/curriculum_data/` must export every new module you create. If you add `module6_stats.py`, you must add `from .module6_stats import MODULE_6` to `__init__.py` and include `MODULE_6` in `ALL_MODULES`.

### 3. TypeScript — Type Safety

- The `QuizQuestion` and `QuizQuestion2` union types in `frontend/lib/api.ts` must include every question `type` string used in curriculum data. If you add a new question type, update the type union first before writing curriculum data that uses it.
- Do not use `any` types unless absolutely unavoidable, and always leave a comment explaining why.

### 4. Workflow — How to Work Safely

1. **Read before writing.** Always read the existing file before editing it.
2. **Test the backend.** After Python edits, restart and confirm the server responds at `http://localhost:8001/health`.
3. **Test the frontend.** Run `npm run build` in `frontend/` to catch TypeScript errors before calling work done.
4. **Git hygiene.** Commit with a meaningful message describing what changed and why.

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
