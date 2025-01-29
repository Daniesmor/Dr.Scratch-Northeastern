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
import uuid
from .models import BatchCSV
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


def remove_circular_references(obj, seen=None):
    if seen is None:
        seen = set()

    if id(obj) in seen:
        return None  # O puedes retornar un valor predeterminado, como un diccionario vacío
    seen.add(id(obj))

    if isinstance(obj, dict):
        return {key: remove_circular_references(value, seen) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [remove_circular_references(item, seen) for item in obj]
    else:
        return obj
    
def gen_filepath(projects_file):
    for root, dirs, files in os.walk(projects_file):
        for i, file in enumerate(files):
            file_path = os.path.join(root, file)
            if os.path.exists(file_path):
                yield file_path


def track_memory_usage():
    """
    Función que imprime el uso de memoria en tiempo real del proceso en ejecución.
    """
    process = psutil.Process(os.getpid())  # Obtener el proceso actual
    memory_info = process.memory_info()    # Obtener información de memoria
    memory_used = memory_info.rss / (1024 ** 2)  # Convertir bytes a MB
    print(f"Memory usage: {memory_used:.4f} MB")


def process_url(request_data_obj: object, skill_points: dict) -> str:
    """
    Función que procesa la URL y maneja el archivo.
    """
    track_memory_usage()  # Verificar la memoria antes de comenzar
    projects_file = request_data_obj.POST['urlsFile']
    dashboard_mode = request_data_obj.POST['dashboard_mode']
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    csvs_dir = os.path.abspath(os.path.join(curr_dir, "..", "csvs"))
    temp_json_file = os.path.join(csvs_dir, f"{str(uuid.uuid4())[:8]}_temp_metrics.json")

    if type(projects_file) != list:
        if os.path.isdir(projects_file):
            dir_name = os.listdir(projects_file)[0]
            projects_file = os.path.join(projects_file, dir_name)

            for file_path in gen_filepath(projects_file):
                if os.path.exists(file_path):
                    try:
                        print("BEFORE READING FILE:")
                        track_memory_usage()
                        print("Reading file...")
                        with open(file_path, 'rb') as f:
                            file_name = os.path.basename(file_path)
                            file_data = BytesIO(f.read())
                        
                        track_memory_usage()  # Verificar el uso de memoria después de cargar el archivo

                        with file_data:
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

                            print(f"\033[32m ----------> Analyzing: {file_name}\033[0m")
                            print("TRACKEO ANTES DE ANALYSIS")
                            track_memory_usage()  
                            analysis_by_upload(request_data_obj, skill_points, inmemory_file)
                            print("TRACKEO DESPUES DE ANALYSIS")
                            track_memory_usage()  

                        
                        # Liberar recursos y verificar la memoria
                        del file_data, inmemory_file
                        gc.collect()
                        try:
                            print(file_data)
                        except NameError:
                            print("file_data ha sido borrada correctamente")

                        try:
                            print(inmemory_file)
                        except NameError:
                            print("inmemory_file ha sido borrada correctamente")
                        track_memory_usage()  # Verificar la memoria después de liberar recursos

                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

            # Limpiar archivos temporales
            if os.path.exists(projects_file):
                shutil.rmtree(projects_file)

    track_memory_usage()  # Verificar la memoria al final del proceso

def mk_url(csv_id: uuid) -> str:
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

def mk_html(csv_id: uuid, url: str) -> str:
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

def send_mail(email: str, csv_id: uuid) -> None:
    url = mk_url(csv_id)
    ehtml = mk_html(csv_id, url)
    subject = '[Dr.Scratch Batch Analysis Finish]'

    email = EmailMessage(subject, ehtml, settings.EMAIL_HOST_USER, [email])
    email.content_subtype = 'html'
    try:
        email.send(fail_silently=False)
    except:
        print(f"Error seding mail: {email}")

def register_timestamp(csv_id: uuid, start_time, end_endtime: datetime) -> None:
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
    temp_dict_metrics = process_url(request_data_obj, skill_points)
    csv_id = create_csv(request_data_obj, temp_dict_metrics) 
    """
    send_mail(re_email, csv_id)

    # Stop and register time for ETA
    end_time = datetime.now()
    register_timestamp(csv_id, start_time, end_time)
    """

        
