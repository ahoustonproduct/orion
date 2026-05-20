"""Core Analytics: Statistics for Fintech Decisions.

This module is intentionally built as a full mini-course rather than a short survey.
It exports a 30-lesson Python/math-first statistics sequence for financial analysis,
with finance context used as realistic data rather than a narrow portfolio-risk
story.
"""


def _concept(spec):
    pitfalls = "\n".join(f"- {item}" for item in spec["pitfalls"])
    return f"""## Graduate Bridge Goal

This lesson builds one piece of the statistics foundation Hack needs for graduate
analytics work. The finance question is not decorative: every calculation is tied to
how a fintech analyst would defend a risk decision.

## Decision Frame

{spec["decision"]}

Before writing code, name the decision. A statistic is useful only when it helps decide
whether to keep a portfolio policy, investigate risk, change a threshold, or gather
better evidence.

## Statistical Idea

{spec["idea"]}

The goal is to learn the concept, the calculation, and the interpretation together.
Graduate-level statistics requires moving between notation, code, and decision language
without losing track of assumptions.

## Python Function First

```python
{spec["function_code"]}
```

Read the function as a contract. The inputs represent the evidence available right now.
The return value is the statistic. A correct function is not enough by itself; the
analyst still has to explain what the statistic does and does not prove.

## pandas Bridge

{spec["pandas_bridge"]}

```python
{spec["pandas_code"]}
```

The same idea scales from one value to a table. pandas is the bridge between the small
formula and the repeated observations that appear in graduate coursework.

## Interpretation Rule

{spec["interpretation"]}

A strong analyst sentence has three parts: the number, the decision meaning, and the
limitation. Do not say "the data proves" when the statistic only provides evidence.

## Common Mistakes

{pitfalls}

## Practice And Challenge

Practice will check recognition, calculation, syntax, interpretation, and limitation.
The challenge asks you to write the function, apply it to a small portfolio dataset,
and print an analyst-ready result with the required label `{spec["output_label"]}`.
"""


def _questions(spec):
    return [
        {
            "type": "multiple_choice",
            "question": f"What is the main purpose of {spec['metric']} in this lesson?",
            "options": [
                spec["purpose"],
                "To guarantee the portfolio will outperform next month",
                "To avoid explaining assumptions to the risk committee",
                "To replace Python, pandas, and SQL with memorized definitions",
            ],
            "answer": 0,
            "explanation": spec["purpose_explanation"],
        },
        {
            "type": "true_false",
            "question": spec["overclaim"],
            "answer": False,
            "explanation": spec["overclaim_explanation"],
        },
        {
            "type": "fill_blank",
            "question": "Complete the key syntax from the lesson.",
            "template": spec["syntax_template"],
            "answer": spec["syntax_answer"],
            "explanation": spec["syntax_explanation"],
        },
        {
            "type": "multiple_choice",
            "question": "Which interpretation is most appropriate for graduate-level analytics work?",
            "options": [
                spec["good_interpretation"],
                "This number proves the portfolio is safe for every investor.",
                "This number should be reported without context because code ran successfully.",
                "This number is irrelevant because all statistics are subjective.",
            ],
            "answer": 0,
            "explanation": "The best interpretation connects the statistic to a decision while avoiding overclaiming.",
        },
        {
            "type": "multiple_choice",
            "question": "Which limitation should accompany this analysis?",
            "options": [
                spec["limitation"],
                "There are no limitations once pandas is used.",
                "The limitation is that the result was printed with a label.",
                "The limitation is that finance decisions never use statistics.",
            ],
            "answer": 0,
            "explanation": "Graduate-level work is explicit about what the statistic cannot establish.",
        },
        {
            "type": "true_false",
            "question": "A decision frame should be named before treating the statistic as evidence.",
            "answer": True,
            "explanation": "The same number can imply different actions under different decisions, users, and risk limits.",
        },
        {
            "type": "multiple_choice",
            "question": "Why should the formula be written as a Python function before scaling it in pandas?",
            "options": [
                "It makes inputs, calculation, and output explicit before tools become more complex.",
                "It removes the need to understand the statistic.",
                "It makes every result automatically significant.",
                "It prevents the analyst from using pandas later.",
            ],
            "answer": 0,
            "explanation": "The function is the clearest beginner-readable version of the formula.",
        },
        {
            "type": "fill_blank",
            "question": "Fill in the function name used in the challenge.",
            "template": "def ___(...):",
            "answer": spec["function_name"],
            "explanation": f"The challenge asks for `{spec['function_name']}`.",
        },
        {
            "type": "multiple_choice",
            "question": "What should the challenge output include?",
            "options": [
                f"A line beginning with `{spec['output_label']}`",
                "Only raw Python object memory addresses",
                "A chart with no explanation",
                "A recommendation that ignores the computed result",
            ],
            "answer": 0,
            "explanation": "The output label makes the result readable as analyst evidence.",
        },
        {
            "type": "multiple_choice",
            "question": "Which mistake would most weaken the analysis?",
            "options": [
                spec["main_mistake"],
                "Using a clear variable name",
                "Printing the result with an explanatory label",
                "Checking the calculation before interpreting it",
            ],
            "answer": 0,
            "explanation": spec["mistake_explanation"],
        },
        {
            "type": "true_false",
            "question": spec["pandas_true_false"],
            "answer": True,
            "explanation": spec["pandas_explanation"],
        },
        {
            "type": "multiple_choice",
            "question": "What is the best next analyst move after computing the statistic?",
            "options": [
                spec["next_step"],
                "Delete the code because the first result is enough",
                "Claim the future will match the sample exactly",
                "Skip the memo and show only the line number",
            ],
            "answer": 0,
            "explanation": "A statistic should lead into interpretation, diagnostics, comparison, or a better data request.",
        },
    ]


def _build_lesson(spec):
    return {
        "id": spec["id"],
        "title": spec["title"],
        "order": spec["order"],
        "duration_min": spec.get("duration_min", 60),
        "difficulty": spec["difficulty"],
        "is_capstone": spec.get("is_capstone", False),
        "real_world_context": spec["context"],
        "concept": _concept(spec),
        "worked_example": {
            "description": spec["worked_description"],
            "code": spec["worked_code"],
            "explanation": spec["worked_explanation"],
        },
        "reference": {
            "key_syntax": spec["key_syntax"],
            "notes": spec["reference_notes"],
        },
        "questions": _questions(spec),
        "challenge": {
            "instructions": spec["challenge_instructions"],
            "starter_code": spec["starter_code"],
            "tests": spec["tests"],
            "solution": spec["solution"],
        },
    }


LESSON_SPECS = [
    {
        "id": "casfd-l1",
        "label": "Evidence And Portfolio Risk",
        "title": "What Counts As Evidence In Portfolio Risk?",
        "order": 1,
        "difficulty": "beginner",
        "metric": "simple return",
        "function_name": "simple_return",
        "output_label": "Portfolio return",
        "context": "A fintech investing team wants to know whether a starter portfolio moved enough to raise a risk question for cautious users.",
        "decision": "The committee needs to know whether a single period portfolio move is meaningful evidence or just an isolated price change.",
        "idea": "Simple return measures percentage change from a starting value to an ending value. It is the first finance formula because it teaches scale, sign, and interpretation.",
        "function_code": "def simple_return(start_price, end_price):\n    return (end_price - start_price) / start_price",
        "pandas_bridge": "When prices become rows, the same formula can be applied to every asset in a DataFrame.",
        "pandas_code": "prices[\"simple_return\"] = (prices[\"end_price\"] - prices[\"start_price\"]) / prices[\"start_price\"]",
        "interpretation": "A 0.03 simple return should be communicated as a 3.00 percent gain over the measured period, not as proof that the portfolio is low risk.",
        "pitfalls": ["Confusing dollar change with percent change", "Treating a positive return as proof of safety", "Forgetting to state the period measured"],
        "purpose": "To turn a price move into percentage evidence that can be compared across assets or portfolios",
        "purpose_explanation": "Simple return scales the move by the starting value so different assets can be compared.",
        "overclaim": "A positive simple return proves the portfolio is suitable for cautious investors.",
        "overclaim_explanation": "A single positive return says nothing about volatility, drawdown, or future losses.",
        "syntax_template": "return (end_price - start_price) ___ start_price",
        "syntax_answer": "/",
        "syntax_explanation": "The slash operator divides the price change by the starting value.",
        "good_interpretation": "The portfolio returned 3.00 percent over the period; this shows direction and magnitude, not total risk.",
        "limitation": "A single return does not show volatility, drawdown, tail risk, or future performance.",
        "main_mistake": "Comparing raw dollar changes across portfolios with different starting values",
        "mistake_explanation": "Raw dollars ignore scale; return converts the move into a comparable percentage.",
        "pandas_true_false": "A pandas column can store repeated simple-return observations for later statistics.",
        "pandas_explanation": "A DataFrame column is how one formula becomes many observations.",
        "next_step": "Compare the return against volatility, benchmark, and customer risk tolerance.",
        "worked_description": "Compute a portfolio return and state its limitation.",
        "worked_code": "def simple_return(start_price, end_price):\n    return (end_price - start_price) / start_price\n\nportfolio_return = simple_return(25000, 25750)\nprint(f\"Portfolio return: {portfolio_return:.2%}\")\nprint(\"Limitation: one return does not establish total risk.\")",
        "worked_explanation": "The portfolio gained 3.00 percent. The result is useful, but it is only the first evidence point.",
        "key_syntax": ["def simple_return(start_price, end_price):", "(end_price - start_price) / start_price", "print(f\"{value:.2%}\")"],
        "reference_notes": "Keep decimals for calculation and percentages for communication.",
        "challenge_instructions": "Write simple_return for a portfolio that moves from 25000 to 25750. Print Portfolio return, Risk interpretation, and Limitation.",
        "starter_code": "def simple_return(start_price, end_price):\n    # return percentage change\n    pass\n\nportfolio_return = simple_return(25000, 25750)\n# Print Portfolio return, Risk interpretation, and Limitation.",
        "tests": [{"type": "code_contains", "value": "def simple_return"}, {"type": "output_contains", "value": "Portfolio return"}, {"type": "output_contains", "value": "Risk interpretation"}, {"type": "output_contains", "value": "Limitation"}, {"type": "runs_without_error"}],
        "solution": "def simple_return(start_price, end_price):\n    return (end_price - start_price) / start_price\n\nportfolio_return = simple_return(25000, 25750)\nprint(f\"Portfolio return: {portfolio_return:.2%}\")\nprint(\"Risk interpretation: The portfolio gained 3.00%, which gives direction and magnitude for the risk discussion.\")\nprint(\"Limitation: A single return does not show volatility, drawdown, tail risk, or future performance.\")",
    },
    {
        "id": "casfd-l2",
        "label": "Returns As Data",
        "title": "Returns As Rows, Columns, And Distributions",
        "order": 2,
        "difficulty": "beginner",
        "metric": "return table inspection",
        "function_name": "build_return_table",
        "output_label": "Worst equity day",
        "context": "The risk team receives a small file of daily asset returns and needs to inspect it before trusting any conclusion.",
        "decision": "The analyst must decide whether the table is usable enough for first-pass portfolio evidence.",
        "idea": "A distribution is the pattern of observed returns: center, spread, skew, and unusual observations.",
        "function_code": "def build_return_table(data):\n    return pd.DataFrame(data)",
        "pandas_bridge": "pandas lets Hack inspect shape, columns, missingness, summary statistics, and worst observations.",
        "pandas_code": "print(returns.shape)\nprint(returns.describe())\nprint(returns[\"equity_return\"].min())",
        "interpretation": "A worst day is downside evidence, while describe() shows whether the sample has enough observations to discuss center and spread.",
        "pitfalls": ["Skipping shape and missing-value checks", "Treating one row as a stable distribution", "Ignoring which column represents which asset"],
        "purpose": "To convert scattered returns into a table that can support repeated statistical questions",
        "purpose_explanation": "Graduate analytics work starts by understanding the observational unit and variables.",
        "overclaim": "Once a return table exists, its statistics are automatically trustworthy.",
        "overclaim_explanation": "The table can still be too small, missing values, mislabeled, or unrepresentative.",
        "syntax_template": "returns.___()",
        "syntax_answer": "describe",
        "syntax_explanation": "describe() summarizes numeric columns.",
        "good_interpretation": "The table shows observed return patterns; it still needs data-quality checks before a risk claim.",
        "limitation": "A tiny sample may not represent normal or stressed market conditions.",
        "main_mistake": "Making a risk recommendation before checking shape, columns, and summary statistics",
        "mistake_explanation": "Bad or misunderstood data can make correct formulas produce bad analysis.",
        "pandas_true_false": "df.describe() is a useful first summary for numeric return columns.",
        "pandas_explanation": "It provides count, mean, standard deviation, quartiles, and extremes.",
        "next_step": "Identify worst days, missing values, and columns that need deeper risk metrics.",
        "worked_description": "Create a small return table and inspect downside evidence.",
        "worked_code": "import pandas as pd\n\nreturns = pd.DataFrame({\n    \"equity_return\": [0.012, -0.006, 0.018, -0.021],\n    \"bond_return\": [0.002, 0.001, -0.003, 0.004],\n})\nprint(returns.shape)\nprint(returns.describe())\nprint(f\"Worst equity day: {returns['equity_return'].min():.2%}\")",
        "worked_explanation": "The analyst sees both table structure and the most severe equity loss before moving into volatility.",
        "key_syntax": ["pd.DataFrame({...})", "df.shape", "df.describe()", "df['column'].min()"],
        "reference_notes": "Inspect before modeling. Data shape is part of statistical evidence.",
        "challenge_instructions": "Build a pandas return table, print its shape and describe output, then print Worst equity day.",
        "starter_code": "import pandas as pd\n\n# Build a DataFrame with equity_return, bond_return, and cash_return.\n\n# Print shape, describe(), and Worst equity day.",
        "tests": [{"type": "code_contains", "value": "pd.DataFrame"}, {"type": "output_contains", "value": "Worst equity day"}, {"type": "runs_without_error"}],
        "solution": "import pandas as pd\n\nreturns = pd.DataFrame({\n    \"equity_return\": [0.012, -0.006, 0.018, -0.021, 0.009],\n    \"bond_return\": [0.002, 0.001, -0.003, 0.004, -0.001],\n    \"cash_return\": [0.0001] * 5,\n})\nprint(returns.shape)\nprint(returns.describe())\nprint(f\"Worst equity day: {returns['equity_return'].min():.2%}\")",
    },
    {
        "id": "casfd-l3",
        "label": "Descriptive Statistics",
        "title": "Center, Spread, Quantiles, And Outliers",
        "order": 3,
        "difficulty": "beginner",
        "metric": "descriptive statistics",
        "function_name": "summarize_returns",
        "output_label": "Median return",
        "context": "A portfolio dashboard needs summary statistics that are more informative than a single average.",
        "decision": "The analyst must decide whether typical return and extreme observations tell the same risk story.",
        "idea": "Mean, median, standard deviation, minimum, maximum, and quantiles summarize different parts of a distribution.",
        "function_code": "def summarize_returns(series):\n    return {\n        \"mean\": series.mean(),\n        \"median\": series.median(),\n        \"p05\": series.quantile(0.05),\n    }",
        "pandas_bridge": "pandas makes center and tail summaries available as Series methods.",
        "pandas_code": "summary = returns[\"portfolio\"].agg([\"mean\", \"median\", \"std\", \"min\", \"max\"])\nprint(summary)",
        "interpretation": "If the mean is higher than the median, large positive observations may be pulling the average upward.",
        "pitfalls": ["Using the mean alone", "Ignoring quantiles when downside risk matters", "Calling an outlier an error without investigation"],
        "purpose": "To describe center, spread, and tails before formal inference",
        "purpose_explanation": "Descriptive statistics are the map of the sample before the analyst generalizes.",
        "overclaim": "The sample mean alone fully describes a return distribution.",
        "overclaim_explanation": "Mean ignores spread, skew, and tail outcomes.",
        "syntax_template": "series.___(0.05)",
        "syntax_answer": "quantile",
        "syntax_explanation": "quantile(0.05) gives the 5th percentile.",
        "good_interpretation": "The summary shows typical return and downside tail evidence, but it remains sample-specific.",
        "limitation": "Descriptive statistics summarize observed data; they do not prove the future distribution.",
        "main_mistake": "Reporting only the mean when the decision is about downside risk",
        "mistake_explanation": "A cautious-user risk decision needs tails and spread, not just average return.",
        "pandas_true_false": "A pandas Series can compute mean, median, standard deviation, and quantiles.",
        "pandas_explanation": "These Series methods are foundational for return analysis.",
        "next_step": "Compare center and tail statistics before choosing a formal risk metric.",
        "worked_description": "Summarize a portfolio return series.",
        "worked_code": "import pandas as pd\n\nportfolio = pd.Series([0.004, -0.006, 0.008, -0.015, 0.005, 0.002])\nprint(f\"Mean return: {portfolio.mean():.2%}\")\nprint(f\"Median return: {portfolio.median():.2%}\")\nprint(f\"5th percentile: {portfolio.quantile(0.05):.2%}\")",
        "worked_explanation": "The median gives a typical observation, while the 5th percentile points toward downside risk.",
        "key_syntax": ["series.mean()", "series.median()", "series.std()", "series.quantile(0.05)"],
        "reference_notes": "Center and spread should be interpreted together.",
        "challenge_instructions": "Create a Series of portfolio returns. Print Mean return, Median return, and 5th percentile.",
        "starter_code": "import pandas as pd\n\nportfolio = pd.Series([0.004, -0.006, 0.008, -0.015, 0.005, 0.002])\n# Print Mean return, Median return, and 5th percentile.",
        "tests": [{"type": "output_contains", "value": "Median return"}, {"type": "output_contains", "value": "5th percentile"}, {"type": "runs_without_error"}],
        "solution": "import pandas as pd\n\nportfolio = pd.Series([0.004, -0.006, 0.008, -0.015, 0.005, 0.002])\nprint(f\"Mean return: {portfolio.mean():.2%}\")\nprint(f\"Median return: {portfolio.median():.2%}\")\nprint(f\"5th percentile: {portfolio.quantile(0.05):.2%}\")",
    },
    {
        "id": "casfd-l4",
        "label": "Probability And Expected Value",
        "title": "Probability, Scenarios, And Expected Return",
        "order": 4,
        "difficulty": "beginner",
        "metric": "expected value",
        "function_name": "expected_return",
        "output_label": "Expected return",
        "context": "A product team compares upside, base, and downside scenarios for a model portfolio.",
        "decision": "The analyst must decide whether scenario-weighted return is attractive enough relative to downside risk.",
        "idea": "Expected value is a probability-weighted average. It links uncertainty to a single planning estimate.",
        "function_code": "def expected_return(probabilities, returns):\n    return sum(p * r for p, r in zip(probabilities, returns))",
        "pandas_bridge": "A scenario table makes probabilities and returns auditable.",
        "pandas_code": "scenarios[\"weighted_return\"] = scenarios[\"probability\"] * scenarios[\"return\"]\nprint(scenarios[\"weighted_return\"].sum())",
        "interpretation": "Expected return is a planning average across scenarios, not the return that must occur.",
        "pitfalls": ["Using probabilities that do not sum to one", "Ignoring the downside scenario", "Treating expected value as a guaranteed outcome"],
        "purpose": "To combine scenario probabilities and returns into one planning estimate",
        "purpose_explanation": "Expected value is a first step in reasoning under uncertainty.",
        "overclaim": "Expected return is the return investors will actually receive.",
        "overclaim_explanation": "Expected value is an average over scenarios; any single outcome can differ.",
        "syntax_template": "sum(p * r for p, r in ___(probabilities, returns))",
        "syntax_answer": "zip",
        "syntax_explanation": "zip pairs each probability with its scenario return.",
        "good_interpretation": "The expected return summarizes scenario-weighted evidence, but the downside scenario still matters.",
        "limitation": "Expected value can hide severe losses if tail outcomes are not examined.",
        "main_mistake": "Forgetting to verify that scenario probabilities sum to one",
        "mistake_explanation": "Invalid probabilities make the expected value meaningless.",
        "pandas_true_false": "A scenario DataFrame can store probabilities, returns, and weighted returns.",
        "pandas_explanation": "This makes the expected-value calculation transparent.",
        "next_step": "Compare expected return with downside loss probability and risk tolerance.",
        "worked_description": "Compute probability-weighted expected return.",
        "worked_code": "probabilities = [0.25, 0.50, 0.25]\nreturns = [-0.08, 0.04, 0.14]\n\ndef expected_return(probabilities, returns):\n    return sum(p * r for p, r in zip(probabilities, returns))\n\nprint(f\"Expected return: {expected_return(probabilities, returns):.2%}\")",
        "worked_explanation": "The expected value summarizes the scenario table, but downside loss remains visible.",
        "key_syntax": ["sum(p * r for p, r in zip(probabilities, returns))", "probabilities must sum to 1", "scenario table"],
        "reference_notes": "Expected value is useful, but risk decisions need tails too.",
        "challenge_instructions": "Define expected_return for three scenarios and print Expected return plus a limitation.",
        "starter_code": "probabilities = [0.25, 0.50, 0.25]\nreturns = [-0.08, 0.04, 0.14]\n\n# Define expected_return and print Expected return.",
        "tests": [{"type": "code_contains", "value": "def expected_return"}, {"type": "output_contains", "value": "Expected return"}, {"type": "runs_without_error"}],
        "solution": "probabilities = [0.25, 0.50, 0.25]\nreturns = [-0.08, 0.04, 0.14]\n\ndef expected_return(probabilities, returns):\n    return sum(p * r for p, r in zip(probabilities, returns))\n\nprint(f\"Expected return: {expected_return(probabilities, returns):.2%}\")\nprint(\"Limitation: Expected return does not remove downside scenario risk.\")",
    },
    {
        "id": "casfd-l5",
        "label": "Random Variables",
        "title": "Random Variables And Simulated Portfolio Outcomes",
        "order": 5,
        "difficulty": "beginner",
        "metric": "simulated loss probability",
        "function_name": "loss_probability",
        "output_label": "Loss probability",
        "context": "The team wants to estimate how often a portfolio might lose money under a simple simulated return model.",
        "decision": "The analyst must decide whether simulated losses are frequent enough to justify more investigation.",
        "idea": "A random variable maps uncertain outcomes to numbers. Simulation gives a beginner-readable way to see many possible returns.",
        "function_code": "def loss_probability(simulated_returns):\n    return (simulated_returns < 0).mean()",
        "pandas_bridge": "Simulation outputs can be placed in a Series so the same descriptive tools apply.",
        "pandas_code": "simulated = pd.Series(rng.normal(0.004, 0.018, size=1000))\nprint((simulated < 0).mean())",
        "interpretation": "A simulated loss probability is model-based evidence, not an observed historical frequency.",
        "pitfalls": ["Forgetting to set a random seed for reproducibility", "Treating simulated output as fact", "Using unrealistic mean or volatility assumptions"],
        "purpose": "To connect uncertainty, repeated outcomes, and probability using code",
        "purpose_explanation": "Simulation helps learners see distributions before formal probability notation becomes heavy.",
        "overclaim": "A simulation proves the exact future loss probability.",
        "overclaim_explanation": "Simulation depends on model assumptions and random sampling.",
        "syntax_template": "(simulated_returns < 0).___()",
        "syntax_answer": "mean",
        "syntax_explanation": "The mean of True/False values gives the proportion True.",
        "good_interpretation": "The simulated loss probability estimates downside frequency under the chosen assumptions.",
        "limitation": "The result depends on the assumed distribution, mean, volatility, and seed.",
        "main_mistake": "Using simulation assumptions without naming them",
        "mistake_explanation": "Unstated assumptions make model-based evidence look more certain than it is.",
        "pandas_true_false": "A boolean Series such as simulated < 0 can be averaged to estimate a proportion.",
        "pandas_explanation": "In Python, True behaves like 1 and False behaves like 0 for the mean.",
        "next_step": "Stress-test the assumptions by changing mean, volatility, and distribution shape.",
        "worked_description": "Simulate returns and estimate the probability of loss.",
        "worked_code": "import numpy as np\nimport pandas as pd\n\nrng = np.random.default_rng(7)\nsimulated = pd.Series(rng.normal(0.004, 0.018, size=1000))\nprint(f\"Simulated mean: {simulated.mean():.2%}\")\nprint(f\"Loss probability: {(simulated < 0).mean():.2%}\")",
        "worked_explanation": "The code creates many possible returns and counts the share below zero.",
        "key_syntax": ["np.random.default_rng(7)", "rng.normal(mean, std, size=1000)", "(series < 0).mean()"],
        "reference_notes": "Simulation is transparent only when assumptions are stated.",
        "challenge_instructions": "Simulate 1000 returns with a fixed seed and print Loss probability.",
        "starter_code": "import numpy as np\nimport pandas as pd\n\nrng = np.random.default_rng(7)\n# Simulate returns and print Loss probability.",
        "tests": [{"type": "code_contains", "value": "default_rng"}, {"type": "output_contains", "value": "Loss probability"}, {"type": "runs_without_error"}],
        "solution": "import numpy as np\nimport pandas as pd\n\nrng = np.random.default_rng(7)\nsimulated = pd.Series(rng.normal(0.004, 0.018, size=1000))\nprint(f\"Loss probability: {(simulated < 0).mean():.2%}\")\nprint(\"Limitation: This probability depends on the simulated normal-return assumptions.\")",
    },
]


