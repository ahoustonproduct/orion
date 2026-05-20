# Core Analytics Graduate Statistics Rebuild Plan

Status: grading draft for Hack.

This document replaces the earlier portfolio-risk-first statistics spine with a
graduate statistics course for financial analysis. The module should teach statistics
deeply, not merely introduce statistical vocabulary. Finance is the data context, but
the target skill is statistics: probability, estimation, inference, regression,
diagnostics, multivariate methods, resampling, Bayesian thinking, and time series.

The rebuilt module should be a 30-lesson mini-course. Every lesson should be code
first, math explained alongside, and practice-heavy. Hack should be writing Python in
nearly every meaningful task.

## What Changed

The earlier module treated "portfolio risk decision" as the organizing frame. That
was too narrow and made the curriculum feel as if statistics existed only to answer
one investment question. The new spine uses generic financial-analysis datasets:
revenue, costs, margins, cash flow, loan payments, customer balances, transaction
counts, default flags, pricing, churn, fraud flags, and time-indexed financial
metrics.

The new sequence is also stricter about dependency. A lesson cannot jump to a new
abstraction unless the previous lesson built the object needed for that abstraction.
The rhythm is:

1. Create the data object in Python.
2. Perform one operation on it.
3. Name the mathematical object created by that operation.
4. Rebuild the calculation manually with NumPy.
5. Check it with pandas, SciPy, or statsmodels.
6. Interpret the result in financial-analysis language.
7. Drill the exact move several ways.
8. Finish with a homework-style coding problem and model answer.

## Video Integration

The source video is [Python for Data Analytics - Full Course for Beginners][video] by
Luke Barousse. The usable curriculum lesson from the video is its apprenticeship
structure:

- It starts with Python objects before expecting data analysis.
- It introduces variables, types, operators, conditionals, lists, dictionaries, loops,
  functions, modules, NumPy, pandas, inspection, cleaning, analysis, plotting, and a
  final project in a visible progression.
- It repeatedly pauses for exercises instead of treating practice as an afterthought.
- It uses a cumulative project so later skills reuse earlier tools.

Orion should adapt that rhythm, but not copy the topic order literally. Hack is not
trying to take a generic beginner Python course. Orion should use the same gradual
coding apprenticeship while teaching graduate statistics for financial analysis.

## Teaching Standard

Each lesson should feel like a compact textbook chapter plus a lab.

The Learn section should be the longest section. It should include:

- a short "you already know" bridge from the prior lesson
- the exact new concept for the current lesson
- a small financial dataset built or loaded in Python
- at least three worked code examples
- formal notation after the code object exists
- a manual NumPy implementation before a library shortcut
- a pandas, SciPy, or statsmodels confirmation
- common mistakes and why they matter
- a short model-answer interpretation

Practice should include 15 to 25 connected drills:

- syntax drills
- calculation drills
- notation-to-code translation
- code-to-notation translation
- interpretation checks
- small debugging tasks
- one cumulative mini-problem using the same dataset

Challenge should be a graduate homework-style coding task:

- no written-only response unless code produced the answer
- starter data included
- multiple required intermediate outputs
- model answer included
- tests should check calculations, not just printed labels

## Lesson 1 Repair

The old Lesson 1 jumped too quickly from "a dataset has variables" to "a column is a
vector." The bridge must become explicit:

1. A row is one observation: one period, customer, loan, account, or transaction.
2. A column is one variable measured across all observations.
3. Selecting a column in pandas creates a `Series`.
4. A `Series` can be converted to a NumPy array.
5. A NumPy array is the computational form of a statistical vector.
6. Once the vector exists, formulas can operate over it.
7. The first formula over a vector is a sum.
8. The second formula is a mean, which is a sum divided by count.

The lesson should not introduce vector notation until the learner has already pulled
the column in code:

```python
import pandas as pd

financials = pd.DataFrame({
    "period": ["Q1", "Q2", "Q3", "Q4"],
    "revenue_growth": [0.04, 0.06, 0.03, 0.07],
})

growth_series = financials["revenue_growth"]
growth_vector = growth_series.to_numpy()

print(growth_series)
print(growth_vector)
```

Then the notation is introduced as a name for the object already visible:

```text
x = (x_1, x_2, x_3, x_4)
x = (0.04, 0.06, 0.03, 0.07)
```

Only after that should the lesson compute:

```python
n = len(growth_vector)
total = growth_vector.sum()
mean_growth = total / n
```

That is the intended lesson flow: data table -> column -> Series -> vector -> sum ->
mean. Each step earns the next one.

## Thirty-Lesson Syllabus

### Unit 1: Statistical Data And Descriptive Foundations

1. Statistical Tables In Python
   - Builds from: Python objects and small financial records.
   - Adds: observations, variables, DataFrames, numeric vs categorical columns.
   - Produces: a clean financial-analysis table ready for statistical work.

2. Columns, Series, And Vectors
   - Builds from: DataFrames created in Lesson 1.
   - Adds: selecting columns, converting to arrays, vector notation.
   - Produces: one numeric vector and one categorical vector from the same table.

