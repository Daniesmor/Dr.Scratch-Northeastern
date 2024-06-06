from drScratch.celery import app
from .analyzer import _make_analysis_by_txt
import types
from .batch import create_csv, create_summary
from email.message import EmailMessage
from django.core.mail import EmailMessage as DjangoEmailMessage
from django.conf import settings

@app.task(bind=True)
def init_batch(self, request_data, skill_points):
    print("----------------------- BATCH MODE CELERY ----------------------------------------------")
    urls_file = request_data['POST']['urlsFile']

    dict_metrics = {}
    url = None
    filename = None
    project_counter = 0
    dashboard_mode = request_data['POST']['dashboard_mode']
    email = request_data['POST']['email']
    print("mi email", email)
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
    csv_id = create_csv(request_data_obj, dict_metrics)
    url = '{}/{}'.format('https://www.drscratch.org/batch',csv_id)
    local_url = '{}/{}'.format('http://0.0.0.0:8000/batch',csv_id)
    print("mi url", local_url) 


    # SEND MAIL

    message = f'''
    Thanks for using Dr.Scratch for analyze your projects!, you can download your csv by clicking here: {local_url}
    '''

    # Asunto del correo electrónico
    subject = '[Dr.Scratch Batch Analysis Finish]'

    # Crear el objeto EmailMessage
    email = DjangoEmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])

    # Envíar el correo electrónico
    email.send()

        