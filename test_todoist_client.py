import pytest
from config import AppConfig
from todoist_client import TodoistClient

def test_todoist_client_read_elements():
    """
    Integration test matching step 6. Connects to the real Todoist endpoint.
    Requires valid TODOIST_API_KEY and TODOIST_PROJECT_ID in the local .env.
    """
    try:
        config = AppConfig()
    except ValueError as e:
        pytest.skip(f"Skipping Todoist read test due to missing environment config: {e}")

    # Check if variables are valid/not dummy values
    if not config.todoist_api_key or config.todoist_api_key == "dummy" or not config.todoist_project_id or config.todoist_project_id == "dummy":
        pytest.skip("Skipping Todoist read test as .env variables contain dummy values or are incomplete.")

    client = TodoistClient(config.todoist_api_key)

    # Fetch sections
    sections = client.get_project_sections(config.todoist_project_id)
    assert isinstance(sections, list)

    # Fetch tasks
    tasks = client.get_project_tasks(config.todoist_project_id)
    assert isinstance(tasks, list)

    # Print results out when testing with -s
    print(f"\\n[Real Endpoint] Fetched {len(sections)} sections and {len(tasks)} tasks from Todoist Project: {config.todoist_project_id}")
    
    print("Sections:")
    for idx, sec in enumerate(sections, 1):
        print(f" - {idx}: {sec.get('name', 'Unnamed')}")

    print("Tasks:")
    for idx, task in enumerate(tasks, 1):
        # Using a fallback string if the task is not in a section
        section_name = "No Section"
        for sec in sections:
            if task.get('section_id') == sec.get('id'):
                section_name = sec.get('name', 'Unnamed')
                break
        print(f" - {idx}: {task.get('content', 'Unnamed')} (Section: {section_name})")
