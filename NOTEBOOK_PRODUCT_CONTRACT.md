# Notebook Product Contract

## Core Contract

Orion notebooks are saved study modules. They are not created from YouTube, transcripts, web pages, or other sources inside the running app.

The core app supports:

- listing saved notebook modules for the local user
- opening a saved module and viewing its lessons
- launching saved-module lessons in the standard lesson experience
- tracking completion, stars, attempts, confidence, review, quiz, and mastery data for saved-module lessons
- deleting saved modules

The core app does not support:

- pasting a YouTube URL into Orion
- fetching transcripts from Orion
- calling an LLM to generate notebook lessons from Orion
- retrying failed in-app generation jobs
- managing a generation queue

## Future Curriculum Updates

Future video-based curriculum expansion should happen outside the app. The expected workflow is:

1. The app remains focused on learning, review, notes, and progress.
2. Source videos or links are reviewed separately.
3. New curriculum or saved-module JSON is produced outside Orion.
4. The resulting lessons are imported or committed as app content.

This keeps the current product stable while preserving a future path for richer curriculum expansion.