LESSON_SPECS.extend([
    {
        "id": "casfd-l6",
        "label": "Sampling And Standard Error",
        "title": "Sampling, Standard Error, And Estimate Stability",
        "order": 6,
        "difficulty": "intermediate",
        "metric": "standard error",
        "function_name": "standard_error",
        "output_label": "Standard error",
        "context": "A short return history gives an average return, but the team needs to know how unstable that estimate may be.",
        "decision": "The analyst must decide whether the sample mean is precise enough to communicate.",
        "idea": "Standard error estimates how much a sample mean tends to vary across repeated samples.",
        "function_code": "def standard_error(series):\n    return series.std() / (len(series) ** 0.5)",
        "pandas_bridge": "pandas supplies sample standard deviation and length; Python supplies the square root through exponentiation.",
        "pandas_code": "se = returns[\"portfolio\"].std() / (len(returns) ** 0.5)\nprint(se)",
        "interpretation": "A larger standard error means the mean estimate is less precise.",
        "pitfalls": ["Confusing standard deviation with standard error", "Ignoring sample size", "Treating small-sample estimates as stable"],
        "purpose": "To measure uncertainty around a sample mean estimate",
        "purpose_explanation": "Standard error is the bridge from descriptive statistics to inference.",
        "overclaim": "A small sample mean is stable just because it has been computed correctly.",
        "overclaim_explanation": "A small sample can produce a fragile estimate even when code is correct.",
        "syntax_template": "series.std() / (len(series) ___ 0.5)",
        "syntax_answer": "**",
        "syntax_explanation": "Python uses ** for exponentiation.",
        "good_interpretation": "The standard error communicates precision of the estimated mean return.",
        "limitation": "The formula relies on the sample and does not fix biased or nonrepresentative data.",
        "main_mistake": "Calling standard error the volatility of individual returns",
        "mistake_explanation": "Volatility describes observations; standard error describes the estimate of the mean.",
        "pandas_true_false": "len(series) is needed because estimate precision depends on sample size.",
        "pandas_explanation": "More observations generally reduce standard error.",
        "next_step": "Use the standard error to build a confidence interval.",
        "worked_description": "Compute standard error for daily portfolio returns.",
        "worked_code": "import pandas as pd\n\nportfolio = pd.Series([0.004, -0.006, 0.008, -0.003, 0.005, -0.002])\n\ndef standard_error(series):\n    return series.std() / (len(series) ** 0.5)\n\nprint(f\"Standard error: {standard_error(portfolio):.2%}\")",
        "worked_explanation": "The standard error is smaller than daily volatility because it is uncertainty around the mean.",
        "key_syntax": ["series.std()", "len(series)", "std / sqrt(n)"],
        "reference_notes": "Standard error prepares the learner for confidence intervals and hypothesis tests.",
        "challenge_instructions": "Define standard_error for a return Series and print Standard error.",
        "starter_code": "import pandas as pd\n\nportfolio = pd.Series([0.004, -0.006, 0.008, -0.003, 0.005, -0.002])\n# Define standard_error and print Standard error.",
        "tests": [{"type": "code_contains", "value": "def standard_error"}, {"type": "output_contains", "value": "Standard error"}, {"type": "runs_without_error"}],
        "solution": "import pandas as pd\n\nportfolio = pd.Series([0.004, -0.006, 0.008, -0.003, 0.005, -0.002])\n\ndef standard_error(series):\n    return series.std() / (len(series) ** 0.5)\n\nprint(f\"Standard error: {standard_error(portfolio):.2%}\")",
    },
    {
        "id": "casfd-l7",
        "label": "Confidence Intervals",
        "title": "Confidence Intervals For Mean Return",
        "order": 7,
        "difficulty": "intermediate",
        "metric": "confidence interval",
        "function_name": "mean_confidence_interval",
        "output_label": "Return interval",
        "context": "A risk committee wants a range, not just one average return estimate.",
        "decision": "The analyst must decide whether the average return estimate is precise enough to support action.",
        "idea": "A confidence interval wraps an estimate with a margin of error so uncertainty is visible.",
        "function_code": "def mean_confidence_interval(series):\n    mean = series.mean()\n    se = series.std() / (len(series) ** 0.5)\n    margin = 1.96 * se\n    return mean - margin, mean + margin",
        "pandas_bridge": "The interval uses pandas mean and standard deviation, then Python arithmetic for the margin.",
        "pandas_code": "low, high = mean_confidence_interval(returns[\"portfolio\"])\nprint(low, high)",
        "interpretation": "The interval is a plausible range for the mean under assumptions; it is not a guarantee about every future return.",
        "pitfalls": ["Saying the interval guarantees the next return", "Ignoring assumptions", "Reporting only the midpoint"],
        "purpose": "To communicate uncertainty around an estimated mean return",
        "purpose_explanation": "Intervals make estimate uncertainty visible to decision-makers.",
        "overclaim": "A confidence interval guarantees that the next daily return will fall inside the range.",
        "overclaim_explanation": "The interval describes uncertainty around the estimated mean, not a guarantee for individual outcomes.",
        "syntax_template": "margin = 1.96 * ___",
        "syntax_answer": "se",
        "syntax_explanation": "The margin of error multiplies standard error by a critical value.",
        "good_interpretation": "The interval gives a plausible range for mean return under the approximation used.",
        "limitation": "Small samples and non-normal returns can make the simple interval fragile.",
        "main_mistake": "Explaining the interval as a prediction range for the next return",
        "mistake_explanation": "A confidence interval for the mean is not the same as a prediction interval.",
        "pandas_true_false": "The interval calculation can be built from Series mean, standard deviation, and length.",
        "pandas_explanation": "Those are the needed ingredients for the beginner normal-approximation interval.",
        "next_step": "Check whether the interval includes zero and decide how cautious the claim should be.",
        "worked_description": "Compute a confidence interval for mean daily return.",
        "worked_code": "import pandas as pd\n\nportfolio = pd.Series([0.004, -0.006, 0.008, -0.003, 0.005, -0.002, 0.006, 0.001])\n\ndef mean_confidence_interval(series):\n    mean = series.mean()\n    se = series.std() / (len(series) ** 0.5)\n    margin = 1.96 * se\n    return mean - margin, mean + margin\n\nlow, high = mean_confidence_interval(portfolio)\nprint(f\"Return interval: {low:.2%} to {high:.2%}\")",
        "worked_explanation": "The output presents a range, making uncertainty more honest than a single average.",
        "key_syntax": ["mean = series.mean()", "se = series.std() / sqrt(n)", "margin = 1.96 * se"],
        "reference_notes": "Later modules can replace the normal approximation with t intervals or bootstraps.",
        "challenge_instructions": "Define mean_confidence_interval and print Return interval.",
        "starter_code": "import pandas as pd\n\nportfolio = pd.Series([0.004, -0.006, 0.008, -0.003, 0.005, -0.002, 0.006, 0.001])\n# Define mean_confidence_interval and print Return interval.",
        "tests": [{"type": "code_contains", "value": "mean_confidence_interval"}, {"type": "output_contains", "value": "Return interval"}, {"type": "runs_without_error"}],
        "solution": "import pandas as pd\n\nportfolio = pd.Series([0.004, -0.006, 0.008, -0.003, 0.005, -0.002, 0.006, 0.001])\n\ndef mean_confidence_interval(series):\n    mean = series.mean()\n    se = series.std() / (len(series) ** 0.5)\n    margin = 1.96 * se\n    return mean - margin, mean + margin\n\nlow, high = mean_confidence_interval(portfolio)\nprint(f\"Return interval: {low:.2%} to {high:.2%}\")",
    },
])


ADDITIONAL_SPECS = [
    ("casfd-l8", "Hypothesis Tests", "Hypothesis Testing For Portfolio Decisions", "intermediate", "hypothesis test decision", "test_mean_against_zero", "Test decision"),
    ("casfd-l9", "P Values", "P-Values, Significance, And Practical Importance", "intermediate", "p-value decision", "evaluate_p_value", "P-value decision"),
    ("casfd-l10", "Volatility", "Volatility And Annualized Standard Deviation", "intermediate", "annualized volatility", "annualized_volatility", "Annualized volatility"),
    ("casfd-l11", "Drawdown", "Drawdown, Downside Risk, And Investor Pain", "intermediate", "maximum drawdown", "max_drawdown", "Maximum drawdown"),
    ("casfd-l12", "Correlation", "Correlation, Covariance, And Diversification", "intermediate", "correlation", "asset_correlation", "Equity bond correlation"),
    ("casfd-l13", "Portfolio Metrics", "Weights, Portfolio Return, Volatility, And Sharpe Ratio", "intermediate", "portfolio metrics", "portfolio_metrics", "Portfolio volatility"),
    ("casfd-l14", "Normal Model", "Z-Scores, Normal Approximation, And Tail Checks", "intermediate", "z-score", "z_score", "Worst day z-score"),
    ("casfd-l15", "VaR And CVaR", "Historical Value At Risk And Conditional Value At Risk", "advanced", "VaR and CVaR", "historical_var_cvar", "Historical VaR"),
    ("casfd-l16", "Regression Beta", "Regression Foundations: Market Beta", "advanced", "market beta", "market_beta", "Market beta"),
    ("casfd-l17", "Diagnostics", "Residuals, R-Squared, And Model Assumptions", "advanced", "model diagnostics", "diagnose_model", "Model RMSE"),
    ("casfd-l18", "SQL Pipeline", "SQL-To-pandas Risk Pipeline", "intermediate", "SQL risk pipeline", "load_portfolio_returns", "SQL average return"),
    ("casfd-l19", "A/B Testing", "A/B Testing For Fintech Product Decisions", "advanced", "A/B test difference", "conversion_difference", "Conversion difference"),
    ("casfd-capstone", "Capstone Memo", "Capstone: Portfolio Risk Memo Plus Notebook", "advanced", "capstone risk memo", "portfolio_risk_memo", "Recommendation"),
]


def _additional_spec(item, order):
    lesson_id, label, title, difficulty, metric, function_name, output_label = item
    base_series = "pd.Series([0.012, -0.006, 0.018, -0.021, 0.009, -0.004, 0.006, -0.011])"
    templates = {
        "test_mean_against_zero": {
            "idea": "A hypothesis test compares sample evidence against a baseline claim. In finance, the baseline may be that mean return is zero.",
            "function_code": "def test_mean_against_zero(series):\n    se = series.std() / (len(series) ** 0.5)\n    z = series.mean() / se\n    return z",
            "pandas_code": f"returns = {base_series}\nz_stat = test_mean_against_zero(returns)",
            "syntax_template": "z = series.mean() / ___",
            "syntax_answer": "se",
            "solution": "import pandas as pd\n\nreturns = pd.Series([0.012, -0.006, 0.018, -0.021, 0.009, -0.004, 0.006, -0.011])\n\ndef test_mean_against_zero(series):\n    se = series.std() / (len(series) ** 0.5)\n    return series.mean() / se\n\nz_stat = test_mean_against_zero(returns)\nprint(f\"Test decision: z-statistic is {z_stat:.2f}; evidence is preliminary, not conclusive.\")",
        },
        "evaluate_p_value": {
            "idea": "A p-value measures how surprising the observed evidence would be if the null hypothesis were true.",
            "function_code": "def evaluate_p_value(p_value, alpha=0.05):\n    return \"statistically significant\" if p_value < alpha else \"not statistically significant\"",
            "pandas_code": "decision = evaluate_p_value(0.08, alpha=0.05)\nprint(decision)",
            "syntax_template": "p_value ___ alpha",
            "syntax_answer": "<",
            "solution": "def evaluate_p_value(p_value, alpha=0.05):\n    return \"statistically significant\" if p_value < alpha else \"not statistically significant\"\n\nprint(f\"P-value decision: {evaluate_p_value(0.08)} at alpha 0.05\")\nprint(\"Limitation: statistical significance is not the same as economic importance.\")",
        },
        "annualized_volatility": {
            "idea": "Volatility uses standard deviation to describe how much returns move around their average.",
            "function_code": "def annualized_volatility(series, trading_days=252):\n    return series.std() * (trading_days ** 0.5)",
            "pandas_code": f"returns = {base_series}\nprint(annualized_volatility(returns))",
            "syntax_template": "series.std() * (252 ___ 0.5)",
            "syntax_answer": "**",
            "solution": "import pandas as pd\n\nreturns = pd.Series([0.012, -0.006, 0.018, -0.021, 0.009, -0.004, 0.006, -0.011])\n\ndef annualized_volatility(series, trading_days=252):\n    return series.std() * (trading_days ** 0.5)\n\nprint(f\"Annualized volatility: {annualized_volatility(returns):.2%}\")",
        },
        "max_drawdown": {
            "idea": "Drawdown measures the decline from a previous peak. It captures investor pain that volatility can hide.",
            "function_code": "def max_drawdown(returns):\n    wealth = (1 + returns).cumprod()\n    drawdown = wealth / wealth.cummax() - 1\n    return drawdown.min()",
            "pandas_code": f"returns = {base_series}\nprint(max_drawdown(returns))",
            "syntax_template": "wealth / wealth.___() - 1",
            "syntax_answer": "cummax",
            "solution": "import pandas as pd\n\nreturns = pd.Series([0.012, -0.006, 0.018, -0.021, 0.009, -0.004, 0.006, -0.011])\n\ndef max_drawdown(returns):\n    wealth = (1 + returns).cumprod()\n    drawdown = wealth / wealth.cummax() - 1\n    return drawdown.min()\n\nprint(f\"Maximum drawdown: {max_drawdown(returns):.2%}\")",
        },
        "asset_correlation": {
            "idea": "Correlation describes how two return series move together. Diversification weakens when correlations rise.",
            "function_code": "def asset_correlation(frame, left, right):\n    return frame[left].corr(frame[right])",
            "pandas_code": "corr = returns[\"equity\"].corr(returns[\"bond\"])\nprint(corr)",
            "syntax_template": "frame[left].___(frame[right])",
            "syntax_answer": "corr",
            "solution": "import pandas as pd\n\nreturns = pd.DataFrame({\"equity\": [0.012, -0.006, 0.018, -0.021, 0.009], \"bond\": [0.002, 0.001, -0.003, 0.004, -0.001]})\n\ndef asset_correlation(frame, left, right):\n    return frame[left].corr(frame[right])\n\nprint(f\"Equity bond correlation: {asset_correlation(returns, 'equity', 'bond'):.2f}\")",
        },
        "portfolio_metrics": {
            "idea": "Portfolio metrics combine asset returns with weights to estimate portfolio return, volatility, and risk-adjusted return.",
            "function_code": "def portfolio_metrics(frame, weights):\n    portfolio = frame @ weights\n    return portfolio.mean(), portfolio.std() * (252 ** 0.5)",
            "pandas_code": "portfolio = returns @ weights\nprint(portfolio.mean(), portfolio.std())",
            "syntax_template": "portfolio = frame ___ weights",
            "syntax_answer": "@",
            "solution": "import numpy as np\nimport pandas as pd\n\nreturns = pd.DataFrame({\"equity\": [0.012, -0.006, 0.018, -0.021], \"bond\": [0.002, 0.001, -0.003, 0.004], \"cash\": [0.0001] * 4})\nweights = np.array([0.60, 0.30, 0.10])\n\ndef portfolio_metrics(frame, weights):\n    portfolio = frame @ weights\n    return portfolio.mean(), portfolio.std() * (252 ** 0.5)\n\nmean_return, vol = portfolio_metrics(returns, weights)\nprint(f\"Portfolio volatility: {vol:.2%}\")\nprint(f\"Mean daily return: {mean_return:.2%}\")",
        },
        "z_score": {
            "idea": "A z-score expresses how many standard deviations an observation is from the mean.",
            "function_code": "def z_score(value, mean, std):\n    return (value - mean) / std",
            "pandas_code": f"returns = {base_series}\nprint(z_score(returns.min(), returns.mean(), returns.std()))",
            "syntax_template": "(value - mean) / ___",
            "syntax_answer": "std",
            "solution": "import pandas as pd\n\nreturns = pd.Series([0.012, -0.006, 0.018, -0.021, 0.009, -0.004, 0.006, -0.011])\n\ndef z_score(value, mean, std):\n    return (value - mean) / std\n\nworst_z = z_score(returns.min(), returns.mean(), returns.std())\nprint(f\"Worst day z-score: {worst_z:.2f}\")",
        },
        "historical_var_cvar": {
            "idea": "Historical VaR estimates a loss threshold; CVaR averages losses beyond that threshold.",
            "function_code": "def historical_var_cvar(series, level=0.05):\n    var = series.quantile(level)\n    cvar = series[series <= var].mean()\n    return var, cvar",
            "pandas_code": f"returns = {base_series}\nprint(historical_var_cvar(returns))",
            "syntax_template": "series.___(0.05)",
            "syntax_answer": "quantile",
            "solution": "import pandas as pd\n\nreturns = pd.Series([0.012, -0.006, 0.018, -0.021, 0.009, -0.004, 0.006, -0.011, -0.028, 0.014])\n\ndef historical_var_cvar(series, level=0.05):\n    var = series.quantile(level)\n    cvar = series[series <= var].mean()\n    return var, cvar\n\nvar, cvar = historical_var_cvar(returns)\nprint(f\"Historical VaR: {var:.2%}\")\nprint(f\"Historical CVaR: {cvar:.2%}\")",
        },
        "market_beta": {
            "idea": "Beta estimates sensitivity of portfolio returns to market returns using covariance divided by market variance.",
            "function_code": "def market_beta(portfolio, market):\n    return portfolio.cov(market) / market.var()",
            "pandas_code": "beta = portfolio.cov(market) / market.var()\nprint(beta)",
            "syntax_template": "portfolio.cov(market) / market.___()",
            "syntax_answer": "var",
            "solution": "import pandas as pd\n\nportfolio = pd.Series([0.010, -0.005, 0.014, -0.018, 0.008])\nmarket = pd.Series([0.008, -0.004, 0.012, -0.015, 0.006])\n\ndef market_beta(portfolio, market):\n    return portfolio.cov(market) / market.var()\n\nprint(f\"Market beta: {market_beta(portfolio, market):.2f}\")",
        },
        "diagnose_model": {
            "idea": "Diagnostics examine residuals so a model is not judged only by fitted values.",
            "function_code": "def diagnose_model(actual, predicted):\n    residuals = actual - predicted\n    rmse = (residuals.pow(2).mean()) ** 0.5\n    return residuals.mean(), rmse",
            "pandas_code": "residuals = actual - predicted\nprint(residuals.mean())",
            "syntax_template": "residuals = actual ___ predicted",
            "syntax_answer": "-",
            "solution": "import pandas as pd\n\nactual = pd.Series([0.010, -0.006, 0.012, -0.015, 0.007])\npredicted = pd.Series([0.008, -0.004, 0.010, -0.012, 0.006])\n\ndef diagnose_model(actual, predicted):\n    residuals = actual - predicted\n    rmse = (residuals.pow(2).mean()) ** 0.5\n    return residuals.mean(), rmse\n\nmean_error, rmse = diagnose_model(actual, predicted)\nprint(f\"Model RMSE: {rmse:.2%}\")\nprint(f\"Mean error: {mean_error:.2%}\")",
        },
        "load_portfolio_returns": {
            "idea": "SQL retrieves the correct rows; pandas performs the statistical summary. The tools have different jobs.",
            "function_code": "def load_portfolio_returns(conn):\n    query = \"SELECT day, daily_return FROM returns WHERE asset = 'portfolio'\"\n    return pd.read_sql_query(query, conn)",
            "pandas_code": "portfolio = pd.read_sql_query(query, conn)\nprint(portfolio[\"daily_return\"].mean())",
            "syntax_template": "SELECT day, daily_return FROM returns ___ asset = 'portfolio'",
            "syntax_answer": "WHERE",
            "solution": "import sqlite3\nimport pandas as pd\n\nconn = sqlite3.connect(\":memory:\")\nconn.execute(\"CREATE TABLE returns (asset TEXT, day TEXT, daily_return REAL)\")\nconn.executemany(\"INSERT INTO returns VALUES (?, ?, ?)\", [(\"portfolio\", \"2026-01-01\", 0.004), (\"portfolio\", \"2026-01-02\", -0.006), (\"portfolio\", \"2026-01-03\", 0.008)])\n\ndef load_portfolio_returns(conn):\n    query = \"SELECT day, daily_return FROM returns WHERE asset = 'portfolio'\"\n    return pd.read_sql_query(query, conn)\n\nportfolio = load_portfolio_returns(conn)\nprint(f\"SQL average return: {portfolio['daily_return'].mean():.2%}\")",
        },
        "conversion_difference": {
            "idea": "An A/B test compares conversion rates between product variants while accounting for sample size.",
            "function_code": "def conversion_difference(control_rate, treatment_rate):\n    return treatment_rate - control_rate",
            "pandas_code": "summary[\"conversion_rate\"] = summary[\"conversions\"] / summary[\"visitors\"]",
            "syntax_template": "treatment_rate ___ control_rate",
            "syntax_answer": "-",
            "solution": "def conversion_difference(control_rate, treatment_rate):\n    return treatment_rate - control_rate\n\ncontrol_rate = 92 / 1000\ntreatment_rate = 118 / 1000\nlift = conversion_difference(control_rate, treatment_rate)\nprint(f\"Conversion difference: {lift:.2%}\")\nprint(\"Limitation: Check statistical and practical significance before shipping.\")",
        },
        "portfolio_risk_memo": {
            "idea": "The capstone combines return, volatility, drawdown, VaR, and interpretation into a memo-plus-notebook deliverable.",
            "function_code": "def portfolio_risk_memo(volatility, drawdown, var):\n    return f\"Recommendation: review risk; vol={volatility:.2%}, drawdown={drawdown:.2%}, var={var:.2%}\"",
            "pandas_code": "memo = portfolio_risk_memo(volatility, drawdown, var)\nprint(memo)",
            "syntax_template": "print(\"___: review risk\")",
            "syntax_answer": "Recommendation",
            "solution": "import pandas as pd\n\nreturns = pd.Series([0.012, -0.006, 0.018, -0.021, 0.009, -0.004, 0.006, -0.011, -0.028, 0.014])\n\ndef annualized_volatility(series):\n    return series.std() * (252 ** 0.5)\n\ndef max_drawdown(series):\n    wealth = (1 + series).cumprod()\n    return (wealth / wealth.cummax() - 1).min()\n\ndef historical_var(series, level=0.05):\n    return series.quantile(level)\n\ndef portfolio_risk_memo(volatility, drawdown, var):\n    return (\n        \"Recommendation: Keep the portfolio under review for cautious users and request \"\n        \"a longer return history before approving it as a default. \"\n        f\"Volatility is {volatility:.2%}, maximum drawdown is {drawdown:.2%}, \"\n        f\"and historical VaR is {var:.2%}.\"\n    )\n\nvolatility = annualized_volatility(returns)\ndrawdown = max_drawdown(returns)\nvar = historical_var(returns)\nprint(f\"Annualized volatility: {volatility:.2%}\")\nprint(f\"Maximum drawdown: {drawdown:.2%}\")\nprint(f\"Historical VaR: {var:.2%}\")\nprint(portfolio_risk_memo(volatility, drawdown, var))",
        },
    }
    tpl = templates[function_name]
    return {
        "id": lesson_id,
        "label": label,
        "title": title,
        "order": order,
        "duration_min": 60 if lesson_id != "casfd-capstone" else 90,
        "difficulty": difficulty,
        "is_capstone": lesson_id == "casfd-capstone",
        "metric": metric,
        "function_name": function_name,
        "output_label": output_label,
        "context": f"A fintech analytics team needs {metric} evidence for a portfolio or product-risk decision.",
        "decision": f"The analyst must decide how {metric} should influence a risk committee recommendation.",
        "idea": tpl["idea"],
        "function_code": tpl["function_code"],
        "pandas_bridge": "The calculation becomes graduate-ready when it can be repeated across a pandas Series or DataFrame and then explained clearly.",
        "pandas_code": tpl["pandas_code"],
        "interpretation": f"{metric.title()} is evidence for the decision, but it must be paired with assumptions, sample size, and practical importance.",
        "pitfalls": ["Reporting the number without a decision frame", "Treating statistical output as a guarantee", "Skipping assumptions and sample-size limits"],
        "purpose": f"To use {metric} as disciplined evidence in a fintech decision",
        "purpose_explanation": f"{metric.title()} turns raw observations into a statistic that can be discussed with a risk committee.",
        "overclaim": f"{metric.title()} proves the correct business decision without judgment or context.",
        "overclaim_explanation": "Statistics support decisions; they do not remove assumptions, tradeoffs, or accountability.",
        "syntax_template": tpl["syntax_template"],
        "syntax_answer": tpl["syntax_answer"],
        "syntax_explanation": "This is the key operator or method needed for the lesson calculation.",
        "good_interpretation": f"{metric.title()} provides evidence for the risk decision while leaving room for assumptions and limitations.",
        "limitation": "The result depends on sample quality, assumptions, and the business threshold chosen.",
        "main_mistake": "Skipping the limitation sentence after computing the result",
        "mistake_explanation": "Graduate-level analytics requires both computation and defensible interpretation.",
        "pandas_true_false": "pandas helps repeat this calculation across return observations or summarized groups.",
        "pandas_explanation": "The app's Python-first pattern scales into pandas once the formula is understood.",
        "next_step": "Compare the statistic with a benchmark, threshold, or alternative portfolio.",
        "worked_description": f"Compute {metric} and turn it into a short analyst statement.",
        "worked_code": tpl["solution"],
        "worked_explanation": f"The example shows how {metric} becomes a labeled result for a memo or notebook.",
        "key_syntax": [function_name, tpl["syntax_template"], output_label],
        "reference_notes": "Keep the calculation reproducible and the interpretation appropriately cautious.",
        "challenge_instructions": f"Write the {function_name} calculation and print a line beginning with {output_label}.",
        "starter_code": f"# Build the data, define {function_name}, and print {output_label}.\n",
        "tests": [{"type": "code_contains", "value": function_name}, {"type": "output_contains", "value": output_label}, {"type": "runs_without_error"}],
        "solution": tpl["solution"],
    }


for index, item in enumerate(ADDITIONAL_SPECS, start=8):
    LESSON_SPECS.append(_additional_spec(item, index))


LESSONS = [_build_lesson(spec) for spec in LESSON_SPECS]

MODULE_CORE_ANALYTICS_STATISTICS = {
    "id": "core-analytics-statistics",
    "title": "Graduate Statistics For Financial Analysis",
    "description": (
        "A code-heavy graduate statistics module for financial analysis. Lesson 1 has "
        "been rebuilt around textbook-style statistical foundations, formal notation, "
        "numpy, pandas, and generic financial datasets."
    ),
    "course": "Core Analytics - WashU MSBA FinTech Prep",
    "order": 1,
    "locked": False,
    "supplementary_courses": [],
    "concept_map": [
        {
            "id": spec["id"],
            "label": spec["label"],
            "connects_to": [LESSON_SPECS[i + 1]["id"]] if i + 1 < len(LESSON_SPECS) else [],
        }
        for i, spec in enumerate(LESSON_SPECS)
    ],
    "lessons": LESSONS,
}


