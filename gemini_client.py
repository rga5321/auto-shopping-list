import json
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self, api_key: str):
        """
        Initializes the Gemini Client.
        """
        self.client = genai.Client(api_key=api_key)
        # Using gemini-1.5-flash which is the fastest and cheapest production model with generous free quotas
        self.model_name = "gemini-3.1-flash-lite"

    def filter_duplicates(self, keep_items: list[str], todoist_tasks: list[dict]) -> dict:
        """
        Takes a list of new items from Keep and a list of existing tasks from Todoist.
        Uses Gemini to semantically understand if a Keep item already exists in Todoist
        (handling plurals, slight wording differences, etc).
        
        Returns a dictionary separating the original keep items into two lists:
        {
            "to_insert": ["new item 1", "new item 2"],
            "duplicates": ["existing item 1", "existing item 2"]
        }
        """
        if not keep_items:
            return {"to_insert": [], "duplicates": []}

        existing_item_names = [task.get("content", "") for task in todoist_tasks]
        
        prompt = f"""
        You are an intelligent shopping list assistant.
        I have a list of newly added grocery items, and a list of grocery items that are already in my shopping project.
        
        New items to check: {json.dumps(keep_items, ensure_ascii=False)}
        Already existing items: {json.dumps(existing_item_names, ensure_ascii=False)}
        
        For each new item, determine if it is semantically a duplicate of an already existing item.
        Consider plurals (e.g., "apple" vs "apples"), synonyms, and slight wording differences as duplicates.
        
        Return ONLY a JSON object with two keys:
        - "to_insert": an array of strings from the 'New items' list that are NOT duplicates.
        - "duplicates": an array of strings from the 'New items' list that ARE duplicates.
        
        Do not include any explanation or markdown formatting, just the raw JSON object.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        try:
            result = json.loads(response.text)
            return {
                "to_insert": result.get("to_insert", []),
                "duplicates": result.get("duplicates", [])
            }
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse Gemini response as JSON: {response.text}") from e

    def categorize_items(self, item_names: list[str], valid_sections: list[str]) -> dict[str, str]:
        """
        Takes a list of new grocery items and a list of valid section names from Todoist.
        Uses Gemini to determine which section each item belongs to in a single bulk request.
        If no obvious match exists, or if the list of sections is empty, it assigns "OTROS".
        
        Returns a dictionary mapping: {"item_name": "Section Name"}
        """
        if not valid_sections or not item_names:
            return {item: "OTROS" for item in item_names}

        prompt = f"""
        You are an intelligent shopping list assistant.
        I have a list of grocery items:
        {json.dumps(item_names, ensure_ascii=False)}
        
        I have the following valid section categories in my shopping list:
        {json.dumps(valid_sections, ensure_ascii=False)}
        
        Which category does each item best fit into?
        
        Return ONLY a JSON object where the keys are the exact item names provided, and the values are the exact string value of the matching category from the list above. 
        If an item does not fit nicely into any of them, assign it to "OTROS".
        
        Do not include any explanation or markdown formatting, just the raw JSON object.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        try:
            result = json.loads(response.text)
            final_map = {}
            for item in item_names:
                cat = result.get(item, "OTROS")
                if cat not in valid_sections and cat != "OTROS":
                    cat = "OTROS"
                final_map[item] = cat
                
            return final_map
            
        except json.JSONDecodeError:
            return {item: "OTROS" for item in item_names}
