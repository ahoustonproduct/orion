# Orion — Fix Session Handoff

You are taking over a code-review + fix session from a previous agent. Pick up exactly where they stopped. Do not re-plan, do not re-review — the review is done and agreed. Your job is to finish the agreed fix list.

---

## 1. What this repo is

- **Orion** — a single-user personal learning app for Hack (the user). No other accounts exist. Do NOT propose, design, or implement login/signup/auth. `user_key` in localStorage + URL is an acceptable identifier for this app.
- **Location:** `/Users/hack/orion`
- **Stack:** FastAPI + SQLite backend (`/backend`), Next.js 15 App Router frontend (`/frontend`), MLX LoRA tutor-training (`/tutor-training`).
- **Remote:** `https://github.com/ahoustonproduct/orion.git`. Push via macOS Keychain; there is already a fine-grained PAT stored under host `github.com` / username `ahoustonproduct`. Do NOT embed tokens in remote URLs. Do NOT switch to classic PATs.

## 2. Work driver

`/Users/hack/orion/ADVERSARIAL_REVIEW_2026-04-24.md` is the authoritative finding list. It has four CRITICAL items (C1–C4) already fixed and pushed as commit `c783b86` on `main`.

Hack then greenlighted tackling **C5, C6, C7, H2** next. Status of those four:

| ID | Status | Note |
|----|--------|------|
| **C5** (real auth) | **DROPPED** | Single-user app. Confirmed by Hack directly. Do not reopen. |
| **H2** (collapse 4-commit progress update into one tx) | **IN PROGRESS** | See §3 — one half done, one half remaining. |
| **C7** (rehype-sanitize on ReactMarkdown) | Queued | §4 |
| **C6** (SQL executor → sandbox DB) | Queued | §5 |

Every other finding in the review doc (H1, H3–H17, all MEDIUM, all LOW) is NOT in scope right now. If you see one while touching nearby code, DO NOT silently fix it. Call it out to Hack, move on.

## 3. IMMEDIATE NEXT ACTION — finish H2

**File:** `/Users/hack/orion/backend/routes/progress.py`

The handler `update_lesson_progress` has already been rewritten to do a single `db.commit()` at the end inside a try/except rollback block. But the three helpers it calls — `_update_streak`, `_update_weak_topics`, `_update_mastered` — still have the OLD signature (`db: Session` param + internal `db.commit()`). The new handler calls them WITHOUT the `db` arg, so the code currently raises `TypeError` at runtime. Fix this first.

**Change each helper to drop the `db` parameter and the internal commit.** Target state:

```python
def _update_streak(profile: LearningProfile, minutes: int) -> None:
    """Mutate streak / study_log on the profile in-place. Does NOT commit —
    the caller writes all mutations in a single transaction."""
    today = date.today()
    study_log = dict(profile.study_log or {})
    today_str = today.isoformat()
    study_log[today_str] = study_log.get(today_str, 0) + minutes
    profile.study_log = study_log

    if profile.last_active and profile.last_active == today:
        pass
    else:
        yesterday = today - timedelta(days=1)
        if profile.last_active == yesterday:
            profile.streak_count += 1
        else:
            profile.streak_count = 1
        profile.last_active = today


def _update_weak_topics(profile: LearningProfile, lesson_id: str, stars: int) -> None:
    """Mutate weak_topics on the profile in-place. Does NOT commit."""
    weak = list(profile.weak_topics or [])
    if stars < 3 and lesson_id not in weak:
        weak.append(lesson_id)
    elif stars == 3 and lesson_id in weak:
        weak.remove(lesson_id)
    profile.weak_topics = weak


def _update_mastered(profile: LearningProfile, lesson_id: str, stars: int) -> None:
    """Mutate mastered_concepts on the profile in-place. Does NOT commit."""
    mastered = list(profile.mastered_concepts or [])
    if stars == 3 and lesson_id not in mastered:
        mastered.append(lesson_id)
    profile.mastered_concepts = mastered
```

**Verify:**
```bash
grep -nE "db\.commit|db: Session" /Users/hack/orion/backend/routes/progress.py
```
The three helpers should NOT appear in that output. `get_or_create_profile` legitimately keeps its `db.commit()` — don't touch it. The main handler keeps its single `db.commit()` inside the try block — don't touch it.

