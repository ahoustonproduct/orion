"""
Orion Code — Dataset Seed Script
Generates 6 synthetic FinTech CSV datasets and loads them into SQLite.
Run from: /Users/hack/Desktop/Claude/orion-code/backend/datasets/
    python seed.py
"""

import random
import math
import os
import datetime

import pandas as pd
import sqlite3

random.seed(42)

# ─── helpers ────────────────────────────────────────────────────────────────

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def normal(mu, sigma):
    return random.gauss(mu, sigma)

def lognormal(mu_log, sigma_log):
    """Return exp(N(mu_log, sigma_log))."""
    return math.exp(normal(mu_log, sigma_log))

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def random_date(start: datetime.date, end: datetime.date) -> datetime.date:
    delta = (end - start).days
    return start + datetime.timedelta(days=random.randint(0, delta))

def weighted_choice(choices, weights):
    total = sum(weights)
    r = random.uniform(0, total)
    cumulative = 0
    for c, w in zip(choices, weights):
        cumulative += w
        if r <= cumulative:
            return c
    return choices[-1]

HERE = os.path.dirname(os.path.abspath(__file__))

# ─── 1. loan_applications.csv  (10,000 rows) ────────────────────────────────

def generate_loan_applications():
    TODAY = datetime.date(2026, 3, 25)
    three_years_ago = TODAY - datetime.timedelta(days=365 * 3)

    purposes = ['personal', 'auto', 'home_improvement', 'debt_consolidation', 'business']
    purpose_weights = [0.30, 0.20, 0.18, 0.25, 0.07]

    rows = []
    for i in range(1, 10_001):
        app_id = f"APP_{i:06d}"

        # Credit score: N(682, 72) clipped [500, 850]
        credit_score = int(clamp(round(normal(682, 72)), 500, 850))

        # Annual income: lognormal correlated with credit score
        # Base log-income ~ln(65000)=11.08, nudge by credit
        credit_nudge = (credit_score - 682) / 72 * 0.18
        income = lognormal(11.08 + credit_nudge, 0.55)
        annual_income = round(clamp(income, 12_000, 500_000), 2)

        # Loan amount: lognormal median ~8500
        loan_amount = round(clamp(lognormal(9.05, 0.65), 1_000, 35_000), 2)

        purpose = weighted_choice(purposes, purpose_weights)

        # Employment years: right-skewed (use lognormal capped at 30)
        emp_years = round(clamp(lognormal(1.2, 0.9), 0, 30), 1)

        # DTI: higher for lower credit scores
        dti_base = 0.32 - (credit_score - 682) / 72 * 0.06
        dti = round(clamp(normal(dti_base, 0.10), 0.05, 0.65), 4)

        # Approval logic with noise
        base_approve = 1 if (credit_score >= 640 and dti < 0.45) else 0
        noise = random.random()
        if base_approve == 1:
            approved = 0 if noise < 0.05 else 1   # 5% false-negative
        else:
            approved = 1 if noise < 0.08 else 0   # 8% false-positive

        # Interest rate: 8% base + risk adjustment
        risk_spread = max(0, (700 - credit_score) / 700 * 12)
        interest_rate = round(clamp(8.0 + risk_spread + normal(0, 0.5), 5.5, 28.0), 2)

        # Default flag (only meaningful for approved loans)
        p_default = sigmoid(-(credit_score - 600) / 80)
        default_flag = 1 if (approved == 1 and random.random() < p_default) else 0

        orig_date = random_date(three_years_ago, TODAY).isoformat()

        rows.append({
            "application_id": app_id,
            "credit_score": credit_score,
            "annual_income": annual_income,
            "loan_amount": loan_amount,
            "loan_purpose": purpose,
            "employment_years": emp_years,
            "debt_to_income": dti,
            "approved": approved,
            "interest_rate": interest_rate,
            "default_flag": default_flag,
            "origination_date": orig_date,
        })

    df = pd.DataFrame(rows)
    path = os.path.join(HERE, "loan_applications.csv")
    df.to_csv(path, index=False)
    print(f"Generated loan_applications.csv ({len(df)} rows)")
    return df

