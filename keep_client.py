import gkeepapi

class KeepClient:
    def __init__(self, email: str, master_token: str):
        """
        Initializes the KeepClient. Authenticates to Google Keep and performs an 
        initial sync to fetch the user's notes.
        """
        self.keep = gkeepapi.Keep()
        try:
            self.keep.authenticate(email, master_token)
        except Exception as e:
            raise Exception(f"Failed to authenticate to Google Keep: {e}")
        
        # Synchronize to fetch the notes
        self.keep.sync()

    def get_list_items(self, note_id: str) -> list[str]:
        """
        Fetches the specified list note and returns a list of its unchecked items.
        """
        note = self.keep.get(note_id)
        if not note:
            # Maybe the note was not found or is trashed
            raise ValueError(f"Note with ID '{note_id}' not found.")
        
        # Ensure it's a 'List' type note which has 'items'
        if not hasattr(note, 'items'):
            raise ValueError(f"Note with ID '{note_id}' is not a Checklist/List note.")

        # Extract only items that are not checked as completed
        unchecked_items = [item.text for item in note.items if not item.checked]
        return unchecked_items

    def mark_items_checked(self, note_id: str, item_names: list[str]):
        """
        Takes a list of string item names, finds them in the specified Keep note,
        and marks them as checked/completed, synchronizing back to Google.
        """
        if not item_names:
            return
            
        note = self.keep.get(note_id)
        if not note or not hasattr(note, 'items'):
            raise ValueError(f"Note with ID '{note_id}' is not valid for item modification.")
            
        # Lowercase search set for loose matching
        targets = set([i.lower() for i in item_names])
        modified = False
        
        for item in note.items:
            if not item.checked and item.text.lower() in targets:
                item.checked = True
                modified = True
                
        if modified:
            self.keep.sync()