**Smoke test:**
```bash
cd /Users/hack/orion/backend
source venv/bin/activate
python -c "from routes.progress import update_lesson_progress, _update_streak, _update_weak_topics, _update_mastered; print('imports ok')"
uvicorn main:app --port 8001 &
sleep 2
curl -s -X POST http://localhost:8001/progress/test_user/lesson \
  -H 'Content-Type: application/json' \
  -d '{"lesson_id":"m01_l01","stars":3,"attempts":1,"hints_used":0,"completed":true,"time_spent_minutes":5}'
kill %1
```
Expect `{"success":true,"stars":3}` and no exception in the uvicorn log.

**Commit message style (follow this voice):**
```
progress: collapse lesson update into one transaction

update_lesson_progress previously committed 4 times (progress row,
then streak / weak-topics / mastered in three helpers). A mid-flight
exception could leave half of the session persisted; two concurrent
POSTs could clobber each other's writes.

Helpers are now mutate-only; the handler wraps the whole update in one
commit with rollback on error. One commit, one consistent snapshot.
```

## 4. THEN — C7 (rehype-sanitize)

**Problem:** LLM-streamed markdown renders through `react-markdown` with no sanitization, so raw HTML, `javascript:` URLs, and `<img onerror=…>` all execute. Prompt-injection → XSS is plausible.

**Steps:**
1. `cd /Users/hack/orion/frontend && npm install --save rehype-sanitize`
2. Find every call site: `grep -rn "ReactMarkdown\|from \"react-markdown\"" app components lib`
3. At each site, add `import rehypeSanitize from "rehype-sanitize";` and thread it into `rehypePlugins`. Merge with existing `rehypePlugins` if any:
   ```tsx
   <ReactMarkdown
     remarkPlugins={[remarkGfm]}
     rehypePlugins={[rehypeSanitize]}
     components={{ /* existing */ }}
   >
     {content}
   </ReactMarkdown>
   ```
4. Also `grep -rn "dangerouslySetInnerHTML"` under `frontend/`. Each hit either needs removal or an explicit DOMPurify wrapper. Flag to Hack, don't auto-fix.
5. **Manual test:** Send a message to the AI sidebar containing `<script>alert('xss')</script>` and `<img src=x onerror=alert(1)>`. Neither should execute; both should render as visible text or be stripped.

**Commit message skeleton:**
```
frontend: sanitize all react-markdown render sites

Every <ReactMarkdown/> now runs through rehype-sanitize. LLM output
and streamed tokens flow through this path, so a model that emits
<script>, <iframe>, or javascript: URLs can no longer execute them
in the user's DOM.
```

## 5. THEN — C6 (sandbox SQL DB)

**Problem:** `POST /execute/sql` in `/Users/hack/orion/backend/routes/execute.py` runs SELECTs against `backend/orion_code.db` — the live app DB. A student query can `SELECT * FROM user_progress` and read Hack's own data. Even in a single-user app, this is a pedagogical-hygiene problem: the "student sandbox" and the "application state" must not share a file.

**End state:** a separate file `backend/sandbox_data.db` containing realistic pedagogical tables. `/execute/sql` points at that file. The app DB is never exposed to the SQL sandbox.

**Steps:**
1. Create `backend/scripts/seed_sandbox_db.py`:
   - Connects to `backend/sandbox_data.db` (absolute path relative to the script — use `os.path.join(os.path.dirname(__file__), "..", "sandbox_data.db")`).
   - `DROP TABLE IF EXISTS` each target table, then recreate. Idempotent.
   - Creates ~5 tables with natural FK relationships. Suggested schema:
     - `customers(id, name, email, country, signup_date)`
     - `products(id, name, category, price_cents, stock)`
     - `orders(id, customer_id FK, order_date, status)`
     - `order_items(id, order_id FK, product_id FK, quantity, unit_price_cents)`
     - `employees(id, name, role, hire_date, manager_id FK self)`
   - Seeds each: ~200 customers, ~50 products, ~500 orders, ~1500 order_items, ~30 employees. Hand-roll the data or use `random` with a fixed seed for reproducibility. Do not add `faker` as a dependency.