LESSON_1_REBUILD = {
    "id": "casfd-l1",
    "title": "Statistical Data In Python: Observations, Variables, Samples, And Financial Datasets",
    "order": 1,
    "duration_min": 90,
    "difficulty": "beginner",
    "real_world_context": (
        "You are given a small generic financial dataset where each row is one "
        "company-quarter observation. Before regression, probability, hypothesis "
        "testing, or machine learning can be meaningful, you must know exactly what "
        "the observations are, which variables are measured, what belongs in a feature "
        "matrix, what belongs in a response vector, and how the first statistics are "
        "computed from the raw columns."
    ),
    "concept": """## Textbook Aim

This lesson is the foundation for the entire statistics module. It teaches how a
financial dataset becomes statistical objects in Python:

1. observations
2. variables
3. samples and populations
4. vectors
5. matrices
6. summary statistics
7. feature matrix `X`
8. response vector `y`

The goal is not to "look at data" casually. The goal is to build the mental model that
graduate statistics uses constantly:

```text
raw financial dataset -> sample -> variables -> vectors -> matrix X -> response y -> model
```

In later lessons you will estimate variance, probability models, confidence intervals,
hypothesis tests, regressions, GLMs, PCA, clustering, and time series models. Every one
of those methods starts with the same question:

```text
What are the observations, and what variables were measured on each observation?
```

## Source Anchors For This Lesson

This rebuild uses open textbook patterns from:

- OpenIntro Statistics: data basics, numerical summaries, probability, inference, and
  regression structure.
- Think Stats: learning probability and statistics by writing short Python programs.
- An Introduction to Statistical Learning with Python: the habit of pairing concepts
  with Python labs.
- The Elements of Statistical Learning: the long-run target of prediction, inference,
  and model-based analysis.

You do not need to read those books before this lesson. They are the design standard:
formal statistics, code, and applied data should move together.

## 1. Build A Financial Dataset First

Start with code. Then attach the math.

```python
import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["A", "B", "C", "D", "E", "F", "G", "H"],
    "quarter": ["2026Q1"] * 8,
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01, 0.14, 0.04],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35, 0.52, 0.40],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47, 0.22, 0.36],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02, 0.15, 0.05],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34, 0.53, 0.41],
})

print(financials)
```

This is a **sample** of financial observations. It is not "the market." It is not
"all companies." It is the dataset currently available for analysis.

A graduate statistics course will ask you to distinguish:

```text
population: the full set of units you want to understand
sample: the observed subset you actually have
observation: one row, one measured unit
variable: one column, one measured attribute
```

Here:

- Population: all comparable company-quarter observations you care about.
- Sample: the 8 company-quarter rows in `financials`.
- Observation: one company in one quarter.
- Variables: revenue growth, gross margin, debt-to-assets, free cash flow margin, and
  next-quarter margin.

That vocabulary matters because statistical conclusions are always about moving from a
sample toward a population claim.

## 2. Observation Count And Variable Count

The first mathematical object is the sample size:

```text
n = number of observations
```

In pandas:

```python
n_observations = len(financials)
print("Observation count:", n_observations)
```

The second object is the number of statistical variables you are going to analyze:

```python
numeric_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
    "next_quarter_margin",
]

p_variables = len(numeric_columns)
print("Variable count:", p_variables)
```

Do not count `company` as a statistical variable for this lesson. It is an identifier.
It tells us which row is which. It is not a measured numeric attribute for computing a
mean, variance, covariance, or regression coefficient.

Do not count `quarter` as a numeric variable here either. It is a time label. Later, in
time series, time labels become essential. In this lesson, we are learning the core
statistical structure first.

## 3. A Column Is A Vector

Take one variable:

```python
revenue_growth = financials["revenue_growth"].to_numpy()
print(revenue_growth)
```

Mathematically, this column is a vector:

```text
x = (x_1, x_2, ..., x_n)
```

For the revenue growth column:

```text
x_1 = 0.08
x_2 = 0.03
x_3 = 0.11
...
x_8 = 0.04
```

The subscript `i` means "which observation." So `x_i` is the value of variable `x` for
observation `i`.

This is the first major bridge:

```text
pandas Series/DataFrame column <-> statistical vector
```

Once you understand that bridge, formulas stop feeling abstract. A formula is usually
just an operation over a vector.

## 4. Mean From First Principles

The sample mean is:

```text
x_bar = (1 / n) * sum_{i=1 to n} x_i
```

In words:

1. add every observed value
2. divide by the number of observations

Write it as a Python function before using pandas:

```python
def sample_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

mean_growth = sample_mean(revenue_growth)
print("Mean revenue growth:", mean_growth)
print("Mean revenue growth, pandas check:", financials["revenue_growth"].mean())
```

This is code-first mathematics. The formula and the code are the same idea:

```text
values.sum()          -> sum of x_i
len(values)           -> n
values.sum() / n      -> x_bar
```

The pandas method `.mean()` is convenient, but you should know what it is doing. Top
of the class means you can use the tool and explain the calculation underneath it.

## 5. Deviations From The Mean

Most statistics begin with deviations:

```text
d_i = x_i - x_bar
```

Each deviation tells how far one observation is from the sample mean.

```python
deviation_vector = revenue_growth - mean_growth
print("Deviation vector:", deviation_vector)
print("Deviation sum:", deviation_vector.sum())
```

The sum of deviations from the sample mean should be approximately zero. It may print a
tiny floating-point number like `-2.7755575615628914e-17`. That is not a statistical
mistake. It is computer arithmetic.

The deviation vector is the raw material for variance, standard deviation, covariance,
correlation, regression residuals, PCA, and many model diagnostics.

## 6. Sample Variance And Why `n - 1` Appears

Variance measures average squared distance from the mean. For a sample:

```text
s^2 = (1 / (n - 1)) * sum_{i=1 to n} (x_i - x_bar)^2
```

The sample standard deviation is:

```text
s = sqrt(s^2)
```

In Python:

```python
def sample_variance(values):
    values = np.asarray(values)
    x_bar = sample_mean(values)
    squared_deviations = (values - x_bar) ** 2
    return squared_deviations.sum() / (len(values) - 1)

variance_growth = sample_variance(revenue_growth)
std_growth = variance_growth ** 0.5

print("Sample variance:", variance_growth)
print("Sample standard deviation:", std_growth)
print("pandas variance check:", financials["revenue_growth"].var(ddof=1))
print("pandas standard deviation check:", financials["revenue_growth"].std(ddof=1))
```

Why `n - 1` instead of `n`?

Because once the sample mean is estimated from the same data, the deviations are not
fully free to vary. If you know `n - 1` deviations, the last deviation is forced by the
fact that deviations sum to zero. This is called **degrees of freedom**.

You do not need to love that explanation yet. But you do need to recognize the pattern:

```text
population variance uses n
sample variance commonly uses n - 1
```

In pandas, `Series.var()` and `Series.std()` use `ddof=1` by default, which gives the
sample version. `ddof` means "delta degrees of freedom."

## 7. Multiple Variables Become A Matrix

Regression and multivariate statistics do not work with one column at a time. They use
matrices.

Choose predictor variables:

```python
feature_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
]

X = financials[feature_columns].to_numpy()
print("Feature matrix shape:", X.shape)
```

Mathematically:

```text
X is an n by p matrix
```

For this dataset:

```text
n = 8 observations
p = 4 predictor variables
X.shape = (8, 4)
```

The response variable is what you want to explain, predict, or model:

```python
y = financials["next_quarter_margin"].to_numpy()
print("Response vector shape:", y.shape)
```

Now you have the basic supervised learning structure:

```text
X -> predictors
y -> response
```

Later regression lessons will use:

```text
y = X beta + epsilon
```

But Lesson 1 is where that notation becomes concrete:

- `y` is a vector with one value per observation.
- `X` is a matrix with one row per observation and one column per predictor.
- `beta` will be a vector of coefficients.
- `epsilon` will be the vector of errors/residuals.

## 8. Data Types Matter

Run:

```python
print(financials.dtypes)
```

You should see numeric columns and non-numeric columns. Statistics depends on type:

- Numeric continuous variables: revenue growth, margins, ratios.
- Identifier variables: company.
- Time labels: quarter.
- Binary variables: later lessons may use indicators such as default, approval, churn,
  or covenant breach.

Do not compute a mean on an identifier. Do not feed a raw company label into regression
as though it were a financial measurement. Do not treat a time label as a normal number
without thinking about time ordering.

## 9. Missingness Is A Statistical Fact, Not A Cleanup Detail

Check missing values:

```python
print(financials.isna().sum())
```

In real financial datasets, missingness can be informative:

- a young company may not have long history
- a private firm may not report every metric
- a distressed company may have delayed statements
- a vendor feed may omit fields

For this lesson, the synthetic data has no missing values. The important habit is to
check.

## 10. Lesson 1 Mental Checklist

Before any statistical model, you should be able to answer:

1. What is one observation?
2. What is the sample?
3. What population would I like to generalize to?
4. Which columns are identifiers?
5. Which columns are numeric variables?
6. Which variable is the response, if any?
7. Which variables are predictors?
8. What is `n`?
9. What is `p`?
10. What is the shape of `X`?
11. What is the shape of `y`?
12. Can I compute the mean and variance of a numeric column from first principles?

That checklist is the doorway to graduate statistics.

## What You Should Be Able To Code After This Lesson

You should be able to write code that:

1. builds a DataFrame
2. counts observations
3. selects numeric variables
4. converts a column to a numpy vector
5. computes a sample mean manually
6. computes a deviation vector
7. computes sample variance manually with `n - 1`
8. checks the result against pandas
9. creates a feature matrix `X`
10. creates a response vector `y`
11. prints the shapes of `X` and `y`
12. checks missing values

This is not optional background. This is the grammar of the course.
""",
    "worked_example": {
        "description": "Build a generic financial dataset and compute the first statistics from raw vectors.",
        "code": """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["A", "B", "C", "D", "E", "F", "G", "H"],
    "quarter": ["2026Q1"] * 8,
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01, 0.14, 0.04],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35, 0.52, 0.40],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47, 0.22, 0.36],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02, 0.15, 0.05],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34, 0.53, 0.41],
})

def sample_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def sample_variance(values):
    values = np.asarray(values)
    mean = sample_mean(values)
    return ((values - mean) ** 2).sum() / (len(values) - 1)

revenue_growth = financials["revenue_growth"].to_numpy()
mean_growth = sample_mean(revenue_growth)
deviation_vector = revenue_growth - mean_growth
variance_growth = sample_variance(revenue_growth)

feature_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
]
X = financials[feature_columns].to_numpy()
y = financials["next_quarter_margin"].to_numpy()

print("Observation count:", len(financials))
print("Variable count:", len(feature_columns) + 1)
print("Mean revenue growth:", round(mean_growth, 4))
print("Deviation vector:", np.round(deviation_vector, 4))
print("Sample variance:", round(variance_growth, 6))
print("Pandas variance check:", round(financials["revenue_growth"].var(ddof=1), 6))
print("Feature matrix shape:", X.shape)
print("Response vector shape:", y.shape)
print("Missing values:", int(financials[feature_columns + ["next_quarter_margin"]].isna().sum().sum()))""",
        "explanation": (
            "The worked example builds the core statistical objects directly: one "
            "sample, numeric variables, one vector, a mean, deviations, sample "
            "variance, a feature matrix X, and a response vector y. This is the "
            "foundation for regression and every later model in the module."
        ),
    },
    "reference": {
        "key_syntax": [
            "financials = pd.DataFrame({...})",
            "n = len(financials)",
            "x = financials['revenue_growth'].to_numpy()",
            "x_bar = values.sum() / len(values)",
            "s_squared = ((values - x_bar) ** 2).sum() / (len(values) - 1)",
            "X = financials[feature_columns].to_numpy()",
            "y = financials['next_quarter_margin'].to_numpy()",
            "financials.isna().sum()",
        ],
        "notes": (
            "Lesson 1 is about converting financial data into statistical objects. "
            "If you can name the observation, sample, variables, X matrix, y vector, "
            "mean, deviations, and sample variance, later models become much easier."
        ),
    },
    "questions": [
        {
            "type": "multiple_choice",
            "question": "In the lesson dataset, what is one observation?",
            "options": [
                "One company-quarter row",
                "The entire DataFrame",
                "Only the revenue_growth column",
                "The formula for sample variance",
            ],
            "answer": 0,
            "explanation": "An observation is one measured unit. Here, each row is one company-quarter.",
        },
        {
            "type": "multiple_choice",
            "question": "Which column is an identifier rather than a numeric statistical variable?",
            "options": ["company", "gross_margin", "debt_to_assets", "revenue_growth"],
            "answer": 0,
            "explanation": "company labels the row. It is not a numeric measurement for mean or variance.",
        },
        {
            "type": "fill_blank",
            "question": "Fill in the function that returns the number of observations.",
            "template": "n_observations = ___(financials)",
            "answer": "len",
            "explanation": "len(financials) returns the number of rows in the DataFrame.",
        },
        {
            "type": "multiple_choice",
            "question": "What does `x_i` mean in the vector x = (x_1, x_2, ..., x_n)?",
            "options": [
                "The value of variable x for observation i",
                "The number of columns in the DataFrame",
                "The name of the response variable",
                "A missing value indicator",
            ],
            "answer": 0,
            "explanation": "The subscript i indexes the observation.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the manual sample mean calculation.",
            "template": "return values.sum() / ___(values)",
            "answer": "len",
            "explanation": "The sample mean divides the sum of observed values by n.",
        },
        {
            "type": "multiple_choice",
            "question": "Which formula represents the sample mean?",
            "options": [
                "x_bar = (1 / n) * sum x_i",
                "s_squared = sum x_i",
                "X = y - beta",
                "n = p - 1",
            ],
            "answer": 0,
            "explanation": "The mean is the sum of values divided by the number of observations.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the deviation vector calculation.",
            "template": "deviation_vector = revenue_growth ___ mean_growth",
            "answer": "-",
            "explanation": "Each deviation subtracts the mean from an observed value.",
        },
        {
            "type": "multiple_choice",
            "question": "Why does sample variance usually divide by n - 1?",
            "options": [
                "Because the sample mean is estimated from the same data, leaving n - 1 degrees of freedom",
                "Because pandas cannot divide by n",
                "Because financial datasets always have one missing column",
                "Because variance must always be negative",
            ],
            "answer": 0,
            "explanation": "Estimating the mean uses one degree of freedom, so the sample variance uses n - 1.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the squared-deviation expression.",
            "template": "squared_deviations = (values - x_bar) ___ 2",
            "answer": "**",
            "explanation": "Python uses ** for exponentiation.",
        },
        {
            "type": "multiple_choice",
            "question": "In supervised statistical modeling, what is X?",
            "options": [
                "The feature matrix of predictor variables",
                "The final written recommendation",
                "The company identifier column only",
                "The sample variance of y",
            ],
            "answer": 0,
            "explanation": "X is the matrix of predictor variables, with rows as observations and columns as features.",
        },
        {
            "type": "multiple_choice",
            "question": "In supervised statistical modeling, what is y?",
            "options": [
                "The response vector",
                "The list of predictor column names",
                "The number of rows",
                "The missing-value count",
            ],
            "answer": 0,
            "explanation": "y is the vector containing the outcome or response value for each observation.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the pandas-to-numpy feature matrix conversion.",
            "template": "X = financials[feature_columns].___()",
            "answer": "to_numpy",
            "explanation": "to_numpy() converts selected DataFrame columns into a numpy matrix.",
        },
        {
            "type": "true_false",
            "question": "A DataFrame can contain both statistical variables and non-statistical identifiers.",
            "answer": True,
            "explanation": "A DataFrame often includes IDs, labels, dates, and measured variables. You must distinguish them.",
        },
        {
            "type": "true_false",
            "question": "If code runs successfully, the selected variables must be statistically appropriate.",
            "answer": False,
            "explanation": "Code execution does not prove that the variables are meaningful or appropriate for inference.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the missing-value check.",
            "template": "financials.___().sum()",
            "answer": "isna",
            "explanation": "isna() identifies missing values before sum() counts them by column.",
        },
        {
            "type": "multiple_choice",
            "question": "If X has shape (8, 4), what does 8 represent?",
            "options": [
                "The number of observations",
                "The number of predictor variables",
                "The number of response variables",
                "The sample variance",
            ],
            "answer": 0,
            "explanation": "Rows are observations, so 8 is n.",
        },
        {
            "type": "multiple_choice",
            "question": "If X has shape (8, 4), what does 4 represent?",
            "options": [
                "The number of predictor variables",
                "The number of observations",
                "The number of missing values",
                "The response vector length",
            ],
            "answer": 0,
            "explanation": "Columns are predictor variables, so 4 is p.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the response-vector selection.",
            "template": "y = financials[___].to_numpy()",
            "answer": "\"next_quarter_margin\"",
            "explanation": "The response variable in this lesson is next_quarter_margin.",
        },
    ],
    "challenge": {
        "instructions": (
            "Create the generic financial DataFrame from the lesson, then compute the "
            "core statistical objects. Your code must print: Observation count, "
            "Variable count, Mean vector, Deviation vector, Sample variance, Feature "
            "matrix shape, Response vector shape, and Missing values."
        ),
        "starter_code": """import numpy as np
import pandas as pd

# 1. Build the financials DataFrame from the lesson.


# 2. Define numeric_columns and feature_columns.


# 3. Write sample_mean(values) and sample_variance(values).


# 4. Compute mean vector, deviation vector for revenue_growth, sample variance,
#    feature matrix X, response vector y, and missing-value count.


# 5. Print all required labels.
""",
        "tests": [
            {"type": "code_contains", "value": "pd.DataFrame"},
            {"type": "code_contains", "value": "sample_mean"},
            {"type": "code_contains", "value": "sample_variance"},
            {"type": "output_contains", "value": "Observation count"},
            {"type": "output_contains", "value": "Variable count"},
            {"type": "output_contains", "value": "Mean vector"},
            {"type": "output_contains", "value": "Deviation vector"},
            {"type": "output_contains", "value": "Sample variance"},
            {"type": "output_contains", "value": "Feature matrix shape"},
            {"type": "output_contains", "value": "Response vector shape"},
            {"type": "output_contains", "value": "Missing values"},
            {"type": "runs_without_error"},
        ],
        "solution": """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["A", "B", "C", "D", "E", "F", "G", "H"],
    "quarter": ["2026Q1"] * 8,
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01, 0.14, 0.04],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35, 0.52, 0.40],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47, 0.22, 0.36],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02, 0.15, 0.05],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34, 0.53, 0.41],
})

numeric_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
    "next_quarter_margin",
]
feature_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
]

def sample_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def sample_variance(values):
    values = np.asarray(values)
    x_bar = sample_mean(values)
    return ((values - x_bar) ** 2).sum() / (len(values) - 1)

mean_vector = financials[numeric_columns].mean()
revenue_growth = financials["revenue_growth"].to_numpy()
deviation_vector = revenue_growth - sample_mean(revenue_growth)
variance_growth = sample_variance(revenue_growth)
X = financials[feature_columns].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
missing_values = int(financials[numeric_columns].isna().sum().sum())

print("Observation count:", len(financials))
print("Variable count:", len(numeric_columns))
print("Mean vector:")
print(mean_vector.round(4))
print("Deviation vector:", np.round(deviation_vector, 4))
print("Sample variance:", round(variance_growth, 6))
print("Feature matrix shape:", X.shape)
print("Response vector shape:", y.shape)
print("Missing values:", missing_values)""",
    },
}

MODULE_CORE_ANALYTICS_STATISTICS["lessons"][0] = LESSON_1_REBUILD
MODULE_CORE_ANALYTICS_STATISTICS["concept_map"][0] = {
    "id": "casfd-l1",
    "label": "Statistical Data In Python",
    "connects_to": [MODULE_CORE_ANALYTICS_STATISTICS["concept_map"][1]["id"]],
}


LESSON_1_GRADUATE_STATS_REBUILD = {
    "id": "casfd-l1",
    "title": "Statistical Tables, Vectors, Means, And Variance",
    "order": 1,
    "duration_min": 120,
    "difficulty": "beginner",
    "real_world_context": (
        "A financial analyst receives a small table of company-quarter metrics. "
        "Before any graduate-level method is meaningful, the analyst must convert "
        "that table into statistical objects: observations, variables, vectors, "
        "sample means, deviations, sample variance, a feature matrix X, and a "
        "response vector y."
    ),
    "concept": """## Lesson Aim

This lesson teaches the first grammar of graduate statistics in Python.

You are not starting with a formula sheet. You are starting with a financial table and
learning how each statistical object is created from that table.

The chain is:

```text
financial table
-> observation
-> variable
-> pandas Series
-> NumPy vector
-> sum
-> mean
-> deviation
-> sample variance
-> feature matrix X
-> response vector y
```

That order matters. You should not meet a formula before you can point to the data
object it acts on.

By the end of this lesson, you should be able to write Python code that builds a small
financial dataset, names its statistical structure, computes the first summary
statistics manually, checks your work with pandas, and prepares `X` and `y` for later
regression.

## 1. Build The Financial Table

We will use generic company-quarter data. It is financial enough to matter, but not
about investment theory, portfolio risk, or market mechanics.

```python
import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "quarter": ["2026Q1", "2026Q1", "2026Q1", "2026Q1", "2026Q1", "2026Q1"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34],
})

print(financials)
```

This table is the raw material for every calculation in the lesson.

Do not rush past the table. In graduate statistics, every formula depends on knowing
what the rows and columns mean.

## 2. Rows Are Observations

An **observation** is one measured unit.

In this dataset, one observation is:

```text
one company in one quarter
```

The first row is Aster in 2026Q1. The second row is Beacon in 2026Q1. Each row carries
several measurements about that company-quarter.

In code, count observations with `len`.

```python
n = len(financials)
print("n:", n)
```

Mathematically:

```text
n = sample size
```

Here:

```text
n = 6
```

That number will appear constantly. The mean divides by `n`. Sample variance divides
by `n - 1`. Regression later uses `n` rows in the feature matrix.

## 3. Columns Are Variables

A **variable** is one measured attribute.

Examples from this dataset:

```text
revenue_growth
gross_margin
debt_to_assets
free_cash_flow_margin
next_quarter_margin
```

Not every column is a statistical variable for calculation.

`company` is an identifier. It tells you which row is which.

`quarter` is a time label. It matters later for time series, but it is not a numeric
variable in this first lesson.

Select the numeric variables:

```python
numeric_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
    "next_quarter_margin",
]

print(financials[numeric_columns])
```

The habit is:

```text
name the observations
name the variables
separate identifiers from measured numeric variables
```

That habit prevents a common beginner mistake: feeding labels into formulas just
because they appear in the DataFrame.

## 4. A Column Becomes A Series

Select one financial variable:

```python
growth_series = financials["revenue_growth"]
print(growth_series)
print(type(growth_series))
```

This creates a pandas `Series`.

A `Series` is a one-dimensional labeled object. It still remembers row labels. It is
excellent for inspection, alignment, and pandas calculations.

The concept chain is now:

```text
DataFrame -> column selection -> Series
```

You have not reached vector notation yet. First you need to see the column as a Python
object.

## 5. A Series Becomes A Vector

Convert the `Series` to a NumPy array:

```python
growth_vector = growth_series.to_numpy()
print(growth_vector)
print(type(growth_vector))
```

Now the statistical notation has something concrete to name.

The vector is:

```text
x = (0.08, 0.03, 0.11, -0.02, 0.06, 0.01)
```

In general notation:

```text
x = (x_1, x_2, ..., x_n)
```

The subscript tells you which observation you are looking at:

```text
x_1 = 0.08
x_2 = 0.03
x_3 = 0.11
x_4 = -0.02
x_5 = 0.06
x_6 = 0.01
```

That is the bridge:

```text
pandas Series -> NumPy array -> statistical vector
```

Formulas act on vectors. Code gives you the vector first.

## 6. The First Vector Operation Is Sum

Before the mean, compute the sum.

```python
growth_total = growth_vector.sum()
print("Total revenue growth:", growth_total)
```

Mathematically:

```text
sum_{i=1 to n} x_i
```

Read that notation as:

```text
start at the first observation
add every x_i
stop at the nth observation
```

Code translation:

```text
growth_vector.sum() <-> sum of all x_i
```

Do not treat summation notation as decoration. It is a compact description of a loop
over observations.

## 7. The Mean Is Sum Divided By Count

The sample mean is:

```text
x_bar = (1 / n) * sum_{i=1 to n} x_i
```

In code:

```python
mean_growth = growth_vector.sum() / len(growth_vector)
print("Mean revenue growth:", mean_growth)
```

Now write it as a reusable function:

```python
def sample_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

mean_growth = sample_mean(growth_vector)
print("Manual mean:", mean_growth)
print("pandas check:", growth_series.mean())
```

This is the correct relationship between manual code and library code:

```text
manual function -> teaches the calculation
pandas method -> checks and scales the calculation
```

The pandas method is not magic. It is a reliable shortcut after you understand the
operation.

## 8. Interpretation Of The Mean

If the mean revenue growth is about `0.045`, the analyst sentence is:

```text
The sample average revenue growth is 4.5 percent across the six company-quarter
observations.
```

A stronger sentence includes the boundary:

```text
This is a sample average, not proof that the population average revenue growth is
4.5 percent.
```

The distinction matters:

```text
sample statistic: calculated from observed data
population parameter: true value in the broader population
```

For now, `mean_growth` is a sample statistic. Later lessons will ask how uncertain
that statistic is.

## 9. Deviations Build On The Mean

Variance does not appear from nowhere. It starts with deviations from the mean.

For each observation:

```text
d_i = x_i - x_bar
```

In code:

```python
deviations = growth_vector - mean_growth
print("Deviations:", deviations)
print("Sum of deviations:", deviations.sum())
```

The deviations should sum to approximately zero.

That happens because the mean is the balancing point of the data.

This matters because many later ideas are built from deviations:

```text
variance
standard deviation
covariance
correlation
regression residuals
PCA
diagnostics
```

So the sequence is:

```text
vector -> mean -> deviations
```

You must understand that before variance.

## 10. Squared Deviations Build Variance

If you simply average deviations, they cancel out. Positive and negative distances
offset each other.

So variance squares the deviations:

```python
squared_deviations = deviations ** 2
print("Squared deviations:", squared_deviations)
```

Now every distance is nonnegative.

The sample variance is:

```text
s^2 = (1 / (n - 1)) * sum_{i=1 to n} (x_i - x_bar)^2
```

In code:

```python
sample_variance_growth = squared_deviations.sum() / (len(growth_vector) - 1)
print("Manual sample variance:", sample_variance_growth)
print("pandas sample variance check:", growth_series.var(ddof=1))
```

The sample standard deviation is the square root:

```python
sample_std_growth = sample_variance_growth ** 0.5
print("Manual sample standard deviation:", sample_std_growth)
print("pandas sample standard deviation check:", growth_series.std(ddof=1))
```

Now the dependency chain is:

```text
vector -> mean -> deviations -> squared deviations -> sample variance
```

That is the smooth build. Variance is not a separate topic. It is the next operation
after deviations.

## 11. Why Sample Variance Uses n - 1

The formula uses `n - 1` because the sample mean was estimated from the same sample.
Once the mean is fixed, the deviations must sum to zero. If you know five of the six
deviations, the last one is forced.

That leaves:

```text
n - 1 degrees of freedom
```

In pandas:

```python
growth_series.var(ddof=1)
```

means:

```text
divide by n - 1
```

The argument `ddof` means delta degrees of freedom.

You do not need to master every theoretical detail yet. You do need to know that:

```text
sample variance uses n - 1
population variance uses n
```

Graduate coursework will expect that distinction.

## 12. Mean And Variance For Several Financial Variables

Now repeat the same idea across multiple numeric variables.

```python
mean_vector = financials[numeric_columns].mean()
variance_vector = financials[numeric_columns].var(ddof=1)

print("Mean vector:")
print(mean_vector)

print("Variance vector:")
print(variance_vector)
```

This produces one mean and one variance for each selected variable.

The word "vector" now appears again, but it is earned:

```text
mean vector = one mean per variable
variance vector = one variance per variable
```

You started with one column as a vector. Now you are summarizing several columns.

## 13. Feature Matrix X And Response Vector y

Regression will come later. But Lesson 1 should prepare the objects.

Suppose you eventually want to model next-quarter margin using current-quarter
financial metrics.

Predictor variables:

```python
feature_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
]
```

Feature matrix:

```python
X = financials[feature_columns].to_numpy()
print("X shape:", X.shape)
```

Response vector:

```python
y = financials["next_quarter_margin"].to_numpy()
print("y shape:", y.shape)
```

Mathematically:

```text
X is an n by p matrix
y is an n-element vector
```

Here:

```text
X shape = (6, 4)
y shape = (6,)
```

That means:

```text
6 observations
4 predictor variables
1 response value per observation
```

Later, ordinary least squares will use:

```text
y = X beta + epsilon
```

For now, just know what `X` and `y` physically are in Python.

## 14. Missing Values Are Part Of Statistical Thinking

Check missing values before modeling:

```python
missing_by_column = financials[numeric_columns].isna().sum()
print(missing_by_column)
```

Missingness is not merely "dirty data." In financial analysis it can reveal reporting
lags, vendor problems, distressed firms, young companies, or unavailable customer
history.

This dataset has no missing numeric values. The point is to build the habit:

```text
inspect missingness before trusting summary statistics
```

## 15. Assemble The Full Code Path

Here is the full flow in one place:

```python
import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "quarter": ["2026Q1", "2026Q1", "2026Q1", "2026Q1", "2026Q1", "2026Q1"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34],
})

numeric_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
    "next_quarter_margin",
]

feature_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
]

def sample_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def sample_variance(values):
    values = np.asarray(values)
    x_bar = sample_mean(values)
    deviations = values - x_bar
    squared_deviations = deviations ** 2
    return squared_deviations.sum() / (len(values) - 1)

growth_series = financials["revenue_growth"]
growth_vector = growth_series.to_numpy()
mean_growth = sample_mean(growth_vector)
deviations = growth_vector - mean_growth
variance_growth = sample_variance(growth_vector)
std_growth = variance_growth ** 0.5
mean_vector = financials[numeric_columns].mean()
variance_vector = financials[numeric_columns].var(ddof=1)
X = financials[feature_columns].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
missing_values = financials[numeric_columns].isna().sum().sum()

print("Observation count:", len(financials))
print("Numeric variable count:", len(numeric_columns))
print("Growth vector:", growth_vector)
print("Mean revenue growth:", round(mean_growth, 4))
print("Deviation vector:", np.round(deviations, 4))
print("Sample variance:", round(variance_growth, 6))
print("Sample standard deviation:", round(std_growth, 6))
print("Mean vector:")
print(mean_vector.round(4))
print("Variance vector:")
print(variance_vector.round(6))
print("X shape:", X.shape)
print("y shape:", y.shape)
print("Missing numeric values:", int(missing_values))
```

## What You Should Now Own

You should be able to explain and code this chain:

```text
DataFrame -> Series -> vector -> sum -> mean -> deviations -> variance
```

You should also be able to explain:

- `n` is the number of observations.
- A variable is a measured column.
- An identifier is not automatically a statistical variable.
- A sample statistic is calculated from observed data.
- The sample mean estimates a population mean.
- Sample variance uses `n - 1`.
- `X` is the feature matrix.
- `y` is the response vector.

This is the base layer. Lesson 2 should build directly on this by making columns,
vectors, and elementwise operations feel automatic before moving deeper into summary
statistics.
""",
    "worked_example": {
        "description": (
            "Build a financial table, turn one column into a vector, compute mean "
            "and variance manually, then prepare X and y."
        ),
        "code": """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "quarter": ["2026Q1", "2026Q1", "2026Q1", "2026Q1", "2026Q1", "2026Q1"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34],
})

def sample_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def sample_variance(values):
    values = np.asarray(values)
    x_bar = sample_mean(values)
    return ((values - x_bar) ** 2).sum() / (len(values) - 1)

growth = financials["revenue_growth"].to_numpy()
mean_growth = sample_mean(growth)
deviations = growth - mean_growth
variance_growth = sample_variance(growth)

feature_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
]
X = financials[feature_columns].to_numpy()
y = financials["next_quarter_margin"].to_numpy()

print("Observation count:", len(financials))
print("Mean revenue growth:", round(mean_growth, 4))
print("Deviation vector:", np.round(deviations, 4))
print("Sample variance:", round(variance_growth, 6))
print("pandas variance check:", round(financials["revenue_growth"].var(ddof=1), 6))
print("X shape:", X.shape)
print("y shape:", y.shape)""",
        "explanation": (
            "The example moves in the same order as the lesson: table, column, "
            "vector, sum/mean, deviations, variance, and then X/y for later "
            "regression."
        ),
    },
    "reference": {
        "key_syntax": [
            "financials = pd.DataFrame({...})",
            "n = len(financials)",
            "growth_series = financials['revenue_growth']",
            "growth_vector = growth_series.to_numpy()",
            "x_bar = values.sum() / len(values)",
            "deviations = values - x_bar",
            "s_squared = (deviations ** 2).sum() / (len(values) - 1)",
            "X = financials[feature_columns].to_numpy()",
            "y = financials['next_quarter_margin'].to_numpy()",
            "financials[numeric_columns].isna().sum()",
        ],
        "notes": (
            "The key chain is DataFrame -> Series -> vector -> mean -> deviations "
            "-> variance -> X/y. Later lessons should build from this chain."
        ),
    },
    "questions": [
        {
            "type": "multiple_choice",
            "question": "What is one observation in the Lesson 1 dataset?",
            "options": [
                "One company in one quarter",
                "The entire financials DataFrame",
                "The revenue_growth column by itself",
                "The formula for sample variance",
            ],
            "answer": 0,
            "explanation": "Each row is one company-quarter observation.",
        },
        {
            "type": "multiple_choice",
            "question": "Which column is an identifier rather than a measured numeric variable?",
            "options": ["company", "gross_margin", "debt_to_assets", "free_cash_flow_margin"],
            "answer": 0,
            "explanation": "company labels the row; it is not a numeric measurement for mean or variance.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the code that counts observations.",
            "template": "n = ___(financials)",
            "answer": "len",
            "explanation": "len(financials) returns the number of rows.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the code that selects the revenue growth Series.",
            "template": "growth_series = financials[___]",
            "answer": "\"revenue_growth\"",
            "explanation": "financials[\"revenue_growth\"] selects one column as a pandas Series.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the conversion from Series to NumPy vector.",
            "template": "growth_vector = growth_series.___()",
            "answer": "to_numpy",
            "explanation": "to_numpy() converts the Series into a NumPy array.",
        },
        {
            "type": "multiple_choice",
            "question": "What does x_i mean in x = (x_1, x_2, ..., x_n)?",
            "options": [
                "The value of variable x for observation i",
                "The number of columns in the DataFrame",
                "The company identifier",
                "The response variable name",
            ],
            "answer": 0,
            "explanation": "The subscript i indexes the observation.",
        },
        {
            "type": "multiple_choice",
            "question": "Which sequence matches the lesson's build order?",
            "options": [
                "DataFrame -> Series -> vector -> sum -> mean",
                "variance -> DataFrame -> identifier -> response",
                "p-value -> regression -> Series -> mean",
                "X matrix -> missing values -> row labels -> DataFrame",
            ],
            "answer": 0,
            "explanation": "The lesson deliberately earns each abstraction in that order.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the manual sample mean calculation.",
            "template": "return values.sum() / ___(values)",
            "answer": "len",
            "explanation": "The mean divides the sum by the number of values.",
        },
        {
            "type": "multiple_choice",
            "question": "Which formula represents the sample mean?",
            "options": [
                "x_bar = (1 / n) * sum x_i",
                "s_squared = sum x_i",
                "X = y - beta",
                "n = p - 1",
            ],
            "answer": 0,
            "explanation": "The sample mean is the sum of observed values divided by n.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the deviation calculation.",
            "template": "deviations = growth_vector ___ mean_growth",
            "answer": "-",
            "explanation": "A deviation is the observed value minus the sample mean.",
        },
        {
            "type": "multiple_choice",
            "question": "Why do deviations from the sample mean sum to approximately zero?",
            "options": [
                "The sample mean is the balancing point of the observed values",
                "The dataset has no categorical columns",
                "Pandas automatically deletes nonzero deviations",
                "Financial variables must always sum to zero",
            ],
            "answer": 0,
            "explanation": "The mean balances the observed values, so positive and negative deviations offset.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the squared-deviation expression.",
            "template": "squared_deviations = deviations ___ 2",
            "answer": "**",
            "explanation": "Python uses ** for exponentiation.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the sample variance denominator.",
            "template": "sample_variance = squared_deviations.sum() / (len(growth_vector) ___ 1)",
            "answer": "-",
            "explanation": "Sample variance uses n - 1 in the denominator.",
        },
        {
            "type": "multiple_choice",
            "question": "Why does sample variance use n - 1?",
            "options": [
                "The sample mean was estimated from the same data, leaving n - 1 degrees of freedom",
                "The response vector has one column",
                "All financial datasets have one missing observation",
                "Variance is always calculated with negative sample size",
            ],
            "answer": 0,
            "explanation": "Estimating the mean uses one degree of freedom.",
        },
        {
            "type": "multiple_choice",
            "question": "What does pandas `var(ddof=1)` compute?",
            "options": [
                "Sample variance using n - 1",
                "Population variance using n",
                "The sample mean",
                "The number of missing values",
            ],
            "answer": 0,
            "explanation": "ddof=1 subtracts one from n in the denominator.",
        },
        {
            "type": "multiple_choice",
            "question": "What is X in later regression work?",
            "options": [
                "The feature matrix of predictor variables",
                "The company-name identifier",
                "The sample variance only",
                "The written interpretation",
            ],
            "answer": 0,
            "explanation": "X contains predictor variables, with rows as observations and columns as features.",
        },
        {
            "type": "multiple_choice",
            "question": "What is y in later regression work?",
            "options": [
                "The response vector",
                "The list of feature column names",
                "The count of numeric variables",
                "The pandas DataFrame index",
            ],
            "answer": 0,
            "explanation": "y is the outcome or response value for each observation.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the feature matrix conversion.",
            "template": "X = financials[feature_columns].___()",
            "answer": "to_numpy",
            "explanation": "to_numpy() converts selected predictor columns into a matrix.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the response vector selection.",
            "template": "y = financials[___].to_numpy()",
            "answer": "\"next_quarter_margin\"",
            "explanation": "next_quarter_margin is the response variable in Lesson 1.",
        },
        {
            "type": "multiple_choice",
            "question": "If X has shape (6, 4), what does 6 represent?",
            "options": [
                "The number of observations",
                "The number of predictor variables",
                "The number of response variables",
                "The variance denominator",
            ],
            "answer": 0,
            "explanation": "Rows are observations, so 6 is n.",
        },
        {
            "type": "multiple_choice",
            "question": "If X has shape (6, 4), what does 4 represent?",
            "options": [
                "The number of predictor variables",
                "The number of observations",
                "The response vector length",
                "The missing-value count",
            ],
            "answer": 0,
            "explanation": "Columns are predictor variables, so 4 is p.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the missing-value check.",
            "template": "financials[numeric_columns].___().sum()",
            "answer": "isna",
            "explanation": "isna() identifies missing values before sum() counts them.",
        },
        {
            "type": "true_false",
            "question": "A sample statistic is calculated from observed data.",
            "answer": True,
            "explanation": "The sample mean and sample variance are statistics calculated from the sample.",
        },
        {
            "type": "true_false",
            "question": "If code runs, the selected variables are automatically appropriate for inference.",
            "answer": False,
            "explanation": "Code execution does not prove the statistical design is meaningful.",
        },
        {
            "type": "multiple_choice",
            "question": "Which statement is the strongest interpretation of the sample mean?",
            "options": [
                "The sample average revenue growth is about 4.5 percent across the observed company-quarters, but this alone does not prove the population mean.",
                "The true population growth rate is definitely 4.5 percent.",
                "The companies are guaranteed to grow next quarter.",
                "The mean replaces the need to inspect variance.",
            ],
            "answer": 0,
            "explanation": "A strong interpretation reports the statistic and states its limit.",
        },
    ],
    "challenge": {
        "instructions": (
            "Build the Lesson 1 financial table, then compute the statistical objects "
            "from the lesson. Your code must define `sample_mean` and "
            "`sample_variance`, convert revenue growth to a vector, compute "
            "deviations, sample variance, a mean vector, a variance vector, X, y, "
            "and missing-value counts. Print every required label."
        ),
        "starter_code": """import numpy as np
import pandas as pd

# 1. Build the financials DataFrame from the lesson.


# 2. Define numeric_columns and feature_columns.


# 3. Write sample_mean(values).


# 4. Write sample_variance(values).


# 5. Select revenue_growth as a Series and convert it to a vector.


# 6. Compute mean, deviations, variance, standard deviation, X, y, and missing values.


# 7. Print each required label:
# Observation count
# Numeric variable count
# Growth vector
# Mean revenue growth
# Deviation vector
# Sample variance
# Sample standard deviation
# Mean vector
# Variance vector
# X shape
# y shape
# Missing numeric values
""",
        "tests": [
            {"type": "code_contains", "value": "pd.DataFrame"},
            {"type": "code_contains", "value": "sample_mean"},
            {"type": "code_contains", "value": "sample_variance"},
            {"type": "code_contains", "value": "to_numpy"},
            {"type": "output_contains", "value": "Observation count"},
            {"type": "output_contains", "value": "Numeric variable count"},
            {"type": "output_contains", "value": "Growth vector"},
            {"type": "output_contains", "value": "Mean revenue growth"},
            {"type": "output_contains", "value": "Deviation vector"},
            {"type": "output_contains", "value": "Sample variance"},
            {"type": "output_contains", "value": "Sample standard deviation"},
            {"type": "output_contains", "value": "Mean vector"},
            {"type": "output_contains", "value": "Variance vector"},
            {"type": "output_contains", "value": "X shape"},
            {"type": "output_contains", "value": "y shape"},
            {"type": "output_contains", "value": "Missing numeric values"},
            {"type": "runs_without_error"},
        ],
        "solution": """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "quarter": ["2026Q1", "2026Q1", "2026Q1", "2026Q1", "2026Q1", "2026Q1"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34],
})

numeric_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
    "next_quarter_margin",
]

feature_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
]

def sample_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def sample_variance(values):
    values = np.asarray(values)
    x_bar = sample_mean(values)
    deviations = values - x_bar
    squared_deviations = deviations ** 2
    return squared_deviations.sum() / (len(values) - 1)

growth_series = financials["revenue_growth"]
growth_vector = growth_series.to_numpy()
mean_growth = sample_mean(growth_vector)
deviation_vector = growth_vector - mean_growth
sample_variance_growth = sample_variance(growth_vector)
sample_std_growth = sample_variance_growth ** 0.5
mean_vector = financials[numeric_columns].mean()
variance_vector = financials[numeric_columns].var(ddof=1)
X = financials[feature_columns].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
missing_values = int(financials[numeric_columns].isna().sum().sum())

print("Observation count:", len(financials))
print("Numeric variable count:", len(numeric_columns))
print("Growth vector:", growth_vector)
print("Mean revenue growth:", round(mean_growth, 4))
print("Deviation vector:", np.round(deviation_vector, 4))
print("Sample variance:", round(sample_variance_growth, 6))
print("Sample standard deviation:", round(sample_std_growth, 6))
print("Mean vector:")
print(mean_vector.round(4))
print("Variance vector:")
print(variance_vector.round(6))
print("X shape:", X.shape)
print("y shape:", y.shape)
print("Missing numeric values:", missing_values)""",
    },
}

