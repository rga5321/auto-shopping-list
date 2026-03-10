import requests

class TodoistClient:
    def __init__(self, api_key: str):
        """
        Initializes the Todoist Client using active REST v1.
        """
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.base_url = "https://api.todoist.com/api/v1"

    def get_project_sections(self, project_id: str) -> list[dict]:
        """
        Fetches all sections for a given project.
        """
        url = f"{self.base_url}/sections?project_id={project_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch sections for project {project_id}: {response.text}")
        json_data = response.json()
        if isinstance(json_data, dict) and 'results' in json_data:
            return json_data['results']
        return json_data

    def get_project_tasks(self, project_id: str) -> list[dict]:
        """
        Fetches all tasks for a given project.
        """
        url = f"{self.base_url}/tasks?project_id={project_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch tasks for project {project_id}: {response.text}")
        json_data = response.json()
        if isinstance(json_data, dict) and 'results' in json_data:
            return json_data['results']
        return json_data
