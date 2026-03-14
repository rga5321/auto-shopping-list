import sys
from config import AppConfig
from keep_client import KeepClient
from todoist_client import TodoistClient
from gemini_client import GeminiClient

def main():
    print("=== Auto-Shopping-List Orchestrator ===")
    
    try:
        config = AppConfig()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    print(f"[*] Execution Mode: {config.mode.upper()}")
    
    # Initialize Clients
    try:
        keep_client = KeepClient(config.keep_email, config.keep_token)
        todoist_client = TodoistClient(config.todoist_api_key)
        gemini_client = GeminiClient(config.gemini_api_key)
    except Exception as e:
        print(f"Failed to initialize clients: {e}")
        sys.exit(1)

    # 1. Fetch Data
    print("\\n[*] Fetching unchecked items from Keep...")
    try:
        keep_items = keep_client.get_list_items(config.keep_note_id)
        print(f"    -> Found {len(keep_items)} items.")
    except Exception as e:
        print(f"Error fetching from Keep: {e}")
        sys.exit(1)

    if not keep_items:
        print("\\nAll items are completed in Keep. Nothing to do!")
        sys.exit(0)

    print("\\n[*] Fetching Todoist project data...")
    try:
        todoist_sections_raw = todoist_client.get_project_sections(config.todoist_project_id)
        todoist_tasks_raw = todoist_client.get_project_tasks(config.todoist_project_id)
        
        # Valid section names mapping
        section_name_map = {sec.get("name"): sec.get("id") for sec in todoist_sections_raw if "name" in sec}
        valid_sections = list(section_name_map.keys())
        
        print(f"    -> Found {len(valid_sections)} sections and {len(todoist_tasks_raw)} existing tasks.")
    except Exception as e:
        print(f"Error fetching from Todoist: {e}")
        sys.exit(1)

    # 2. Filter Duplicates
    print("\\n[*] Analyzing duplicates with Gemini...")
    try:
        filter_result = gemini_client.filter_duplicates(keep_items, todoist_tasks_raw)
        to_insert = filter_result.get("to_insert", [])
        duplicates = filter_result.get("duplicates", [])
        
        print(f"    -> Identified {len(duplicates)} duplicates.")
        print(f"    -> {len(to_insert)} new items to insert.")
    except Exception as e:
        print(f"Error communicating with Gemini (Duplicate Check): {e}")
        sys.exit(1)

    # 3. Categorization & Aggregation
    categorized_items = {}
    print("\\n[*] Categorizing new items with Gemini in bulk...")
    if to_insert:
        try:
            category_mapping = gemini_client.categorize_items(to_insert, valid_sections)
            for item, category in category_mapping.items():
                if category not in categorized_items:
                    categorized_items[category] = []
                categorized_items[category].append(item)
        except Exception as e:
            print(f"Error communicating with Gemini (Categorization): {e}")
            sys.exit(1)
            
    print("\\n===========================================")
    print("      SUMMARY OF PLANNED OPERATIONS      ")
    print("===========================================\\n")
    
    # Print results out
    print(f"Duplicates Skipped ({len(duplicates)} total):")
    for dup in duplicates:
        print(f" - {dup}")
        
    print(f"\\nCategorized Additions ({len(to_insert)} total):")
    for cat, items in categorized_items.items():
        print(f"\\n  [{cat}]")
        for i in items:
            print(f"   + {i}")

    if config.mode == "real":
        print("\\n===========================================")
        print(" [!] LIVE MODE ACTIVE: APPLYING CHANGES... ")
        print("===========================================\\n")
        
        # Insert to Todoist
        for cat, items in categorized_items.items():
            # Lookup section id
            section_id = section_name_map.get(cat)
            
            for item in items:
                try:
                    todoist_client.add_task(config.todoist_project_id, section_id, item)
                    print(f"    ✓ Added '{item}' to '{cat}'")
                except Exception as e:
                    print(f"    ✗ Failed to add '{item}': {e}")
                    
        # Mark as completed in Keep
        print("\\n[*] Checking off items in Google Keep...")
        try:
            # We check off BOTH duplicates (since they exist) AND items we just inserted
            items_to_check = to_insert + duplicates
            keep_client.mark_items_checked(config.keep_note_id, items_to_check)
            print(f"    ✓ Marked {len(items_to_check)} items as complete.")
        except Exception as e:
             print(f"    ✗ Failed to update Google Keep note: {e}")
             
        print("\\n[*] ALL SYNC OPERATIONS COMPLETE.")

    else:
        print("\\n[*] SIMULATION COMPLETE: No changes were written to Keep or Todoist.")

if __name__ == "__main__":
    main()
