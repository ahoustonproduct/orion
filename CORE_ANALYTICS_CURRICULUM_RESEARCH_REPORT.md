# Core Analytics Curriculum Research Report

Date: 2026-05-06

## Purpose

This report recommends how Orion should develop its curriculum to prepare Hack for
WashU Olin's MS in Business Analytics program, Financial Technology Analytics
concentration.

The practical product question is not "what should Orion cover?" The answer is already
visible in the WashU curriculum. The better question is:

> How should Orion sequence, teach, review, and apply Core Analytics so Hack can enter
> the program with enough fluency to learn the graduate material instead of fighting the
> prerequisites?

The recommendation is to rebuild Core Analytics as a finance-first preparation system:
Python/pandas first, SQL close behind, statistics rebuilt patiently through fintech
decisions, finance math rebuilt from scratch, and Excel used as a supporting audit and
communication tool.

## Executive Recommendation

Orion should become Hack's personal pre-program bootcamp for WashU MSBA Core Analytics.
It should teach fewer topics at once, but make every topic usable.

The rebuild should begin with `Statistics for Fintech Decisions`, supported by small
Python/pandas tasks from the first week. Each lesson should use this learning loop:

1. Name the fintech decision.
2. Explain the concept in plain language.
3. Walk through a worked example.
4. Ask Hack to complete or modify a Python/pandas, SQL, or formula step.
5. Give short retrieval practice.
6. Route misses into spaced review.
7. End each unit with a polished analyst deliverable.

This design is consistent with the repo contracts: Core Analytics first, finance-first
examples, beginner Python/SQL, shaky statistics, finance math from scratch, 60-minute
daily sessions, and no streak mechanics.

## WashU Target

The current WashU Olin MSBA curriculum page says the program is 39 credits, with a
statistics prerequisite, 18 core credits, concentration requirements, electives, and a
required experiential course. The core courses include Database Design and SQL,
Prescriptive Analytics, Big Data and Cloud Computing, Professional Business
Communication, Machine Learning Tools for Prediction of Business Outcomes, Introduction
to Python and Data Science, A/B Testing in Business and Social Science, Data
Visualization for Business Insights, and Text Mining.

For the Financial Technology Analytics concentration, WashU lists Financial Management,
Advanced Corporate Finance I-Valuation, Investment Theory, Options and Futures, Fixed
Income Securities, Financial Technology-Methods and Practice, and Seminar in Financial
Technology.

Source:

