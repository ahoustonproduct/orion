# Orion — Adversarial Code Review

**Date:** 2026-04-24
**Scope:** `/backend` (FastAPI + SQLite), `/frontend` (Next.js 15 App Router), `/tutor-training` (MLX LoRA + Modelfile), root configs, `.git` state, shell scripts.
**Excluded from deep pass:** vendored `tutor-training/llama.cpp/**`, safetensors weights, `node_modules`, Python venv.
**Findings verified against source:** CORS config, execute.py shell construction, SQL regex filter, `.gitignore` contents, tracked-files list. Where agent output disagreed with `git ls-files`, the git state wins and is noted inline.

---

## TL;DR

The repo has four **CRITICAL** problems you should fix today, in this order:

1. **Your GitHub PAT is committed into `.git/config`** as a plaintext remote URL. It is readable by anyone who ever clones this machine's working copy. Rotate it now.
2. **`frontend/backend/orion.db` is tracked in git.** Any user data in it is in the repo history.
3. **`/execute/python` builds a shell-looking `pip install …` command by string-concatenating library names into a Python string passed to `python -c`.** It doesn't go through a real shell, so it isn't a classic shell injection, but the control flow is fragile and already has a defensive-regex gap (see finding C3). Fix by never constructing the command as a string.
4. **CORS is `allow_origins=["*"]` with `allow_credentials=True`.** Modern browsers reject that combination, so it actually hides bugs rather than opening you up — but if you ever add cookies / real auth, every origin becomes trusted.

After that, the theme is the same across the stack: **no auth, `user_key` is a URL/localStorage string that grants full read/write to that user's data**, and **everything trusts everything**. Right now that's fine for a single-user learning app, but it caps your production readiness hard.

Counts across the three review streams:

| Severity   | Backend | Frontend | Repo/Training | Total |
|------------|--------:|---------:|--------------:|------:|
| CRITICAL   |       4 |        4 |             2 |    10 |
| HIGH       |       7 |        7 |             3 |    17 |
| MEDIUM     |       7 |       10 |             5 |    22 |
| LOW / NIT  |      20+|        8 |             5 |    33+|

---

## 1. CRITICAL

### C1 — GitHub Personal Access Token committed to local git config
**File:** `.git/config`
**Evidence:** `git remote -v` shows `https://github.com/ahoustonproduct/orion.git`
**Impact:** Anyone with read access to this workstation (or a backup, or a leaked `~/Library/Application Support` folder) has your push creds for `ahoustonproduct/orion` and whatever scopes the token grants.
**Fix:**
1. Revoke the token at https://github.com/settings/tokens immediately.
2. Switch to the `gh` credential helper or SSH:
   ```bash
   cd ~/orion
   git remote set-url origin git@github.com:ahoustonproduct/orion.git
   # or:
   gh auth login
   git remote set-url origin https://github.com/ahoustonproduct/orion.git
   ```
3. Check the token wasn't ever pushed. It wasn't tracked (`.git/config` is local-only), so the remote is clean — but the token *is* in the shell history of any terminal that ran `git clone` with that URL, and it's in this conversation. Rotate.

### C2 — SQLite database file tracked in git
**File:** `frontend/backend/orion.db` (confirmed via `git ls-files`)
**Note on a related agent claim:** `backend/orion_code.db` is NOT tracked — `backend/*.db` in `.gitignore` covers it. Only the frontend copy leaks.
**Impact:** User progress, confidence ratings, notebooks — whatever is in that file is in the repo and in every clone and every fork.
**Fix:**
```bash
cd ~/orion
git rm --cached frontend/backend/orion.db
echo -e '\n**/*.db\n*.db\nfrontend/backend/*.db\n' >> .gitignore
git commit -m "stop tracking stray sqlite db, widen gitignore"
```
If the DB contained anything sensitive, also rewrite history with `git filter-repo --path frontend/backend/orion.db --invert-paths` and force-push, or rotate any secrets that were inside the db rows.