# ─── 2. transactions.csv  (50,000 rows) ─────────────────────────────────────

MERCHANTS = [
    ("Amazon", "shopping"), ("Walmart", "shopping"), ("Target", "shopping"),
    ("Best Buy", "shopping"), ("eBay", "shopping"), ("Etsy", "shopping"),
    ("Nike", "shopping"), ("Costco", "shopping"),
    ("McDonald's", "food"), ("Starbucks", "food"), ("DoorDash", "food"),
    ("Uber Eats", "food"), ("Chipotle", "food"), ("Domino's", "food"),
    ("Panera", "food"), ("Subway", "food"),
    ("Uber", "transport"), ("Lyft", "transport"), ("Delta Airlines", "travel"),
    ("United Airlines", "travel"), ("Airbnb", "travel"), ("Marriott", "travel"),
    ("Hertz", "travel"), ("Expedia", "travel"),
    ("Netflix", "entertainment"), ("Spotify", "entertainment"),
    ("Hulu", "entertainment"), ("Apple Music", "entertainment"),
    ("AMC Theaters", "entertainment"), ("Steam", "entertainment"),
    ("AT&T", "utilities"), ("Verizon", "utilities"), ("Comcast", "utilities"),
    ("PG&E", "utilities"), ("T-Mobile", "utilities"),
    ("CVS Pharmacy", "healthcare"), ("Walgreens", "healthcare"),
    ("UnitedHealth", "healthcare"), ("Kaiser", "healthcare"),
    ("One Medical", "healthcare"),
    ("PayPal", "shopping"), ("Square", "shopping"), ("Venmo", "shopping"),
    ("Robinhood", "shopping"), ("Coinbase", "shopping"),
    ("Whole Foods", "food"), ("Trader Joe's", "food"),
    ("Shell Gas", "transport"), ("BP Gas", "transport"),
    ("American Airlines", "travel"),
]

def generate_transactions():
    TODAY = datetime.date(2026, 3, 25)
    ninety_days_ago = TODAY - datetime.timedelta(days=90)

    devices = ['mobile', 'web', 'pos']
    device_weights = [0.55, 0.28, 0.17]

    statuses = ['completed', 'declined', 'pending']
    status_weights = [0.97, 0.02, 0.01]

    rows = []
    for i in range(1, 50_001):
        txn_id = f"TXN_{i:08d}"
        user_id = f"USR_{random.randint(1, 10000):05d}"

        merchant, category = random.choice(MERCHANTS)

        # Amount: lognormal median ~42
        amount = round(clamp(lognormal(3.74, 1.1), 1.0, 15_000), 2)

        # Timestamp: skewed toward business hours
        day = random_date(ninety_days_ago, TODAY)
        # Business hours bias: hour weighted toward 8am-8pm
        hour_r = random.random()
        if hour_r < 0.70:
            hour = random.randint(8, 20)
        else:
            hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        ts = datetime.datetime(day.year, day.month, day.day, hour, minute, second)

        # Country
        is_foreign = random.random() < 0.08
        country = random.choice(['CA', 'GB', 'MX', 'AU', 'DE', 'FR', 'JP', 'BR']) if is_foreign else 'US'

        # Fraud: base 0.3%, higher for foreign + high amount
        p_fraud = 0.003
        if is_foreign:
            p_fraud *= 5
        if amount > 500:
            p_fraud *= 3
        if amount > 2000:
            p_fraud *= 2
        p_fraud = min(p_fraud, 0.40)
        is_fraud = 1 if random.random() < p_fraud else 0

        device = weighted_choice(devices, device_weights)
        status = weighted_choice(statuses, status_weights)

        rows.append({
            "transaction_id": txn_id,
            "user_id": user_id,
            "merchant_name": merchant,
            "category": category,
            "amount": amount,
            "timestamp": ts.isoformat(),
            "is_fraud": is_fraud,
            "device_type": device,
            "country": country,
            "status": status,
        })

    df = pd.DataFrame(rows)
    path = os.path.join(HERE, "transactions.csv")
    df.to_csv(path, index=False)
    print(f"Generated transactions.csv ({len(df)} rows)")
    return df

# ─── 3. payments_funnel.csv  (20,000 rows) ──────────────────────────────────

