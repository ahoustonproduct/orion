# Orion "Premium SaaS" Feature Expansion

Please resume work on the Orion Code platform. I have successfully upgraded the visual aesthetics across the entire platform, deploying a highly optimized **"Night Mode Digital Reader"** theme (warm charcoals, amber highlights, zero blue-light glare). Now, we need to significantly expand the platform's features to rival premium Business Analytics educational software.

Here is your exact roadmap. Please implement these in phases to ensure the application remains stable:

## Phase 1: The AI Co-Pilot & Rescue Mechanics
* **Interactive AI Sidebar**: Build a slide-out chat component right next to the code editor in `frontend/app/learn/[lessonId]/page.tsx`. Wire this up to a new streaming endpoint in `backend/routes/ai.py` so the user can highlight confusing text and ask questions mid-lesson.
* **Proactive Refactoring**: Attach an AI evaluation step to successful code submissions in the challenge runner. If the user's code passes but is poorly written (e.g., highly complex loop structures), have Orion point out a more elegant, industry-standard solution.
* **Rescue Mechanics**: If a user attempts a challenge more than 3 times and fails, display a "Reveal Solution" button. This should offer a full breakdown of the correct code so the user never gets permanently stuck.

## Phase 2: Curriculum Expansion & Data Science Sandbox
* **Data Science Infrastructure**: Update the backend code execution engine (`backend/routes/execute.py`) and the virtual environment (`requirements.txt`) to formally support executing Data Science libraries (`pandas`, `numpy`, `scipy`). Keep it secure, but ensure these run flawlessly.
* **Statistical Curriculum**: Build out a new `backend/curriculum_data/module6_stats.py` which teaches deep statistical concepts (regressions, p-values, correlations) tailored for business analytics via Pandas.
* **SQL Curriculum**: There is already a rudimentary `/sql` endpoint in `execute.py`. Build out `backend/curriculum_data/module7_sql.py` to teach SQLite database design, table joins, and aggregations.

## Phase 3: The Full IDE & Automated Notebook
* **Multi-file Editor Engine**: Upgrade the Frontend Monaco editor to support managing multiple tabs (files) at once, and upgrade the Backend `execute.py` to process multiple linked files concurrently. This will enable complex Capstone projects. 
* **The Smart Notebook**: Completely overhaul the `/notebook` UI. Instead of just a blank page, it should dynamically query the SQLite backend to automatically pull in the specific code structures the user struggled with from past lessons (essentially creating an automated midterm study cheat-sheet).

Please proceed with Phase 1 immediately, ensure the UI matches the new digital reader aesthetic, and verify the backend stays perfectly bug-free!
