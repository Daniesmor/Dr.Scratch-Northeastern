import requests
import app.consts_drscratch as consts


class Project:

    def __init__(self, json_data):
        self.id = json_data["id"]
        self.title = json_data["title"]

        self.description = json_data["description"] if "description" in json_data else None
        self.instructions = json_data["instructions"] if "instructions" in json_data else None

        self.visible = json_data["visibility"] == "visible"
        self.public = json_data["public"]
        self.comments_allowed = json_data["comments_allowed"]
        self.is_published = json_data["is_published"]
        self.project_token = json_data["project_token"]


class RemixtreeProject:

    def __init__(self, data):
        self.id = data["id"]
        self.author = data["username"]
        self.moderation_status = data["moderation_status"]
        self.title = data["title"]

        self.created_timestamp = data["datetime_created"]["$date"]
        self.last_modified_timestamp = data["mtime"]["$date"]
        self.shared_timestamp = (
            data["datetime_shared"]["$date"] if data["datetime_shared"] else None
        )


class ScratchSession:

    def __init__(self, username=None):
        self.logged_in = False
        self.username = username
        self.csrf_token = None
        
   

    def get_project(self, project):
        project_id = (project.id if isinstance(project, (RemixtreeProject, Project)) else project)
        project_url = '{}/{}/'.format(consts.URL_SCRATCH_API, project_id)
        print("TRAZA CONST API------------------------")
        print(consts.URL_SCRATCH_API)
        print("TRAZA DE URL:----------------------------")
        print(project_url)
        print('http://0.0.0.0:9050/scratch_requests/handle-request/{}'.format(project_id))
        return Project(
            requests.get('http://0.0.0.0:9050/scratch_requests/handle-request/{}'.format(project_id))
        )