def generate_payments_funnel():
    TODAY = datetime.date(2026, 3, 25)
    one_year_ago = TODAY - datetime.timedelta(days=365)

    # Conversion rates per step transition
    rates = {
        'A': [0.78, 0.72, 0.85, 0.91],
        'B': [0.81, 0.75, 0.88, 0.92],
    }

    rows = []
    for i in range(1, 20_001):
        session_id = f"SES_{i:07d}"
        user_id = f"USR_{random.randint(1, 10000):05d}"
        date = random_date(one_year_ago, TODAY).isoformat()
        variant = 'A' if random.random() < 0.5 else 'B'
        r = rates[variant]

        step1 = 1  # always viewed
        step2 = 1 if random.random() < r[0] else 0
        step3 = 1 if (step2 == 1 and random.random() < r[1]) else 0
        step4 = 1 if (step3 == 1 and random.random() < r[2]) else 0
        step5 = 1 if (step4 == 1 and random.random() < r[3]) else 0

        converted = step5
        revenue = round(lognormal(4.44, 0.65), 2) if converted else 0.0

        # Drop step
        if converted:
            drop_step = None
        elif step4 == 1:
            drop_step = 5
        elif step3 == 1:
            drop_step = 4
        elif step2 == 1:
            drop_step = 3
        elif step1 == 1:
            drop_step = 2
        else:
            drop_step = 1

        rows.append({
            "session_id": session_id,
            "user_id": user_id,
            "date": date,
            "step_1_viewed": step1,
            "step_2_details": step2,
            "step_3_payment": step3,
            "step_4_confirm": step4,
            "step_5_complete": step5,
            "variant": variant,
            "converted": converted,
            "revenue": revenue,
            "drop_step": drop_step,
        })

    df = pd.DataFrame(rows)
    path = os.path.join(HERE, "payments_funnel.csv")
    df.to_csv(path, index=False)
    print(f"Generated payments_funnel.csv ({len(df)} rows)")
    return df

# ─── 4. user_growth.csv  (5,000 rows) ───────────────────────────────────────

def generate_user_growth():
    TODAY = datetime.date(2026, 3, 25)
    eighteen_months_ago = TODAY - datetime.timedelta(days=548)

    channels = ['organic', 'paid_search', 'referral', 'social', 'email']
    channel_weights = [0.30, 0.25, 0.18, 0.17, 0.10]

    tiers = ['free', 'basic', 'premium']
    tier_weights = [0.50, 0.35, 0.15]

    tier_revenue = {'free': 0.0, 'basic': 9.0, 'premium': 29.0}

    rows = []
    for i in range(1, 5_001):
        user_id = f"UGR_{i:05d}"
        signup_date = random_date(eighteen_months_ago, TODAY)

        channel = weighted_choice(channels, channel_weights)

        # Days to first transaction: right-skewed, most within 3 days
        r = random.random()
        if r < 0.55:
            days_to_first = random.randint(0, 3)
        elif r < 0.85:
            days_to_first = random.randint(4, 14)
        else:
            days_to_first = random.randint(15, 30)

        # LTV: lognormal median ~48, referral 40% higher
        ltv_base = 3.87  # ln(48)
        ltv_boost = 0.34 if channel == 'referral' else 0.0  # ~40% higher
        ltv_90d = round(max(0, lognormal(ltv_base + ltv_boost, 0.75)), 2)

        # Churn: 18% rate
        churned = 1 if random.random() < 0.18 else 0
        if churned:
            churn_days = random.randint(14, 90)
            churn_date = (signup_date + datetime.timedelta(days=churn_days)).isoformat()
        else:
            churn_date = None

        tier = weighted_choice(tiers, tier_weights)
        # Add small noise to revenue
        base_rev = tier_revenue[tier]
        monthly_revenue = round(base_rev + normal(0, base_rev * 0.05) if base_rev > 0 else 0.0, 2)
        monthly_revenue = max(0.0, monthly_revenue)

        rows.append({
            "user_id": user_id,
            "signup_date": signup_date.isoformat(),
            "acquisition_channel": channel,
            "days_to_first_transaction": days_to_first,
            "ltv_90d": ltv_90d,
            "churned": churned,
            "churn_date": churn_date,
            "product_tier": tier,
            "monthly_revenue": monthly_revenue,
        })

    df = pd.DataFrame(rows)
    path = os.path.join(HERE, "user_growth.csv")
    df.to_csv(path, index=False)
    print(f"Generated user_growth.csv ({len(df)} rows)")
    return df

