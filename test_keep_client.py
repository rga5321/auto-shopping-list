import pytest
import os
from config import AppConfig
from keep_client import KeepClient

def test_keep_client_read_elements():
    """
    Integration test matching step 4. Connects to the real Google Keep endpoint.
    Requires valid KEEP_EMAIL, KEEP_TOKEN, and KEEP_NOTE_ID in the local `.env`.
    """
    # Initialize config. If .env isn't set up yet, this will gracefully raise ValueError 
    try:
        config = AppConfig()
    except ValueError as e:
        pytest.skip(f"Skipping Keep read test due to missing environment config: {e}")

    # Check if necessary variables are actually defined (in case they are empty strings etc)
    if not config.keep_email or not config.keep_token or not config.keep_note_id or config.keep_note_id == 'your_note_id':
        pytest.skip("Skipping Keep read test as .env variables are incomplete or contain dummy values.")

    # Initialize client (will hit Google Login endpoint)
    # This may raise an exception if credentials are invalid.
    client = KeepClient(config.keep_email, config.keep_token)

    # Note reading
    items = client.get_list_items(config.keep_note_id)
    
    # Validation logic - we expect a list. Even if the note is empty, it returns an empty list.
    assert isinstance(items, list)
    
    # Print the resulting elements if the test is run with `pytest -s` to inspect manually
    print(f"\\n[Real Endpoint] Fetched {len(items)} remaining items from Keep Note: {config.keep_note_id}")
    for idx, item in enumerate(items, 1):
         print(f" - {idx}: {item}")
