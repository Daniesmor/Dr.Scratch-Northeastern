from drScratch.celery import app
from .analyzer import _make_analysis_by_txt
import types
from .batch import create_csv, create_summary

@app.task(bind=True)
def init_batch(self, request_data, skill_points):
    print("----------------------- BATCH MODE CELERY ----------------------------------------------")
    urls_file = request_data['POST']['urlsFile']

    dict_metrics = {}
    url = None
    filename = None
    project_counter = 0
    dashboard_mode = request_data['POST']['dashboard_mode']
    request_data_obj = types.SimpleNamespace(**request_data)

    
    for i, url in enumerate(urls_file):
        if i >= 10:
            break
            
        url = url.decode('utf-8').strip()
        filename = url
        dict_metrics[project_counter] = _make_analysis_by_txt(request_data_obj, url, skill_points)
        dict_metrics[project_counter].update({
            'url': url,
            'filename': filename,
            'dashboard_mode': dashboard_mode,
        })
        project_counter += 1

        # CREATE CSV
        csv_filepath = create_csv(request_data_obj, dict_metrics)
        summary = create_summary(request_data_obj, dict_metrics)   
        print("summary", summary) 