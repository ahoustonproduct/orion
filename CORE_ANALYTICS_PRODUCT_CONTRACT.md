# Core Analytics Product Contract

## Purpose

Orion's first serious curriculum rebuild is Core Analytics preparation for a single learner entering the WashU MS in Business Analytics program with the Financial Technology Analytics concentration.

The app should help Hack earn high grades by building dependable skill in statistics, Python, pandas, SQL, data visualization, and finance math before and during the program. The curriculum should frame examples, drills, quizzes, and projects from a finance and fintech point of view whenever that framing is natural.

## Learner Profile

- Program: WashU MS in Business Analytics
- Concentration: Financial Technology Analytics
- Priority: Core Analytics first
- Python level: beginner
- SQL level: beginner
- Statistics confidence: shaky
- Finance/accounting baseline: familiar with basics, but formulas need to be rebuilt
- Finance math: teach from scratch
- Preferred technical path: Python/pandas first, Excel as a supporting skill
- Study target: 60 minutes per day
- Main anxiety areas: finance math and programming
- Gamification constraint: no streak mechanics
- Device access: Hack should be able to use Orion from this Windows device and the
  MacBook LAN URL without splitting progress across browser origins.

## Current Rebuild Decisions

- Local progress identity: use stable key `orion_local_user` by default for
  `localhost`, `127.0.0.1`, and `http://<windows-lan-ip>:3000`.
- The Windows launcher should allow trusted-LAN code execution through the Next
  proxy so the MacBook can run Python challenges against the Windows backend.
- First rebuild module: Graduate Statistics for Financial Analysis.
- Core Analytics modules should be full mini-courses, not short surveys. The first
  statistics rebuild is a 30-lesson sequence with textbook-like Learn sections, 20+
  connected practice checks per lesson, and coding challenges that directly apply
  the lesson material.
- Module 1 should teach statistics from the viewpoint of financial analysis. It should
  not be constrained to portfolio risk, investment theory, risk modeling, or financial
  markets.
- The first statistics module should be Python/math only. Excel and SQL can support
  later Core Analytics modules, but Hack already knows enough Excel for this phase.
- Finance formulas and statistics should be introduced as Python functions or NumPy
  operations first, with formal notation explained beside the code.
- The first datasets should be small built-in generic financial-analysis datasets so
  lessons stay deterministic, local, beginner-readable, and testable.
- First polished deliverable format: mixed analyst memo plus notebook.
- Every lesson should progress gradually: each topic should explicitly build on the
  object, calculation, notation, or model introduced immediately before it.

## Near-Term Core Analytics Path

1. Rebuild `Graduate Statistics for Financial Analysis` as a 30-lesson mini-course:
   statistical tables, vectors, means, variance, standardization, covariance,
   probability, distributions, simulation, estimation, MLE, confidence intervals,
   hypothesis testing, regression, diagnostics, GLMs, mixed effects, PCA, factor
   analysis, clustering, MANOVA, SEM foundations, bootstrap, Bayesian inference,
   MCMC foundations, time series, ethics, and a mixed memo plus notebook.
2. Rebuild review and drill coverage only from material actually taught in the new
   lessons: Python syntax, formula implementation, notation-to-code translation,
   calculation checks, debugging, and interpretation.
3. Rebuild the next Core Analytics modules around Python/pandas, SQL, visualization,
   A/B testing, finance math, and communication after the statistics spine is stable.
4. Keep finance and fintech examples natural, but do not let a narrow business context
   replace the statistical concept being taught.

## Live Module Rebuild Scope

The live Core Analytics curriculum is a 180-lesson suite:

- Graduate Statistics for Financial Analysis: 30 lessons.
- Python Foundations for Financial Analytics: 30 lessons.
- Data Analytics with Python: 30 lessons.
- Structured Data and SQL for Financial Analytics: 30 lessons.
- Machine Learning for Financial Analytics: 30 lessons.
- Build It Yourself - Analytics Systems and Tools: 30 lessons.

Every rebuilt lesson should have a substantial Learn section, 20+ connected practice
checks, and an executable coding challenge. The current implementation is a full
structural pass across all modules. Future passes should deepen individual lessons to
the same textbook depth as the first graduate statistics lesson.