3. Summation, Count, Mean, And Weighted Mean
   - Builds from: vectors created in Lesson 2.
   - Adds: `sum`, `len`, arithmetic mean, weighted mean, notation for averages.
   - Produces: revenue growth averages and weighted customer-balance averages.

4. Deviations, Variance, And Standard Deviation
   - Builds from: the mean in Lesson 3.
   - Adds: deviations from mean, squared deviations, sample variance, sample standard
     deviation, degrees of freedom.
   - Produces: manual and pandas standard deviation for financial metrics.

5. Standardization, Z-Scores, And Empirical Distributions
   - Builds from: mean and standard deviation in Lesson 4.
   - Adds: z-scores, standardized variables, histograms, empirical percentiles.
   - Produces: standardized financial observations and outlier flags.

6. Covariance, Correlation, And Relationship Matrices
   - Builds from: paired standardized vectors in Lesson 5.
   - Adds: covariance, correlation, correlation matrices, scatter plots.
   - Produces: a relationship matrix among revenue growth, margin, cash flow, and
     customer balance.

### Unit 2: Probability From Data

7. Probability As Counting With Indicator Variables
   - Builds from: categorical and numeric flags in Lesson 6.
   - Adds: indicator vectors, event counts, relative frequency.
   - Produces: probabilities for late payment, fraud flag, churn, or margin miss.

8. Conditional Probability And Bayes Rule With Masks
   - Builds from: event probabilities in Lesson 7.
   - Adds: pandas masks, intersections, conditional probability, Bayes rule.
   - Produces: probability of default given delinquency and reverse conditioning.

9. Random Variables, Expected Value, And Variance
   - Builds from: events and probabilities in Lesson 8.
   - Adds: discrete random variables, probability mass functions, expectation,
     variance.
   - Produces: expected loss or expected margin from a scenario table.

10. Bernoulli And Binomial Models
   - Builds from: indicator variables in Lesson 7 and random variables in Lesson 9.
   - Adds: Bernoulli trials, binomial counts, binomial mean and variance.
   - Produces: default-count and conversion-count calculations.

11. Normal, Poisson, And Gamma Models
   - Builds from: distribution logic in Lessons 9 and 10.
   - Adds: normal continuous outcomes, Poisson counts, Gamma positive amounts.
   - Produces: model choices for returns-like metrics, transaction counts, and loss
     severity.

12. Simulation And The Central Limit Theorem
   - Builds from: named distributions in Lesson 11.
   - Adds: repeated sampling, sampling distributions, CLT intuition, Monte Carlo.
   - Produces: simulated sample means and a visual CLT demonstration.

### Unit 3: Estimation

13. Estimators, Bias, Variance, And Sampling Error
   - Builds from: simulated sampling distributions in Lesson 12.
   - Adds: estimator notation, bias, variance of an estimator, standard error.
   - Produces: repeated estimates of mean margin or default rate.

14. Method Of Moments
   - Builds from: sample moments in Lessons 3, 4, and 13.
   - Adds: matching sample moments to distribution parameters.
   - Produces: moment estimates for normal and Gamma parameters.

15. Maximum Likelihood Estimation
   - Builds from: probability models in Lessons 10 and 11.
   - Adds: likelihood, log-likelihood, grid search, numerical optimization.
   - Produces: MLE estimates for Bernoulli default probability and normal mean/sigma.

16. Confidence Intervals
   - Builds from: standard error and estimators in Lesson 13.
   - Adds: estimate plus/minus margin, t intervals, proportion intervals.
   - Produces: intervals for average margin and default rate.

### Unit 4: Hypothesis Testing

17. Hypothesis Test Anatomy
   - Builds from: estimates and intervals in Lesson 16.
   - Adds: `H0`, `HA`, test statistic, null distribution, rejection rule.
   - Produces: a coded one-sample test skeleton.

18. One-Sample And Two-Sample Mean Tests
   - Builds from: test anatomy in Lesson 17.
   - Adds: one-sample t test, independent two-sample t test, paired t test.
   - Produces: tests of financial metric changes across periods or groups.

19. Proportion Tests And Chi-Square Tests
   - Builds from: Bernoulli/binomial thinking in Lesson 10.
   - Adds: one-proportion, two-proportion, goodness-of-fit, independence tests.
   - Produces: default-rate, approval-rate, fraud-rate, and category-mix tests.

20. P-Values, Power, Effect Size, And Practical Significance
   - Builds from: tests in Lessons 17 to 19.
   - Adds: p-value interpretation, Type I/II error, power, effect size.
   - Produces: decisions that separate statistical significance from financial size.

### Unit 5: Regression And Generalized Linear Models

21. Simple Linear Regression From Covariance
   - Builds from: covariance and correlation in Lesson 6.
   - Adds: slope as covariance divided by variance, intercept, residuals.
   - Produces: manual simple regression and statsmodels confirmation.

