import pytest
import os
import sys
from importlib import reload
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_env(monkeypatch):
    """Provides a valid test environment set."""
    monkeypatch.setenv("KEEP_EMAIL", "test@test.com")
    monkeypatch.setenv("KEEP_TOKEN", "keep_token_123")
    monkeypatch.setenv("KEEP_NOTE_ID", "note_xyz")
    monkeypatch.setenv("TODOIST_API_KEY", "todoist_123")
    monkeypatch.setenv("TODOIST_PROJECT_ID", "proj_456")
    monkeypatch.setenv("GEMINI_API_KEY", "gemini_abc")
    monkeypatch.setenv("EXECUTION_MODE", "simulation")

@patch('main.KeepClient')
@patch('main.TodoistClient')
@patch('main.GeminiClient')
def test_main_simulation_flow(mock_gemini, mock_todoist, mock_keep, mock_env, capsys):
    """
    Test Step 12: Verifies mode orchestration and data flow via stdout parsing.
    Tests the case where new items are found, sorted, and no errors exist.
    """
    import main

    # 1. Setup Mock Returns
    mock_keep_inst = MagicMock()
    mock_keep_inst.get_list_items.return_value = ["apples", "milk", "bread"]
    mock_keep.return_value = mock_keep_inst

    mock_todoist_inst = MagicMock()
    mock_todoist_inst.get_project_sections.return_value = [{"id": "sec1", "name": "Produce"}, {"id": "sec2", "name": "Dairy"}]
    mock_todoist_inst.get_project_tasks.return_value = [{"content": "bread"}]
    mock_todoist.return_value = mock_todoist_inst

    mock_gemini_inst = MagicMock()
    # "bread" is evaluated as duplicate
    mock_gemini_inst.filter_duplicates.return_value = {
        "to_insert": ["apples", "milk"],
        "duplicates": ["bread"]
    }
    # Categorization map
    def side_effect_categorize(item, sections):
        if item == "apples": return "Produce"
        if item == "milk": return "Dairy"
        return "OTROS"
    mock_gemini_inst.categorize_item.side_effect = side_effect_categorize
    mock_gemini.return_value = mock_gemini_inst

    # 2. Run Main
    with patch.object(sys, 'argv', ['main.py']):
        try:
            main.main()
        except SystemExit as e:
            # We don't want the script to exit(1) on failure.
            # But the script will exit(0) on success? Actually currently it just falls off the end without exit(0).
            assert e.code == 0

    # 3. Assert Outputs
    captured = capsys.readouterr()
    output = captured.out

    assert "[*] Execution Mode: SIMULATION" in output
    assert "Found 3 items." in output             # Keep items
    assert "Found 2 sections and 1 existing tasks." in output # Todoist
    assert "Identified 1 duplicates." in output   # Gemini Filter
    assert "2 new items to insert." in output
    assert "SIMULATION COMPLETE" in output

    assert "Duplicates Skipped (1 total):" in output
    assert " - bread" in output
    assert "Categorized Additions (2 total):" in output
    assert "[Produce]" in output
    assert " + apples" in output
    assert "[Dairy]" in output
    assert " + milk" in output
