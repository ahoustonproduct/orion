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

- Which Core Analytics course becomes the first full rebuild once the current product shell is stable?
- Should formulas be introduced as named finance formulas first, or as Python functions first?
- Which fintech domains feel most motivating for practice datasets: lending, markets, banking, payments, crypto, wealth management, or risk?
- For polished deliverables, should the default format be memo, notebook, dashboard, or slide outline?