## Curriculum Source

The local curriculum source currently reviewed is:

`C:\Users\Hack\orion\business-analytics-wash.pdf`

The live program reference is:

`https://olin.washu.edu/programs/specialized-masters/ms-in-business-analytics/curriculum.php`

The Core Analytics foundation should map to these WashU common-core courses:

- DAT 5561 Introduction to Python and Data Science
- DAT 5563 Data Visualization for Business Insights
- DAT 5564 Database Design and SQL
- DAT 5569 A/B Testing in Business and Social Science
- DAT 5550 Machine Learning Tools for Prediction of Business Outcomes
- DAT 5562 Text Mining
- DAT 5566 Big Data and Cloud Computing
- DAT 5567 Prescriptive Analytics
- MGT 5600 Professional Business Communication

The Financial Technology Analytics destination should keep future examples pointed toward:

- financial management
- options and futures
- fixed income securities
- investment theory
- valuation
- fintech methods and practice
- blockchain and cryptocurrencies
- financial markets
- forecasting and risk analysis

The current WashU alignment map lives in
`CORE_ANALYTICS_WASHU_COVERAGE_MATRIX.md`. It should be updated whenever the live
WashU curriculum page or the Core Analytics module set changes.

## Learning Experience Contract

The app should adaptively recommend what to do next. Recommendations should be based on weak topics, recent misses, lesson completion, review due, confidence, and the current Core Analytics priority.

Daily work should usually combine:

- short drills for recall and speed
- guided practice for applied problem solving
- review of recent misses
- a small amount of new material

The default daily session should fit a 60-minute budget:

- 10 minutes: review due items
- 15 minutes: short mixed drill
- 25 minutes: guided Python/pandas, SQL, statistics, or finance-math practice
- 10 minutes: reflection, notes, or one quiz retry

Weak areas should receive extra weight. Given the current profile, finance math, programming, and statistics should receive early emphasis.

## Study Modes

Orion should support three study modes.

### Exam-Style Repetition

Short, timed questions that build recall, speed, and formula memory. These are best for statistics terms, Python syntax, SQL clauses, finance formulas, and quick interpretation.

Example:

> A fintech lender tests two onboarding flows. Flow A converts 8.2% of 4,000 applicants. Flow B converts 9.1% of 4,100 applicants. What statistical test or concept should you reach for first, and what decision risk matters?

### Homework-Style Practice

Multi-step applied work that resembles coursework. These tasks should combine tools and interpretation.

Example:

> Use pandas to load loan-performance data, compute default rate by credit-score band, visualize the pattern, and write a short explanation of which borrower segment deserves closer underwriting review.

### Polished Deliverable Mode

End-of-module work products that look like graded submissions or professional analytics artifacts.

Example:

> Prepare a one-page fintech analyst memo recommending whether a digital lender should adjust approval thresholds. Include one chart, one table, one business recommendation, and one limitation.

## Content Framing Rules

Core Analytics lessons should not be abstract when finance framing is available.

- Python examples should use returns, cash flows, loan balances, customer transactions, pricing, portfolio weights, or risk measures.
- SQL examples should use banking, brokerage, payments, lending, customer, transaction, and account schemas.
- Statistics examples should use A/B tests, conversion, underwriting, default, fraud, volatility, and model error.
- Visualization examples should produce charts an analyst could put in a memo or dashboard.
- Finance math should introduce formulas slowly, with Python/pandas implementations before Excel workflows.

## Product Constraints

The app is for one local user. It does not need multi-user account management, social features, or institutional permissions.

The app should not use streaks. It may show study minutes, days studied, lessons completed, review due, mastery, confidence, weak topics, and deliverables completed.

YouTube-derived curriculum generation remains outside the running app. Future direct YouTube links can be processed externally by Codex/subagents and imported as saved modules later.

Advisor planning, enrolled-course tracking, and assignment calendar support are deferred for at least two months.

## Questions For Hack

Grade `CORE_ANALYTICS_GRADUATE_STATS_REBUILD_PLAN.md` before the lesson content is
rewritten in the app. The next implementation choice is whether to rebuild Lessons 1
to 5 in full depth first, or create all 30 lesson shells and then deepen them in order.