MODULE_CORE_ANALYTICS_STATISTICS["title"] = "Graduate Statistics For Financial Analysis"
MODULE_CORE_ANALYTICS_STATISTICS["description"] = (
    "A code-heavy graduate statistics mini-course for financial analysis. Lesson 1 "
    "now teaches statistical tables, vectors, means, deviations, sample variance, "
    "and X/y construction through Python and math."
)
MODULE_CORE_ANALYTICS_STATISTICS["lessons"][0] = LESSON_1_GRADUATE_STATS_REBUILD
MODULE_CORE_ANALYTICS_STATISTICS["concept_map"][0] = {
    "id": "casfd-l1",
    "label": "Tables, Vectors, Means, Variance",
    "connects_to": [MODULE_CORE_ANALYTICS_STATISTICS["concept_map"][1]["id"]],
}


_COMMON_FINANCIAL_DATA_CODE = """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord", "Granite", "Harbor", "Ion", "Juniper"],
    "segment": ["SaaS", "SaaS", "Lending", "Lending", "Payments", "Payments", "SaaS", "Lending", "Payments", "SaaS"],
    "quarter": ["2026Q1"] * 10,
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01, 0.14, 0.04, -0.01, 0.09],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35, 0.52, 0.40, 0.33, 0.45],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47, 0.22, 0.36, 0.58, 0.29],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02, 0.15, 0.05, -0.01, 0.10],
    "customer_balance": [1200, 850, 1600, 740, 1100, 910, 1900, 1300, 680, 1500],
    "transaction_count": [42, 37, 58, 24, 45, 31, 63, 46, 22, 54],
    "default_flag": [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    "fraud_flag": [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    "churn_flag": [0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34, 0.53, 0.41, 0.30, 0.47],
})

numeric_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
    "customer_balance",
    "transaction_count",
    "next_quarter_margin",
]

feature_columns = [
    "revenue_growth",
    "gross_margin",
    "debt_to_assets",
    "free_cash_flow_margin",
]
"""


def _grad_spec(
    order,
    title,
    prior,
    adds,
    produces,
    object_name,
    math_text,
    syntax_template,
    syntax_answer,
    syntax_explanation,
    worked_goal,
    worked_code,
    solution,
    output_labels,
    code_contains,
    difficulty="intermediate",
    duration=105,
):
    return {
        "id": f"casfd-l{order}",
        "label": title.split(":")[0][:40],
        "title": title,
        "order": order,
        "duration_min": duration,
        "difficulty": difficulty,
        "prior": prior,
        "adds": adds,
        "produces": produces,
        "object_name": object_name,
        "math_text": math_text,
        "syntax_template": syntax_template,
        "syntax_answer": syntax_answer,
        "syntax_explanation": syntax_explanation,
        "worked_goal": worked_goal,
        "worked_code": worked_code,
        "solution": solution,
        "output_labels": output_labels,
        "code_contains": code_contains,
    }


def _graduate_concept(spec):
    labels = "\n".join(f"- `{label}`" for label in spec["output_labels"])
    return f"""## Lesson Aim

This lesson continues the graduate statistics sequence for financial analysis.

You already own:

```text
{spec["prior"]}
```

This lesson adds:

```text
{spec["adds"]}
```

The output you are learning to produce is:

```text
{spec["produces"]}
```

The point is not to memorize a loose definition. The point is to build the next
statistical object from the object you already created in the prior lesson.

## The Dependency Chain

Every lesson in this module must earn the next abstraction. For this lesson, the chain
is:

```text
{spec["prior"]} -> {spec["object_name"]} -> {spec["produces"]}
```

If that chain feels broken, slow down and rebuild the earlier object in code. Graduate
statistics becomes much less intimidating when every formula has a visible Python
object underneath it.

## Build The Working Dataset

Use the same generic financial-analysis table so the course feels cumulative.

```python
{_COMMON_FINANCIAL_DATA_CODE}
```

This table contains company-quarter financial metrics, balances, transaction counts,
and binary event flags. Later lessons reuse the same objects in more advanced ways.

## Code First

The main coding move for this lesson is:

```python
{spec["worked_code"]}
```

Read the code line by line. Ask what object each line creates. The variable names are
not cosmetic; they are the bridge between Python and notation.

## Math Beside The Code

The formal idea is:

```text
{spec["math_text"]}
```

Do not treat the notation as a separate language. The notation names the same object
you created in Python. When you see a summation, vector, matrix, likelihood, test
statistic, coefficient, or posterior, ask where it lives in the code.

## Manual Calculation Before Shortcut

For this course, the preferred order is:

1. create the data object
2. compute the statistic manually with Python, NumPy, or pandas primitives
3. check the result with a library method when useful
4. interpret the result in financial-analysis language

That order builds understanding. Shortcuts are allowed after the underlying
calculation is visible.

## Worked Example Goal

{spec["worked_goal"]}

Run the code, inspect the printed objects, and connect each result back to the
dependency chain above.

## Interpretation Rule

A graduate-level interpretation should include:

- the number or object produced
- the financial-analysis meaning
- the limitation
- the next diagnostic or calculation that should follow

For this lesson:

```text
{spec["produces"]} is useful because it extends {spec["prior"]}. It is not the end of
the analysis; it prepares the next method in the sequence.
```

## Common Mistakes

- Jumping to the library shortcut before knowing the manual calculation.
- Reporting a statistic without saying what sample produced it.
- Treating a sample statistic as if it were automatically a population truth.
- Forgetting that later lessons depend on the object built here.
- Using finance language so loosely that the statistical concept disappears.

## Practice And Challenge

Practice checks syntax, notation, interpretation, and the exact calculation chain. The
challenge asks you to produce these labels:

{labels}

The labels are not decoration. They make the notebook auditable.

## Bridge To The Next Lesson

The next lesson should start from this lesson's output and add exactly one new layer.
That is the spine of the whole module.
"""


def _graduate_questions(spec):
    return [
        {
            "type": "multiple_choice",
            "question": f"What prior object does this lesson build from?",
            "options": [spec["prior"], "A disconnected finance story", "A written-only opinion", "An unrelated chart"],
            "answer": 0,
            "explanation": "Each lesson inherits a specific object or calculation from the prior lesson.",
        },
        {
            "type": "multiple_choice",
            "question": f"What does this lesson add?",
            "options": [spec["adds"], "A shortcut without a manual calculation", "A market forecast guarantee", "A disconnected feature"],
            "answer": 0,
            "explanation": "The lesson adds one explicit statistical layer.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the key syntax from this lesson.",
            "template": spec["syntax_template"],
            "answer": spec["syntax_answer"],
            "explanation": spec["syntax_explanation"],
        },
        {
            "type": "multiple_choice",
            "question": "How should the math notation be treated?",
            "options": [
                "As a compact name for the same object created in code",
                "As decoration that can be ignored",
                "As proof that no code is needed",
                "As a replacement for checking data quality",
            ],
            "answer": 0,
            "explanation": "The course pairs notation with visible Python objects.",
        },
        {
            "type": "true_false",
            "question": "A library shortcut is strongest after the manual calculation is understood.",
            "answer": True,
            "explanation": "Manual calculation builds understanding; the shortcut then scales the workflow.",
        },
        {
            "type": "multiple_choice",
            "question": f"What is the main object in this lesson?",
            "options": [spec["object_name"], "A company name label only", "A badge counter with no statistical meaning", "A screenshot"],
            "answer": 0,
            "explanation": f"The main object is {spec['object_name']}.",
        },
        {
            "type": "multiple_choice",
            "question": "Which output should your code print in the challenge?",
            "options": [spec["output_labels"][0], "Only raw memory addresses", "Only a paragraph with no code", "A guaranteed future outcome"],
            "answer": 0,
            "explanation": "The challenge labels make the notebook readable and testable.",
        },
        {
            "type": "multiple_choice",
            "question": "What should come immediately after computing the statistic?",
            "options": [
                "Interpret it and state a limitation",
                "Assume the population result is proven",
                "Delete the intermediate variables",
                "Skip the next diagnostic",
            ],
            "answer": 0,
            "explanation": "Graduate analysis connects calculation, meaning, and limitation.",
        },
        {
            "type": "true_false",
            "question": "A statistic calculated from this sample is automatically the exact population parameter.",
            "answer": False,
            "explanation": "Sample statistics estimate or describe; they do not automatically equal population parameters.",
        },
        {
            "type": "multiple_choice",
            "question": "Which habit best supports top-of-class performance?",
            "options": [
                "Show the code object, the math object, and the interpretation together",
                "Memorize outputs without checking formulas",
                "Use finance language without statistics",
                "Avoid writing code until the final project",
            ],
            "answer": 0,
            "explanation": "The module is code first with math explained alongside.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the challenge output label.",
            "template": "print(\"___\", value)",
            "answer": spec["output_labels"][0],
            "explanation": f"The first required label is `{spec['output_labels'][0]}`.",
        },
        {
            "type": "multiple_choice",
            "question": "Why use a cumulative financial dataset?",
            "options": [
                "So later lessons reuse earlier objects instead of jumping erratically",
                "So every lesson becomes an investment theory lesson",
                "So formulas can be avoided",
                "So code output no longer matters",
            ],
            "answer": 0,
            "explanation": "Cumulative data helps concepts lean into each other.",
        },
        {
            "type": "multiple_choice",
            "question": "Which mistake would weaken this lesson most?",
            "options": [
                "Using the final number without explaining how it was built",
                "Naming intermediate variables clearly",
                "Checking a manual calculation",
                "Printing labeled outputs",
            ],
            "answer": 0,
            "explanation": "The calculation chain is part of the learning objective.",
        },
        {
            "type": "true_false",
            "question": "The challenge should ask you to write code, not only written prose.",
            "answer": True,
            "explanation": "Hack requested Python/math-first work with no written-only sections unless code produces the answer.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the statement: DataFrame columns can become statistical ___.",
            "template": "DataFrame columns can become statistical ___.",
            "answer": "vectors",
            "explanation": "A selected numeric column can be treated as a statistical vector.",
        },
        {
            "type": "multiple_choice",
            "question": "What does a strong model answer include?",
            "options": [
                "Working code, labeled outputs, and a bounded interpretation",
                "Only the final number",
                "Only generic study advice",
                "Only a claim that the result is important",
            ],
            "answer": 0,
            "explanation": "Model answers should show code and interpretation.",
        },
        {
            "type": "multiple_choice",
            "question": "Which mini-drill best belongs before the challenge?",
            "options": [
                f"Rebuild {spec['object_name']} and connect it to {spec['produces']}",
                "Memorize the page order without writing code",
                "Replace the calculation with a market opinion",
                "Skip the labeled output and keep only a definition",
            ],
            "answer": 0,
            "explanation": "The best drill rehearses the same object, output, and interpretation used in the challenge.",
        },
        {
            "type": "multiple_choice",
            "question": "What makes the lesson graduate-oriented rather than elementary?",
            "options": [
                "It connects code, notation, assumptions, and the next method",
                "It hides the formula",
                "It asks only vocabulary questions",
                "It avoids computation",
            ],
            "answer": 0,
            "explanation": "Graduate preparation requires moving between code, math, and assumptions.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the phrase: code first, math explained ___.",
            "template": "code first, math explained ___",
            "answer": "alongside",
            "explanation": "This is the module's instructional pattern.",
        },
        {
            "type": "multiple_choice",
            "question": "What is the best bridge into the next lesson?",
            "options": [
                f"Use `{spec['produces']}` as the starting object for the next method",
                "Start a completely unrelated topic",
                "Remove the coding challenge",
                "Replace statistics with a finance opinion",
            ],
            "answer": 0,
            "explanation": "The sequence should move gradually from one produced object to the next.",
        },
    ]


def _graduate_lesson(spec):
    return {
        "id": spec["id"],
        "title": spec["title"],
        "order": spec["order"],
        "duration_min": spec["duration_min"],
        "difficulty": spec["difficulty"],
        "real_world_context": (
            "Generic financial-analysis data is used as the setting, but the lesson "
            f"focus is statistics: {spec['adds']}."
        ),
        "concept": _graduate_concept(spec),
        "worked_example": {
            "description": spec["worked_goal"],
            "code": spec["worked_code"],
            "explanation": (
                f"This worked example builds {spec['object_name']} from the previous "
                "lesson's objects and prepares the next lesson's calculation."
            ),
        },
        "reference": {
            "key_syntax": [spec["syntax_template"], *spec["code_contains"]],
            "notes": f"Build from {spec['prior']} into {spec['produces']}.",
        },
        "questions": _graduate_questions(spec),
        "challenge": {
            "instructions": (
                f"Use the common financial dataset to produce {spec['produces']}. "
                "Your code must print the required labels and run without errors."
            ),
            "starter_code": (
                _COMMON_FINANCIAL_DATA_CODE
                + "\n# Continue the lesson challenge below.\n# Required labels:\n"
                + "\n".join(f"# - {label}" for label in spec["output_labels"])
                + "\n"
            ),
            "tests": (
                [{"type": "code_contains", "value": value} for value in spec["code_contains"]]
                + [{"type": "output_contains", "value": label} for label in spec["output_labels"]]
                + [{"type": "runs_without_error"}]
            ),
            "solution": spec["solution"],
        },
    }