# ─── 5. stock_prices.csv  (~5,000 rows: 10 tickers × 500 trading days) ──────

def generate_stock_prices():
    tickers_config = {
        "SQ":   {"S0": 70,  "mu": 0.08,  "sigma": 0.35},
        "AFRM": {"S0": 25,  "mu": -0.05, "sigma": 0.55},
        "PYPL": {"S0": 60,  "mu": 0.05,  "sigma": 0.35},
        "COIN": {"S0": 180, "mu": 0.15,  "sigma": 0.60},
        "HOOD": {"S0": 15,  "mu": 0.03,  "sigma": 0.55},
        "SOFI": {"S0": 8,   "mu": 0.06,  "sigma": 0.50},
        "V":    {"S0": 240, "mu": 0.10,  "sigma": 0.20},
        "MA":   {"S0": 420, "mu": 0.12,  "sigma": 0.20},
        "UPST": {"S0": 30,  "mu": -0.03, "sigma": 0.60},
        "LC":   {"S0": 18,  "mu": 0.04,  "sigma": 0.50},
    }

    # Generate 500 trading dates ending today
    TODAY = datetime.date(2026, 3, 25)
    trading_dates = []
    d = TODAY - datetime.timedelta(days=730)  # start roughly 2 years back
    while len(trading_dates) < 500:
        if d.weekday() < 5:  # Mon-Fri
            trading_dates.append(d)
        d += datetime.timedelta(days=1)
    trading_dates = trading_dates[:500]

    dt = 1 / 252  # daily time step

    rows = []
    for ticker, cfg in tickers_config.items():
        S0 = cfg["S0"]
        mu = cfg["mu"]
        sigma = cfg["sigma"]

        drift = (mu - 0.5 * sigma ** 2) * dt
        vol = sigma * math.sqrt(dt)

        price = S0
        prev_close = S0

        for date in trading_dates:
            # GBM step
            z = normal(0, 1)
            daily_return = drift + vol * z
            close = prev_close * math.exp(daily_return)
            close = max(close, 0.50)  # floor

            # OHLC
            open_price = prev_close * math.exp(normal(0, 0.005))
            open_price = max(open_price, 0.50)

            hi_noise = abs(normal(0, 0.01))
            lo_noise = abs(normal(0, 0.01))
            high = close * (1 + hi_noise)
            low = close * (1 - lo_noise)
            # Ensure high >= open, close and low <= open, close
            high = max(high, open_price, close)
            low = min(low, open_price, close)

            adj_close = close  # simplified: no dividends/splits modeled

            # Volume: lognormal, higher on volatile days
            abs_return = abs(daily_return)
            vol_scalar = 1.0 + abs_return / (vol * 5)  # amplify on big days
            base_vol = lognormal(14.5, 0.6)  # median ~2M shares
            volume = int(base_vol * vol_scalar)

            rows.append({
                "ticker": ticker,
                "date": date.isoformat(),
                "open": round(open_price, 2),
                "high": round(high, 2),
                "low": round(low, 2),
                "close": round(close, 2),
                "volume": volume,
                "adj_close": round(adj_close, 2),
            })

            prev_close = close

    df = pd.DataFrame(rows)
    path = os.path.join(HERE, "stock_prices.csv")
    df.to_csv(path, index=False)
    print(f"Generated stock_prices.csv ({len(df)} rows)")
    return df

# ─── 6. fintech_kpis.csv  (36 rows — monthly) ───────────────────────────────

