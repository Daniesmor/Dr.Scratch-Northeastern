import requests
import app.consts_drscratch as consts


class Project:

    def __init__(self, json_data):
        self.id = json_data.get("id")
        self.title = json_data.get("title")

        self.description = json_data.get("description")
        self.instructions = json_data.get("instructions")

        self.visible = json_data.get("visibility") == "visible"
        self.public = json_data.get("public", False)
        self.comments_allowed = json_data.get("comments_allowed", False)
        self.is_published = json_data.get("is_published", False)
        self.project_token = json_data.get("project_token")


class RemixtreeProject:

    def __init__(self, data):
        self.id = data.get("id")
        self.author = data.get("username")
        self.moderation_status = data.get("moderation_status")
        self.title = data.get("title")

        self.created_timestamp = data.get("datetime_created", {}).get("$date")
        self.last_modified_timestamp = data.get("mtime", {}).get("$date")
        self.shared_timestamp = (
            data.get("datetime_shared", {}).get("$date") if data.get("datetime_shared") else None
        )



class ScratchSession:

    def __init__(self, username=None):
        self.logged_in = False
        self.username = username
        self.csrf_token = None
        
        self.proxies = {
      
            'http': 'socks5h://tor_proxy:9050',
            'https': 'socks5h://tor_proxy:9050'

        }
        
    def get_project(self, project):
        project_id = (project.id if isinstance(project, (RemixtreeProject, Project)) else project)
        print(requests.get(f'{consts.URL_SCRATCH_API}/{project_id}/', proxies=self.proxies).json())
        return Project( 
            requests.get(f'{consts.URL_SCRATCH_API}/{project_id}/', proxies=self.proxies).json()
        )