GRADUATE_STATS_SPECS = [
    _grad_spec(
        2,
        "Columns, Series, Vectors, And Elementwise Operations",
        "Lesson 1's DataFrame and one-column vector",
        "Series selection, NumPy conversion, and elementwise arithmetic",
        "aligned financial vectors that can be added, subtracted, scaled, and compared",
        "aligned vectors",
        "x = (x_1, ..., x_n), z = (z_1, ..., z_n), and x + z = (x_1 + z_1, ..., x_n + z_n)",
        "growth_vector = growth_series.___()",
        "to_numpy",
        "to_numpy() converts a pandas Series into a NumPy vector.",
        "Select two financial columns, convert them to vectors, and compute elementwise spreads.",
        _COMMON_FINANCIAL_DATA_CODE + """
growth_series = financials["revenue_growth"]
margin_series = financials["gross_margin"]
growth_vector = growth_series.to_numpy()
margin_vector = margin_series.to_numpy()
growth_minus_margin = growth_vector - margin_vector

print("Growth vector:", np.round(growth_vector, 4))
print("Margin vector:", np.round(margin_vector, 4))
print("Growth minus margin:", np.round(growth_minus_margin, 4))
print("Aligned length:", len(growth_vector) == len(margin_vector))""",
        _COMMON_FINANCIAL_DATA_CODE + """
growth_series = financials["revenue_growth"]
margin_series = financials["gross_margin"]
balance_series = financials["customer_balance"]

growth_vector = growth_series.to_numpy()
margin_vector = margin_series.to_numpy()
balance_vector = balance_series.to_numpy()

growth_minus_margin = growth_vector - margin_vector
scaled_balance = balance_vector / 1000

print("Growth vector:", np.round(growth_vector, 4))
print("Margin vector:", np.round(margin_vector, 4))
print("Growth minus margin:", np.round(growth_minus_margin, 4))
print("Scaled balance vector:", np.round(scaled_balance, 4))
print("Aligned length:", len(growth_vector) == len(margin_vector) == len(balance_vector))""",
        ["Growth vector", "Margin vector", "Growth minus margin", "Scaled balance vector", "Aligned length"],
        ["to_numpy", "growth_vector", "margin_vector"],
        difficulty="beginner",
    ),
    _grad_spec(
        3,
        "Summation, Count, Mean, And Weighted Mean",
        "aligned numeric vectors from Lesson 2",
        "sum, count, arithmetic mean, and weighted mean",
        "manual and weighted averages for financial variables",
        "mean and weighted mean",
        "x_bar = (1 / n) sum x_i and weighted_mean = sum(w_i x_i) / sum(w_i)",
        "weighted_mean = (values * weights).___() / weights.sum()",
        "sum",
        "The numerator of a weighted mean is the sum of weighted values.",
        "Compute an arithmetic mean and a customer-balance-weighted mean.",
        _COMMON_FINANCIAL_DATA_CODE + """
growth = financials["revenue_growth"].to_numpy()
weights = financials["customer_balance"].to_numpy()

arithmetic_mean = growth.sum() / len(growth)
weighted_mean = (growth * weights).sum() / weights.sum()

print("Arithmetic mean:", round(arithmetic_mean, 6))
print("Weighted mean:", round(weighted_mean, 6))
print("Pandas mean check:", round(financials["revenue_growth"].mean(), 6))""",
        _COMMON_FINANCIAL_DATA_CODE + """
growth = financials["revenue_growth"].to_numpy()
balances = financials["customer_balance"].to_numpy()
transaction_counts = financials["transaction_count"].to_numpy()

def sample_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def weighted_mean(values, weights):
    values = np.asarray(values)
    weights = np.asarray(weights)
    return (values * weights).sum() / weights.sum()

print("Observation count:", len(growth))
print("Revenue growth sum:", round(growth.sum(), 6))
print("Arithmetic mean:", round(sample_mean(growth), 6))
print("Balance-weighted mean:", round(weighted_mean(growth, balances), 6))
print("Transaction-weighted mean:", round(weighted_mean(growth, transaction_counts), 6))""",
        ["Observation count", "Revenue growth sum", "Arithmetic mean", "Balance-weighted mean", "Transaction-weighted mean"],
        ["weighted_mean", "sample_mean", "weights"],
        difficulty="beginner",
    ),
    _grad_spec(
        4,
        "Deviations, Sample Variance, And Standard Deviation",
        "the mean from Lesson 3",
        "deviations, squared deviations, sample variance, and sample standard deviation",
        "manual spread statistics checked against pandas",
        "sample variance",
        "d_i = x_i - x_bar, s^2 = sum(d_i^2) / (n - 1), and s = sqrt(s^2)",
        "deviations = values ___ x_bar",
        "-",
        "A deviation subtracts the mean from each observed value.",
        "Build sample variance from deviations instead of treating it as a new disconnected formula.",
        _COMMON_FINANCIAL_DATA_CODE + """
values = financials["revenue_growth"].to_numpy()
x_bar = values.sum() / len(values)
deviations = values - x_bar
squared_deviations = deviations ** 2
sample_variance = squared_deviations.sum() / (len(values) - 1)
sample_std = sample_variance ** 0.5

print("Mean:", round(x_bar, 6))
print("Deviation sum:", round(deviations.sum(), 10))
print("Sample variance:", round(sample_variance, 6))
print("Sample standard deviation:", round(sample_std, 6))""",
        _COMMON_FINANCIAL_DATA_CODE + """
values = financials["revenue_growth"].to_numpy()

def sample_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def sample_variance(values):
    values = np.asarray(values)
    x_bar = sample_mean(values)
    deviations = values - x_bar
    return (deviations ** 2).sum() / (len(values) - 1)

x_bar = sample_mean(values)
deviations = values - x_bar
variance = sample_variance(values)
standard_deviation = variance ** 0.5

print("Mean from prior lesson:", round(x_bar, 6))
print("Deviation vector:", np.round(deviations, 4))
print("Deviation sum check:", round(deviations.sum(), 10))
print("Sample variance:", round(variance, 6))
print("Sample standard deviation:", round(standard_deviation, 6))
print("Pandas std check:", round(financials["revenue_growth"].std(ddof=1), 6))""",
        ["Mean from prior lesson", "Deviation vector", "Deviation sum check", "Sample variance", "Sample standard deviation", "Pandas std check"],
        ["sample_variance", "deviations", "ddof=1"],
        difficulty="beginner",
    ),
    _grad_spec(
        5,
        "Standardization, Z-Scores, And Empirical Distributions",
        "mean and standard deviation from Lesson 4",
        "z-scores, standardized variables, empirical percentiles, and simple outlier flags",
        "standardized financial variables that can be compared across scales",
        "z-score vector",
        "z_i = (x_i - x_bar) / s",
        "z_scores = (values - values.mean()) ___ values.std(ddof=1)",
        "/",
        "A z-score divides each deviation by the sample standard deviation.",
        "Turn revenue growth and customer balances into comparable standardized values.",
        _COMMON_FINANCIAL_DATA_CODE + """
values = financials["revenue_growth"]
z_scores = (values - values.mean()) / values.std(ddof=1)
percentile_75 = values.quantile(0.75)
high_growth_flag = values >= percentile_75

print("Z-scores:", np.round(z_scores.to_numpy(), 4))
print("75th percentile:", round(percentile_75, 4))
print("High growth flags:", high_growth_flag.astype(int).to_list())""",
        _COMMON_FINANCIAL_DATA_CODE + """
growth = financials["revenue_growth"]
balance = financials["customer_balance"]

growth_z = (growth - growth.mean()) / growth.std(ddof=1)
balance_z = (balance - balance.mean()) / balance.std(ddof=1)
empirical_percentiles = growth.rank(pct=True)
outlier_flags = (growth_z.abs() >= 1.5).astype(int)

print("Growth z-scores:", np.round(growth_z.to_numpy(), 4))
print("Balance z-scores:", np.round(balance_z.to_numpy(), 4))
print("Empirical percentiles:", np.round(empirical_percentiles.to_numpy(), 3))
print("Outlier flags:", outlier_flags.to_list())
print("Standardized mean check:", round(growth_z.mean(), 10))
print("Standardized std check:", round(growth_z.std(ddof=1), 6))""",
        ["Growth z-scores", "Balance z-scores", "Empirical percentiles", "Outlier flags", "Standardized mean check", "Standardized std check"],
        ["growth_z", "std(ddof=1)", "rank"],
    ),
    _grad_spec(
        6,
        "Covariance, Correlation, And Relationship Matrices",
        "standardized and centered vectors from Lesson 5",
        "covariance, correlation, and relationship matrices",
        "a correlation matrix among financial metrics",
        "covariance and correlation matrix",
        "cov(x, y) = sum((x_i - x_bar)(y_i - y_bar)) / (n - 1), corr(x, y) = cov(x, y) / (s_x s_y)",
        "correlation_matrix = financials[feature_columns].___()",
        "corr",
        "DataFrame.corr() computes the pairwise correlation matrix.",
        "Compute covariance manually and compare it to a pandas correlation matrix.",
        _COMMON_FINANCIAL_DATA_CODE + """
x = financials["revenue_growth"].to_numpy()
y = financials["gross_margin"].to_numpy()
cov_xy = ((x - x.mean()) * (y - y.mean())).sum() / (len(x) - 1)
corr_xy = cov_xy / (x.std(ddof=1) * y.std(ddof=1))

print("Manual covariance:", round(cov_xy, 6))
print("Manual correlation:", round(corr_xy, 6))
print("Pandas correlation:", round(financials["revenue_growth"].corr(financials["gross_margin"]), 6))""",
        _COMMON_FINANCIAL_DATA_CODE + """
x = financials["revenue_growth"].to_numpy()
y = financials["gross_margin"].to_numpy()
cov_xy = ((x - x.mean()) * (y - y.mean())).sum() / (len(x) - 1)
corr_xy = cov_xy / (x.std(ddof=1) * y.std(ddof=1))
correlation_matrix = financials[feature_columns].corr()
covariance_matrix = financials[feature_columns].cov()

print("Manual covariance:", round(cov_xy, 6))
print("Manual correlation:", round(corr_xy, 6))
print("Correlation matrix:")
print(correlation_matrix.round(4))
print("Covariance matrix:")
print(covariance_matrix.round(6))
print("Strongest absolute relationship:", correlation_matrix.abs().where(~np.eye(len(feature_columns), dtype=bool)).max().max().round(4))""",
        ["Manual covariance", "Manual correlation", "Correlation matrix", "Covariance matrix", "Strongest absolute relationship"],
        ["corr", "cov", "correlation_matrix"],
    ),
    _grad_spec(
        7,
        "Probability As Counting With Indicator Variables",
        "vectors and relationship matrices from Lesson 6",
        "indicator variables, event counts, and empirical probabilities",
        "event probabilities computed from binary financial flags",
        "indicator vector",
        "P(A) = count(A) / n = sum(I_A) / n",
        "default_probability = default_indicator.___()",
        "mean",
        "The mean of a 0/1 indicator equals the event probability.",
        "Use binary flags to compute empirical probabilities from data.",
        _COMMON_FINANCIAL_DATA_CODE + """
default_indicator = financials["default_flag"]
fraud_indicator = financials["fraud_flag"]

default_probability = default_indicator.mean()
fraud_probability = fraud_indicator.mean()

print("Default event count:", int(default_indicator.sum()))
print("Default probability:", round(default_probability, 4))
print("Fraud probability:", round(fraud_probability, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
default_indicator = financials["default_flag"]
fraud_indicator = financials["fraud_flag"]
churn_indicator = financials["churn_flag"]
high_debt_indicator = (financials["debt_to_assets"] > 0.50).astype(int)

print("Default event count:", int(default_indicator.sum()))
print("Default probability:", round(default_indicator.mean(), 4))
print("Fraud probability:", round(fraud_indicator.mean(), 4))
print("Churn probability:", round(churn_indicator.mean(), 4))
print("High debt probability:", round(high_debt_indicator.mean(), 4))
print("Joint default and high debt probability:", round(((default_indicator == 1) & (high_debt_indicator == 1)).mean(), 4))""",
        ["Default event count", "Default probability", "Fraud probability", "Churn probability", "High debt probability", "Joint default and high debt probability"],
        ["default_indicator", "mean", "astype"],
    ),
    _grad_spec(
        8,
        "Conditional Probability And Bayes Rule With Masks",
        "indicator-event probabilities from Lesson 7",
        "conditional probability, intersections, masks, and Bayes rule",
        "conditional default probabilities for financial subgroups",
        "conditional probability",
        "P(A | B) = P(A and B) / P(B)",
        "conditional_default = joint_probability ___ high_debt_probability",
        "/",
        "Conditional probability divides the joint event probability by the conditioning event probability.",
        "Use pandas masks to compute conditional default probabilities.",
        _COMMON_FINANCIAL_DATA_CODE + """
default = financials["default_flag"] == 1
high_debt = financials["debt_to_assets"] > 0.50

joint_probability = (default & high_debt).mean()
high_debt_probability = high_debt.mean()
conditional_default = joint_probability / high_debt_probability

print("P(default and high debt):", round(joint_probability, 4))
print("P(high debt):", round(high_debt_probability, 4))
print("P(default | high debt):", round(conditional_default, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
default = financials["default_flag"] == 1
high_debt = financials["debt_to_assets"] > 0.50
fraud = financials["fraud_flag"] == 1

p_default = default.mean()
p_high_debt = high_debt.mean()
p_joint = (default & high_debt).mean()
p_default_given_high_debt = p_joint / p_high_debt
p_high_debt_given_default = p_joint / p_default
p_fraud_given_default = (fraud & default).mean() / p_default

print("P(default):", round(p_default, 4))
print("P(high debt):", round(p_high_debt, 4))
print("P(default and high debt):", round(p_joint, 4))
print("P(default | high debt):", round(p_default_given_high_debt, 4))
print("P(high debt | default):", round(p_high_debt_given_default, 4))
print("P(fraud | default):", round(p_fraud_given_default, 4))""",
        ["P(default)", "P(high debt)", "P(default and high debt)", "P(default | high debt)", "P(high debt | default)", "P(fraud | default)"],
        ["p_default_given_high_debt", "p_joint", "high_debt"],
    ),
    _grad_spec(
        9,
        "Random Variables, Expected Value, And Variance",
        "event probabilities and conditional probabilities from Lesson 8",
        "discrete random variables, probability mass functions, expected value, and variance",
        "expected financial outcome and variance from scenario probabilities",
        "discrete random variable",
        "E[X] = sum x_i p_i and Var(X) = sum p_i (x_i - E[X])^2",
        "expected_value = (outcomes * probabilities).___()",
        "sum",
        "Expected value is the probability-weighted sum of possible outcomes.",
        "Compute expected margin impact from a scenario table.",
        """import numpy as np
import pandas as pd

scenarios = pd.DataFrame({
    "scenario": ["stress", "base", "upside"],
    "probability": [0.25, 0.55, 0.20],
    "margin_change": [-0.06, 0.02, 0.08],
})

outcomes = scenarios["margin_change"].to_numpy()
probabilities = scenarios["probability"].to_numpy()
expected_value = (outcomes * probabilities).sum()
variance = (probabilities * (outcomes - expected_value) ** 2).sum()

print("Expected margin change:", round(expected_value, 4))
print("Scenario variance:", round(variance, 6))""",
        """import numpy as np
import pandas as pd

scenarios = pd.DataFrame({
    "scenario": ["stress", "base", "upside"],
    "probability": [0.25, 0.55, 0.20],
    "margin_change": [-0.06, 0.02, 0.08],
    "loss_amount": [90000, 20000, 0],
})

outcomes = scenarios["margin_change"].to_numpy()
losses = scenarios["loss_amount"].to_numpy()
probabilities = scenarios["probability"].to_numpy()

expected_margin_change = (outcomes * probabilities).sum()
margin_variance = (probabilities * (outcomes - expected_margin_change) ** 2).sum()
expected_loss = (losses * probabilities).sum()
loss_variance = (probabilities * (losses - expected_loss) ** 2).sum()

print("Expected margin change:", round(expected_margin_change, 4))
print("Margin variance:", round(margin_variance, 6))
print("Expected loss:", round(expected_loss, 2))
print("Loss variance:", round(loss_variance, 2))
print("Probability check:", round(probabilities.sum(), 6))""",
        ["Expected margin change", "Margin variance", "Expected loss", "Loss variance", "Probability check"],
        ["expected_margin_change", "probabilities", "loss_variance"],
    ),
    _grad_spec(
        10,
        "Bernoulli And Binomial Models",
        "random variables and expected value from Lesson 9",
        "Bernoulli trials, binomial counts, and count probabilities",
        "default-count probabilities and expected default counts",
        "Bernoulli and binomial model",
        "X ~ Binomial(n, p), E[X] = np, Var(X) = np(1 - p)",
        "expected_defaults = n_trials ___ p_default",
        "*",
        "For a binomial count, the expected count is n times p.",
        "Model defaults as 0/1 Bernoulli trials and a binomial count.",
        _COMMON_FINANCIAL_DATA_CODE + """
from math import comb

p_default = financials["default_flag"].mean()
n_trials = len(financials)
expected_defaults = n_trials * p_default
variance_defaults = n_trials * p_default * (1 - p_default)
prob_two_defaults = comb(n_trials, 2) * (p_default ** 2) * ((1 - p_default) ** (n_trials - 2))

print("Default probability p:", round(p_default, 4))
print("Expected default count:", round(expected_defaults, 4))
print("Default count variance:", round(variance_defaults, 4))
print("P(exactly 2 defaults):", round(prob_two_defaults, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
from math import comb

p_default = financials["default_flag"].mean()
n_trials = len(financials)

def binomial_probability(n, k, p):
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

expected_defaults = n_trials * p_default
variance_defaults = n_trials * p_default * (1 - p_default)
prob_zero_defaults = binomial_probability(n_trials, 0, p_default)
prob_two_defaults = binomial_probability(n_trials, 2, p_default)
prob_at_least_one = 1 - prob_zero_defaults

print("Default probability p:", round(p_default, 4))
print("Expected default count:", round(expected_defaults, 4))
print("Default count variance:", round(variance_defaults, 4))
print("P(exactly 2 defaults):", round(prob_two_defaults, 4))
print("P(at least 1 default):", round(prob_at_least_one, 4))""",
        ["Default probability p", "Expected default count", "Default count variance", "P(exactly 2 defaults)", "P(at least 1 default)"],
        ["binomial_probability", "comb", "expected_defaults"],
    ),
    _grad_spec(
        11,
        "Normal, Poisson, And Gamma Models",
        "Bernoulli and binomial distribution thinking from Lesson 10",
        "distribution choice for continuous values, counts, and positive severities",
        "simulated normal, Poisson, and Gamma financial variables",
        "distribution family",
        "normal for continuous measurements, Poisson for counts, Gamma for positive skewed amounts",
        "poisson_counts = rng.___(lam=transaction_rate, size=1000)",
        "poisson",
        "NumPy's generator can simulate Poisson counts.",
        "Simulate candidate distributions for financial metrics.",
        """import numpy as np

rng = np.random.default_rng(42)
normal_growth = rng.normal(loc=0.045, scale=0.047, size=1000)
poisson_counts = rng.poisson(lam=42, size=1000)
gamma_losses = rng.gamma(shape=2.0, scale=20000, size=1000)

print("Normal mean:", round(normal_growth.mean(), 4))
print("Poisson count mean:", round(poisson_counts.mean(), 4))
print("Gamma loss mean:", round(gamma_losses.mean(), 2))""",
        """import numpy as np

rng = np.random.default_rng(42)
normal_growth = rng.normal(loc=0.045, scale=0.047, size=1000)
poisson_counts = rng.poisson(lam=42, size=1000)
gamma_losses = rng.gamma(shape=2.0, scale=20000, size=1000)

print("Normal mean:", round(normal_growth.mean(), 4))
print("Normal std:", round(normal_growth.std(ddof=1), 4))
print("Poisson count mean:", round(poisson_counts.mean(), 4))
print("Poisson count variance:", round(poisson_counts.var(ddof=1), 4))
print("Gamma loss mean:", round(gamma_losses.mean(), 2))
print("Gamma loss 95th percentile:", round(np.quantile(gamma_losses, 0.95), 2))""",
        ["Normal mean", "Normal std", "Poisson count mean", "Poisson count variance", "Gamma loss mean", "Gamma loss 95th percentile"],
        ["normal", "poisson", "gamma"],
    ),
    _grad_spec(
        12,
        "Simulation And The Central Limit Theorem",
        "distribution families from Lesson 11",
        "repeated sampling, sampling distributions, and CLT behavior",
        "a simulated sampling distribution of sample means",
        "sampling distribution",
        "as sample size grows, the distribution of sample means becomes more stable and often more normal",
        "sample_means.append(sample.___())",
        "mean",
        "Each simulation stores one sample mean.",
        "Simulate many sample means from a skewed distribution.",
        """import numpy as np

rng = np.random.default_rng(7)
population = rng.gamma(shape=2.0, scale=20000, size=50000)
sample_means = []
for _ in range(1000):
    sample = rng.choice(population, size=30, replace=True)
    sample_means.append(sample.mean())

sample_means = np.array(sample_means)
print("Population mean:", round(population.mean(), 2))
print("Mean of sample means:", round(sample_means.mean(), 2))
print("Std of sample means:", round(sample_means.std(ddof=1), 2))""",
        """import numpy as np

rng = np.random.default_rng(7)
population = rng.gamma(shape=2.0, scale=20000, size=50000)

def simulated_sample_means(population, sample_size, repetitions):
    means = []
    for _ in range(repetitions):
        sample = rng.choice(population, size=sample_size, replace=True)
        means.append(sample.mean())
    return np.array(means)

means_10 = simulated_sample_means(population, 10, 1000)
means_50 = simulated_sample_means(population, 50, 1000)

print("Population mean:", round(population.mean(), 2))
print("Mean of sample means n=10:", round(means_10.mean(), 2))
print("Std of sample means n=10:", round(means_10.std(ddof=1), 2))
print("Mean of sample means n=50:", round(means_50.mean(), 2))
print("Std of sample means n=50:", round(means_50.std(ddof=1), 2))""",
        ["Population mean", "Mean of sample means n=10", "Std of sample means n=10", "Mean of sample means n=50", "Std of sample means n=50"],
        ["simulated_sample_means", "rng.choice", "sample.mean"],
    ),
    _grad_spec(
        13,
        "Estimators, Bias, Variance, And Sampling Error",
        "sampling distributions from Lesson 12",
        "estimator behavior, bias, variance, and sampling error",
        "repeated estimates compared with a known population parameter",
        "estimator distribution",
        "bias(theta_hat) = E[theta_hat] - theta and Var(theta_hat) measures estimator spread",
        "bias = estimates.mean() ___ true_mean",
        "-",
        "Bias is average estimate minus the true parameter.",
        "Estimate average revenue growth repeatedly and measure estimator behavior.",
        """import numpy as np

rng = np.random.default_rng(9)
population = rng.normal(loc=0.05, scale=0.04, size=100000)
true_mean = population.mean()
estimates = np.array([rng.choice(population, size=25).mean() for _ in range(1000)])

print("True mean:", round(true_mean, 6))
print("Average estimate:", round(estimates.mean(), 6))
print("Estimator bias:", round(estimates.mean() - true_mean, 6))
print("Estimator variance:", round(estimates.var(ddof=1), 8))""",
        """import numpy as np

rng = np.random.default_rng(9)
population = rng.normal(loc=0.05, scale=0.04, size=100000)
true_mean = population.mean()

estimates_10 = np.array([rng.choice(population, size=10).mean() for _ in range(1000)])
estimates_50 = np.array([rng.choice(population, size=50).mean() for _ in range(1000)])

bias_10 = estimates_10.mean() - true_mean
bias_50 = estimates_50.mean() - true_mean

print("True mean:", round(true_mean, 6))
print("Average estimate n=10:", round(estimates_10.mean(), 6))
print("Estimator bias n=10:", round(bias_10, 6))
print("Estimator variance n=10:", round(estimates_10.var(ddof=1), 8))
print("Average estimate n=50:", round(estimates_50.mean(), 6))
print("Estimator variance n=50:", round(estimates_50.var(ddof=1), 8))""",
        ["True mean", "Average estimate n=10", "Estimator bias n=10", "Estimator variance n=10", "Average estimate n=50", "Estimator variance n=50"],
        ["estimates_10", "bias_10", "var(ddof=1)"],
    ),
    _grad_spec(
        14,
        "Method Of Moments",
        "sample moments and estimator behavior from Lesson 13",
        "parameter estimation by matching sample moments to model moments",
        "method-of-moments estimates for normal and Gamma parameters",
        "moment estimator",
        "match sample mean and variance to theoretical mean and variance",
        "gamma_shape = sample_mean ** 2 ___ sample_variance",
        "/",
        "For a Gamma model, shape can be estimated by mean squared divided by variance.",
        "Use sample moments to estimate distribution parameters.",
        """import numpy as np

losses = np.array([25000, 42000, 18000, 76000, 53000, 31000, 88000, 47000])
sample_mean = losses.mean()
sample_variance = losses.var(ddof=1)
gamma_shape = sample_mean ** 2 / sample_variance
gamma_scale = sample_variance / sample_mean

print("Sample mean:", round(sample_mean, 2))
print("Sample variance:", round(sample_variance, 2))
print("Gamma shape estimate:", round(gamma_shape, 4))
print("Gamma scale estimate:", round(gamma_scale, 2))""",
        """import numpy as np

losses = np.array([25000, 42000, 18000, 76000, 53000, 31000, 88000, 47000])
growth = np.array([0.08, 0.03, 0.11, -0.02, 0.06, 0.01, 0.14, 0.04])

loss_mean = losses.mean()
loss_variance = losses.var(ddof=1)
gamma_shape = loss_mean ** 2 / loss_variance
gamma_scale = loss_variance / loss_mean
normal_mu = growth.mean()
normal_sigma = growth.std(ddof=1)

print("Loss sample mean:", round(loss_mean, 2))
print("Loss sample variance:", round(loss_variance, 2))
print("Gamma shape estimate:", round(gamma_shape, 4))
print("Gamma scale estimate:", round(gamma_scale, 2))
print("Normal mu estimate:", round(normal_mu, 6))
print("Normal sigma estimate:", round(normal_sigma, 6))""",
        ["Loss sample mean", "Loss sample variance", "Gamma shape estimate", "Gamma scale estimate", "Normal mu estimate", "Normal sigma estimate"],
        ["gamma_shape", "gamma_scale", "normal_mu"],
    ),
    _grad_spec(
        15,
        "Maximum Likelihood Estimation",
        "probability models and moment estimators from Lesson 14",
        "likelihood, log-likelihood, and parameter search",
        "MLE estimates for Bernoulli and normal models",
        "likelihood function",
        "choose parameters that make the observed data most likely",
        "log_likelihood = (y * np.log(p) + (1 - y) * np.log(1 - p)).___()",
        "sum",
        "The Bernoulli log-likelihood sums observation-level log probabilities.",
        "Estimate default probability and normal growth parameters by likelihood.",
        _COMMON_FINANCIAL_DATA_CODE + """
y = financials["default_flag"].to_numpy()
p_hat = y.mean()
log_likelihood = (y * np.log(p_hat) + (1 - y) * np.log(1 - p_hat)).sum()

growth = financials["revenue_growth"].to_numpy()
mu_hat = growth.mean()
sigma_hat = np.sqrt(((growth - mu_hat) ** 2).mean())

print("Bernoulli MLE p:", round(p_hat, 4))
print("Bernoulli log likelihood:", round(log_likelihood, 4))
print("Normal MLE mu:", round(mu_hat, 6))
print("Normal MLE sigma:", round(sigma_hat, 6))""",
        _COMMON_FINANCIAL_DATA_CODE + """
y = financials["default_flag"].to_numpy()
p_hat = y.mean()
p_grid = np.linspace(0.05, 0.95, 19)
log_likelihoods = []
for p in p_grid:
    ll = (y * np.log(p) + (1 - y) * np.log(1 - p)).sum()
    log_likelihoods.append(ll)
best_grid_p = p_grid[int(np.argmax(log_likelihoods))]

growth = financials["revenue_growth"].to_numpy()
mu_hat = growth.mean()
sigma_hat = np.sqrt(((growth - mu_hat) ** 2).mean())

print("Bernoulli MLE p:", round(p_hat, 4))
print("Best grid p:", round(best_grid_p, 4))
print("Bernoulli log likelihood:", round(max(log_likelihoods), 4))
print("Normal MLE mu:", round(mu_hat, 6))
print("Normal MLE sigma:", round(sigma_hat, 6))""",
        ["Bernoulli MLE p", "Best grid p", "Bernoulli log likelihood", "Normal MLE mu", "Normal MLE sigma"],
        ["log_likelihoods", "np.log", "p_grid"],
    ),
    _grad_spec(
        16,
        "Confidence Intervals",
        "estimators and standard errors from Lesson 13",
        "confidence intervals for means and proportions",
        "interval estimates for margin and default rate",
        "confidence interval",
        "estimate +/- critical_value * standard_error",
        "margin = 1.96 ___ standard_error",
        "*",
        "A normal-approximation interval uses critical value times standard error.",
        "Build intervals around sample estimates.",
        _COMMON_FINANCIAL_DATA_CODE + """
margin = financials["gross_margin"]
estimate = margin.mean()
standard_error = margin.std(ddof=1) / np.sqrt(len(margin))
interval_margin = 1.96 * standard_error

print("Margin mean estimate:", round(estimate, 4))
print("Margin standard error:", round(standard_error, 6))
print("Margin CI low:", round(estimate - interval_margin, 4))
print("Margin CI high:", round(estimate + interval_margin, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
margin = financials["gross_margin"]
default = financials["default_flag"]

mean_estimate = margin.mean()
mean_standard_error = margin.std(ddof=1) / np.sqrt(len(margin))
mean_margin = 1.96 * mean_standard_error

p_hat = default.mean()
prop_standard_error = np.sqrt(p_hat * (1 - p_hat) / len(default))
prop_margin = 1.96 * prop_standard_error

print("Margin mean estimate:", round(mean_estimate, 4))
print("Margin CI low:", round(mean_estimate - mean_margin, 4))
print("Margin CI high:", round(mean_estimate + mean_margin, 4))
print("Default rate estimate:", round(p_hat, 4))
print("Default CI low:", round(p_hat - prop_margin, 4))
print("Default CI high:", round(p_hat + prop_margin, 4))""",
        ["Margin mean estimate", "Margin CI low", "Margin CI high", "Default rate estimate", "Default CI low", "Default CI high"],
        ["standard_error", "1.96", "p_hat"],
    ),
    _grad_spec(
        17,
        "Hypothesis Test Anatomy",
        "confidence intervals and estimators from Lesson 16",
        "null hypothesis, alternative hypothesis, test statistic, and decision rule",
        "a coded one-sample test skeleton",
        "hypothesis test",
        "test_statistic = (estimate - null_value) / standard_error",
        "test_statistic = (estimate - null_value) ___ standard_error",
        "/",
        "A test statistic divides distance from the null by the standard error.",
        "Write the skeleton of a one-sample mean test.",
        _COMMON_FINANCIAL_DATA_CODE + """
values = financials["gross_margin"]
null_value = 0.35
estimate = values.mean()
standard_error = values.std(ddof=1) / np.sqrt(len(values))
test_statistic = (estimate - null_value) / standard_error

print("H0 mean margin:", null_value)
print("Sample estimate:", round(estimate, 4))
print("Standard error:", round(standard_error, 6))
print("Test statistic:", round(test_statistic, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
values = financials["gross_margin"]
null_value = 0.35
estimate = values.mean()
standard_error = values.std(ddof=1) / np.sqrt(len(values))
test_statistic = (estimate - null_value) / standard_error
reject_rule = abs(test_statistic) > 1.96

print("H0 mean margin:", null_value)
print("HA mean margin not equal:", null_value)
print("Sample estimate:", round(estimate, 4))
print("Standard error:", round(standard_error, 6))
print("Test statistic:", round(test_statistic, 4))
print("Reject at rough 5 percent rule:", bool(reject_rule))""",
        ["H0 mean margin", "HA mean margin not equal", "Sample estimate", "Standard error", "Test statistic", "Reject at rough 5 percent rule"],
        ["test_statistic", "null_value", "standard_error"],
    ),
    _grad_spec(
        18,
        "One-Sample And Two-Sample Mean Tests",
        "hypothesis test anatomy from Lesson 17",
        "one-sample, two-sample, and paired mean-test statistics",
        "manual mean-test statistics for financial groups",
        "mean test statistic",
        "t = (x_bar - mu_0) / SE and t_two_sample = (x1_bar - x2_bar) / SE_difference",
        "difference = group_a.mean() ___ group_b.mean()",
        "-",
        "Two-sample tests start with a difference in group means.",
        "Compare gross margins across segments with manual t-style statistics.",
        _COMMON_FINANCIAL_DATA_CODE + """
saas = financials.loc[financials["segment"] == "SaaS", "gross_margin"]
lending = financials.loc[financials["segment"] == "Lending", "gross_margin"]
difference = saas.mean() - lending.mean()
se_difference = np.sqrt(saas.var(ddof=1) / len(saas) + lending.var(ddof=1) / len(lending))
t_statistic = difference / se_difference

print("SaaS mean margin:", round(saas.mean(), 4))
print("Lending mean margin:", round(lending.mean(), 4))
print("Mean difference:", round(difference, 4))
print("Two-sample t statistic:", round(t_statistic, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
saas = financials.loc[financials["segment"] == "SaaS", "gross_margin"]
lending = financials.loc[financials["segment"] == "Lending", "gross_margin"]
payments = financials.loc[financials["segment"] == "Payments", "gross_margin"]

one_sample_null = 0.35
one_sample_se = financials["gross_margin"].std(ddof=1) / np.sqrt(len(financials))
one_sample_t = (financials["gross_margin"].mean() - one_sample_null) / one_sample_se

difference = saas.mean() - lending.mean()
se_difference = np.sqrt(saas.var(ddof=1) / len(saas) + lending.var(ddof=1) / len(lending))
two_sample_t = difference / se_difference

print("One-sample t statistic:", round(one_sample_t, 4))
print("SaaS mean margin:", round(saas.mean(), 4))
print("Lending mean margin:", round(lending.mean(), 4))
print("Payments mean margin:", round(payments.mean(), 4))
print("Mean difference:", round(difference, 4))
print("Two-sample t statistic:", round(two_sample_t, 4))""",
        ["One-sample t statistic", "SaaS mean margin", "Lending mean margin", "Payments mean margin", "Mean difference", "Two-sample t statistic"],
        ["two_sample_t", "se_difference", "group"],
    ),
    _grad_spec(
        19,
        "Proportion Tests And Chi-Square Tests",
        "Bernoulli/binomial models and hypothesis testing from Lessons 10 and 17",
        "proportion tests, expected counts, and chi-square test statistics",
        "manual tests for event rates and category counts",
        "proportion and chi-square statistic",
        "z = (p_hat - p0) / sqrt(p0(1-p0)/n) and chi_square = sum((observed - expected)^2 / expected)",
        "chi_square = (((observed - expected) ** 2) / expected).___()",
        "sum",
        "A chi-square statistic sums scaled squared count differences.",
        "Test default-rate and segment-count patterns.",
        _COMMON_FINANCIAL_DATA_CODE + """
p0 = 0.10
events = financials["default_flag"]
p_hat = events.mean()
se_null = np.sqrt(p0 * (1 - p0) / len(events))
z_statistic = (p_hat - p0) / se_null

observed = financials["segment"].value_counts().sort_index().to_numpy()
expected = np.repeat(len(financials) / len(observed), len(observed))
chi_square = (((observed - expected) ** 2) / expected).sum()

print("Default p_hat:", round(p_hat, 4))
print("Proportion z statistic:", round(z_statistic, 4))
print("Chi-square statistic:", round(chi_square, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
p0 = 0.10
events = financials["default_flag"]
p_hat = events.mean()
se_null = np.sqrt(p0 * (1 - p0) / len(events))
z_statistic = (p_hat - p0) / se_null

observed = financials["segment"].value_counts().sort_index()
expected = pd.Series(np.repeat(len(financials) / len(observed), len(observed)), index=observed.index)
chi_square = (((observed - expected) ** 2) / expected).sum()

print("Default p_hat:", round(p_hat, 4))
print("Null default rate:", p0)
print("Proportion z statistic:", round(z_statistic, 4))
print("Observed segment counts:")
print(observed)
print("Expected segment counts:")
print(expected.round(4))
print("Chi-square statistic:", round(chi_square, 4))""",
        ["Default p_hat", "Null default rate", "Proportion z statistic", "Observed segment counts", "Expected segment counts", "Chi-square statistic"],
        ["chi_square", "p_hat", "observed"],
    ),
    _grad_spec(
        20,
        "P-Values, Power, Effect Size, And Practical Significance",
        "test statistics from Lessons 17 to 19",
        "p-value approximation, effect size, simulation power, and practical significance",
        "a statistical result separated from a financial decision threshold",
        "p-value, power, and effect size",
        "p-value measures extremeness under H0; effect size measures magnitude; power measures detection probability",
        "cohens_d = difference ___ pooled_std",
        "/",
        "Cohen's d divides a mean difference by pooled standard deviation.",
        "Compute approximate p-values, effect size, and simulated power.",
        _COMMON_FINANCIAL_DATA_CODE + """
import math

saas = financials.loc[financials["segment"] == "SaaS", "gross_margin"]
lending = financials.loc[financials["segment"] == "Lending", "gross_margin"]
difference = saas.mean() - lending.mean()
pooled_std = np.sqrt((saas.var(ddof=1) + lending.var(ddof=1)) / 2)
cohens_d = difference / pooled_std
z_like = difference / np.sqrt(saas.var(ddof=1) / len(saas) + lending.var(ddof=1) / len(lending))
p_value_approx = math.erfc(abs(z_like) / np.sqrt(2))

print("Mean difference:", round(difference, 4))
print("Cohen d:", round(cohens_d, 4))
print("Approx p-value:", round(p_value_approx, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
import math

saas = financials.loc[financials["segment"] == "SaaS", "gross_margin"]
lending = financials.loc[financials["segment"] == "Lending", "gross_margin"]
difference = saas.mean() - lending.mean()
pooled_std = np.sqrt((saas.var(ddof=1) + lending.var(ddof=1)) / 2)
cohens_d = difference / pooled_std
z_like = difference / np.sqrt(saas.var(ddof=1) / len(saas) + lending.var(ddof=1) / len(lending))
p_value_approx = math.erfc(abs(z_like) / np.sqrt(2))
practical_threshold = 0.03
practically_large = abs(difference) >= practical_threshold

rng = np.random.default_rng(123)
detected = 0
for _ in range(500):
    simulated_a = rng.normal(0.42, pooled_std, size=20)
    simulated_b = rng.normal(0.38, pooled_std, size=20)
    simulated_diff = simulated_a.mean() - simulated_b.mean()
    simulated_se = np.sqrt(simulated_a.var(ddof=1) / 20 + simulated_b.var(ddof=1) / 20)
    detected += abs(simulated_diff / simulated_se) > 1.96
power_estimate = detected / 500

print("Mean difference:", round(difference, 4))
print("Cohen d:", round(cohens_d, 4))
print("Approx p-value:", round(p_value_approx, 4))
print("Practically large:", bool(practically_large))
print("Simulated power:", round(power_estimate, 4))""",
        ["Mean difference", "Cohen d", "Approx p-value", "Practically large", "Simulated power"],
        ["cohens_d", "p_value_approx", "power_estimate"],
    ),
    _grad_spec(
        21,
        "Simple Linear Regression From Covariance",
        "covariance and hypothesis-testing interpretation from earlier lessons",
        "simple regression slope, intercept, fitted values, and residuals",
        "a one-predictor regression model computed manually",
        "simple linear regression",
        "slope = cov(x, y) / var(x), intercept = y_bar - slope * x_bar",
        "slope = covariance_xy ___ variance_x",
        "/",
        "The simple regression slope is covariance divided by predictor variance.",
        "Compute a regression of next-quarter margin on gross margin.",
        _COMMON_FINANCIAL_DATA_CODE + """
x = financials["gross_margin"].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
covariance_xy = ((x - x.mean()) * (y - y.mean())).sum() / (len(x) - 1)
variance_x = x.var(ddof=1)
slope = covariance_xy / variance_x
intercept = y.mean() - slope * x.mean()
fitted = intercept + slope * x
residuals = y - fitted

print("Regression slope:", round(slope, 4))
print("Regression intercept:", round(intercept, 4))
print("Residual mean:", round(residuals.mean(), 10))""",
        _COMMON_FINANCIAL_DATA_CODE + """
x = financials["gross_margin"].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
covariance_xy = ((x - x.mean()) * (y - y.mean())).sum() / (len(x) - 1)
variance_x = x.var(ddof=1)
slope = covariance_xy / variance_x
intercept = y.mean() - slope * x.mean()
fitted = intercept + slope * x
residuals = y - fitted
sse = (residuals ** 2).sum()

print("Regression slope:", round(slope, 4))
print("Regression intercept:", round(intercept, 4))
print("First fitted value:", round(fitted[0], 4))
print("Residual mean:", round(residuals.mean(), 10))
print("SSE:", round(sse, 6))""",
        ["Regression slope", "Regression intercept", "First fitted value", "Residual mean", "SSE"],
        ["slope", "intercept", "residuals"],
    ),
    _grad_spec(
        22,
        "Matrix Algebra For Ordinary Least Squares",
        "simple regression objects from Lesson 21",
        "design matrix, coefficient vector, normal equations, and OLS solution",
        "beta_hat computed with NumPy matrix algebra",
        "OLS coefficient vector",
        "beta_hat = (X'X)^(-1) X'y",
        "beta_hat = np.linalg.___(X_design.T @ X_design) @ X_design.T @ y",
        "pinv",
        "pinv gives a stable matrix inverse-like solution for OLS.",
        "Compute OLS coefficients with an intercept column.",
        _COMMON_FINANCIAL_DATA_CODE + """
X = financials[["gross_margin"]].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
intercept_column = np.ones((len(X), 1))
X_design = np.column_stack([intercept_column, X])
beta_hat = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y

print("Beta hat:", np.round(beta_hat, 4))
print("Intercept:", round(beta_hat[0], 4))
print("Gross margin coefficient:", round(beta_hat[1], 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
X = financials[["gross_margin"]].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
intercept_column = np.ones((len(X), 1))
X_design = np.column_stack([intercept_column, X])
beta_hat = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y
fitted = X_design @ beta_hat
residuals = y - fitted

print("Design matrix shape:", X_design.shape)
print("Beta hat:", np.round(beta_hat, 4))
print("Intercept:", round(beta_hat[0], 4))
print("Gross margin coefficient:", round(beta_hat[1], 4))
print("Residual sum:", round(residuals.sum(), 10))""",
        ["Design matrix shape", "Beta hat", "Intercept", "Gross margin coefficient", "Residual sum"],
        ["X_design", "beta_hat", "np.linalg.pinv"],
    ),
    _grad_spec(
        23,
        "Multiple Regression And Coefficient Interpretation",
        "OLS matrix algebra from Lesson 22",
        "multiple predictors, controls, fitted values, and coefficient interpretation",
        "a multi-factor financial performance model",
        "multiple regression",
        "y = beta_0 + beta_1 x_1 + ... + beta_p x_p + epsilon",
        "fitted = X_design ___ beta_hat",
        "@",
        "The @ operator performs matrix multiplication.",
        "Fit a multiple regression with several financial predictors.",
        _COMMON_FINANCIAL_DATA_CODE + """
X = financials[feature_columns].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta_hat = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y
fitted = X_design @ beta_hat
residuals = y - fitted

print("Coefficient vector:", np.round(beta_hat, 4))
print("Fitted mean:", round(fitted.mean(), 4))
print("Residual std:", round(residuals.std(ddof=1), 6))""",
        _COMMON_FINANCIAL_DATA_CODE + """
X = financials[feature_columns].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta_hat = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y
fitted = X_design @ beta_hat
residuals = y - fitted
coefs = pd.Series(beta_hat[1:], index=feature_columns)

print("Coefficient vector:")
print(np.round(beta_hat, 4))
print("Predictor coefficients:")
print(coefs.round(4))
print("Fitted mean:", round(fitted.mean(), 4))
print("Residual std:", round(residuals.std(ddof=1), 6))
print("Residual sum of squares:", round((residuals ** 2).sum(), 6))""",
        ["Coefficient vector", "Predictor coefficients", "Fitted mean", "Residual std", "Residual sum of squares"],
        ["feature_columns", "coefs", "residuals"],
    ),
    _grad_spec(
        24,
        "Regression Diagnostics",
        "multiple regression residuals from Lesson 23",
        "residual plots, heteroscedasticity checks, multicollinearity checks, and autocorrelation",
        "diagnostic statistics for a fitted regression model",
        "regression diagnostics",
        "diagnostics study residuals, fitted values, predictor relationships, and error structure",
        "residuals = y ___ fitted",
        "-",
        "Residuals are observed response values minus fitted values.",
        "Compute diagnostics from fitted values and residuals.",
        _COMMON_FINANCIAL_DATA_CODE + """
X = financials[feature_columns].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta_hat = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y
fitted = X_design @ beta_hat
residuals = y - fitted
resid_fitted_corr = np.corrcoef(fitted, np.abs(residuals))[0, 1]
predictor_corr = financials[feature_columns].corr().abs()

print("Residual mean:", round(residuals.mean(), 10))
print("Residual-fitted absolute correlation:", round(resid_fitted_corr, 4))
print("Max predictor correlation:", round(predictor_corr.where(~np.eye(len(feature_columns), dtype=bool)).max().max(), 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
X = financials[feature_columns].to_numpy()
y = financials["next_quarter_margin"].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta_hat = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y
fitted = X_design @ beta_hat
residuals = y - fitted
resid_fitted_corr = np.corrcoef(fitted, np.abs(residuals))[0, 1]
predictor_corr = financials[feature_columns].corr().abs()
max_predictor_corr = predictor_corr.where(~np.eye(len(feature_columns), dtype=bool)).max().max()
durbin_watson_like = ((np.diff(residuals) ** 2).sum()) / ((residuals ** 2).sum())

print("Residual mean:", round(residuals.mean(), 10))
print("Residual std:", round(residuals.std(ddof=1), 6))
print("Residual-fitted absolute correlation:", round(resid_fitted_corr, 4))
print("Max predictor correlation:", round(max_predictor_corr, 4))
print("Durbin-Watson style statistic:", round(durbin_watson_like, 4))""",
        ["Residual mean", "Residual std", "Residual-fitted absolute correlation", "Max predictor correlation", "Durbin-Watson style statistic"],
        ["resid_fitted_corr", "predictor_corr", "durbin_watson_like"],
    ),
    _grad_spec(
        25,
        "Logistic And Probit Regression",
        "Bernoulli outcomes and multiple regression from earlier lessons",
        "binary outcome models, logits, probabilities, and link functions",
        "a simple logistic model for a binary financial event",
        "logistic regression",
        "p_i = 1 / (1 + exp(-X_i beta))",
        "probabilities = 1 / (1 + np.___(-linear_score))",
        "exp",
        "The logistic function uses exp to map scores into probabilities.",
        "Fit a tiny logistic model with gradient steps.",
        _COMMON_FINANCIAL_DATA_CODE + """
y = financials["default_flag"].to_numpy()
X = financials[["debt_to_assets", "free_cash_flow_margin"]].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta = np.zeros(X_design.shape[1])
learning_rate = 0.5
for _ in range(500):
    linear_score = X_design @ beta
    probabilities = 1 / (1 + np.exp(-linear_score))
    gradient = X_design.T @ (probabilities - y) / len(y)
    beta -= learning_rate * gradient

print("Logistic beta:", np.round(beta, 4))
print("Predicted probabilities:", np.round(probabilities, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
y = financials["default_flag"].to_numpy()
X = financials[["debt_to_assets", "free_cash_flow_margin"]].to_numpy()
X_design = np.column_stack([np.ones(len(X)), X])
beta = np.zeros(X_design.shape[1])
learning_rate = 0.5

for _ in range(700):
    linear_score = X_design @ beta
    probabilities = 1 / (1 + np.exp(-linear_score))
    gradient = X_design.T @ (probabilities - y) / len(y)
    beta -= learning_rate * gradient

linear_score = X_design @ beta
probabilities = 1 / (1 + np.exp(-linear_score))
predicted_class = (probabilities >= 0.5).astype(int)
accuracy = (predicted_class == y).mean()

print("Logistic beta:", np.round(beta, 4))
print("Predicted probabilities:", np.round(probabilities, 4))
print("Predicted classes:", predicted_class.tolist())
print("Training accuracy:", round(accuracy, 4))
print("Average predicted default probability:", round(probabilities.mean(), 4))""",
        ["Logistic beta", "Predicted probabilities", "Predicted classes", "Training accuracy", "Average predicted default probability"],
        ["np.exp", "gradient", "probabilities"],
    ),
    _grad_spec(
        26,
        "Hierarchical And Mixed-Effects Models",
        "grouped data and regression residuals from Lessons 23 to 25",
        "group-level variation, fixed effects, random-effect intuition, and partial pooling",
        "segment-level effects separated from overall mean behavior",
        "group effects",
        "observed value = overall mean + group effect + residual",
        "group_effects = group_means ___ overall_mean",
        "-",
        "A group effect is a group mean relative to the overall mean.",
        "Estimate segment-level deviations from the overall margin.",
        _COMMON_FINANCIAL_DATA_CODE + """
overall_mean = financials["gross_margin"].mean()
group_means = financials.groupby("segment")["gross_margin"].mean()
group_effects = group_means - overall_mean

print("Overall mean margin:", round(overall_mean, 4))
print("Group means:")
print(group_means.round(4))
print("Group effects:")
print(group_effects.round(4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
overall_mean = financials["gross_margin"].mean()
group_means = financials.groupby("segment")["gross_margin"].mean()
group_counts = financials.groupby("segment")["gross_margin"].count()
group_effects = group_means - overall_mean
shrinkage_weight = group_counts / (group_counts + 5)
partially_pooled_effects = shrinkage_weight * group_effects

print("Overall mean margin:", round(overall_mean, 4))
print("Group means:")
print(group_means.round(4))
print("Group effects:")
print(group_effects.round(4))
print("Shrinkage weights:")
print(shrinkage_weight.round(4))
print("Partially pooled effects:")
print(partially_pooled_effects.round(4))""",
        ["Overall mean margin", "Group means", "Group effects", "Shrinkage weights", "Partially pooled effects"],
        ["groupby", "group_effects", "partially_pooled_effects"],
    ),
    _grad_spec(
        27,
        "PCA, Factor Analysis, And Latent Structure",
        "standardized variables and covariance matrices from Lessons 5 and 6",
        "eigenvalues, eigenvectors, principal components, and factor-loading intuition",
        "a reduced-dimensional representation of financial indicators",
        "principal components",
        "principal components are directions of maximum variance in standardized variables",
        "eigenvalues, eigenvectors = np.linalg.___(correlation_matrix)",
        "eigh",
        "eigh computes eigenvalues and eigenvectors for a symmetric matrix.",
        "Compute PCA from a standardized financial matrix.",
        _COMMON_FINANCIAL_DATA_CODE + """
Z = (financials[feature_columns] - financials[feature_columns].mean()) / financials[feature_columns].std(ddof=1)
correlation_matrix = Z.corr().to_numpy()
eigenvalues, eigenvectors = np.linalg.eigh(correlation_matrix)
order = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[order]
eigenvectors = eigenvectors[:, order]
component_scores = Z.to_numpy() @ eigenvectors

print("Eigenvalues:", np.round(eigenvalues, 4))
print("First component loadings:", np.round(eigenvectors[:, 0], 4))
print("First component scores:", np.round(component_scores[:, 0], 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
Z = (financials[feature_columns] - financials[feature_columns].mean()) / financials[feature_columns].std(ddof=1)
correlation_matrix = Z.corr().to_numpy()
eigenvalues, eigenvectors = np.linalg.eigh(correlation_matrix)
order = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[order]
eigenvectors = eigenvectors[:, order]
component_scores = Z.to_numpy() @ eigenvectors
explained_variance_ratio = eigenvalues / eigenvalues.sum()
loadings = pd.Series(eigenvectors[:, 0], index=feature_columns)

print("Eigenvalues:", np.round(eigenvalues, 4))
print("Explained variance ratio:", np.round(explained_variance_ratio, 4))
print("First component loadings:")
print(loadings.round(4))
print("First component scores:", np.round(component_scores[:, 0], 4))
print("Two-component score shape:", component_scores[:, :2].shape)""",
        ["Eigenvalues", "Explained variance ratio", "First component loadings", "First component scores", "Two-component score shape"],
        ["np.linalg.eigh", "component_scores", "explained_variance_ratio"],
    ),
    _grad_spec(
        28,
        "Clustering, Discriminant Analysis, MANOVA, And SEM Foundations",
        "standardized multivariate structure from Lesson 27",
        "cluster assignment, group separation, multivariate mean comparison, and path thinking",
        "segments and a first structural-equation-style path matrix",
        "multivariate grouping",
        "clusters minimize within-cluster distance; discriminant thinking separates group means; SEM organizes directional paths",
        "distances = np.linalg.___(Z[:, None, :] - centers[None, :, :], axis=2)",
        "norm",
        "Euclidean distance can assign observations to nearest cluster centers.",
        "Cluster standardized financial observations and summarize group separation.",
        _COMMON_FINANCIAL_DATA_CODE + """
Z = ((financials[feature_columns] - financials[feature_columns].mean()) / financials[feature_columns].std(ddof=1)).to_numpy()
centers = Z[[0, 3]].copy()
for _ in range(5):
    distances = np.linalg.norm(Z[:, None, :] - centers[None, :, :], axis=2)
    labels = distances.argmin(axis=1)
    centers = np.array([Z[labels == k].mean(axis=0) for k in range(2)])

print("Cluster labels:", labels.tolist())
print("Cluster centers:")
print(np.round(centers, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
Z_frame = (financials[feature_columns] - financials[feature_columns].mean()) / financials[feature_columns].std(ddof=1)
Z = Z_frame.to_numpy()
centers = Z[[0, 3]].copy()
for _ in range(5):
    distances = np.linalg.norm(Z[:, None, :] - centers[None, :, :], axis=2)
    labels = distances.argmin(axis=1)
    centers = np.array([Z[labels == k].mean(axis=0) for k in range(2)])

clustered = financials.assign(cluster=labels)
cluster_means = clustered.groupby("cluster")[feature_columns].mean()
segment_means = financials.groupby("segment")[feature_columns].mean()
path_matrix = pd.DataFrame(
    [[0, -1, 1], [0, 0, -1], [0, 0, 0]],
    index=["debt_to_assets", "free_cash_flow_margin", "next_quarter_margin"],
    columns=["debt_to_assets", "free_cash_flow_margin", "next_quarter_margin"],
)

print("Cluster labels:", labels.tolist())
print("Cluster centers:")
print(np.round(centers, 4))
print("Cluster means:")
print(cluster_means.round(4))
print("Segment mean matrix:")
print(segment_means.round(4))
print("SEM path matrix:")
print(path_matrix)""",
        ["Cluster labels", "Cluster centers", "Cluster means", "Segment mean matrix", "SEM path matrix"],
        ["np.linalg.norm", "cluster_means", "path_matrix"],
    ),
    _grad_spec(
        29,
        "Bootstrap, Nonparametric Statistics, Bayesian Inference, And MCMC",
        "sampling distributions, estimators, and uncertainty from earlier lessons",
        "bootstrap intervals, permutation logic, Bayesian updating, and MCMC intuition",
        "resampling and posterior estimates for financial metrics",
        "bootstrap and posterior distribution",
        "bootstrap resamples observed data; posterior combines prior information with observed likelihood",
        "bootstrap_sample = rng.___(values, size=len(values), replace=True)",
        "choice",
        "Bootstrap samples draw with replacement from observed values.",
        "Use bootstrap and Bayesian updating to quantify uncertainty.",
        _COMMON_FINANCIAL_DATA_CODE + """
rng = np.random.default_rng(44)
values = financials["gross_margin"].to_numpy()
bootstrap_means = []
for _ in range(1000):
    bootstrap_sample = rng.choice(values, size=len(values), replace=True)
    bootstrap_means.append(bootstrap_sample.mean())
bootstrap_means = np.array(bootstrap_means)

alpha_prior = 2
beta_prior = 8
defaults = financials["default_flag"].sum()
non_defaults = len(financials) - defaults
posterior_alpha = alpha_prior + defaults
posterior_beta = beta_prior + non_defaults
posterior_mean = posterior_alpha / (posterior_alpha + posterior_beta)

print("Bootstrap mean low:", round(np.quantile(bootstrap_means, 0.025), 4))
print("Bootstrap mean high:", round(np.quantile(bootstrap_means, 0.975), 4))
print("Posterior default mean:", round(posterior_mean, 4))""",
        _COMMON_FINANCIAL_DATA_CODE + """
rng = np.random.default_rng(44)
values = financials["gross_margin"].to_numpy()
bootstrap_means = []
for _ in range(1000):
    bootstrap_sample = rng.choice(values, size=len(values), replace=True)
    bootstrap_means.append(bootstrap_sample.mean())
bootstrap_means = np.array(bootstrap_means)

alpha_prior = 2
beta_prior = 8
defaults = financials["default_flag"].sum()
non_defaults = len(financials) - defaults
posterior_alpha = alpha_prior + defaults
posterior_beta = beta_prior + non_defaults
posterior_draws = rng.beta(posterior_alpha, posterior_beta, size=2000)
posterior_mean = posterior_draws.mean()

current = values.mean()
chain = []
for _ in range(200):
    proposal = current + rng.normal(0, 0.005)
    if values.min() <= proposal <= values.max():
        current = proposal
    chain.append(current)

print("Bootstrap mean low:", round(np.quantile(bootstrap_means, 0.025), 4))
print("Bootstrap mean high:", round(np.quantile(bootstrap_means, 0.975), 4))
print("Posterior default mean:", round(posterior_mean, 4))
print("Posterior default low:", round(np.quantile(posterior_draws, 0.025), 4))
print("Posterior default high:", round(np.quantile(posterior_draws, 0.975), 4))
print("MCMC toy chain mean:", round(np.mean(chain), 4))""",
        ["Bootstrap mean low", "Bootstrap mean high", "Posterior default mean", "Posterior default low", "Posterior default high", "MCMC toy chain mean"],
        ["bootstrap_means", "posterior_draws", "chain"],
    ),
    _grad_spec(
        30,
        "Time Series, Forecasting, Ethics, And Final Project",
        "regression, residuals, and uncertainty from the whole module",
        "time index, lagged variables, autocorrelation, AR(1) forecasting, and ethical communication",
        "a final notebook/memo structure with forecast uncertainty and limitations",
        "time-series forecast",
        "y_t = alpha + phi y_{t-1} + error_t",
        "lagged_margin = margins.___(1)",
        "shift",
        "shift(1) creates a one-period lag.",
        "Create lagged data, fit a simple AR(1), and produce a final project outline.",
        """import numpy as np
import pandas as pd

series = pd.DataFrame({
    "quarter": pd.period_range("2024Q1", periods=10, freq="Q").astype(str),
    "gross_margin": [0.34, 0.35, 0.37, 0.36, 0.38, 0.39, 0.41, 0.40, 0.42, 0.43],
})
series["lagged_margin"] = series["gross_margin"].shift(1)
model_data = series.dropna()
x = model_data["lagged_margin"].to_numpy()
y = model_data["gross_margin"].to_numpy()
slope = np.cov(x, y, ddof=1)[0, 1] / x.var(ddof=1)
intercept = y.mean() - slope * x.mean()
forecast = intercept + slope * series["gross_margin"].iloc[-1]

print("AR1 slope:", round(slope, 4))
print("Next forecast:", round(forecast, 4))""",
        """import numpy as np
import pandas as pd

series = pd.DataFrame({
    "quarter": pd.period_range("2024Q1", periods=10, freq="Q").astype(str),
    "gross_margin": [0.34, 0.35, 0.37, 0.36, 0.38, 0.39, 0.41, 0.40, 0.42, 0.43],
})
series["lagged_margin"] = series["gross_margin"].shift(1)
model_data = series.dropna()
x = model_data["lagged_margin"].to_numpy()
y = model_data["gross_margin"].to_numpy()
slope = np.cov(x, y, ddof=1)[0, 1] / x.var(ddof=1)
intercept = y.mean() - slope * x.mean()
fitted = intercept + slope * x
residuals = y - fitted
forecast = intercept + slope * series["gross_margin"].iloc[-1]
forecast_se = residuals.std(ddof=1)

print("Lagged dataset rows:", len(model_data))
print("AR1 intercept:", round(intercept, 4))
print("AR1 slope:", round(slope, 4))
print("Next forecast:", round(forecast, 4))
print("Forecast interval low:", round(forecast - 1.96 * forecast_se, 4))
print("Forecast interval high:", round(forecast + 1.96 * forecast_se, 4))
print("Ethics note:", "Report uncertainty, sample limits, and model assumptions.")""",
        ["Lagged dataset rows", "AR1 intercept", "AR1 slope", "Next forecast", "Forecast interval low", "Forecast interval high", "Ethics note"],
        ["shift", "forecast", "residuals"],
        duration=120,
    ),
]

