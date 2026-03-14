# Auto-Shopping-List Orchestrator

An intelligent bridge between **Google Keep** and **Todoist**, powered by **Google Gemini**.

This project automates the creation of a categorized shopping list by syncing unchecked items from a Google Keep list into a structured Todoist project. It uses an LLM to understand item categories and prevent duplicates.

As there is not an official Google Keep API for consumers, the script used https://github.com/kiwiz/gkeepapi to interface with Google Keep. Read https://github.com/simon-weber/gpsoauth#alternative-flow to understand how to get the required master token.

## How it works

1.  **Fetch**: Retrieves unchecked items from a specific Google Keep note.
2.  **Analyze**: Compares Keep items with existing Todoist tasks using Gemini.
3.  **Deduplicate**: Identifies items that are already in Todoist (even with slightly different phrasing).
4.  **Categorize**: Maps new items to the appropriate sections in your Todoist project (e.g., "Produce", "Dairy", "Bakery").
5.  **Sync**: Inserts new tasks into Todoist and marks those items as completed in Google Keep.

## Key Features

-   **🧠 AI Categorization**: Automatically places items in the right aisle.
-   **🚫 Smart Deduplication**: Won't add "Milk" if "1L Milk" is already on your list.
-   **🛡️ Simulation Mode**: Preview all changes before they happen.
-   **⚡ Performance Tracking**: Displays execution duration and timestamps.

## Configuration

Define the following in a `.env` file at the root:

```env
EXECUTION_MODE=simulation  # 'simulation' or 'real'

# Google Keep config
KEEP_EMAIL=your_email@gmail.com
KEEP_TOKEN=your_app_password_or_token
KEEP_NOTE_ID=your_target_note_id

# Todoist config
TODOIST_API_KEY=your_todoist_api_key
TODOIST_PROJECT_ID=your_todoist_project_id

# Gemini config
GEMINI_API_KEY=your_gemini_api_key
```

## Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run**:
    ```bash
    python main.py
    ```

> [!TIP]
> Always run in `simulation` mode first to verify the AI's categorization and duplicate detection.
