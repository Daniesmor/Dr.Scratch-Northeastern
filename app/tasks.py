from drScratch.celery import app
from .analyzer import analysis_by_url, analysis_by_upload
import os
import types
import requests
import shutil
import tempfile
from zipfile import ZipFile
from .batch import create_csv, create_summary
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage as DjangoEmailMessage
from django.shortcuts import get_object_or_404
from django.conf import settings
from uuid import UUID
from .models import BatchCSV
from datetime import datetime
from django.template.loader import render_to_string
from css_inline import inline
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from types import SimpleNamespace
from io import BytesIO


def proccess_url(request_data_obj: object, skill_points: dict) -> dict:
    # Obtain request data
    projects_file = request_data_obj.POST['urlsFile']
    dashboard_mode = request_data_obj.POST['dashboard_mode']

    if (type(projects_file) != list):
        # projects_file is path of the batch
        
        dict_metrics = {}
        for root, dirs, files in os.walk(projects_file):
            for i, file in enumerate(files):
                file_path = os.path.join(root, file)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'rb') as f:
                            file_name = os.path.basename(file_path)
                            file_data = BytesIO(f.read())

                            # Intance InMemoryUploadedFile (necessary for analysis_by_upload)
                            inmemory_file = InMemoryUploadedFile(
                                file=file_data,
                                field_name=None,
                                name=file_name,
                                content_type='application/octet-stream',
                                size=file_data.getbuffer().nbytes,
                                charset=None,
                            )
                            request_data_obj.user = SimpleNamespace(is_authenticated=True, username=None)
                            request_data_obj.session = {}

                            dict_metrics[i] = analysis_by_upload(request_data_obj, skill_points, inmemory_file)
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
                else:
                    print(f"File not found: {file_path}")
        if os.path.exists(projects_file):
            shutil.rmtree(projects_file)
    else:
        # projects_file is a list of urls
        # Initialize dicts for metrics
        dict_metrics = {} 

        # Proccess each URL of the list
        for i, url in enumerate(projects_file):
            #if i >= 10:
            #   break 
            url = url.decode('utf-8').strip()
            dict_metrics[i] = analysis_by_url(request_data_obj, url, skill_points)
            dict_metrics[i].update({
                'url': url,
                'filename': url,
                'dashboard_mode': dashboard_mode,
            })
    return dict_metrics

def mk_url(csv_id: UUID) -> str:
    url = ''
    if (settings.PRODUCTION == True):
        url = '{}/{}'.format('https://www.drscratch.org/batch',csv_id)
    else:
        url = '{}/{}'.format('http://127.0.0.1:8000/batch',csv_id)
    print("The link of the batch analysis is:", url) 
    return url

def get_csv_sum(csv) -> dict:
    summary = {}
    summary = {
        'num_projects': csv.num_projects,
        'Points': [csv.points, csv.max_points],
        'Logic': [csv.logic, csv.max_logic],
        'Parallelism': [csv.parallelization, csv.max_parallelization],
        'Data representation': [csv.data, csv.max_data],
        'Synchronization': [csv.synchronization, csv.max_synchronization],
        'User interactivity': [csv.userInteractivity, csv.max_userInteractivity],
        'Flow control': [csv.flowControl, csv.max_flowControl],
        'Abstraction': [csv.abstraction, csv.max_abstraction],
        'Math operators': [csv.math_operators, csv.max_math_operators],
        'Motion operators': [csv.motion_operators, csv.max_motion_operators],
        'Mastery': csv.mastery
    }
    return summary

def mk_html(csv_id: UUID, url: str) -> str:
    try:
        csv = get_object_or_404(BatchCSV, id=csv_id)
        csv_filepath = csv.filepath
        summary = get_csv_sum(csv)
        
        context = {
            'url': url,
            'summary': summary,
            'csv_filepath': csv_filepath
        }

        html_message = render_to_string('main' + '/dashboard-bulk-emailv.html', context)
        inline_html = inline(html_message)
        return inline_html
    except ObjectDoesNotExist:
        return ''

def send_mail(email: str, csv_id: UUID) -> None:
    url = mk_url(csv_id)
    ehtml = mk_html(csv_id, url)
    subject = '[Dr.Scratch Batch Analysis Finish]'

    email = EmailMessage(subject, ehtml, settings.EMAIL_HOST_USER, [email])
    email.content_subtype = 'html'
    try:
        email.send(fail_silently=False)
    except:
        print(f"Error seding mail: {email}")

def register_timestamp(csv_id: UUID, start_time, end_endtime: datetime) -> None:
    timestamp = (end_endtime - start_time).total_seconds() + 60

    obj = get_object_or_404(BatchCSV, id=csv_id)
    obj.task_time = timestamp
    obj.save()

@app.task(bind=True)
def init_batch(self, request_data, skill_points):
    # Start task counter for ETA
    start_time = datetime.now()
    request_data_obj = SimpleNamespace(**request_data)
    re_email = request_data_obj.POST ['email']

    dict_metrics = proccess_url(request_data_obj, skill_points)
    csv_id = create_csv(request_data_obj, dict_metrics) 
    send_mail(re_email, csv_id)

    # Stop and register time for ETA
    end_time = datetime.now()
    register_timestamp(csv_id, start_time, end_time)
    

        