_GRADUATE_STATS_LESSONS = [LESSON_1_GRADUATE_STATS_REBUILD] + [
    _graduate_lesson(spec) for spec in GRADUATE_STATS_SPECS
]

MODULE_CORE_ANALYTICS_STATISTICS["title"] = "Graduate Statistics For Financial Analysis"
MODULE_CORE_ANALYTICS_STATISTICS["description"] = (
    "A 30-lesson Python/math-first statistics mini-course for financial analysis. "
    "The sequence builds gradually from statistical tables and vectors through "
    "probability, estimation, inference, regression, multivariate methods, "
    "resampling, Bayesian thinking, and time series."
)
MODULE_CORE_ANALYTICS_STATISTICS["lessons"] = _GRADUATE_STATS_LESSONS
MODULE_CORE_ANALYTICS_STATISTICS["concept_map"] = [
    {
        "id": lesson["id"],
        "label": lesson["title"][:42],
        "connects_to": [
            _GRADUATE_STATS_LESSONS[index + 1]["id"]
        ] if index + 1 < len(_GRADUATE_STATS_LESSONS) else [],
    }
    for index, lesson in enumerate(_GRADUATE_STATS_LESSONS)
]


def _deep_stats_questions(spec):
    return [
        {
            "type": "multiple_choice",
            "question": "What object from the prior lesson does this lesson build on?",
            "options": [
                spec["prior_object"],
                "An unrelated finance opinion",
                "Only a memorized definition",
                "A chart that has not been created yet",
            ],
            "answer": 0,
            "explanation": f"This lesson starts from {spec['prior_object']}.",
        },
        {
            "type": "multiple_choice",
            "question": "What is the main new statistical object or operation in this lesson?",
            "options": [
                spec["new_operation"],
                "A disconnected market forecast",
                "A written-only reflection",
                "A badge counter with no statistical meaning",
            ],
            "answer": 0,
            "explanation": f"The new operation is {spec['new_operation']}.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the key syntax from the Learn section.",
            "template": spec["syntax_template"],
            "answer": spec["syntax_answer"],
            "explanation": spec["syntax_explanation"],
        },
        {
            "type": "multiple_choice",
            "question": "Which formula matches the lesson's core calculation?",
            "options": [
                spec["formula"],
                "p-value = model accuracy / row count",
                "X = a written opinion with no data",
                "beta = a product label with no connection to the model",
            ],
            "answer": 0,
            "explanation": "The correct formula is the one tied to the Python object built in the lesson.",
        },
        {
            "type": "multiple_choice",
            "question": "Which Python object should you inspect before trusting the final result?",
            "options": [
                spec["inspection_object"],
                "An unrelated page label",
                "Only the lesson title",
                "Only the final rounded number",
            ],
            "answer": 0,
            "explanation": "Inspecting the intermediate object prevents silent analytical mistakes.",
        },
        {
            "type": "true_false",
            "question": "The lesson's calculation should be connected to the object created immediately before it.",
            "answer": True,
            "explanation": "That is the gradual curriculum rule: each calculation earns the next one.",
        },
        {
            "type": "multiple_choice",
            "question": "Which mistake would most damage this analysis?",
            "options": [
                spec["common_mistake"],
                "Printing a labeled intermediate object",
                "Checking the manual result with pandas or NumPy",
                "Writing a short limitation after the output",
            ],
            "answer": 0,
            "explanation": spec["mistake_explanation"],
        },
        {
            "type": "fill_blank",
            "question": "Complete the first required challenge label.",
            "template": "print(\"___\", value)",
            "answer": spec["first_label"],
            "explanation": f"The challenge should print `{spec['first_label']}`.",
        },
        {
            "type": "multiple_choice",
            "question": "How should the result be interpreted?",
            "options": [
                spec["interpretation"],
                "It proves the future value with certainty.",
                "It matters only because the code ran.",
                "It should be reported without saying what sample produced it.",
            ],
            "answer": 0,
            "explanation": "A strong interpretation names the statistic, the sample, and the limitation.",
        },
        {
            "type": "multiple_choice",
            "question": "What should carry forward into the next lesson?",
            "options": [
                spec["next_bridge"],
                "Nothing; the next lesson should restart from scratch",
                "Only a generic definition",
                "Only the confidence rating",
            ],
            "answer": 0,
            "explanation": "The output of this lesson should become the starting object for the next one.",
        },
        {
            "type": "true_false",
            "question": "A sample calculation is automatically a population fact.",
            "answer": False,
            "explanation": "Sample statistics describe or estimate from observed data; they are not automatic population truths.",
        },
        {
            "type": "multiple_choice",
            "question": "Why does the lesson use a financial dataset?",
            "options": [
                "To give the statistical operation realistic data without replacing the statistical objective",
                "To turn the lesson into investment theory",
                "To avoid writing code",
                "To make every output a business recommendation",
            ],
            "answer": 0,
            "explanation": "Finance supplies the context; statistics remains the skill being learned.",
        },
        {
            "type": "multiple_choice",
            "question": "Which practice habit best matches graduate preparation?",
            "options": [
                "Show the code object, formula, output, and limitation together",
                "Only memorize the name of the method",
                "Skip manual calculation and trust the shortcut immediately",
                "Avoid checking intermediate results",
            ],
            "answer": 0,
            "explanation": "Graduate statistics requires movement between code, notation, and interpretation.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the phrase.",
            "template": "code first, math explained ___",
            "answer": "alongside",
            "explanation": "This is the instructional pattern for the rebuilt curriculum.",
        },
        {
            "type": "true_false",
            "question": "Practice questions should rehearse the exact concepts taught in the Learn section.",
            "answer": True,
            "explanation": "Disconnected practice was one of the problems this pass is correcting.",
        },
        {
            "type": "multiple_choice",
            "question": "Which output is most useful in a notebook?",
            "options": [
                "A labeled output plus a short interpretation",
                "An unlabeled array with no context",
                "A paragraph with no calculation",
                "A claim that no assumptions are needed",
            ],
            "answer": 0,
            "explanation": "Labeled outputs are easier to audit and explain.",
        },
        {
            "type": "multiple_choice",
            "question": "What does the challenge require?",
            "options": [
                spec["challenge_goal"],
                "Only reading the Learn section",
                "Only marking the task done",
                "Only defining vocabulary terms",
            ],
            "answer": 0,
            "explanation": "The challenge asks you to code the same skill taught in Learn.",
        },
        {
            "type": "true_false",
            "question": "A result can be numerically correct but still poorly communicated.",
            "answer": True,
            "explanation": "Graduate work requires both correct calculation and clear communication.",
        },
        {
            "type": "multiple_choice",
            "question": "What is the best reason to write a manual calculation before using a shortcut?",
            "options": [
                "The manual calculation reveals the operation hidden inside the shortcut",
                "The shortcut is always wrong",
                "Manual code is always faster",
                "It removes the need for interpretation",
            ],
            "answer": 0,
            "explanation": "Shortcuts are strongest after the underlying operation is understood.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the object name.",
            "template": "The calculation produces: ___",
            "answer": spec["produced_object"],
            "explanation": f"The calculation produces {spec['produced_object']}.",
        },
        {
            "type": "multiple_choice",
            "question": "What should you check when a vector or statistic looks surprising?",
            "options": [
                spec["debug_check"],
                "Whether an unrelated page label changed",
                "Whether the lesson is long enough",
                "Whether the output has enough decimal places only",
            ],
            "answer": 0,
            "explanation": "The best debug check returns to the data object and calculation chain.",
        },
        {
            "type": "multiple_choice",
            "question": "Which repeatable practice pattern best fits this calculation?",
            "options": [
                f"Inspect {spec['inspection_object']}, print `{spec['first_label']}`, and interpret {spec['produced_object']}",
                "Read the title and skip the code",
                "Use the final label without checking the object",
                "Answer from finance intuition without the statistic",
            ],
            "answer": 0,
            "explanation": "The practice batch should connect inspection, labeled output, and interpretation.",
        },
        {
            "type": "multiple_choice",
            "question": "What does a model answer need to include?",
            "options": [
                "Working code, labeled outputs, and bounded interpretation",
                "Only a final number",
                "Only an essay",
                "Only a library import",
            ],
            "answer": 0,
            "explanation": "Model answers should show how the result is produced and interpreted.",
        },
        {
            "type": "fill_blank",
            "question": "Complete the learning chain.",
            "template": spec["chain_template"],
            "answer": spec["chain_answer"],
            "explanation": spec["chain_explanation"],
        },
        {
            "type": "multiple_choice",
            "question": "Which practice task best prepares the challenge?",
            "options": [
                spec["challenge_goal"],
                "Memorize the lesson title without writing code",
                "Skip the intermediate object and guess the label",
                "Replace the calculation with a finance opinion",
            ],
            "answer": 0,
            "explanation": "The strongest practice item rehearses the same code path required by the challenge.",
        },
    ]


