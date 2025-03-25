from drScratch.celery import app
from .analyzer import analysis_by_url, analysis_by_upload
import os
import types
import requests
import shutil
import tempfile
from zipfile import ZipFile
from .batch import create_csv
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage as DjangoEmailMessage
from django.shortcuts import get_object_or_404
from django.conf import settings
import uuid
from .models import File, BatchCSV
from datetime import datetime
from django.template.loader import render_to_string
from css_inline import inline
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from types import SimpleNamespace
from io import BytesIO
import json
import gc
import psutil
import time
from typing import Generator
from memory_profiler import profile


def remove_circular_references(obj, seen=None):
    if seen is None:
        seen = set()

    if id(obj) in seen:
        return None
    seen.add(id(obj))

    if isinstance(obj, dict):
        return {key: remove_circular_references(value, seen) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [remove_circular_references(item, seen) for item in obj]
    else:
        return obj
    
def gen_filepath(projects_file: str) -> Generator[str, None, None]:
    for root, dirs, files in os.walk(projects_file):
        for i, file in enumerate(files):
            file_path = os.path.join(root, file)
            if os.path.exists(file_path):
                yield file_path

def show_top_objects():
    objs = gc.get_objects()
    print(f"Total de objetos en memoria: {len(objs)}")
    
    obj_types = {}
    for obj in objs:
        obj_type = type(obj).__name__
        obj_types[obj_type] = obj_types.get(obj_type, 0) + 1

    sorted_objs = sorted(obj_types.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Top 10 tipos de objetos en memoria:")
    for obj_type, count in sorted_objs:
        print(f"{obj_type}: {count}")


def track_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_used = memory_info.rss / (1024 ** 2)
    print(f"Memory usage: {memory_used:.4f} MB")


def process_url(request_data_obj: object, skill_points: dict) -> str:
    projects_file = request_data_obj.POST['urlsFile']

    if type(projects_file) != list:
        process_multiple_or_file(request_data_obj, skill_points, projects_file)
    else:
        # projects_file is a list of urls
        process_url_list(request_data_obj, skill_points, projects_file)


def process_multiple_or_file(request_data_obj: object, skill_points: dict, projects_file: list):
    if os.path.isdir(projects_file):
        dir_name = os.listdir(projects_file)[0]
        projects_file = os.path.join(projects_file, dir_name)

        for file_path in gen_filepath(projects_file):
            if os.path.exists(file_path):
                process_single_file(request_data_obj, file_path, skill_points)
                gc.collect()
        clean_temporary_files(projects_file)


def clean_temporary_files(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

def process_single_file(request_data_obj: object, file_path: str, skill_points: dict):
    try:
        with open(file_path, 'rb') as f:
            file_name = os.path.basename(file_path)
            inmemory_file = InMemoryUploadedFile(
                file=BytesIO(f.read()),
                field_name=None,
                name=file_name,
                content_type='application/octet-stream',
                size=BytesIO(f.read()).getbuffer().nbytes,
                charset=None,
            )

            request_data_obj.user = SimpleNamespace(is_authenticated=True, username=None)
            request_data_obj.session = {}

            print(f"\033[32m ----------> Analyzing: {file_name}\033[0m")
            analysis_by_upload(request_data_obj, skill_points, inmemory_file)
            track_memory_usage()  
            #show_top_objects()
            inmemory_file = None
            #gc.collect()
        inmemory_file = None

        
        #gc.collect()
        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        inmemory_file = None

def process_url_list(request_data_obj: object, skill_points: dict, projects_file: list):
    # Proccess each URL of the list
    for url in projects_file:
        #if i >= 10:
        #   break 
        url = url.decode('utf-8').strip()
        analysis_by_url(request_data_obj, url, skill_points)
        #gc.collect()


def mk_url(batch_id: uuid) -> str:
    url = ''
    if (settings.PRODUCTION == True):
        url = '{}/{}'.format('https://www.drscratch.org/batch',batch_id)
    else:
        url = '{}/{}'.format('http://127.0.0.1:8000/batch',batch_id)
    print("The link of the batch analysis is:", url) 
    return url


def get_csv_sum(csv) -> dict:
    summary = {}
    summary = {
        'num_projects': csv.num_projects,
        'Points': [csv.points, csv.max_points],
        'Logic': [csv.logic, csv.max_logic],
        'Parallelism': [csv.parallelism, csv.max_parallelism],
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


def mk_html(batch_id: uuid, url: str) -> str:
    try:
        batch_obj = get_object_or_404(BatchCSV, id=batch_id)
        summary = get_csv_sum(batch_obj)
        
        context = {
            'url': url,
            'summary': summary,
            'csv_filepath': batch_obj.filepath
        }

        html_message = render_to_string('main' + '/dashboard-bulk-emailv.html', context)
        inline_html = inline(html_message)
        return inline_html
    except ObjectDoesNotExist:
        return ''


def send_mail(email: str, batch_id: uuid) -> None:
    url = mk_url(batch_id)
    ehtml = mk_html(batch_id, url)
    subject = '[Dr.Scratch Batch Analysis Finish]'

    email = EmailMessage(subject, ehtml, settings.EMAIL_HOST_USER, [email])
    email.content_subtype = 'html'
    try:
        email.send(fail_silently=False)
    except:
        print(f"Error seding mail: {email}")


def register_timestamp(batch_id: uuid, start_time, end_endtime: datetime) -> None:
    timestamp = (end_endtime - start_time).total_seconds() + 60

    obj = get_object_or_404(BatchCSV, id=batch_id)
    obj.task_time = timestamp
    obj.save()


@app.task(bind=True)
def init_batch(self, request_data, skill_points):
    # Start task counter for ETA
    start_time = datetime.now()
    request_data_obj = SimpleNamespace(**request_data)
    re_email = request_data_obj.POST ['email']
    temp_dict_metrics = process_url(request_data_obj, skill_points)
    csv_id = create_csv(request_data_obj, temp_dict_metrics) 
    send_mail(re_email, csv_id)

    # Stop and register time for ETA
    end_time = datetime.now()
    register_timestamp(csv_id, start_time, end_time)