2. Run it: `cd /Users/hack/orion/backend && source venv/bin/activate && python scripts/seed_sandbox_db.py`. Confirm `backend/sandbox_data.db` is created.
3. Edit `/Users/hack/orion/backend/routes/execute.py::execute_sql`. Replace:
   ```python
   db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "orion_code.db")
   ```
   with:
   ```python
   db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sandbox_data.db")
   ```
   Add a one-line comment: `# NEVER point this at the app DB — see C6 in the review.`
4. Create `/Users/hack/orion/backend/SANDBOX_SCHEMA.md` — a short doc listing the five tables, column types, and 2–3 example queries per table. Curriculum authors will need this to write SQL lessons.
5. `.gitignore`: `backend/sandbox_data.db` is already covered by the `*.db` rule. The SEED SCRIPT (`scripts/seed_sandbox_db.py`) IS committed. The generated DB is not. Document how to regenerate in the README or SANDBOX_SCHEMA.md.
6. **Smoke test:**
   ```bash
   uvicorn main:app --port 8001 &
   sleep 2
   curl -s -X POST http://localhost:8001/execute/sql \
     -H 'Content-Type: application/json' \
     -d '{"query":"SELECT name, price_cents FROM products LIMIT 3"}'
   # should return rows from the seeded data, not an error
   curl -s -X POST http://localhost:8001/execute/sql \
     -H 'Content-Type: application/json' \
     -d '{"query":"SELECT * FROM user_progress LIMIT 1"}'
   # should fail with "no such table"
   kill %1
   ```

**Commit message skeleton:**
```
execute: isolate SQL sandbox from the app DB

/execute/sql previously ran SELECTs against orion_code.db, the live
app database. Any student query could SELECT * FROM user_progress.
Point it at sandbox_data.db instead — a separate file, seeded with
pedagogical customer/order/product tables, never touched by the
application. Adds scripts/seed_sandbox_db.py to regenerate and
SANDBOX_SCHEMA.md to document the tables.
```

## 6. Git workflow

- Branch: `main`. Commit directly.
- **One logical fix = one commit.** Descriptive body. Lead with the *why*, not a diff summary.
- **Before pushing**, squash micro-commits so each push has one commit per fix at most. Example:
  ```bash
  git reset --soft origin/main
  git commit -F <message-file>
  git push origin main
  ```
- Keychain-stored PAT handles auth. If you hit 403, the token may have expired or had its scope changed. STOP and tell Hack — do not work around it.

## 7. Style rules (non-negotiable)

- **Surgical.** Only fix what's on the list. If you see H1 (`datetime.utcnow` → `datetime.now(timezone.utc)`) or H5 (rating bounds) or anything else while you're in a file, do NOT touch it. Flag it, move on. Hack hasn't greenlighted it.
- **No chatty responses.** Hack reads diffs. Don't write a summary paragraph after every commit explaining what the diff already shows.
- **Run commands yourself.** If Hack says "run the pip install," you run it — don't print a code block and tell them to run it.
- **No emojis** in code, commits, docs, or responses unless Hack uses them first.
- **No scope-creep dependencies.** `rehype-sanitize` is required for C7. `faker`, `pytest`, `pre-commit`, etc. are not — do not add them.
- **Ask before:** touching schema migrations, switching DBs (SQLite → Postgres), touching the training pipeline, or Docker/sandboxing work.

## 8. What's in the repo that you should leave alone

- `tutor-training/llama.cpp/**` (vendored)
- `tutor-training/orion-fused-safetensors/` (ignored, large)
- `frontend/node_modules/`
- `backend/venv/`
- Any `.safetensors` file

## 9. When the three fixes (H2, C7, C6) are all done

Push. Then tell Hack:

> H2, C7, C6 done and pushed. From the review doc, the remaining HIGH items are H1, H3–H17 (skipping C5 which is dropped). MEDIUM is 22 items across backend/frontend/repo. Want me to keep going, pick a subset, or stop here?

Don't auto-continue. Let Hack choose.

---

*End of handoff. Start with §3.*