_LESSON_2_CODE = """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "quarter": ["2026Q1"] * 6,
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34],
})

growth_series = financials["revenue_growth"]
margin_series = financials["gross_margin"]
balance_proxy = financials["gross_margin"] * 1000

growth_vector = growth_series.to_numpy()
margin_vector = margin_series.to_numpy()
balance_vector = balance_proxy.to_numpy()

derived_spread = margin_vector - growth_vector
scaled_balance = balance_vector / 1000
positive_growth_mask = growth_vector > 0
masked_margin_average = margin_vector[positive_growth_mask].mean()
alignment_check = len(growth_vector) == len(margin_vector) == len(balance_vector)

print("Series index:", growth_series.index.to_list())
print("Growth vector:", np.round(growth_vector, 4))
print("Margin vector:", np.round(margin_vector, 4))
print("Derived spread vector:", np.round(derived_spread, 4))
print("Scaled balance vector:", np.round(scaled_balance, 4))
print("Positive growth mask:", positive_growth_mask.astype(int).tolist())
print("Masked margin average:", round(masked_margin_average, 4))
print("Alignment check:", alignment_check)
print("Next lesson bridge:", "aligned vectors can now be summed and averaged")"""


_LESSON_3_CODE = """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "customer_balance": [1200, 850, 1600, 740, 1100, 910],
    "transaction_count": [42, 37, 58, 24, 45, 31],
})

values = financials["revenue_growth"].to_numpy()
balance_weights = financials["customer_balance"].to_numpy()
transaction_weights = financials["transaction_count"].to_numpy()

def arithmetic_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def weighted_mean(values, weights):
    values = np.asarray(values)
    weights = np.asarray(weights)
    return (values * weights).sum() / weights.sum()

count_n = len(values)
sum_growth = values.sum()
manual_mean = arithmetic_mean(values)
pandas_mean = financials["revenue_growth"].mean()
weight_sum = balance_weights.sum()
balance_weighted_mean = weighted_mean(values, balance_weights)
transaction_weighted_mean = weighted_mean(values, transaction_weights)
weighting_difference = balance_weighted_mean - manual_mean

print("Count n:", count_n)
print("Sum revenue growth:", round(sum_growth, 6))
print("Arithmetic mean:", round(manual_mean, 6))
print("Pandas mean check:", round(pandas_mean, 6))
print("Weight sum:", round(weight_sum, 2))
print("Balance-weighted mean:", round(balance_weighted_mean, 6))
print("Transaction-weighted mean:", round(transaction_weighted_mean, 6))
print("Difference due to weights:", round(weighting_difference, 6))
print("Next lesson bridge:", "means become the center used to calculate deviations")"""


_LESSON_4_CODE = """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
})

values = financials["revenue_growth"].to_numpy()
mean_value = values.sum() / len(values)
deviation_vector = values - mean_value
squared_deviations = deviation_vector ** 2
sum_squared_deviations = squared_deviations.sum()
sample_variance = sum_squared_deviations / (len(values) - 1)
population_variance = sum_squared_deviations / len(values)
sample_standard_deviation = sample_variance ** 0.5
pandas_variance_check = financials["revenue_growth"].var(ddof=1)
pandas_std_check = financials["revenue_growth"].std(ddof=1)

print("Mean from prior lesson:", round(mean_value, 6))
print("Deviation vector:", np.round(deviation_vector, 4))
print("Deviation sum check:", round(deviation_vector.sum(), 10))
print("Squared deviations:", np.round(squared_deviations, 6))
print("Sum squared deviations:", round(sum_squared_deviations, 6))
print("Sample variance:", round(sample_variance, 6))
print("Population variance comparison:", round(population_variance, 6))
print("Sample standard deviation:", round(sample_standard_deviation, 6))
print("Pandas variance check:", round(pandas_variance_check, 6))
print("Pandas std check:", round(pandas_std_check, 6))
print("Next lesson bridge:", "standard deviation turns deviations into z-scores")"""


_LESSON_5_CODE = """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "customer_balance": [1200, 850, 1600, 740, 1100, 910],
})

growth = financials["revenue_growth"]
balance = financials["customer_balance"]

growth_z = (growth - growth.mean()) / growth.std(ddof=1)
balance_z = (balance - balance.mean()) / balance.std(ddof=1)
empirical_percentiles = growth.rank(pct=True)
top_quartile_cutoff = growth.quantile(0.75)
high_growth_flags = (growth >= top_quartile_cutoff).astype(int)
standardized_table = pd.DataFrame({
    "company": financials["company"],
    "growth_z": growth_z,
    "balance_z": balance_z,
    "growth_percentile": empirical_percentiles,
    "high_growth_flag": high_growth_flags,
})

print("Growth z-scores:", np.round(growth_z.to_numpy(), 4))
print("Balance z-scores:", np.round(balance_z.to_numpy(), 4))
print("Empirical percentiles:", np.round(empirical_percentiles.to_numpy(), 3))
print("Top quartile cutoff:", round(top_quartile_cutoff, 4))
print("High growth flags:", high_growth_flags.to_list())
print("Standardized mean check:", round(growth_z.mean(), 10))
print("Standardized std check:", round(growth_z.std(ddof=1), 6))
print("Standardized table rows:", len(standardized_table))
print("Next lesson bridge:", "standardized paired vectors are ready for covariance and correlation")"""


LESSON_2_QUALITY_PASS = {
    "id": "casfd-l2",
    "title": "Columns, Series, Vectors, And Elementwise Operations",
    "order": 2,
    "duration_min": 120,
    "difficulty": "beginner",
    "real_world_context": (
        "A financial analyst has already built a table of company-quarter data. "
        "The next step is to select columns, understand the difference between a "
        "pandas Series and a NumPy vector, and use aligned vectors to create derived "
        "financial measurements."
    ),
    "concept": """## Lesson Aim

Lesson 1 taught the table grammar:

```text
DataFrame -> observation -> variable -> Series -> vector -> mean -> variance
```

Lesson 2 slows down the middle of that chain. A graduate statistics course will use
vectors constantly, but in real Python work those vectors usually begin as DataFrame
columns. This lesson teaches that bridge in detail.

The new chain is:

```text
DataFrame -> selected column -> pandas Series -> NumPy vector -> elementwise operation
```

You should finish this lesson able to explain three different things:

1. what a pandas `Series` keeps that a NumPy array does not
2. why elementwise arithmetic depends on aligned observations
3. how a new analytical vector is created from existing financial vectors

## 1. Start From The Same Financial Table

```python
import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "quarter": ["2026Q1"] * 6,
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "gross_margin": [0.42, 0.37, 0.48, 0.31, 0.39, 0.35],
    "debt_to_assets": [0.31, 0.44, 0.28, 0.62, 0.51, 0.47],
    "free_cash_flow_margin": [0.09, 0.04, 0.12, -0.03, 0.06, 0.02],
    "next_quarter_margin": [0.43, 0.36, 0.50, 0.29, 0.40, 0.34],
})
```

Each row is still one company-quarter observation. That row identity matters. If row
3 in one vector refers to Cobalt, then row 3 in another vector must also refer to
Cobalt before you subtract or compare the two vectors.

## 2. Select A Column As A Series

```python
growth_series = financials["revenue_growth"]
print(growth_series)
print(growth_series.index)
print(growth_series.dtype)
```

A pandas `Series` has:

- values
- an index
- a name
- a data type

That extra labeling is useful for data work. The index helps pandas align values. The
dtype tells you whether the column is numeric, text, datetime, boolean, or something
else.

In notation, the values will eventually become:

```text
x = (x_1, x_2, ..., x_n)
```

But do not jump there too soon. First recognize the object in Python.

## 3. Convert The Series To A Vector

```python
growth_vector = growth_series.to_numpy()
print(growth_vector)
```

Now you have the vector:

```text
x = (0.08, 0.03, 0.11, -0.02, 0.06, 0.01)
```

The vector has the numeric values but not the pandas labels. That is fine when you are
doing numerical operations and you already know the order is correct.

The rule is:

```text
Use Series/DataFrame methods when labels and alignment matter.
Use NumPy arrays when you want direct numerical vector operations.
```

## 4. Build A Second Aligned Vector

```python
margin_series = financials["gross_margin"]
margin_vector = margin_series.to_numpy()

print(margin_vector)
```

Now you have two vectors:

```text
x = revenue growth
m = gross margin
```

They are aligned because both were selected from the same DataFrame without changing
row order.

Check that explicitly:

```python
alignment_check = len(growth_vector) == len(margin_vector)
print(alignment_check)
```

Length alone is not enough in all real datasets. Two tables can have the same number
of rows but different order. Later, pandas joins and indexes will matter. In this
lesson, both vectors come from the same table, so row order is safe.

## 5. Elementwise Subtraction

Elementwise subtraction means subtract observation by observation:

```text
d_i = m_i - x_i
```

In code:

```python
margin_growth_spread = margin_vector - growth_vector
print(margin_growth_spread)
```

Read the first element:

```text
0.42 - 0.08 = 0.34
```

That first result belongs to Aster because both first elements came from Aster's row.

The full vector is:

```text
d = (m_1 - x_1, m_2 - x_2, ..., m_n - x_n)
```

This is the first serious elementwise operation. It prepares you for deviations in
Lesson 4, where you subtract the same mean from every observation.

## 6. Elementwise Scaling

Sometimes the same values need a new unit.

```python
balance_proxy = financials["gross_margin"] * 1000
balance_vector = balance_proxy.to_numpy()
scaled_balance = balance_vector / 1000

print(scaled_balance)
```

Scaling is still elementwise:

```text
z_i = b_i / 1000
```

The operation applies to every observation.

## 7. Boolean Masks Are Also Vectors

A comparison creates a boolean vector:

```python
positive_growth_mask = growth_vector > 0
print(positive_growth_mask)
```

Mathematically, this is an indicator-like object:

```text
I_i = 1 if x_i > 0, otherwise 0
```

In Python it appears as `True` and `False`. You can use it to filter another aligned
vector:

```python
masked_margin_average = margin_vector[positive_growth_mask].mean()
print(masked_margin_average)
```

This asks:

```text
What is the average gross margin only among observations with positive revenue growth?
```

That is the bridge to probability later. Event indicators begin as boolean masks.

## 8. Complete Worked Example

```python
growth_series = financials["revenue_growth"]
margin_series = financials["gross_margin"]
balance_proxy = financials["gross_margin"] * 1000

growth_vector = growth_series.to_numpy()
margin_vector = margin_series.to_numpy()
balance_vector = balance_proxy.to_numpy()

derived_spread = margin_vector - growth_vector
scaled_balance = balance_vector / 1000
positive_growth_mask = growth_vector > 0
masked_margin_average = margin_vector[positive_growth_mask].mean()
alignment_check = len(growth_vector) == len(margin_vector) == len(balance_vector)
```

This example produces five objects:

- `growth_vector`
- `margin_vector`
- `derived_spread`
- `positive_growth_mask`
- `masked_margin_average`

Those objects are not disconnected. They are one chain:

```text
columns -> vectors -> elementwise subtraction -> boolean mask -> masked average
```

## 9. What This Prepares

Lesson 3 will use aligned vectors to compute sums, counts, means, and weighted means.
Lesson 4 will use the same subtraction idea to compute deviations from the mean.
Lesson 5 will divide deviations by standard deviation to create z-scores.

That is why Lesson 2 matters. It is the operational bridge between table columns and
statistical formulas.
""",
    "worked_example": {
        "description": "Select columns, convert them to vectors, and create elementwise derived vectors.",
        "code": _LESSON_2_CODE,
        "explanation": "The example moves from Series to vectors, then uses aligned vectors for spreads, scaling, and masks.",
    },
    "reference": {
        "key_syntax": [
            "growth_series = financials['revenue_growth']",
            "growth_vector = growth_series.to_numpy()",
            "derived_spread = margin_vector - growth_vector",
            "positive_growth_mask = growth_vector > 0",
            "margin_vector[positive_growth_mask].mean()",
        ],
        "notes": "Elementwise operations only make sense when observations are aligned.",
    },
    "questions": _deep_stats_questions({
        "prior_object": "Lesson 1's DataFrame and selected numeric columns",
        "new_operation": "Series-to-vector conversion and aligned elementwise arithmetic",
        "syntax_template": "growth_vector = growth_series.___()",
        "syntax_answer": "to_numpy",
        "syntax_explanation": "`to_numpy()` converts a pandas Series into a NumPy vector.",
        "formula": "d_i = m_i - x_i",
        "inspection_object": "`growth_series.index` and the vector lengths",
        "common_mistake": "Subtracting vectors that are not aligned to the same observations",
        "mistake_explanation": "Elementwise arithmetic assumes position 1 matches position 1, position 2 matches position 2, and so on.",
        "first_label": "Series index:",
        "interpretation": "The derived vector measures an observation-by-observation spread across the sample.",
        "next_bridge": "aligned vectors that can be summed and averaged in Lesson 3",
        "challenge_goal": "select Series, convert vectors, compute spreads, masks, and labeled outputs",
        "produced_object": "aligned derived vectors",
        "debug_check": "check row order, index, vector lengths, and the first few values",
        "chain_template": "DataFrame -> Series -> ___ -> elementwise operation",
        "chain_answer": "vector",
        "chain_explanation": "The Series becomes a vector before direct elementwise arithmetic.",
    }),
    "challenge": {
        "instructions": "Build aligned vectors from financial columns, compute elementwise spreads and masks, and print every required label.",
        "starter_code": "# Build the financials DataFrame, select Series, convert vectors, and compute the required labels.\n",
        "tests": [
            {"type": "code_contains", "value": "to_numpy"},
            {"type": "code_contains", "value": "derived_spread"},
            {"type": "code_contains", "value": "positive_growth_mask"},
            {"type": "output_contains", "value": "Series index:"},
            {"type": "output_contains", "value": "Growth vector:"},
            {"type": "output_contains", "value": "Derived spread vector:"},
            {"type": "output_contains", "value": "Masked margin average:"},
            {"type": "output_contains", "value": "Alignment check:"},
            {"type": "output_contains", "value": "Next lesson bridge:"},
            {"type": "runs_without_error"},
        ],
        "solution": _LESSON_2_CODE,
    },
}


LESSON_3_QUALITY_PASS = {
    "id": "casfd-l3",
    "title": "Summation, Count, Mean, And Weighted Mean",
    "order": 3,
    "duration_min": 120,
    "difficulty": "beginner",
    "real_world_context": (
        "A financial analyst has aligned vectors for revenue growth, balances, and "
        "transaction counts. The next task is to summarize those vectors with sums, "
        "counts, arithmetic means, and weighted means."
    ),
    "concept": """## Lesson Aim

Lesson 2 produced aligned vectors. Lesson 3 teaches the first summary operations over
those vectors.

The chain is:

```text
aligned vector -> count -> sum -> arithmetic mean -> weighted mean
```

This is not a small topic. Mean is the first estimator you will use throughout
statistics. Weighted mean is the first place where "average" becomes a modeling
choice rather than a neutral button.

## 1. Begin With An Aligned Vector

```python
values = financials["revenue_growth"].to_numpy()
```

The vector is:

```text
x = (0.08, 0.03, 0.11, -0.02, 0.06, 0.01)
```

Each element belongs to one company observation.

## 2. Count Is The Sample Size

```python
n = len(values)
```

Mathematically:

```text
n = number of observations
```

This count is the denominator for the arithmetic mean. Later, it appears in standard
error, confidence intervals, hypothesis tests, and regression degrees of freedom.

## 3. Sum Is The First Aggregation

```python
total = values.sum()
```

Notation:

```text
sum_{i=1 to n} x_i
```

This means "add every observation." In code, `values.sum()` does that operation.

## 4. Arithmetic Mean

The arithmetic mean is:

```text
x_bar = (1 / n) * sum_{i=1 to n} x_i
```

In code:

```python
mean_growth = values.sum() / len(values)
```

As a function:

```python
def arithmetic_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)
```

The mean is a sample statistic. It describes the observed data and often estimates a
population mean, but it does not prove the population value by itself.

## 5. Why Weighted Means Exist

An arithmetic mean gives every observation equal weight. In financial analysis, that
may or may not be appropriate.

If a small account and a large account are both rows, do you want them to count the
same? Sometimes yes. Sometimes no.

A weighted mean is:

```text
weighted_mean = sum(w_i x_i) / sum(w_i)
```

Where:

```text
x_i = value for observation i
w_i = weight for observation i
```

In code:

```python
weighted_mean = (values * weights).sum() / weights.sum()
```

## 6. Balance-Weighted Mean

```python
balance_weights = financials["customer_balance"].to_numpy()
balance_weighted_mean = (values * balance_weights).sum() / balance_weights.sum()
```

This gives more influence to companies or accounts with larger balances.

That is not automatically better. It answers a different question:

```text
equal-weighted mean: what is the average row?
balance-weighted mean: what is the average dollar-weighted exposure?
```

## 7. Transaction-Weighted Mean

```python
transaction_weights = financials["transaction_count"].to_numpy()
transaction_weighted_mean = (values * transaction_weights).sum() / transaction_weights.sum()
```

This answers another question:

```text
what revenue growth do heavier-activity observations contribute to the average?
```

The lesson is not "use weights always." The lesson is "know what your denominator
means."

## 8. Complete Worked Example

```python
def arithmetic_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def weighted_mean(values, weights):
    values = np.asarray(values)
    weights = np.asarray(weights)
    return (values * weights).sum() / weights.sum()

manual_mean = arithmetic_mean(values)
balance_weighted_mean = weighted_mean(values, balance_weights)
transaction_weighted_mean = weighted_mean(values, transaction_weights)
```

The arithmetic mean and weighted means are all valid calculations. The analyst must
say which question each one answers.

## 9. Bridge To Lesson 4

Lesson 4 uses the arithmetic mean as the center of the data.

The next chain is:

```text
mean -> deviations from mean -> squared deviations -> sample variance
```

If you do not understand the mean, variance becomes a memorized formula. If you do
understand the mean, variance becomes the next natural operation.
""",
    "worked_example": {
        "description": "Compute arithmetic and weighted means from aligned financial vectors.",
        "code": _LESSON_3_CODE,
        "explanation": "The example compares equal-weighted and weighted averages so the denominator choice is explicit.",
    },
    "reference": {
        "key_syntax": [
            "n = len(values)",
            "values.sum()",
            "values.sum() / len(values)",
            "(values * weights).sum() / weights.sum()",
        ],
        "notes": "A weighted mean changes the question being answered; it is not just a fancier mean.",
    },
    "questions": _deep_stats_questions({
        "prior_object": "aligned vectors from Lesson 2",
        "new_operation": "sum, count, arithmetic mean, and weighted mean",
        "syntax_template": "weighted_mean = (values * weights).___() / weights.sum()",
        "syntax_answer": "sum",
        "syntax_explanation": "The numerator adds the weighted values.",
        "formula": "weighted_mean = sum(w_i x_i) / sum(w_i)",
        "inspection_object": "`values`, `weights`, `len(values)`, and `weights.sum()`",
        "common_mistake": "Using a weighted mean without explaining what the weights represent",
        "mistake_explanation": "Weights change the meaning of the average.",
        "first_label": "Count n:",
        "interpretation": "The mean summarizes the sample; a weighted mean summarizes the sample under an explicit weighting rule.",
        "next_bridge": "the arithmetic mean used as the center for deviations in Lesson 4",
        "challenge_goal": "compute count, sum, arithmetic mean, weighted means, and labeled checks",
        "produced_object": "manual and weighted averages",
        "debug_check": "check the vector length, weight length, total weight, and denominator",
        "chain_template": "aligned vector -> count -> sum -> ___",
        "chain_answer": "mean",
        "chain_explanation": "Mean is sum divided by count.",
    }),
    "challenge": {
        "instructions": "Compute arithmetic and weighted means from financial vectors and print every required label.",
        "starter_code": "# Build the financials DataFrame, define arithmetic_mean and weighted_mean, then print the required labels.\n",
        "tests": [
            {"type": "code_contains", "value": "weighted_mean"},
            {"type": "code_contains", "value": "arithmetic_mean"},
            {"type": "output_contains", "value": "Count n:"},
            {"type": "output_contains", "value": "Sum revenue growth:"},
            {"type": "output_contains", "value": "Arithmetic mean:"},
            {"type": "output_contains", "value": "Balance-weighted mean:"},
            {"type": "output_contains", "value": "Transaction-weighted mean:"},
            {"type": "output_contains", "value": "Next lesson bridge:"},
            {"type": "runs_without_error"},
        ],
        "solution": _LESSON_3_CODE,
    },
}