- [WashU Olin MSBA curriculum](https://olin.washu.edu/programs/specialized-masters/ms-in-business-analytics/curriculum.php)

Implications for Orion:

- Orion should treat statistics, Python, pandas, and SQL as prerequisites to being able
  to breathe in the program, not as isolated subjects.
- The Core Analytics rebuild should map to WashU's analytics core first, then keep the
  examples pointed toward the fintech concentration.
- Finance math should start early enough that valuation, fixed income, investment
  theory, options, and futures are not encountered as surprise languages later.
- Professional communication is not optional. Every module should eventually produce a
  memo, notebook, dashboard snapshot, or concise recommendation.

## What Elite Programs Reveal

Elite analytics, finance, and quant programs are not just topic lists. They tend to
organize curriculum around a stack:

1. A prerequisite or launch layer that refreshes programming, math, statistics, and
   finance language.
2. A rigorous core where theory, statistics, computation, and finance are taught
   together.
3. Applied labs, seminars, internships, practicums, or capstones that force students to
   convert technical work into decisions and communication.
4. Electives or concentrations that specialize after the core is stable.

### MIT Sloan Master of Finance

MIT Sloan's MFin curriculum combines required core courses, restricted electives, and
Action Learning. Its core includes modern finance, financial mathematics, programming
for finance professionals, corporate financial accounting, finance ethics and
regulation, corporate finance, financial markets, analytics of finance, and
communications. The programming course applies Python to financial problems, including
data manipulation, visualization, and reporting. The Action Learning layer includes
proseminars and Finance Lab projects with industry practitioners.

Sources:

- [MIT Sloan MFin curriculum](https://mitsloan.mit.edu/mfin/explore-program/mfin-curriculum)

Orion lesson:

- Hack should not learn Python as generic syntax first. Python should be introduced as
  the working language for finance data manipulation, visualization, reporting, and
  decision support.

### MIT Sloan Master of Business Analytics

MIT Sloan's MBAn curriculum foregrounds analytics tools, optimization, machine learning,
analytics lab, communication through data, ethics and data privacy, and a capstone with
company projects. The curriculum is built around applying data science, optimization,
and machine learning to real business problems.

Sources:

- [MIT Sloan MBAn curriculum](https://mitsloan.mit.edu/master-of-business-analytics/explore-program/mban-curriculum)

Orion lesson:

- Core Analytics should not end at quizzes. It should lead to applied deliverables that
  resemble analytics work: analysis, code, explanation, recommendation, limitation, and
  handoff.

### Berkeley Haas Master of Financial Engineering

Berkeley Haas describes its MFE curriculum as integrating mathematical, statistical,
and computer science methods with finance theory and institutional context. Courses
build on previous courses. Early work includes investments and derivatives, empirical
methods in finance, and stochastic calculus. The curriculum includes programming and
analytical exercises, financial data science with Python implementations, fixed income
markets, risk management, an applied finance project, and an internship or industry
project.

Sources:

- [Berkeley Haas MFE curriculum](https://mfe.haas.berkeley.edu/academics/curriculum)

Orion lesson:

- Orion should use a spiral sequence. Each return to a topic should raise the level:
  first intuition, then formula, then Python implementation, then interpretation, then
  deliverable.

### Carnegie Mellon MSCF

CMU's MSCF describes an integrated, industry-driven curriculum across finance,
mathematics, statistics and data science, and computer science. It emphasizes courses
that build on one another, rigorous theory with hands-on application, applied learning,
real-world projects, competitions, internships, and collaboration with firms.

Sources:

- [CMU MSCF academics](https://www.cmu.edu/mscf/academics/index.html)

Orion lesson:

- Orion should keep the disciplines connected. A statistics lesson should touch data
  and decisions. A Python lesson should touch finance data. A finance-math lesson should
  touch uncertainty and implementation.

### Columbia MS Financial Engineering

Columbia's MSFE expects entering students to have strong probability, statistics,
linear algebra, and programming skills. Its core includes optimization, stochastic
models, Monte Carlo simulation, financial engineering foundations, continuous-time
models, statistical analysis and time series, a quantitative and computational
bootcamp, and a practitioner seminar. Concentrations include computation and
programming, derivatives, financial technology, and machine learning for financial
engineering.

Sources:

- [Columbia MS Financial Engineering catalog](https://bulletin.columbia.edu/columbia-engineering/academic-departments-programs/industrial-engineering-operations-research/graduate-programs/financial-engineering-ms/)

Orion lesson:

- Hack does not need Columbia-level math before WashU, but the direction is useful:
  probability, statistics, programming, simulation, time series, optimization, and
  finance should be introduced as connected prerequisites.

## Learning Effectiveness Evidence

### Backward Design

Backward design starts with learning outcomes, then defines acceptable evidence, then
builds learning activities. This is a good fit for Orion because the desired outcomes
are concrete: Hack should be able to solve coursework-style analytics problems and
communicate finance/fintech decisions.

Sources:

- [MIT Teaching and Learning Lab on backward design](https://tll.mit.edu/teaching-resources/course-design/backward-design/)
- [UIC guide to backward design](https://teaching.uic.edu/resources/teaching-guides/learning-principles-and-frameworks/backward-design/)

Orion application:

- Start each module from the deliverable Hack should be able to produce.
- Derive the quizzes, drills, guided practice, and explanations from that evidence.
- Avoid "coverage" units that teach topics without showing what skill they unlock.

### Spacing, Retrieval, Worked Examples, and Explanation

The Institute of Education Sciences practice guide recommends spacing learning over
time, interleaving worked example solutions with problem-solving exercises, combining
graphics with verbal descriptions, connecting abstract and concrete representations,
using quizzes for re-exposure, and asking deep explanatory questions.

Dunlosky et al. rate practice testing and distributed practice as high-utility learning
techniques. They rate self-explanation and interleaving as promising moderate-utility
techniques, while warning that highlighting and rereading are relatively weak study
strategies when used alone.

Sources:

- [IES What Works Clearinghouse practice guide](https://ies.ed.gov/ncee/wwc/practiceguide/1)
- [Dunlosky et al., 2013](https://journals.sagepub.com/stoken/rbtfl/Z10jaVH/60XQM/full)

Orion application:

- Use daily review due items, recent-miss review, and mixed drills.
- Teach formula and syntax recall through retrieval, not through rereading.
- Use worked examples for new Python, SQL, statistics, and finance math.
- Fade worked examples into partial-completion tasks, then independent tasks.
- Ask Hack to explain what a result means for a lender, investor, payment firm, or
  portfolio manager.

### Active Learning

Freeman et al.'s meta-analysis of undergraduate STEM courses found that active learning
improves exam performance and lowers failure rates compared with traditional lecturing.
The exact classroom setting is different from Orion, but the design lesson transfers:
Hack should spend most study time doing, checking, explaining, and revising.

Source:

- [Freeman et al., 2014](https://pubmed.ncbi.nlm.nih.gov/24821756/)

Orion application:

- Keep explanation short and usable.
- Put the learner into code, queries, calculations, interpretation, or writing quickly.
- Make each session produce evidence of skill, even if the evidence is small.

### Modern Statistics Education

The 2025 staged update of the ASA GAISE College Report recommends teaching statistics
and data science as processes for extracting insight from data to inform decisions. It
emphasizes communication, conceptual understanding over algebraic manipulation, real
data, multivariable thinking, software, ethics, active learning, and varied assessment.

Sources:

- [GAISE College Report recommendations](https://amstat.quarto.pub/college-gaise/recommendations.html)
- [ASA GAISE reports](https://www.amstat.org/education/guidelines-for-assessment-and-instruction-in-statistics-education-%28gaise%29-reports)

Orion application:

- Statistics should be taught as decision support, not as formula memorization.
- Formulas should still be rebuilt, but they should support interpretation.
- Realistic finance datasets should include missing values, outliers, skew, confounding,
  and sample-size tradeoffs.
- Assessment should include conceptual interpretation, tool fluency, and written
  recommendations.

### Novice Programming

Research on novice programming supports worked examples, faded worked examples, and
metacognitive scaffolding. A 2023 study of Python problem solving found that faded
worked examples paired with metacognitive scaffolding were especially effective for
problem-solving performance and self-regulation.

Sources:

- [Shin et al., 2023](https://journals.sagepub.com/doi/abs/10.1177/07356331231174454)
- [Renkl, Atkinson, and Grosse, 2004](https://link.springer.com/article/10.1023/B%3ATRUC.0000021815.74806.f6)

Orion application:

- For beginner Python, Orion should not jump straight from explanation to blank-editor
  problems.
- Use "read this code", "predict the output", "fill the missing line", "change one
  assumption", and "explain the result" before independent coding.
- Include brief reflection prompts: "What did this line group by?", "What changed after
  filtering?", "What would break if the column had missing values?"

## Skill-by-Skill Teaching Recommendations

### Python And Pandas

Teach Python through finance data tasks, with pandas as the main early interface.
Generic Python syntax should appear when needed, but the first win should be loading,
inspecting, filtering, grouping, plotting, and interpreting finance-shaped data.

The pandas user guide explicitly points brand-new users to "10 minutes to pandas" and
organizes the library around data structures, selection, missing data, operations,
merge, grouping, reshaping, plotting, and import/export. Those are exactly the early
pandas skills Hack needs for Core Analytics.

Sources:

- [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [10 minutes to pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html)

Recommended Orion sequence:

1. Read a CSV of loan, transaction, or return data.
2. Inspect shape, columns, dtypes, missingness, and sample rows.
3. Filter rows for a business question.
4. Create calculated columns such as return, balance change, delinquency flag, or
   payment ratio.
5. Group by borrower band, date, product, merchant, or portfolio bucket.
6. Plot a simple chart and write one sentence of interpretation.
7. Package the result into a small memo or notebook cell sequence.

### SQL

Teach SQL as the language of asking questions of relational finance data. The learner
needs a strong mental model of tables, keys, joins, filters, grouping, and query
execution order.

PostgreSQL's `SELECT` documentation lays out the practical processing order: `WITH`,
`FROM`, `WHERE`, `GROUP BY`, output expressions, distinct handling, set operators,
`ORDER BY`, and limiting. Orion does not need to expose every PostgreSQL feature early,
but it should teach this mental model.

Sources:

- [PostgreSQL SELECT documentation](https://www.postgresql.org/docs/18/sql-select.html)
- [Mode SQL tutorial](https://mode.com/sql-tutorial/)
- [SQLBolt interactive SQL lessons](https://w.sqlbolt.com/)

Recommended Orion sequence:

1. Single-table `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`.
2. Aggregates and `GROUP BY` for balances, transaction counts, conversion rates, and
   default rates.
3. Joins across customers, accounts, transactions, loans, applications, and payments.
4. `CASE` for risk bands and business flags.
5. Date logic for cohorts, monthly rollups, delinquency windows, and revenue periods.
6. Window functions after grouping and joins are comfortable.
7. SQL-to-pandas comparison tasks so Hack learns when each tool is useful.

### Statistics

Teach statistics as the language of uncertainty and decision risk. Start from fintech
questions:

- Is this conversion lift real enough to ship?
- Is this default-rate difference meaningful or just sample noise?
- How much uncertainty is in this forecast?
- What could confound this underwriting result?
- Which model mistake is more costly: false approval or false rejection?

Recommended Orion sequence:

1. Variables, units, rows, samples, and populations.
2. Distributions, skew, outliers, and missingness in finance data.
3. Summary statistics for returns, balances, conversion, loss, and volatility.
4. Probability, conditional probability, and expected value.
5. Sampling variability and standard error through simulation.
6. Confidence intervals for means, rates, and differences.
7. Hypothesis tests as structured decision risk.
8. A/B testing, power, minimum detectable effect, and practical significance.
9. Correlation, regression, confounding, and residuals.
10. Model evaluation basics: accuracy, precision, recall, false positives, false
    negatives, calibration, and cost-weighted interpretation.

The first rebuild, `Statistics for Fintech Decisions`, should use pandas for small
calculations and simulations from the beginning. This reduces fear of both statistics
and Python because the same data story carries both.

### Finance Math

Teach finance math from scratch, but never as isolated symbol pushing. Each formula
should appear in four forms:

1. Plain-language idea.
2. Tiny numeric example.
3. Python function or pandas calculation.
4. Excel check or presentation version.

Recommended Orion sequence:

1. Percent change, simple return, log return, and annualization.
2. Time value of money, compounding, discounting, and net present value.
3. Cash-flow schedules, loan amortization, interest rates, and balances.
4. Risk and return: mean, volatility, covariance, correlation, and Sharpe ratio.
5. Portfolio weights, rebalancing, and contribution to return.
6. Valuation basics: DCF, multiples, sensitivity, and scenario analysis.
7. Fixed income basics: price, yield, duration, convexity, and rate sensitivity.
8. Options and futures intuition: payoff diagrams, hedging, no-arbitrage, and
   simulation before advanced pricing.

This gives Hack formula memory, but keeps formulas attached to code, decisions, and
finance contexts.

### Excel

Excel should support, not lead. The main learning path should stay Python/pandas first,
because WashU's core includes Python and data science, SQL, machine learning, text
mining, big data, and prescriptive analytics.

Excel is still useful for:

- checking finance formulas by hand
- building simple sensitivity tables
- making coursework-friendly exhibits
- communicating with finance audiences
- validating a Python output against a familiar tool

## Core Analytics Rebuild

The rebuild should have three layers: a diagnostic layer, a module layer, and a review
layer.

### Layer 1: Diagnostic

Before the first real module, Orion should identify Hack's current fluency:

- Python basics: variables, lists, functions, errors, notebooks, imports.
- Pandas basics: DataFrame, columns, filters, groupby, missing values, plotting.
- SQL basics: select, filter, aggregate, join.
- Statistics: variable types, distributions, standard deviation, probability,
  confidence intervals, p-values, regression.
- Finance math: returns, compounding, discounting, cash flows, amortization, valuation.

The diagnostic should not feel like a gate. It should produce a study map and a few
first review items.

### Layer 2: Modules

Recommended first module:

`Statistics for Fintech Decisions`

First polished deliverable format:

- A mixed analyst memo plus notebook. The memo should make the business
  recommendation, summarize evidence, and name limitations. The notebook should show
  the reproducible pandas/statistics work that supports the memo.

Suggested unit sequence:

1. What counts as evidence in a fintech decision?
2. Rows, variables, data quality, and finance context.
3. Distributions, outliers, and summary statistics.
4. Probability, expected value, and simulation.
5. Sampling variability and standard error.
6. Confidence intervals for rates and averages.
7. Hypothesis testing and decision risk.
8. A/B testing for conversion and product changes.
9. Regression, confounding, and business interpretation.
10. Final analyst memo: recommend a fintech decision with evidence and limitations.

Parallel micro-track:

- 10 to 15 minutes of Python/pandas inside most units.
- 5 to 10 minutes of formula retrieval where needed.
- SQL introduced once table thinking is stable, then reinforced with finance schemas.

Next modules:

1. `Python And Pandas For Financial Data`
2. `SQL For Financial Data`
3. `Data Visualization And Analyst Communication`
4. `Finance Math For Analytics`
5. `A/B Testing And Experimentation`
6. `Machine Learning For Business Outcomes`
7. `Text Mining, Big Data, And Prescriptive Analytics Preview`

The later modules should stay lighter until the first statistics rebuild proves the
lesson, drill, review, and deliverable model.

### Layer 3: Review

The review layer should replace streak motivation with competence signals:

- review due
- weak topics
- recent misses
- confidence
- time since last correct answer
- lesson completion
- deliverables completed
- retry readiness

Recommended 60-minute session:

1. 10 minutes: review due items.
2. 15 minutes: mixed drill across stats, Python/pandas, SQL, and finance formulas.
3. 25 minutes: guided practice tied to the current module.
4. 10 minutes: reflection, notes, quiz retry, or one deliverable paragraph.

This matches the product contract and keeps daily work serious without turning it into
a streak game.

## Lesson Schema For Orion

Every new Core Analytics lesson should carry structured metadata:

- WashU target: one or more core/concentration courses.
- Skill: statistics, Python, pandas, SQL, finance math, visualization, communication.
- Context: lending, payments, investing, fraud, underwriting, portfolio, valuation, or
  fixed income.
- Prerequisites: concepts or syntax Hack should already know.
- Concept goal: what Hack should understand.
- Performance goal: what Hack should be able to do.
- Worked example: complete solution with explanation.
- Practice task: faded or independent task.
- Retrieval items: short questions for review.
- Miss tags: concept tags used for adaptive review.
- Deliverable: chart, table, memo, notebook, or calculation artifact.
- Reflection: one prompt asking what the result means for a finance decision.

This schema lets Orion recommend the next action without pretending the learner is
starting from a blank slate each day.

## Assessment Model

Orion should assess four kinds of mastery:

1. Recall: formulas, vocabulary, syntax, and definitions.
2. Procedure: can Hack carry out the calculation, query, or pandas operation?
3. Interpretation: can Hack explain what the output means?
4. Transfer: can Hack use the idea in a new finance/fintech situation?

For early modules, most assessment should be formative. Hack needs fast feedback and
repair, not high-stakes scoring.

Recommended assessment types:

- quick retrieval cards
- prediction questions before running code
- fill-the-missing-line code tasks
- SQL expected-output checks
- formula reconstruction
- chart interpretation
- short analyst recommendations
- end-of-unit polished deliverables

## Source Map

Program and curriculum sources:

- [WashU Olin MSBA curriculum](https://olin.washu.edu/programs/specialized-masters/ms-in-business-analytics/curriculum.php)
- [WashU Olin MS in Quantitative Finance curriculum](https://olin.washu.edu/programs/specialized-masters/ms-in-quantitative-finance/curriculum.php)
- [MIT Sloan MFin curriculum](https://mitsloan.mit.edu/mfin/explore-program/mfin-curriculum)
- [MIT Sloan MBAn curriculum](https://mitsloan.mit.edu/master-of-business-analytics/explore-program/mban-curriculum)
- [Berkeley Haas MFE curriculum](https://mfe.haas.berkeley.edu/academics/curriculum)
- [CMU MSCF academics](https://www.cmu.edu/mscf/academics/index.html)
- [Columbia MSFE catalog](https://bulletin.columbia.edu/columbia-engineering/academic-departments-programs/industrial-engineering-operations-research/graduate-programs/financial-engineering-ms/)

Learning effectiveness sources:

- [IES What Works Clearinghouse practice guide](https://ies.ed.gov/ncee/wwc/practiceguide/1)
- [Dunlosky et al., 2013](https://journals.sagepub.com/stoken/rbtfl/Z10jaVH/60XQM/full)
- [Freeman et al., 2014](https://pubmed.ncbi.nlm.nih.gov/24821756/)
- [GAISE College Report recommendations](https://amstat.quarto.pub/college-gaise/recommendations.html)
- [ASA GAISE reports](https://www.amstat.org/education/guidelines-for-assessment-and-instruction-in-statistics-education-%28gaise%29-reports)
- [MIT Teaching and Learning Lab on backward design](https://tll.mit.edu/teaching-resources/course-design/backward-design/)
- [UIC guide to backward design](https://teaching.uic.edu/resources/teaching-guides/learning-principles-and-frameworks/backward-design/)
- [Shin et al., 2023](https://journals.sagepub.com/doi/abs/10.1177/07356331231174454)
- [Renkl, Atkinson, and Grosse, 2004](https://link.springer.com/article/10.1023/B%3ATRUC.0000021815.74806.f6)

Tool learning sources:

- [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [10 minutes to pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html)
- [PostgreSQL SELECT documentation](https://www.postgresql.org/docs/18/sql-select.html)
- [Mode SQL tutorial](https://mode.com/sql-tutorial/)
- [SQLBolt interactive SQL lessons](https://w.sqlbolt.com/)

## Hack Decisions

- The first `Statistics for Fintech Decisions` polished deliverable should be a mixed
  analyst memo plus notebook.
- The first fintech context should be portfolio risk.
- SQL can be included inside `Statistics for Fintech Decisions` once the lesson needs
  table thinking.
- Finance formulas should be introduced as Python functions first, then checked with
  hand calculation or Excel.
- The first dataset should be a small built-in synthetic portfolio so the module stays
  deterministic, local, beginner-readable, and easy to test.
- The first memo-plus-notebook deliverable should be addressed to a risk committee.
- The next fintech context after portfolio risk should be lending and credit risk:
  default, delinquency, underwriting, borrower segmentation, and decision thresholds.

## Chosen Path Forward

The curriculum should move in three passes.

1. Build a tight portfolio-risk statistics module using a built-in synthetic dataset.
   This keeps the first module reproducible and avoids API, data licensing, and market
   data cleanup issues while Hack is still rebuilding statistics and Python fluency.
2. Use the capstone as a risk-committee deliverable. That audience forces disciplined
   evidence: recommendation, metric, uncertainty, limitation, and next step.
3. Move next into lending and credit risk. It is the best second context because it
   naturally introduces SQL schemas, default and delinquency rates, borrower bands,
   underwriting thresholds, classification errors, and A/B testing.

## Questions for Hack

No open decisions for this phase. Continue with the chosen path forward above.
