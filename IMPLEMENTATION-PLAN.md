# Auto-Shopping-List Implementation Plan

This script synchronizes a grocery shopping list from a temporary Google Keep note to a final Todoist project. It uses Gemini Flash to handle duplicate detection and categorization, and supports both `simulation` and `real` operation modes.

## Implementation Steps

1 - Code the core configuration and environment variable loading (`.env` parsing).
2 - Code the test for (1) using pytest.
3 - Code the integration with Google Keep for reading the note and extracting checklist elements.
4 - Code the test for (3) hitting the real endpoint.
5 - Code the integration with Todoist for fetching the target project, its sections, and current tasks.
6 - Code the test for (5) hitting the real endpoint.
7 - Code the integration with Gemini-Flash-Latest for duplicate detection.
8 - Code the test for (7).
9 - Code the integration with Gemini-Flash-Latest for categorizing new items into Todoist sections.
10 - Code the test for (9).
11 - Code the logic to orchestrate the execution mode (`simulation` vs. `real`) and the data flow.
12 - Code the test for (11).
13 - Code the integration with Todoist for inserting new tasks into the appropriate sections (No test needed).
14 - Code the integration with Google Keep for marking checklist elements as completed (No test needed).
15 - Code the console output formatter (summary of insertions, section splits, and duplicates).
16 - Code the test for (15).

## Proposed Changes

### Core Script

#### [NEW] [main.py](file:///home/arg/repos/auto-shopping-list/main.py)
- Code the core configuration and environment variable loading (`.env` parsing).
- Code the mode orchestration logic (`simulation` vs. `real`).
- Code the console output formatter.

#### [NEW] [keep_client.py](file:///home/arg/repos/auto-shopping-list/keep_client.py)
- Code the integration with Google Keep for reading the note and extracting checklist elements.
- Code the integration for marking checklist elements as completed (active only in `real` mode).

#### [NEW] [todoist_client.py](file:///home/arg/repos/auto-shopping-list/todoist_client.py)
- Code the integration with the official Todoist API for fetching the target project, its sections, and current tasks.
- Code the integration for inserting new tasks into the appropriate sections (active only in `real` mode).

#### [NEW] [gemini_client.py](file:///home/arg/repos/auto-shopping-list/gemini_client.py)
- Code the integration with Gemini-Flash-Latest for duplicate detection.
- Code the integration for categorizing new items into Todoist sections.

### Testing Suite

#### [NEW] [test_config.py](file:///home/arg/repos/auto-shopping-list/test_config.py)
- Code tests for configuration loading using `pytest`.

#### [NEW] [test_keep_client.py](file:///home/arg/repos/auto-shopping-list/test_keep_client.py)
- Code tests for READING Keep notes utilizing the explicit Google Keep real endpoints via `pytest`.

#### [NEW] [test_todoist_client.py](file:///home/arg/repos/auto-shopping-list/test_todoist_client.py)
- Code tests for READING Todoist projects and tasks against the explicit Todoist real endpoints via `pytest`.

#### [NEW] [test_gemini_client.py](file:///home/arg/repos/auto-shopping-list/test_gemini_client.py)
- Code unit tests for Gemini duplicate detection and item categorization via `pytest`.

#### [NEW] [test_main.py](file:///home/arg/repos/auto-shopping-list/test_main.py)
- Code integration tests covering mode orchestration and simulated formatting output verification via `pytest`.

## Verification Plan

### Automated Tests
- Framework: `pytest`.
- Tests for READING elements from Keep API and Todoist API will intentionally hit **real endpoints** to ensure data synchronization and logic robustness.
- WRITING actions (marking elements as completed in Keep, adding to Todoist) will strictly **NOT** be tested automatically to prevent destructive operations against live user accounts.

### Manual Verification
- We'll run the script in `simulation` mode against a real Keep note and Todoist project to check the console output.
- After confirming the `simulation` successfully structures insertions and duplicate detections natively, we'll verify operations in `real` mode.