22. Matrix Algebra For OLS
   - Builds from: simple regression in Lesson 21.
   - Adds: design matrix `X`, coefficient vector `beta`, normal equations.
   - Produces: `beta_hat = (X'X)^(-1)X'y` in NumPy.

23. Multiple Regression And Coefficient Interpretation
   - Builds from: OLS matrix algebra in Lesson 22.
   - Adds: multiple predictors, controls, fitted values, adjusted interpretation.
   - Produces: a multi-factor financial performance model.

24. Regression Diagnostics
   - Builds from: residuals and fitted values in Lessons 21 to 23.
   - Adds: heteroscedasticity, multicollinearity, autocorrelation, influence.
   - Produces: diagnostic plots, VIF, residual checks, and remediation choices.

25. Logistic And Probit Regression
   - Builds from: Bernoulli outcomes in Lesson 10 and regression in Lesson 23.
   - Adds: log odds, probability models, logistic/probit link functions.
   - Produces: a binary outcome model for default, churn, fraud, or approval.

26. Hierarchical And Mixed-Effects Models
   - Builds from: grouped financial data and regression in Lesson 23.
   - Adds: fixed effects, random effects, group-level variation.
   - Produces: a model that separates account-level and segment-level effects.

### Unit 6: Multivariate, Resampling, Bayesian, And Time Series

27. PCA, Factor Analysis, And Latent Structure
   - Builds from: covariance and correlation matrices in Lesson 6.
   - Adds: eigenvectors, principal components, factor loadings.
   - Produces: dimension reduction for correlated financial indicators.

28. Clustering, Discriminant Analysis, MANOVA, And SEM Foundations
   - Builds from: standardized variables in Lesson 5 and multivariate structure in
     Lesson 27.
   - Adds: k-means, hierarchical clustering, discriminant separation, group mean
     vectors, path thinking for SEM.
   - Produces: customer or account segments and a first structural model diagram.

29. Bootstrap, Nonparametric Statistics, Bayesian Inference, And MCMC
   - Builds from: sampling distributions in Lesson 12 and estimators in Lesson 13.
   - Adds: bootstrap resampling, permutation logic, priors, posteriors, MCMC idea.
   - Produces: bootstrap intervals and a simple Bayesian estimate.

30. Time Series, Forecasting, Ethics, And Final Project
   - Builds from: regression, residuals, and uncertainty.
   - Adds: time index, lag, autocorrelation, ARIMA foundations, forecast intervals,
     ethical communication.
   - Produces: a final notebook with data cleaning, statistics, model diagnostics,
     uncertainty, and model answers.

## Curriculum Implementation Standard

For every lesson, the in-app content should be built as:

1. Learn: textbook-style chapter with code examples.
2. Practice: 15 to 25 linked drills.
3. Challenge: one multi-part coding homework problem.
4. Review: generated only from concepts and code that were actually taught.
5. Model answer: always available after the learner attempts the problem.

The app should remove self-referential language such as "Why does Orion keep the
Python function first?" Questions should ask about the concept, not the app. Better:

```text
Why write the calculation as a Python function before using a library shortcut?
```

The answer is:

```text
Because the function makes the inputs, operation, and output explicit before the
same calculation is scaled across a table.
```

## First Module Deliverable

The final deliverable should be a mixed notebook plus memo:

- cleaned generic financial dataset
- descriptive statistics table
- probability and distribution section
- estimation and inference section
- regression model with diagnostics
- one multivariate or resampling extension
- final recommendation
- limitations and ethics note
- appendix with reproducible Python code

## Source Spine

These sources should guide the rebuild:

- [Python for Data Analytics - Full Course for Beginners][video]: instructional
  rhythm, cumulative coding, exercises, pandas workflow, and final project structure.
- [OpenIntro Statistics][openintro]: data, probability, distributions, inference,
  regression, labs, and companion resources.
- [Think Stats 2e][think-stats]: Python-first probability/statistics pedagogy, real
  datasets, and simulation-based exercises.
- [An Introduction to Statistical Learning][isl]: regression, classification,
  resampling, model selection, unsupervised learning, and Python labs.
- [ISL Python resources][isl-python]: notebook and dataset pattern for chapter-linked
  labs.
- [The Elements of Statistical Learning][esl]: advanced statistical learning depth for
  the upper end of the module.

[video]: https://www.youtube.com/watch?v=wUSDVGivd-8
[openintro]: https://www.openintro.org/book/os/
[think-stats]: https://greenteapress.com/wp/think-stats-2e/
[isl]: https://www.statlearning.com/
[isl-python]: https://www.statlearning.com/resources-python
[esl]: https://hastie.su.domains/ElemStatLearn/

## Questions For Hack

1. Should Lesson 1 use quarterly company financials, customer-account records, or loan
   performance records as the first cumulative dataset?
2. Should the final project emphasize corporate financial analysis, lending analytics,
   payments/fraud analytics, or a mixed financial dataset?
3. Should the first implementation pass rebuild only Lessons 1 to 5 in full depth, or
   should it create all 30 lesson shells first and then deepen them in order?