### C3 — `/execute/python` pip-install path is string-built and bypasses its own whitelist
**File:** `backend/routes/execute.py` lines ~95–103 (verified)
```python
needed_libs = _check_data_science_imports(code)
cmd = [sys.executable, "-c", code]
if needed_libs:
    install_cmd = f"pip install --quiet {' '.join(needed_libs)} && {sys.executable} -c {repr(code)}"
    cmd = [sys.executable, "-c", install_cmd]
```
**Impact:** Not a classic shell injection — `subprocess.run(cmd)` has `shell=False`, so `python -c "…"` treats the entire `install_cmd` as one Python program. But that Python program ends up running `pip install <names> && python -c <code>` via Python's own subprocess layer. The "whitelist" is `_check_data_science_imports(code)`, which greps the user's source. A submitted string like `import numpy # also\nimport pwntools` can confuse that regex and surface a library name the user didn't intend. Even without an exploit, the whole pattern is brittle: you're round-tripping user code through `repr()` and re-executing the string.
**Fix:** Don't build a command as a string.
```python
if needed_libs:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", *needed_libs],
        timeout=30, check=False,
    )
result = subprocess.run(
    [sys.executable, "-c", code],
    capture_output=True, text=True, timeout=15,
)
```
Same fix applies to `/execute/multi` (lines ~230–232).
**Bigger point:** This endpoint runs arbitrary student Python on your server with a 15 s timeout and no sandbox (no `seccomp`, no `nsjail`, no Docker, no uid isolation). That's fine for localhost, but if this ever faces the public internet, put the executor behind gVisor, Firecracker, or at minimum a hardened container.

### C4 — CORS: wildcard origins with credentials
**File:** `backend/main.py` lines 33–39 (verified)
```python
allow_origins=["*"], allow_credentials=True,
allow_methods=["*"], allow_headers=["*"],
```
**Impact:** Browsers silently refuse this combo, so it's not exploitable *today* — you're just getting no CORS enforcement at all. The moment you add a session cookie or `Authorization` header, every site on the web can ride the user's credentials.
**Fix:**
```python
allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
allow_credentials=True,
allow_methods=["GET", "POST", "PUT", "DELETE"],
allow_headers=["Content-Type"],
```

### C5 — No authentication or authorization anywhere
**Files:** every route under `backend/routes/` that takes `{user_key}` as a path param.
**Impact:** The user_key in the URL is the identity. There is nothing stopping me from `POST /progress/alice/lesson {lesson_id:…, stars:3}` or reading `/progress/alice`. Combined with C4 being fixed wrong (e.g. you later add `allow_origins=["*"]` from the frontend), this becomes a "horizontal privilege escalation" across all users.
**Fix plan:** Add a minimal bearer-token or httpOnly-cookie auth middleware. For now, at least validate that `user_key` matches a claim:
```python
def require_user(user_key: str, token: str = Depends(oauth2_scheme)) -> str:
    claimed = verify(token).sub
    if claimed != user_key: raise HTTPException(403)
    return user_key
```

### C6 — SQL executor whitelist is regex-only and leaks data
**File:** `backend/routes/execute.py` lines ~135–166 (verified)
The filter rejects non-`SELECT`, semicolons, and certain DML keywords, then runs the user's raw SQL against the shared app database `orion_code.db`.
**Impact:** Students can `SELECT * FROM user_progress` or `SELECT * FROM learning_profiles` and see every user's data. There is no row-level filter. Commenting out the semicolon check, inline UNION, recursive CTEs, or `json_each()` of a JSON column all slip through a keyword-only deny list.
**Fix:** Expose a **curated** set of views, not the live app DB. Create `/backend/sandbox_data.db` with pedagogical tables (`customers`, `orders`, etc.) and point the executor at *that* file. Never give students read access to the same DB that holds user progress.