LESSON_4_QUALITY_PASS = {
    "id": "casfd-l4",
    "title": "Deviations, Sample Variance, And Standard Deviation",
    "order": 4,
    "duration_min": 120,
    "difficulty": "beginner",
    "real_world_context": (
        "A financial analyst has computed the mean revenue growth. The next task is "
        "to measure how far each observation sits from that center, then turn those "
        "distances into variance and standard deviation."
    ),
    "concept": """## Lesson Aim

Lesson 3 produced the mean. Lesson 4 asks the obvious next question:

```text
How spread out are the observations around that mean?
```

The chain is:

```text
mean -> deviations -> squared deviations -> sample variance -> standard deviation
```

Variance is not a random formula. It is built directly from the mean.

## 1. Start With The Mean

```python
values = financials["revenue_growth"].to_numpy()
mean_value = values.sum() / len(values)
```

The mean is the center:

```text
x_bar
```

But the mean alone hides variation. Two samples can have the same mean and very
different spread.

## 2. Deviations From The Mean

For each observation:

```text
d_i = x_i - x_bar
```

In code:

```python
deviation_vector = values - mean_value
```

This subtracts the same center from every observation. It is elementwise subtraction,
which Lesson 2 already taught.

## 3. The Deviation Sum Check

```python
deviation_vector.sum()
```

The sum should be approximately zero. That is not a coincidence. The sample mean is
the balancing point of the data.

If the sum is not close to zero, check whether:

- you used the same vector for the mean and deviations
- you changed row order
- you mixed columns
- you rounded too early

## 4. Why Squared Deviations

Raw deviations cancel out:

```text
positive deviations + negative deviations = approximately 0
```

To measure spread, square them:

```python
squared_deviations = deviation_vector ** 2
```

Now all distances are nonnegative.

## 5. Sample Variance

Sample variance is:

```text
s^2 = sum((x_i - x_bar)^2) / (n - 1)
```

In code:

```python
sample_variance = squared_deviations.sum() / (len(values) - 1)
```

The denominator is `n - 1` because the mean was estimated from the same sample.
Estimating the center uses one degree of freedom.

## 6. Population Variance Comparison

If these six observations were the entire population, the denominator would be `n`:

```python
population_variance = squared_deviations.sum() / len(values)
```

This lesson uses sample variance because the data is a sample of a broader financial
population we may care about.

## 7. Standard Deviation

Variance is in squared units. Standard deviation returns to the original unit:

```text
s = sqrt(s^2)
```

In code:

```python
sample_standard_deviation = sample_variance ** 0.5
```

If revenue growth is measured in decimal growth rates, standard deviation is also in
decimal growth-rate units.

## 8. pandas Checks

```python
financials["revenue_growth"].var(ddof=1)
financials["revenue_growth"].std(ddof=1)
```

`ddof=1` tells pandas to use `n - 1`.

The manual calculation teaches. The pandas calculation checks.

## 9. Bridge To Lesson 5

Lesson 5 uses the mean and standard deviation together:

```text
z_i = (x_i - x_bar) / s
```

So the output of Lesson 4 becomes the input to standardization.
""",
    "worked_example": {
        "description": "Build deviations, squared deviations, sample variance, and standard deviation from a mean.",
        "code": _LESSON_4_CODE,
        "explanation": "The example makes variance a sequence of operations rather than a memorized formula.",
    },
    "reference": {
        "key_syntax": [
            "deviation_vector = values - mean_value",
            "squared_deviations = deviation_vector ** 2",
            "sample_variance = squared_deviations.sum() / (len(values) - 1)",
            "sample_standard_deviation = sample_variance ** 0.5",
            "financials['revenue_growth'].std(ddof=1)",
        ],
        "notes": "Sample variance uses n - 1 because the mean is estimated from the sample.",
    },
    "questions": _deep_stats_questions({
        "prior_object": "the arithmetic mean from Lesson 3",
        "new_operation": "deviations, squared deviations, sample variance, and standard deviation",
        "syntax_template": "deviation_vector = values ___ mean_value",
        "syntax_answer": "-",
        "syntax_explanation": "A deviation subtracts the mean from each observed value.",
        "formula": "s^2 = sum((x_i - x_bar)^2) / (n - 1)",
        "inspection_object": "`deviation_vector` and `deviation_vector.sum()`",
        "common_mistake": "Using variance without understanding that it is built from deviations around the mean",
        "mistake_explanation": "Variance is not a separate magic number; it comes from squared deviations.",
        "first_label": "Mean from prior lesson:",
        "interpretation": "Standard deviation reports typical spread around the sample mean in the original unit.",
        "next_bridge": "standard deviation used as the denominator for z-scores in Lesson 5",
        "challenge_goal": "compute deviations, squared deviations, sample variance, standard deviation, and pandas checks",
        "produced_object": "sample variance and sample standard deviation",
        "debug_check": "check the mean, deviation sum, denominator, and ddof setting",
        "chain_template": "mean -> deviations -> squared deviations -> ___",
        "chain_answer": "sample variance",
        "chain_explanation": "Sample variance averages squared deviations using n - 1.",
    }),
    "challenge": {
        "instructions": "Compute deviation-based spread statistics manually and check them with pandas.",
        "starter_code": "# Build the financials DataFrame, compute mean, deviations, variance, and standard deviation.\n",
        "tests": [
            {"type": "code_contains", "value": "deviation_vector"},
            {"type": "code_contains", "value": "sample_variance"},
            {"type": "code_contains", "value": "ddof=1"},
            {"type": "output_contains", "value": "Mean from prior lesson:"},
            {"type": "output_contains", "value": "Deviation vector:"},
            {"type": "output_contains", "value": "Sample variance:"},
            {"type": "output_contains", "value": "Sample standard deviation:"},
            {"type": "output_contains", "value": "Pandas variance check:"},
            {"type": "output_contains", "value": "Next lesson bridge:"},
            {"type": "runs_without_error"},
        ],
        "solution": _LESSON_4_CODE,
    },
}


LESSON_5_QUALITY_PASS = {
    "id": "casfd-l5",
    "title": "Standardization, Z-Scores, And Empirical Distributions",
    "order": 5,
    "duration_min": 120,
    "difficulty": "beginner",
    "real_world_context": (
        "A financial analyst has mean and standard deviation for revenue growth. "
        "The next task is to express each observation in standard-deviation units, "
        "compare variables on different scales, and create empirical percentile flags."
    ),
    "concept": """## Lesson Aim

Lesson 4 produced standard deviation. Lesson 5 uses it.

The chain is:

```text
mean -> deviation -> standard deviation -> z-score -> empirical distribution
```

Standardization is the bridge from raw financial units to comparable statistical
units.

## 1. Why Raw Units Are Hard To Compare

Revenue growth is a decimal rate:

```text
0.08 means 8 percent growth
```

Customer balance is dollars:

```text
1200 means $1,200
```

Those two variables cannot be compared directly. A difference of `0.03` in growth and
a difference of `$300` in balance live on different scales.

Standardization puts each variable into standard-deviation units.

## 2. Z-Score Formula

For one observation:

```text
z_i = (x_i - x_bar) / s
```

Where:

- `x_i` is the observed value
- `x_bar` is the sample mean
- `s` is the sample standard deviation

In code:

```python
growth_z = (growth - growth.mean()) / growth.std(ddof=1)
```

This says:

```text
subtract the mean
divide by the standard deviation
```

## 3. Interpret A Z-Score

A z-score of `1.2` means the observation is 1.2 sample standard deviations above the
sample mean.

A z-score of `-0.8` means the observation is 0.8 sample standard deviations below the
sample mean.

Do not say:

```text
This proves the company is abnormal.
```

Say:

```text
Within this sample, this observation is far above or below the sample center relative
to the sample spread.
```

## 4. Standardize A Second Variable

```python
balance_z = (balance - balance.mean()) / balance.std(ddof=1)
```

Now revenue growth and customer balance can be compared in the same unit:

```text
standard deviations from each variable's own sample mean
```

## 5. Mean And Standard Deviation Checks

A standardized sample should have:

```text
mean approximately 0
sample standard deviation approximately 1
```

Check:

```python
growth_z.mean()
growth_z.std(ddof=1)
```

Small floating-point noise is normal.

## 6. Empirical Percentiles

Z-scores use mean and standard deviation. Percentiles use rank.

```python
empirical_percentiles = growth.rank(pct=True)
```

This asks where each observation sits in the observed distribution.

Percentiles are often more intuitive for communication:

```text
This company is in the top quartile of observed revenue growth.
```

## 7. Top-Quartile Flags

```python
top_quartile_cutoff = growth.quantile(0.75)
high_growth_flags = (growth >= top_quartile_cutoff).astype(int)
```

This creates a 0/1 indicator from an empirical distribution rule.

That prepares the probability lessons:

```text
indicator mean = event probability
```

## 8. Complete Worked Example

```python
growth_z = (growth - growth.mean()) / growth.std(ddof=1)
balance_z = (balance - balance.mean()) / balance.std(ddof=1)
empirical_percentiles = growth.rank(pct=True)
top_quartile_cutoff = growth.quantile(0.75)
high_growth_flags = (growth >= top_quartile_cutoff).astype(int)
```

This produces:

- standardized revenue growth
- standardized balance
- empirical percentile ranks
- a high-growth indicator

## 9. Bridge To Lesson 6

Lesson 6 pairs standardized variables and asks whether they move together:

```text
z_x and z_y -> covariance -> correlation
```

So Lesson 5 is the gateway to relationship measures.
""",
    "worked_example": {
        "description": "Compute z-scores, percentiles, and high-growth flags from mean and standard deviation.",
        "code": _LESSON_5_CODE,
        "explanation": "The example turns raw financial variables into standardized and rank-based comparisons.",
    },
    "reference": {
        "key_syntax": [
            "growth_z = (growth - growth.mean()) / growth.std(ddof=1)",
            "growth.rank(pct=True)",
            "growth.quantile(0.75)",
            "(growth >= cutoff).astype(int)",
        ],
        "notes": "Z-scores use mean and standard deviation; percentiles use rank.",
    },
    "questions": _deep_stats_questions({
        "prior_object": "mean and standard deviation from Lesson 4",
        "new_operation": "z-scores, empirical percentiles, and indicator flags",
        "syntax_template": "growth_z = (growth - growth.mean()) ___ growth.std(ddof=1)",
        "syntax_answer": "/",
        "syntax_explanation": "A z-score divides the deviation by the sample standard deviation.",
        "formula": "z_i = (x_i - x_bar) / s",
        "inspection_object": "`growth_z.mean()` and `growth_z.std(ddof=1)`",
        "common_mistake": "Comparing raw variables on different scales as if they used the same unit",
        "mistake_explanation": "Standardization exists because variables like growth rates and balances have different units.",
        "first_label": "Growth z-scores:",
        "interpretation": "A z-score reports how many sample standard deviations an observation sits from the sample mean.",
        "next_bridge": "paired standardized vectors for covariance and correlation in Lesson 6",
        "challenge_goal": "compute z-scores, empirical percentiles, quantile flags, and standardization checks",
        "produced_object": "standardized and rank-based comparison variables",
        "debug_check": "check the mean, standard deviation, percentile ranks, and cutoff rule",
        "chain_template": "mean -> standard deviation -> ___ -> empirical flag",
        "chain_answer": "z-score",
        "chain_explanation": "The z-score is the standardized observation.",
    }),
    "challenge": {
        "instructions": "Compute z-scores, empirical percentiles, and high-growth flags, then print every required label.",
        "starter_code": "# Build the financials DataFrame, compute z-scores, percentiles, and flags.\n",
        "tests": [
            {"type": "code_contains", "value": "growth_z"},
            {"type": "code_contains", "value": "rank"},
            {"type": "code_contains", "value": "quantile"},
            {"type": "output_contains", "value": "Growth z-scores:"},
            {"type": "output_contains", "value": "Balance z-scores:"},
            {"type": "output_contains", "value": "Empirical percentiles:"},
            {"type": "output_contains", "value": "High growth flags:"},
            {"type": "output_contains", "value": "Standardized mean check:"},
            {"type": "output_contains", "value": "Next lesson bridge:"},
            {"type": "runs_without_error"},
        ],
        "solution": _LESSON_5_CODE,
    },
}


LESSON_3_QUALITY_PASS["concept"] += """

## 10. Average Is A Design Choice

When a dashboard says "average revenue growth," the first graduate-level question is:

```text
Average over what unit?
```

If every company row receives equal weight, the statistic answers:

```text
What is the average observed company-quarter growth rate?
```

If each row is weighted by customer balance, the statistic answers:

```text
What growth rate is experienced by the average dollar of customer balance?
```

If each row is weighted by transaction count, the statistic answers:

```text
What growth rate is associated with the average observed transaction?
```

Those are not the same question. This is why a serious analyst does not write
"the average is 6.8 percent" without saying how the average was constructed.

## 11. Manual Trace Of The Weighted Mean

Take three simplified rows:

```text
x = (0.08, 0.03, 0.11)
w = (1200, 850, 1600)
```

The weighted numerator is:

```text
(0.08 * 1200) + (0.03 * 850) + (0.11 * 1600)
```

The denominator is:

```text
1200 + 850 + 1600
```

So the weighted mean is:

```text
sum(w_i x_i) / sum(w_i)
```

In Python, the expression:

```python
(values * weights).sum() / weights.sum()
```

is not a trick. It is exactly the mathematical expression above.

## 12. What To Say In An Analyst Note

A weak sentence:

```text
The average revenue growth is 0.068.
```

A stronger sentence:

```text
The balance-weighted average revenue growth is 6.83 percent, which is higher than
the equal-weighted mean because larger-balance observations have stronger growth in
this sample.
```

That sentence does three things:

1. names the statistic
2. reports the value
3. explains why it differs from another statistic

## 13. Why This Prepares Variance

Variance is built from the arithmetic mean. Before you can understand spread, you must
understand the center. Lesson 4 will subtract the mean from every observation:

```text
d_i = x_i - x_bar
```

So if the mean is not clear, deviations will not be clear. If deviations are not
clear, variance will feel like a formula to memorize instead of a statistic you can
derive.
"""


LESSON_4_QUALITY_PASS["concept"] += """

## 10. Variance Is A Two-Step Story

Variance is often taught too quickly:

```text
s^2 = sum((x_i - x_bar)^2) / (n - 1)
```

That notation hides the story. The story is:

1. find the center
2. measure each observation's distance from the center
3. square those distances so they do not cancel out
4. add the squared distances
5. divide by the sample degrees of freedom

In code, that story is visible:

```python
mean_value = values.sum() / len(values)
deviation_vector = values - mean_value
squared_deviations = deviation_vector ** 2
sample_variance = squared_deviations.sum() / (len(values) - 1)
```

Each line earns the next one.

## 11. Degrees Of Freedom Without Handwaving

The deviations from the sample mean must sum to zero:

```text
sum(d_i) = 0
```

That means the final deviation is constrained by the others. If five deviations are
known in a six-row sample, the sixth deviation is forced. The sample has six
observations, but only five independent deviations around the estimated sample mean.

That is why the denominator is:

```text
n - 1
```

This is not trivia. Later, regression degrees of freedom will follow the same logic:
every estimated parameter consumes information.

## 12. Standard Deviation Is Usually The Communicated Statistic

Variance is mathematically central, but standard deviation is easier to discuss
because it returns to the original unit.

If revenue growth is measured as decimal growth, then:

```text
standard deviation = 0.0476
```

means roughly:

```text
typical spread around the sample mean is about 4.76 percentage points
```

Do not overclaim. Standard deviation does not say the data is normal. It does not
prove future volatility. It summarizes spread in the observed sample.

## 13. Diagnostic Habit

Whenever a variance or standard deviation seems wrong, inspect:

```python
print(values)
print(mean_value)
print(deviation_vector)
print(deviation_vector.sum())
print(squared_deviations)
```

Do not debug variance from the final number alone. Debug the chain.
"""


LESSON_5_QUALITY_PASS["concept"] += """

## 10. Z-Scores Are Not The Same As Percentiles

Both z-scores and percentiles describe position, but they answer different questions.

Z-score:

```text
How many standard deviations from the mean is this observation?
```

Percentile:

```text
What share of observations are at or below this value?
```

A z-score uses the mean and standard deviation. A percentile uses ranking. In skewed
financial data, these can tell different stories. That is why this lesson teaches
both.

## 11. Why Standardization Matters Before Correlation

Lesson 6 will study relationships between paired variables. If two variables are on
very different scales, raw comparisons can mislead.

Customer balance might range from hundreds to thousands of dollars. Revenue growth
might range from negative 2 percent to positive 11 percent. Standardization expresses
each in the same unit:

```text
standard deviations from that variable's own mean
```

That shared unit prepares covariance, correlation, PCA, clustering, and regression
diagnostics.

## 12. Indicator Flags From Empirical Rules

The high-growth flag is:

```python
high_growth_flags = (growth >= top_quartile_cutoff).astype(int)
```

This line turns a continuous variable into an event:

```text
1 = high-growth observation
0 = not high-growth observation
```

That prepares probability. In a later lesson, the mean of a 0/1 indicator becomes an
empirical probability:

```text
P(high growth) = mean(high_growth_flag)
```

This is another example of gradual construction. Percentiles create a threshold.
The threshold creates an event flag. The event flag becomes a probability.

## 13. Analyst Communication

A weak sentence:

```text
Aster has a z-score of 0.67.
```

A stronger sentence:

```text
Aster's revenue growth is 0.67 sample standard deviations above the sample mean,
which places it above the center of this six-company sample but does not by itself
prove unusual performance.
```

That sentence reports the statistic and controls the claim. This is the tone the
course should keep.
"""


_LESSON_3_CODE_EXPANDED = """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "customer_balance": [1200, 850, 1600, 740, 1100, 910],
    "transaction_count": [42, 37, 58, 24, 45, 31],
})

values = financials["revenue_growth"].to_numpy()
balance_weights = financials["customer_balance"].to_numpy()
transaction_weights = financials["transaction_count"].to_numpy()

def arithmetic_mean(values):
    values = np.asarray(values)
    return values.sum() / len(values)

def weighted_mean(values, weights):
    values = np.asarray(values)
    weights = np.asarray(weights)
    return (values * weights).sum() / weights.sum()

count_n = len(values)
sum_growth = values.sum()
manual_mean = arithmetic_mean(values)
pandas_mean = financials["revenue_growth"].mean()
weighted_numerator = (values * balance_weights).sum()
weight_sum = balance_weights.sum()
balance_weighted_mean = weighted_mean(values, balance_weights)
transaction_weighted_mean = weighted_mean(values, transaction_weights)
weighting_difference = balance_weighted_mean - manual_mean

contribution_table = financials.assign(
    balance_weight=financials["customer_balance"] / financials["customer_balance"].sum(),
    weighted_growth_contribution=financials["revenue_growth"] * financials["customer_balance"] / financials["customer_balance"].sum(),
)

interpretation = (
    "The balance-weighted mean differs from the equal-weighted mean because larger "
    "balance observations receive more influence."
)

print("Count n:", count_n)
print("Sum revenue growth:", round(sum_growth, 6))
print("Arithmetic mean:", round(manual_mean, 6))
print("Pandas mean check:", round(pandas_mean, 6))
print("Weighted numerator:", round(weighted_numerator, 6))
print("Weight sum:", round(weight_sum, 2))
print("Balance-weighted mean:", round(balance_weighted_mean, 6))
print("Transaction-weighted mean:", round(transaction_weighted_mean, 6))
print("Difference due to weights:", round(weighting_difference, 6))
print("Contribution table:")
print(contribution_table[["company", "balance_weight", "weighted_growth_contribution"]].round(6))
print("Interpretation sentence:", interpretation)
print("Next lesson bridge:", "means become the center used to calculate deviations")"""


_LESSON_4_CODE_EXPANDED = """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
})

values = financials["revenue_growth"].to_numpy()
mean_value = values.sum() / len(values)
deviation_vector = values - mean_value
squared_deviations = deviation_vector ** 2
sum_squared_deviations = squared_deviations.sum()
degrees_of_freedom = len(values) - 1
sample_variance = sum_squared_deviations / degrees_of_freedom
population_variance = sum_squared_deviations / len(values)
sample_standard_deviation = sample_variance ** 0.5
pandas_variance_check = financials["revenue_growth"].var(ddof=1)
pandas_std_check = financials["revenue_growth"].std(ddof=1)

variance_audit = pd.DataFrame({
    "company": financials["company"],
    "value": values,
    "deviation": deviation_vector,
    "squared_deviation": squared_deviations,
})

interpretation = (
    "The sample standard deviation reports typical spread around the sample mean "
    "in revenue-growth units."
)

print("Mean from prior lesson:", round(mean_value, 6))
print("Deviation vector:", np.round(deviation_vector, 4))
print("Deviation sum check:", round(deviation_vector.sum(), 10))
print("Squared deviations:", np.round(squared_deviations, 6))
print("Sum squared deviations:", round(sum_squared_deviations, 6))
print("Degrees of freedom:", degrees_of_freedom)
print("Sample variance:", round(sample_variance, 6))
print("Population variance comparison:", round(population_variance, 6))
print("Sample standard deviation:", round(sample_standard_deviation, 6))
print("Pandas variance check:", round(pandas_variance_check, 6))
print("Pandas std check:", round(pandas_std_check, 6))
print("Variance audit table:")
print(variance_audit.round(6))
print("Interpretation sentence:", interpretation)
print("Next lesson bridge:", "standard deviation turns deviations into z-scores")"""


_LESSON_5_CODE_EXPANDED = """import numpy as np
import pandas as pd

financials = pd.DataFrame({
    "company": ["Aster", "Beacon", "Cobalt", "Drift", "Ember", "Fjord"],
    "revenue_growth": [0.08, 0.03, 0.11, -0.02, 0.06, 0.01],
    "customer_balance": [1200, 850, 1600, 740, 1100, 910],
})

growth = financials["revenue_growth"]
balance = financials["customer_balance"]

growth_z = (growth - growth.mean()) / growth.std(ddof=1)
balance_z = (balance - balance.mean()) / balance.std(ddof=1)
empirical_percentiles = growth.rank(pct=True)
top_quartile_cutoff = growth.quantile(0.75)
high_growth_flags = (growth >= top_quartile_cutoff).astype(int)
high_growth_probability = high_growth_flags.mean()

standardized_table = pd.DataFrame({
    "company": financials["company"],
    "growth_z": growth_z,
    "balance_z": balance_z,
    "growth_percentile": empirical_percentiles,
    "high_growth_flag": high_growth_flags,
})

most_unusual_company = standardized_table.loc[standardized_table["growth_z"].abs().idxmax(), "company"]
interpretation = (
    "Z-scores express distance from the sample mean in standard-deviation units; "
    "percentiles express rank within the observed sample."
)

print("Growth z-scores:", np.round(growth_z.to_numpy(), 4))
print("Balance z-scores:", np.round(balance_z.to_numpy(), 4))
print("Empirical percentiles:", np.round(empirical_percentiles.to_numpy(), 3))
print("Top quartile cutoff:", round(top_quartile_cutoff, 4))
print("High growth flags:", high_growth_flags.to_list())
print("High growth probability:", round(high_growth_probability, 4))
print("Standardized mean check:", round(growth_z.mean(), 10))
print("Standardized std check:", round(growth_z.std(ddof=1), 6))
print("Standardized table:")
print(standardized_table.round(4))
print("Most unusual company by growth z:", most_unusual_company)
print("Interpretation sentence:", interpretation)
print("Next lesson bridge:", "standardized paired vectors are ready for covariance and correlation")"""


LESSON_3_QUALITY_PASS["concept"] += """

## 14. Contribution Tables Make Weighted Means Auditable

A weighted mean can feel abstract until you show each row's contribution.

Create a contribution table:

```python
contribution_table = financials.assign(
    balance_weight=financials["customer_balance"] / financials["customer_balance"].sum(),
    weighted_growth_contribution=financials["revenue_growth"]
    * financials["customer_balance"]
    / financials["customer_balance"].sum(),
)
```

This table answers:

```text
How much does each observation contribute to the weighted mean?
```

The balance weights should sum to 1. The weighted growth contributions should sum to
the balance-weighted mean.

That is an important audit habit. If the weighted mean changes a conclusion, you need
to know which observations drove the change.

## 15. Three Means, Three Questions

This lesson now produces three related averages:

```text
arithmetic mean
balance-weighted mean
transaction-weighted mean
```

The arithmetic mean is the baseline. The balance-weighted mean is exposure-sensitive.
The transaction-weighted mean is activity-sensitive.

Do not ask which one is "the real average" in isolation. Ask which one matches the
decision:

- Use arithmetic mean when each observation should count equally.
- Use balance-weighted mean when larger balances should matter more.
- Use transaction-weighted mean when activity volume should matter more.

## 16. Stronger Model Answer Pattern

A model answer should not end with the number. It should explain the design:

```text
The equal-weighted mean treats every company-quarter equally. The balance-weighted
mean gives larger-balance observations more influence. Because the weighted mean is
higher here, larger-balance observations have stronger revenue growth in this sample.
```
"""

LESSON_3_QUALITY_PASS["worked_example"]["code"] = _LESSON_3_CODE_EXPANDED
LESSON_3_QUALITY_PASS["challenge"]["solution"] = _LESSON_3_CODE_EXPANDED
LESSON_3_QUALITY_PASS["challenge"]["tests"] = [
    {"type": "code_contains", "value": "weighted_mean"},
    {"type": "code_contains", "value": "contribution_table"},
    {"type": "code_contains", "value": "weighted_growth_contribution"},
    {"type": "output_contains", "value": "Count n:"},
    {"type": "output_contains", "value": "Arithmetic mean:"},
    {"type": "output_contains", "value": "Weighted numerator:"},
    {"type": "output_contains", "value": "Balance-weighted mean:"},
    {"type": "output_contains", "value": "Contribution table:"},
    {"type": "output_contains", "value": "Interpretation sentence:"},
    {"type": "output_contains", "value": "Next lesson bridge:"},
    {"type": "runs_without_error"},
]

LESSON_4_QUALITY_PASS["concept"] += """

## 14. Variance Audit Table

A variance audit table makes each step visible:

```python
variance_audit = pd.DataFrame({
    "company": financials["company"],
    "value": values,
    "deviation": deviation_vector,
    "squared_deviation": squared_deviations,
})
```

This is useful because variance is easy to misread when only the final scalar appears.
The audit table shows which observations are far from the mean and which observations
drive the sum of squared deviations.

In graduate work, this habit matters. A large standard deviation is not just a number.
It invites inspection:

```text
Which observations created the spread?
Are those observations valid?
Are they different subgroups?
Should the next model include another explanatory variable?
```

## 15. Sample Versus Population Variance In Code

This lesson prints both:

```python
sample_variance = sum_squared_deviations / (len(values) - 1)
population_variance = sum_squared_deviations / len(values)
```

The goal is not to memorize two denominators. The goal is to know what claim you are
making. If the observed values are a sample used to learn about a broader process, use
sample variance. If the observed values are the full population of interest, population
variance can be appropriate.

## 16. What Carries Forward

Lesson 5 needs the sample standard deviation:

```text
z_i = (x_i - x_bar) / s
```

So Lesson 4's output is not just "spread." It is the denominator of the next lesson's
standardized score.
"""

LESSON_4_QUALITY_PASS["worked_example"]["code"] = _LESSON_4_CODE_EXPANDED
LESSON_4_QUALITY_PASS["challenge"]["solution"] = _LESSON_4_CODE_EXPANDED
LESSON_4_QUALITY_PASS["challenge"]["tests"] = [
    {"type": "code_contains", "value": "deviation_vector"},
    {"type": "code_contains", "value": "variance_audit"},
    {"type": "code_contains", "value": "degrees_of_freedom"},
    {"type": "output_contains", "value": "Mean from prior lesson:"},
    {"type": "output_contains", "value": "Deviation vector:"},
    {"type": "output_contains", "value": "Degrees of freedom:"},
    {"type": "output_contains", "value": "Sample variance:"},
    {"type": "output_contains", "value": "Variance audit table:"},
    {"type": "output_contains", "value": "Interpretation sentence:"},
    {"type": "output_contains", "value": "Next lesson bridge:"},
    {"type": "runs_without_error"},
]

LESSON_5_QUALITY_PASS["concept"] += """

## 14. Standardized Tables Are More Useful Than Loose Arrays

The z-score vector is useful, but a table is easier to audit:

```python
standardized_table = pd.DataFrame({
    "company": financials["company"],
    "growth_z": growth_z,
    "balance_z": balance_z,
    "growth_percentile": empirical_percentiles,
    "high_growth_flag": high_growth_flags,
})
```

This table keeps each standardized value attached to the company observation. That
prevents a common mistake: producing a vector and forgetting which row each value
belongs to.

## 15. Event Probability Appears Naturally

Once the high-growth flag exists, you can compute:

```python
high_growth_probability = high_growth_flags.mean()
```

That works because the flag is a 0/1 indicator. The mean of a 0/1 indicator equals
the share of observations where the event occurs.

This prepares Lesson 7:

```text
indicator vector -> event count -> empirical probability
```

## 16. Stronger Model Answer Pattern

A model answer should distinguish standardization and ranking:

```text
The z-score measures distance from the sample mean in standard-deviation units. The
percentile measures rank in the observed sample. The high-growth flag converts the
top quartile rule into a 0/1 event that can later be counted as a probability.
```

That is the conceptual bridge: z-scores compare scale, percentiles compare rank, and
flags prepare probability.
"""

LESSON_5_QUALITY_PASS["worked_example"]["code"] = _LESSON_5_CODE_EXPANDED
LESSON_5_QUALITY_PASS["challenge"]["solution"] = _LESSON_5_CODE_EXPANDED
LESSON_5_QUALITY_PASS["challenge"]["tests"] = [
    {"type": "code_contains", "value": "growth_z"},
    {"type": "code_contains", "value": "standardized_table"},
    {"type": "code_contains", "value": "high_growth_probability"},
    {"type": "output_contains", "value": "Growth z-scores:"},
    {"type": "output_contains", "value": "Empirical percentiles:"},
    {"type": "output_contains", "value": "High growth probability:"},
    {"type": "output_contains", "value": "Standardized table:"},
    {"type": "output_contains", "value": "Most unusual company by growth z:"},
    {"type": "output_contains", "value": "Interpretation sentence:"},
    {"type": "output_contains", "value": "Next lesson bridge:"},
    {"type": "runs_without_error"},
]


for _quality_index, _quality_lesson in enumerate(
    [LESSON_2_QUALITY_PASS, LESSON_3_QUALITY_PASS, LESSON_4_QUALITY_PASS, LESSON_5_QUALITY_PASS],
    start=1,
):
    MODULE_CORE_ANALYTICS_STATISTICS["lessons"][_quality_index] = _quality_lesson
    MODULE_CORE_ANALYTICS_STATISTICS["concept_map"][_quality_index] = {
        "id": _quality_lesson["id"],
        "label": _quality_lesson["title"][:42],
        "connects_to": [MODULE_CORE_ANALYTICS_STATISTICS["lessons"][_quality_index + 1]["id"]],
    }
