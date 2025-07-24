from drScratch.celery import app
from .analyzer import analysis_by_url, analysis_by_upload
import os
import types
import requests
import shutil
import tempfile
from zipfile import ZipFile
from .batch import create_csv_by_id
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
from celery import chord, group
from io import BytesIO
import json
import gc
import psutil
import time
from typing import Generator


    
def gen_filepath(projects_file: str) -> Generator[str, None, None]:
    for root, dirs, files in os.walk(projects_file):
        for i, file in enumerate(files):
            file_path = os.path.join(root, file)
            if os.path.exists(file_path):
                yield file_path


def clean_temporary_files(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def mk_url(batch_id: uuid) -> str:
    url = ''
    if (settings.DEBUG == False):
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


@app.task
def analyze_single_project_task(project_input_identifier, batch_id_str, 
                                skill_points_dict, is_url, 
                                post_data_dict):
    
    class MinimalRequestData:
        def __init__(self):
            self.POST = post_data_dict
            self.LANGUAGE_CODE = post_data_dict.get('LANGUAGE_CODE', 'en')
            self.user = SimpleNamespace(is_authenticated=False, username=None)
            self.session = {}
    
    request_for_analysis = MinimalRequestData()
    request_for_analysis.POST['batch_id'] = batch_id_str

    try:
        if is_url:
            print(f"\033[34m [Worker] Analyzing URL: {project_input_identifier} for batch {batch_id_str}\033[0m")
            analysis_by_url(request_for_analysis, project_input_identifier, skill_points_dict)
        else:
            file_path = project_input_identifier
            with open(file_path, 'rb') as f:
                file_name = os.path.basename(file_path)
                inmemory_file = InMemoryUploadedFile(
                    file=BytesIO(f.read()),
                    field_name=None, name=file_name, content_type='application/octet-stream',
                    size=os.path.getsize(file_path), charset=None,
                )
                print(f"\033[34m [Worker] Analyzing File: {file_name} for batch {batch_id_str}\033[0m")
                analysis_by_upload(request_for_analysis, skill_points_dict, inmemory_file)
                inmemory_file = None
            gc.collect()
    except Exception as e:
        print(f"\033[31mError analyzing project {project_input_identifier} for batch {batch_id_str}: {e}\033[0m")


@app.task
def finalize_batch_task(results, batch_id_str, email, start_time_iso, extracted_path_to_clean=None, original_post_data=None):
    print(f"\033[32mFinalizing batch: {batch_id_str}\033[0m")
    batch_uuid = create_csv_by_id(batch_id_str) 

    if batch_uuid:
        send_mail(email, batch_uuid)

        end_time = datetime.now()
        start_time = datetime.fromisoformat(start_time_iso)
        register_timestamp(batch_uuid, start_time, end_time)
    else:
        print(f"\033[31mError: No se pudo crear/finalizar el BatchCSV para {batch_id_str}\033[0m")

    if extracted_path_to_clean and os.path.exists(extracted_path_to_clean):
        print(f"Cleaning up temporary path: {extracted_path_to_clean}")
        clean_temporary_files(extracted_path_to_clean)
    
    print(f"\033[32mBatch {batch_id_str} finalized successfully.\033[0m")


@app.task(bind=True)
def init_batch_dispatcher(self, request_data_dict, skill_points_dict):
    start_time = datetime.now()

    original_post_data = request_data_dict.get('POST', {})
    batch_id_str = original_post_data.get('batch_id')
    email = original_post_data.get('email')
    projects_input = original_post_data['urlsFile'] # List of URLs (bytes) o path (str)
    extracted_path_for_cleanup = original_post_data.get('extracted_path_for_cleanup')

    tasks_to_run: list = []

    if isinstance(projects_input, list):
        for url_bytes in projects_input:
            url = url_bytes.decode('utf-8').strip()
            tasks_to_run.append(analyze_single_project_task.s(url, batch_id_str, skill_points_dict, True, original_post_data))
    elif isinstance(projects_input, str) and os.path.isdir(projects_input):
        curr_projects_dir = projects_input
        dir_contents = os.listdir(projects_input)
        if len(dir_contents) == 1 and os.path.isdir(os.path.join(projects_input, dir_contents[0])):
                curr_projects_dir = os.path.join(projects_input, dir_contents[0])
        
        for file_path in gen_filepath(curr_projects_dir):
            if os.path.exists(file_path):
                tasks_to_run.append(analyze_single_project_task.s(
                    file_path, batch_id_str, skill_points_dict, False, original_post_data
                ))

    else:
        print(f"\033[31mError: projects_input no es una lista de URLs ni una ruta de directorio válida: {projects_input}\033[0m")
        finalize_batch_task.delay(
            results=None, 
            batch_id_str=batch_id_str, 
            email=email, 
            start_time_iso=start_time.isoformat(),
            extracted_path_to_clean=extracted_path_for_cleanup,
            original_post_data=original_post_data
        )
        return
    
    if not tasks_to_run:
        print(f"No projects to analyze for batch {batch_id_str}.")
        finalize_batch_task.delay(
            results=None, 
            batch_id_str=batch_id_str, 
            email=email, 
            start_time_iso=start_time.isoformat(),
            extracted_path_to_clean=extracted_path_for_cleanup,
            original_post_data=original_post_data
        )
        return
    
    callback = finalize_batch_task.s(
        batch_id_str=batch_id_str,
        email=email,
        start_time_iso=start_time.isoformat(),
        extracted_path_to_clean=extracted_path_for_cleanup,
        original_post_data=original_post_data
    )

    chord(header=group(tasks_to_run), body=callback).apply_async()

    print(f"Dispatched {len(tasks_to_run)} analysis tasks for batch {batch_id_str}.")