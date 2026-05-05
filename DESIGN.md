# DESIGN.md

This is Orion's design system draft for AI-assisted frontend work. It is intentionally
plain text so Codex, Claude, Copilot, Gemini, and future agents can use the same visual
rules.

Status: active draft. Hack selected Calm Academic Finance Workspace as the
preferred direction, using the app's existing warm stone color scheme.

## Product Feel

Orion should feel like a serious personal analytics workspace for Core Analytics and
Financial Technology Analytics preparation. It should be calm, focused, and capable.
It should not feel like a generic SaaS landing page, a game, or a decorative portfolio.

The product should help Hack sit down, see what matters today, practice, review misses,
and build polished finance/fintech deliverables.

## Audience

The user is one local learner preparing for WashU MSBA, Financial Technology Analytics
concentration.

The design should support:

- beginner Python and SQL confidence
- shaky statistics confidence
- finance math rebuilt from scratch
- 60-minute daily study sessions
- short drills
- adaptive recommendations
- review of misses
- polished deliverables
- finance-first practice contexts

## Design Principles

### 1. Study First

The first viewport should show useful study state or the next action. Avoid large hero
sections, decorative welcome panels, or explanatory marketing copy.

### 2. Finance-First Clarity

Examples and dashboards should feel related to analyst work: risk, returns, cash flows,
default rates, A/B tests, underwriting, portfolio behavior, and deliverables.

### 3. Calm Density

Orion should be information-rich without becoming noisy. Use compact panels, clear
labels, tight spacing, and obvious hierarchy.

### 4. No Streak Pressure

Do not use streak mechanics, flame icons, heat language, daily pressure badges, or
streak-recovery patterns. Motivation should come from competence, clarity, and useful
progress.

### 5. Deliverable Quality

Completed work should feel like something Hack could submit, discuss, or reuse:
analyst memos, charts, tables, notebooks, dashboard snapshots, and project summaries.

## Official Direction

Use Calm Academic Finance Workspace as Orion's direction.

Mood:

- focused
- quiet
- credible
- study-friendly

Visual language:

- warm stone/off-white background from the current app
- charcoal text
- amber and dark-stone accents from the current app
- thin borders
- compact panels
- small academic-finance cues such as formulas, tables, and notebook cells

Best for:

- long study sessions
- beginner confidence
- reducing visual fatigue

Risk:

- may feel too plain unless the charts and module states carry enough polish

## Color Rules

Use the current app palette as the source of truth. Do not introduce a new teal, navy,
green, or corporate-fintech palette unless Hack explicitly chooses a redesign.

Current working palette:

- Background: `#EDE6DA`
- Surface: `#F5F0E8`
- Surface muted: `#EAE3D6`
- Border: `#CCC5B6`
- Text primary: `#1C1917`
- Text secondary: `#44403C`
- Text muted: `#78716C`
- Primary action: `#292524`
- Primary action hover: `#1C1917`
- Accent light: `#44403C`
- Gold accent: `#D97706`
- Success: `#166534`
- Warning: `#92400E`
- Error: `#B91C1C`

Use amber/gold sparingly for highlights, ratings, or deliverable polish. Keep most
interface weight on warm surfaces, dark text, borders, and compact hierarchy.

## Typography

Use the current sans-serif direction unless a deliberate redesign changes it:

- Primary UI: Inter, Outfit, or system sans
- Code: JetBrains Mono, Fira Code, or monospace
- Long reading content may use a restrained serif only when it improves comfort

Rules:

- Do not scale font size with viewport width.
- Do not use negative letter spacing.
- Use compact headings inside dashboards and tools.
- Reserve large headings for true page introductions.
- Keep button and nav labels short enough for mobile.

## Layout

Desktop:

- Keep the persistent nav compact.
- Prefer a focused content column for lessons.
- Use two-column layouts for dashboard and progress when information density helps.
- Keep primary actions near the relevant content.

Mobile:

- Avoid horizontal scrolling.
- Keep bottom nav labels short.
- Ensure text wraps before it hits the viewport edge.
- Collapse dense dashboard panels into a clear vertical order.
- Keep code, tables, and charts scroll-contained when necessary.

## Components

### Navigation

- Use `lucide-react` icons.
- Keep active state obvious but calm.
- Avoid flame icons and streak-coded visuals.
- Recommended quiz icon: `CircleHelp`, `Brain`, `ClipboardCheck`, or `ListChecks`.
- Official top-level nav should stay aligned to real app routes: Home, Learn, Quiz,
  Review, Progress, Notebooks, Notes, Glossary, and Settings.
- Do not add mockup-only tabs such as `Data Lab` or `Analytics` unless the feature is
  explicitly defined and implemented.

### Cards And Panels

- Prefer 6px to 8px radius for app panels.
- Avoid nested cards.
- Avoid decorative floating page sections.
- Cards are for repeated items, modals, and genuinely framed tools.
- Use full-width bands or unframed layouts for page structure.

### Buttons

- Use icon buttons for familiar tools.
- Use icon plus text for primary commands.
- Use clear text only when the command needs no icon.
- Build hover, focus, disabled, loading, and error states.

### Forms And Controls

- Use segmented controls for modes.
- Use toggles or checkboxes for binary settings.
- Use sliders, steppers, or numeric inputs for quantities.
- Use menus for option sets.
- Use tabs for switching views.

### Charts

- Charts should answer a business or learning question.
- Use direct labels when possible.
- Include units.
- Avoid decorative chart junk.
- Make color meaning consistent across the app.
- Every chart in deliverable mode should support a written recommendation.

### Lessons

Lesson pages should provide:

- concept explanation
- finance/fintech context
- worked example
- short Python/pandas or SQL task when relevant
- reflection or interpretation prompt
- review trigger for misses

Do not bury the next action below a long intro.

### Quizzes And Drills

Quizzes should feel like practice, not punishment.

Use:

- clear question stems
- immediate feedback
- explanation of why the answer works
- review routing for misses
- confidence rating when useful

Avoid:

- streak pressure
- hype language
- excessive confetti or game rewards

### Notebooks

Saved notebooks are saved study modules. UI should say "Study Notes" or "Saved Modules"
depending on context, not "YouTube generator" or "Smart Notebook".

Notebook screens should make it clear whether a module is ready, how many lessons it
contains, and which lessons can be launched in the standard lesson experience.

## Content Voice

Use plain, encouraging, serious language. Orion should sound like a capable tutor and
study partner, not a game announcer.

Prefer:

- "Review recent misses"
- "Practice A/B test interpretation"
- "Build confidence with loan-default rates"
- "Prepare a one-page analyst memo"

Avoid:

- "Keep your streak alive"
- "Crush today's challenge"
- "Unlock epic rewards"
- "You're on fire"

## Known Design Debt

These issues were spotted during the skill/design research pass:

- Several components use large `rounded-2xl` panel shapes. Future redesign work should
  move toward tighter app-like radii.
- The dashboard still shows `Total Stars`; stars are not daily-chain mechanics, but
  future work should consider replacing them with mastery, confidence, or deliverable
  measures.

Do not fix all of these in unrelated work. Address them when touching the relevant
components or during a focused visual cleanup pass.

## Accessibility And QA

Before completing significant UI work:

- check desktop and mobile layouts
- check text overflow
- check color contrast
- check focus states
- check empty, loading, error, and success states
- check that charts and tables remain readable
- check that page content does not require horizontal scrolling

## Questions for Hack

- Which visual direction should become Orion's official design direction?
- Should stars remain as lightweight feedback, or be replaced by mastery/confidence?
- Should the app visually reference WashU at all, or remain fully Orion-branded?