def generate_fintech_kpis():
    # 36 months ending 2026-03-01
    start = datetime.date(2023, 4, 1)
    months = []
    for i in range(36):
        y = start.year + (start.month - 1 + i) // 12
        m = (start.month - 1 + i) % 12 + 1
        months.append(datetime.date(y, m, 1))

    rows = []
    gmv = 2_000_000
    active_users = 5_000

    for idx, month_date in enumerate(months):
        t = idx  # 0-indexed

        # Seasonal variation: slight dip in summer, bump in Q4
        month_num = month_date.month
        seasonal = 1.0 + 0.04 * math.sin((month_num - 3) * math.pi / 6)

        # GMV: 4% MoM growth + seasonal + noise
        gmv *= (1 + 0.04 + normal(0, 0.005)) * seasonal
        gmv_val = round(gmv, 0)

        # Active users: correlated with GMV growth
        active_users = int(active_users * (1 + 0.035 + normal(0, 0.004)) * seasonal)

        # Take rate: starts 2.0%, slight compression to ~1.85%
        take_rate = 0.020 - t * 0.000042 + normal(0, 0.001)
        take_rate = round(clamp(take_rate, 0.018, 0.022), 5)

        revenue = round(gmv_val * take_rate, 0)

        # Net loss rate: starts 3.5%, improves to ~2.8%
        net_loss_rate = 0.035 - t * 0.000194 + normal(0, 0.001)
        net_loss_rate = round(clamp(net_loss_rate, 0.026, 0.038), 5)

        # CAC: starts $85, falls to ~$55
        cac = 85 - t * 0.833 + normal(0, 1.5)
        cac = round(clamp(cac, 52, 90), 2)

        # LTV: starts $120, rises to ~$180
        ltv = 120 + t * 1.667 + normal(0, 2.0)
        ltv = round(clamp(ltv, 115, 190), 2)

        ltv_cac_ratio = round(ltv / cac, 3)

        # NPS: starts 32, trends to 48
        nps = 32 + t * 0.444 + normal(0, 2.0)
        nps = round(clamp(nps, 28, 52), 1)

        # Approval rate: 58-67%
        approval_rate = 0.58 + t * 0.00025 + normal(0, 0.005)
        approval_rate = round(clamp(approval_rate, 0.56, 0.68), 4)

        # Default rate: 3.5-5.2%
        default_rate = 0.052 - t * 0.000333 + normal(0, 0.002)
        default_rate = round(clamp(default_rate, 0.032, 0.054), 5)

        rows.append({
            "month": month_date.isoformat(),
            "gmv": gmv_val,
            "active_users": active_users,
            "take_rate": take_rate,
            "revenue": revenue,
            "net_loss_rate": net_loss_rate,
            "cac": cac,
            "ltv": ltv,
            "ltv_cac_ratio": ltv_cac_ratio,
            "nps": nps,
            "approval_rate": approval_rate,
            "default_rate": default_rate,
        })

    df = pd.DataFrame(rows)
    path = os.path.join(HERE, "fintech_kpis.csv")
    df.to_csv(path, index=False)
    print(f"Generated fintech_kpis.csv ({len(df)} rows)")
    return df

# ─── load into SQLite ────────────────────────────────────────────────────────

def load_to_sqlite(dataframes: dict):
    db_path = os.path.join(HERE, "..", "orion.db")
    db_path = os.path.abspath(db_path)
    conn = sqlite3.connect(db_path)

    datasets = [
        ("loan_applications", "loan_applications.csv"),
        ("transactions", "transactions.csv"),
        ("payments_funnel", "payments_funnel.csv"),
        ("user_growth", "user_growth.csv"),
        ("stock_prices", "stock_prices.csv"),
        ("fintech_kpis", "fintech_kpis.csv"),
    ]
    for table_name, filename in datasets:
        df = pd.read_csv(os.path.join(HERE, filename))
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {len(df)} rows into {table_name}")

    conn.close()
    print(f"\nDone! Database written to: {db_path}")

# ─── main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating datasets...\n")
    dfs = {}
    dfs["loan_applications"] = generate_loan_applications()
    dfs["transactions"] = generate_transactions()
    dfs["payments_funnel"] = generate_payments_funnel()
    dfs["user_growth"] = generate_user_growth()
    dfs["stock_prices"] = generate_stock_prices()
    dfs["fintech_kpis"] = generate_fintech_kpis()

    print("\nLoading into SQLite...")
    load_to_sqlite(dfs)