### C7 — Streaming markdown through `react-markdown` with no sanitization
**File:** `frontend/app/learn/[lessonId]/page.tsx` (custom `Markdown` component)
**Impact:** Your LLM can produce HTML-in-markdown, raw HTML blocks, `javascript:` URLs, and `<img onerror=…>`. Whatever the backend streams into the chat sidebar or lesson body executes as DOM. Since the payload source includes user-supplied prompts being reflected by the model, a classic prompt-injection → XSS chain is plausible.
**Fix:** Either `rehype-sanitize` or a disallowlist:
```tsx
import rehypeSanitize from "rehype-sanitize";
<ReactMarkdown rehypePlugins={[rehypeSanitize]} remarkPlugins={[remarkGfm]}>
```
and audit every other place where streamed text from `streamPost` goes into a React tree.

### C8 — Hydration mismatch: `useState(Date.now())`
**File:** `frontend/app/learn/[lessonId]/page.tsx:52`
```ts
const [startTime] = useState(Date.now());
```
**Impact:** Server render captures the server's `Date.now()`, client render captures the client's. React 19's stricter hydration flags this and triggers a full client re-render, which silently resets any other component state that was derived from SSR output. Fix by moving to `useRef`:
```ts
const startTimeRef = useRef<number | null>(null);
if (startTimeRef.current === null) startTimeRef.current = Date.now();
```
Or just make the page a client-only component (the file is already `"use client"`, so SSR probably doesn't actually render it — verify and either remove the worry or apply the ref fix).

### C9 — `localStorage` + `user_key` treated as a bearer credential
**File:** `frontend/lib/user.ts`
**Impact:** The `user_key` is generated client-side, stored in `localStorage`, *and* exposed in the URL (for cross-device sync). Any XSS (see C7) exfiltrates every user's progress forever. A shared-link QR code can be intercepted in transit.
**Fix (medium-term):** Move auth to httpOnly cookies issued by the backend. **Short-term mitigation:** at least wrap every `localStorage` access in `typeof window !== "undefined"` + `try/catch` so SSR and private-mode Safari stop throwing.

### C10 — SQLite with `check_same_thread=False` + background threads writing to the same DB
**File:** `backend/models.py:12`, `backend/routes/notebooks.py` (`_generate_notebook_background`)
**Impact:** `check_same_thread=False` silences the safety check, it doesn't create safety. `notebooks.py` spawns background workers that open their own `SessionLocal()` and commit mid-flight while the FastAPI request handler might be reading the same row. SQLite will serialize writes, but readers can see the "generating" tombstone row as `ready` with partial `module_data` depending on commit ordering.
**Fix:** For real concurrency, move to Postgres. As a stopgap in SQLite, set `pool_pre_ping=True`, `journal_mode=WAL`, `timeout=10`, and collapse the 3-commit background flow to one atomic write at the end.

---

## 2. HIGH

### H1 — Datetime: naive vs aware mixed across models and routes
`backend/models.py` uses `datetime.now(timezone.utc)` in defaults, but routes (`progress.py`, `notebooks.py`) call the deprecated `datetime.utcnow()`. Comparisons across these will raise or silently bucket wrong across DST / midnight UTC. Standardize on `datetime.now(timezone.utc)` and lint with `ruff DTZ005`.

### H2 — Lesson progress updates span four commits with no transaction
`backend/routes/progress.py` `update_lesson_progress` commits the progress row, then `_update_streak`, `_update_weak_topics`, `_update_mastered` each commit separately. Two concurrent `POST /progress/{user}/lesson` requests interleave and the later one can reset earlier fields. Collapse into one `db.commit()` at the end wrapped in `try/except → db.rollback(); raise`.

### H3 — Silent `except Exception: pass` blocks
`backend/routes/notebooks.py:113,118,149,179,397` and `progress.py:314`. Swapping these for `logger.warning("…", exc_info=True)` turns "the notebook just never generated, I don't know why" into a debuggable error.

### H4 — Quiz generation drops malformed LLM JSON silently
`backend/routes/quiz.py:104–114`. The user sees a short quiz, you don't know why. Log the parse failure, and fall back to a seeded question from the lesson's `questions[]` so you always return the count you promised.

### H5 — `ConfidenceUpdate.rating` not bounded
`backend/routes/progress.py` ~224. Student can POST `rating: 9999` and it's stored. Add `rating: int = Field(..., ge=1, le=5)`.

### H6 — `/execute/multi` file paths not basename-stripped
`backend/routes/execute.py:205`. `file["name"]` goes straight into `os.path.join(tmp, …)`. `"../../evil.py"` escapes the tempdir. Fix: `safe = os.path.basename(file["name"])` and reject non-`.py`/`.txt`.

### H7 — Pages-Router patterns in App Router: missing `error.tsx` / `loading.tsx`
`frontend/app/layout.tsx` has no error boundary, and most route folders lack `loading.tsx`. On any `fetchLesson` failure the user sees blank. Add `app/error.tsx` + per-route `loading.tsx` skeletons.

### H8 — `streamPost` never aborts on component unmount
`frontend/lib/api.ts` creates an AbortController for the per-request timeout but exposes no external signal. Every lesson page that streams (`lesson/…`, `week-review`) leaks a live fetch + calls `setState` on unmounted components. Add an optional `abortSignal?: AbortSignal` param and wire `useEffect` cleanup to abort.

### H9 — Type drift between `Lesson` interface and lesson JSON
Spot-checked `frontend/backend/curriculum_data/lessons/m01_l01.json` (rich `blocks[]` array) vs `m22_l01.json` (adds `lesson_number`, `status: "coming_soon"`, has only a stub notice block). The `Lesson` TypeScript interface does not describe this polymorphism; code that assumes `lesson.questions` or `lesson.challenge` will get `undefined` for capstone/coming-soon lessons and blow up. Add a discriminated union or validate with `zod` on fetch.

### H10 — Duplicate curriculum source of truth
Both `backend/curriculum_data/*.py` (Python objects, authoritative) and `frontend/backend/curriculum_data/lessons/*.json` (JSON copy) exist. They appear to be populated by different flows. Pick one. The JSON-per-lesson layout is better for partial loading; the Python modules are better for type-checked quiz rendering. Don't keep both in sync by hand.

### H11 — `prompt()` used for quiz free-text answers
`frontend/app/quiz/page.tsx:184–186`. Browser `prompt()` dialogs are inaccessible, unstyled, blocking, and blocked by some browsers. Replace with an inline `<input>` the way the lesson page does.

### H12 — CSP header not set
`frontend/next.config.ts`. Combined with C7, any XSS foothold becomes full account takeover. Add a CSP via `headers()` even if it starts permissive:
```ts
{ key: "Content-Security-Policy",
  value: "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' http://localhost:8001; img-src 'self' data: https:;" }
```

### H13 — `requirements.txt` and `package.json` have unpinned majors
`backend/requirements.txt` lists `fastapi`, `sqlalchemy`, `openai`, `requests` with no versions. A pip install six months from now could pull SQLAlchemy 3.x and break the entire app. Pin at least minor versions, ideally with `pip-tools` generating a `requirements.lock`.

### H14 — `run_training.sh` base model mismatch
`tutor-training/run_training.sh` line 16 sets `BASE_MODEL="unsloth/gemma-4-E4B-it"` but the `adapters/adapter_config.json` references a different base (the agent reported `mlx-community/gemma-2-9b-it-4bit`). If true, the LoRA adapter won't merge cleanly into the Modelfile base. Verify both files point at the same HF path and add `set -euo pipefail` to the shell script.

### H15 — `ahoustonproduct:<PAT>` in remote history is also in user's shell history
Separate from C1: even after token rotation, your `~/.zsh_history` / `~/.bash_history` still contains the `git clone https://…ghp_…@…` line. Scrub with `history -d` or delete the relevant file rows.

### H16 — No request size limits / rate limiting on the backend
Any endpoint, especially `/execute/python`, `/ai/*`, `/notebooks/generate`, can be spammed. Add `slowapi` or an upstream nginx limit.

### H17 — Frontend `BACKEND_URL` hardcoded to `http://localhost:8001` in `start.sh`
`frontend/start.sh:36`. Blocks staging deploys. Make it `${BACKEND_URL:-http://localhost:8001}`.

---

## 3. MEDIUM

### Backend
- **M-B1** — `ai.py` uses `print()` for warnings; move to `logger.warning(…)`.
- **M-B2** — `execute.py:4` unused `sqlite3` import in `execute_python` scope.
- **M-B3** — `ExecutePythonRequest.files` is defined but never read in `execute_python`; either use it or delete it.
- **M-B4** — `sqlite3` path to `orion_code.db` is recomputed from `__file__` in `execute.py`; reuse `models.DATABASE_URL` instead so moving the DB only touches one file.
- **M-B5** — Response shape inconsistency: `/execute/python` returns `{output, error, duration_ms}`; `/execute/multi` returns `{outputs, errors, duration_ms}`. Normalize to one envelope.
- **M-B6** — No FK / index on `UserProgress.lesson_id` or `ConfidenceRating.lesson_id` despite every query filtering on them; add `index=True`.
- **M-B7** — Weak topics stored as a JSON list on the profile row, rewritten on every update. Race-prone and non-indexable. If this scales past 100 weak topics per user, promote to a normalized table.
- **M-B8** — Global `_active_model` in `ai.py` is mutated from request handlers without a lock. Replace with `functools.lru_cache(maxsize=1)`.
- **M-B9** — `YouTube URL` validator accepts any 11-char `[A-Za-z0-9_-]` string even without a `youtube.com`/`youtu.be` host. Require a host match before falling through to the ID regex.
- **M-B10** — No pagination on `GET /notebooks/{user_key}` — fine now, hazard later.

### Frontend
- **M-F1** — `useRef<any>(null)` in `MultiFileEditor.tsx:27`. Type it with `monaco.editor.IStandaloneCodeEditor`.
- **M-F2** — `get<T>()` in `lib/api.ts:3–7` has no runtime validation; any backend shape-drift is a silent `undefined` in render. Introduce `zod`.
- **M-F3** — Tailwind `content` glob misses `./lib/**/*.{ts,tsx}`; any classNames built in libs won't be compiled in.
- **M-F4** — `components/AIChatSidebar.tsx` has no `Escape`-to-close and no focus trap, so keyboard users get stuck.
- **M-F5** — `components/NavBar.tsx` links to `/notebooks` which currently routes to `app/notebooks/page.tsx` — verify this actually renders the list (there's also `app/notebook/page.tsx`, singular, which looks older and may be dead).
- **M-F6** — `app/progress/page.tsx:9` calls `getUserKey()` on every render; stabilize with `useState` initializer or `useRef`.
- **M-F7** — `app/learn/[lessonId]/page.tsx` useEffect chain has no `isMounted` guard; on fast back/forward you'll set state on unmounted components.
- **M-F8** — `tsconfig.json` strict is on (good), but `noUncheckedIndexedAccess` is off — enable it; several `answers[currentIdx]` patterns assume non-undefined.
- **M-F9** — `post()` in `lib/api.ts` sends no `credentials: "include"`. When you finally add cookie-auth (see C9), you'll have to touch every call site.
- **M-F10** — `eslint.config.mjs` does not enable `react-hooks/exhaustive-deps` as `error`; the stale-closure bugs in the useEffect chain above would've been caught.

### Repo / training
- **M-R1** — `test.txt` at the repo root is tracked and empty. Delete.
- **M-R2** — `tutor-training/train.jsonl` has the "Hi Orion!" greeting repeated 50+ times; the model will overfit the greeting. Deduplicate and augment.
- **M-R3** — `generate_dataset.js` shuffles with `Math.random()` — not reproducible across runs. Use a seeded RNG.
- **M-R4** — Modelfile base model path `./orion-fused` is relative to cwd; break if run from repo root.
- **M-R5** — `start.sh` uses `export $(grep -v '^#' .env | xargs)` to load env — word-splits on values containing spaces. Use `set -a; . .env; set +a` instead.

---

## 4. LOW / NIT

These came through cleanly and are worth a sweep when you're in the area, not a dedicated sprint:

- Deprecated `datetime.utcnow()` usages throughout `progress.py`, `notebooks.py`.
- No cascade deletes on `UserProgress`/`ConfidenceRating` referencing `user_key`.
- Hardcoded backend port `8001` in `start.sh`.
- Global exception handler logs full tracebacks in any environment — gate on `ENV=production`.
- No soft-delete on notebooks; a mistaken `DELETE` is permanent.
- No database migration tool (Alembic) — `create_all()` works for prototypes, breaks at the first column rename.
- `frontend/app/curriculum/page.tsx:22` hardcodes `text-[#1c1410]` instead of the CSS var theme — creates drift with the `tailwind.config.ts` palette.
- `alert("Sync key applied…")` in `app/settings/page.tsx` should be a toast.
- `ConceptMap.tsx` returns `null` if `nodes` is empty — users see nothing and don't know why.
- Animation `style={{ animationDelay: "0.2s" }}` magic numbers in `app/page.tsx` — constantize.
- `tutor-training/orion-fused-safetensors/` is ignored; good. Make sure you don't accidentally add the raw `.safetensors` weights (check `git status` after any training run).

### Agent claims I could not verify and are likely wrong
- "12+ `.DS_Store` files are tracked" — `git ls-files | grep DS_Store` returned **zero**. `.DS_Store` is in `.gitignore` and no such files are tracked. Skip this one.
- "`backend/orion_code.db` is tracked" — it isn't. `.gitignore`'s `backend/*.db` covers it. Only `frontend/backend/orion.db` leaks.
- "SQL injection via `… OR '1'='1'`" in `execute.py` — strictly this is *data disclosure* (see C6), not classical SQL injection; the query is parameterless by design. Same severity, different label.

---

## 5. Suggested fix order

**Today (30 minutes of work):**
1. Rotate the GitHub PAT.
2. `git remote set-url origin` to SSH.
3. `git rm --cached frontend/backend/orion.db`, widen `.gitignore`, commit.
4. Delete `test.txt`.

**This week:**
5. Lock CORS origins (C4).
6. Rewrite `/execute/python` and `/execute/multi` to never string-build commands (C3); point SQL executor at a sandbox DB (C6).
7. Add `rehype-sanitize` to all `ReactMarkdown` call sites (C7).
8. Standardize datetime to `datetime.now(timezone.utc)` + collapse the 4-commit progress update into one transaction (H1, H2).
9. Pin `requirements.txt` versions; run `pip-audit`.

**Next sprint:**
10. Introduce real auth (httpOnly cookie + `Depends(get_current_user)` guard on every `{user_key}` route). Retire localStorage-based `user_key`.
11. Migrate SQLite → Postgres (C10). Add Alembic.
12. Deduplicate curriculum: delete `frontend/backend/curriculum_data/`, serve via API, validate with `zod` on the client.
13. Add `error.tsx` + `loading.tsx` at every route; add CSP + a real error boundary.
14. Fix training data: dedupe greetings, seed the shuffle, verify base-model/adapter match.

---

*End of review. I did not modify any files except this report. Let me know which section you want to start attacking and I'll hand you a PR-sized diff for it.*
