from drScratch.celery import app
from .analyzer import _make_analysis_by_txt


@app.task
def init_batch(request_data, skill_points):
    print("----------------------- BATCH MODE CELERY ----------------------------------------------")
    urls_file = request_data['urlsFile']

    dict_metrics = {}
    url = None
    filename = None
    project_counter = 0
    dashboard_mode = request_data['dashboard_mode']
    
    for i, url in enumerate(urls_file):
        if i >= 10:
            break
            
        url = url.decode('utf-8').strip()
        filename = url
        dict_metrics[project_counter] = _make_analysis_by_txt(request_data, url, skill_points)
        dict_metrics[project_counter].update({
            'url': url,
            'filename': filename,
            'dashboard_mode': dashboard_mode,
        })
        project_counter += 1
    return dict_metrics