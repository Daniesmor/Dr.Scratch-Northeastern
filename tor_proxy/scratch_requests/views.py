from django.shortcuts import render
from django.http import JsonResponse
import requests


proxie_list = {
      
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'

}

# Create your views here.
def handle_request(request, project_id: str):
    if request.method == 'GET':       
        url_scratch_api = 'https://api.scratch.mit.edu/projects'
        project_url = '{}/{}/'.format(url_scratch_api, project_id)
        print("MI project url: "+ project_url)
        response = requests.get(project_url, proxies=proxie_list)
        json_data = response.json()
        return JsonResponse(json_data)
    