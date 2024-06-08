#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import os
import ast
import json
import uuid
import requests
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate,get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils import timezone
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from app.forms import UrlForm, OrganizationForm, OrganizationHashForm, LoginOrganizationForm, CoderForm, DiscussForm
from app.models import File, CSVs, Organization, OrganizationHash, Coder, Discuss, Stats
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from zipfile import ZipFile, BadZipfile
import pickle
import shutil
import unicodedata
import csv
from datetime import datetime, timedelta, date
import traceback
import re
import app.consts_drscratch as consts
from app.scratchclient import ScratchSession
from app.pyploma import generate_certificate
from app.hairball3.mastery import Mastery
from app.hairball3.spriteNaming import SpriteNaming
from app.hairball3.backdropNaming import BackdropNaming
from app.hairball3.duplicateScripts import DuplicateScripts
from app.hairball3.deadCode import DeadCode
from app.hairball3.refactor import RefactorDuplicate
from app.hairball3.comparsionMode import ComparsionMode
from app.exception import DrScratchException
from app.hairball3.scratchGolfing import ScratchGolfing

import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)
supported_languages = ['es', 'ca', 'gl', 'pt']

def main(request):

    user = None

    if request.user.is_authenticated:
        user_name = request.user.username
        user_type = identify_user_type(request)
        is_admin = identify_admin(user_type)
        if (is_admin):
            return render(request, 'main/main.html', {'username': user_name})
        else:
            if user_type == 'coder':
                user = Coder.objects.get(username=user_name)
            elif user_type == 'organization':
                user = Organization.objects.get(username=user_name)
            return render(request, user_type + '/main.html', {'username': user_name, "img": str(user.img)})
    else:
        return render(request, 'main/main.html', {'username': None})


def contest(request):
    return render(request, 'contest.html', {})


def collaborators(request):
    return render(request, 'main/collaborators.html')


def create_csv_main(request ,d: dict, folder_path: str) -> str:
    csv_name = "main.csv"
    csv_filepath = os.path.join(folder_path, csv_name)
    #fieldnames = list(d[0].keys())
    
    mastery_fields = skills_translation(request) 
    mastery_fields = {skill_en: skill_trans for skill_trans, skill_en in mastery_fields.items()}
    mastery_fields['points'] = 'points'

    headers = [
        'url', 'filename', 'points', 
        'Abstraction', 'Parallelism', 'Logic', 'Synchronization',
        'Flow control', 'User interactivity', 'Data representation',
        'Math operators', 'Motion operators',
        'DuplicateScripts', 'DeadCode', 'SpriteNaming', 'BackdropNaming', 
        'Error', 'dashboard_mode', 
    ]

    # Abir el archivo csv en modo de escritura
    with open(csv_filepath, 'w') as csv_file:
        writer_csv = csv.DictWriter(csv_file, fieldnames=headers)
        writer_csv.writeheader()

        row_to_write = {}
        for project in d:
            for clave in headers:
                if clave in d[project]:
                    row_to_write[clave] = d[project].get(clave, '')
                elif clave in mastery_fields.keys():
                    clave_trans = mastery_fields[clave]
                    mastery_list = d[project]['mastery'].get(clave_trans, [])
                    if type(mastery_list[0]) == list:
                        row_to_write[clave] = mastery_list[0][0]
                    else:
                        row_to_write[clave] = mastery_list[0]
                elif clave == 'DuplicateScripts':
                    row_to_write[clave] = d[project]['duplicateScript'].get('number', '')
                elif clave == 'DeadCode':
                    row_to_write[clave] = d[project]['deadCode'].get('number', '')
                elif clave == 'SpriteNaming':
                    row_to_write[clave] = d[project]['spriteNaming'].get('number', '')
                elif clave == "BackdropNaming":
                    row_to_write[clave] = d[project]['backdropNaming'].get('number', '')
                else:
                    row_to_write[clave] = ''
            writer_csv.writerow(row_to_write)
    return csv_filepath

def create_csv_dups(d: dict, folder_path: str):
    csv_name = "duplicateScript.csv"
    csv_filepath = os.path.join(folder_path, csv_name)
    
    # headers list
    headers = ['url', 'filename', 'number']
    max_dup_scripts = 0
    # create headers
    for project in d.values():
        duplicate_scripts = project.get('duplicateScript', {}).get('csv_format', [])
        
        if duplicate_scripts:
            for block in duplicate_scripts:
                max_dup_scripts_temp = max(len(instruction_list) for instruction_list in block)
                if max_dup_scripts < max_dup_scripts_temp:
                    max_dup_scripts = max_dup_scripts_temp
    for i in range(1, max_dup_scripts + 1):
        headers.append(f'duplicateScript_{i}')
    # open csv file
    with open(csv_filepath, 'w') as csv_file:
        writer_csv = csv.DictWriter(csv_file, fieldnames=headers)
        writer_csv.writeheader()

        for project_data in d.values():
            row_to_write = {
                'url': project_data.get('url', ''),
                'filename': project_data.get('filename', ''),
                'number': project_data['duplicateScript'].get('number', ''),
            }
            duplicate_scripts = project_data.get('duplicateScript', {}).get('csv_format', [])
            if duplicate_scripts:
                script_number = 0
                for block in duplicate_scripts:
                    for instruction in block:
                        script_number += 1
                        row_to_write[f'duplicateScript_{script_number}'] = instruction
            else:
                row_to_write.update({f'duplicateScript_{i}': 'N/A' for i in range(1, max_dup_scripts + 1)})        
            writer_csv.writerow(row_to_write)



def create_csv_sprites(d: dict, folder_path: str):
    csv_name = "spriteNaming.csv"
    csv_filepath = os.path.join(folder_path, csv_name)
    headers = ['url', 'filename', 'number']

    # Get the maximum number of sprites
    total_sprites_names = max(len(proj['spriteNaming'].get('sprite', [])) for proj in d.values())

    # Add the names of the sprites as headers
    headers.extend(f'spriteNaming{i}' for i in range(1, total_sprites_names + 1))

    # Write in the CSV file
    with open(csv_filepath, 'w', newline='') as csv_file:
        writer_csv = csv.DictWriter(csv_file, fieldnames=headers)
        writer_csv.writeheader()

        for project in d.values():
            row_to_write = {key: project.get(key, 'N/A') for key in headers} 
            row_to_write['number'] = project['spriteNaming'].get('number', 'N/A')
            # Fill the sprites
            sprites = project['spriteNaming'].get('sprite', [])
            for i, sprite in enumerate(sprites, 1):
                row_to_write[f'spriteNaming{i}'] = sprite
            # Write the row
            writer_csv.writerow(row_to_write)
  
def create_csv_backdrops(d: dict, folder_path: str):
    csv_name = "backdropNaming.csv"
    csv_filepath = os.path.join(folder_path, csv_name)
    # headers list
    headers = ['url', 'filename','number']
    
    total_backdrop_names = max(len(proj['backdropNaming'].get('backdrop', [])) for proj in d.values())
    headers.extend(f'backdropNaming{i}' for i in range(1, total_backdrop_names+1))
    
    with open(csv_filepath, 'w') as csv_file:
        writer_csv = csv.DictWriter(csv_file, fieldnames=headers)
        writer_csv.writeheader()

        row_to_write = {}
        for project in d.values():
            row_to_write = {key: project.get(key, 'N/A') for key in headers}
            
            # Fill backdrops
            backdrops = project['backdropNaming'].get('backdrop', [])
            for i, backdrop in enumerate(backdrops, 1):
                row_to_write[f'backdropNaming{i}'] = backdrop if backdrop else 'N/A'
            writer_csv.writerow(row_to_write)

def create_csv_deadcode(d: dict, folder_path: str):
    csv_name = "deadCode.csv"
    csv_filepath = os.path.join(folder_path, csv_name)
    # headers list
    headers = ['url', 'filename', 'number', 'sprite']
    
    max_sprites = 0
    for project_data in d.values():   
        dead_code_data = project_data.get('deadCode', {})  
        for key, value in dead_code_data.items():
            if key not in ['number', 'deadCode']:
                sprite_list_counter = len(value)
                if sprite_list_counter > max_sprites:
                    max_sprites = sprite_list_counter
    
    headers.extend(f'deadCode{i}' for i in range(1, max_sprites+1))
            
    with open(csv_filepath, 'w', newline='') as csv_file:
        writer_csv = csv.DictWriter(csv_file, fieldnames=headers)
        writer_csv.writeheader()

        row_to_write = {}
        for project_data in d.values():      
            for sprite_list_name, sprite_list in project_data['deadCode'].items():
                if sprite_list_name not in ['number', 'deadCode']:
                    row_to_write = {
                        'url': project_data['url'],
                        'filename': project_data['filename'],
                        'number': project_data['deadCode']['number'],
                        'sprite': sprite_list_name
                    }
                    
                    for i, sprite in enumerate(sprite_list, 1):
                        row_to_write[f'deadCode{i}'] = sprite
                    for j in range(1, max_sprites+1):
                        if row_to_write.get(f'deadCode{j}', '') == '':
                            row_to_write[f'deadCode{j}'] = 'N/A'
                    writer_csv.writerow(row_to_write)    
        
    
def zip_folder(folder_path: str):
    with ZipFile(folder_path + '.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, os.path.basename(filePath))
                
    # Remove the original folder
    shutil.rmtree(folder_path)
    return folder_path + '.zip'
    
def create_csv(request, d):
    now = datetime.now()
    folder_name = str(uuid.uuid4()) + '_' + now.strftime("%Y%m%d%H%M%S")
    base_dir = os.getcwd()
    folder_path = os.path.join(base_dir, 'csvs', 'Dr.Scratch', folder_name)
    os.mkdir(folder_path)
    
   
    
    create_csv_main(request, d, folder_path)
    #create_csv_dups(d, folder_path)
    create_csv_sprites(d, folder_path)
    create_csv_backdrops(d, folder_path)
    create_csv_deadcode(d, folder_path)
    csv_filepath = zip_folder(folder_path)
    return csv_filepath
    
def rubric_creator(request):
    user = str(identify_user_type(request))
    return render(request, user + '/rubric-creator.html')

def upload_personalized(request, skill_points=None):
    user = str(identify_user_type(request))
    return render(request, user + '/rubric-uploader.html')

def compare_uploader(request):
    user = str(identify_user_type(request))
    return render(request, user + '/compare-uploader.html')

def base32_to_str(base32_str: str) -> str:
    value = int(base32_str, 32)
    return str(value).zfill(9)
    
def show_dashboard(request, skill_points=None):
    
    if request.method == 'POST':
        url = request.path.split('/')[-1]
        if url != '':
            numbers = base32_to_str(url)
        else:
            numbers = ''
        skill_rubric = generate_rubric(numbers)
        user = str(identify_user_type(request))
        if request.POST.get('dashboard_mode') == 'Comparison':
            print("Comparison mode:", request.POST)
            d = build_dictionary_with_automatic_analysis(request, skill_rubric)
            print("Context Dictionary:", d)
            return render(request, user + '/dashboard-compare-1.html', d)   
        print("Mode:", request.POST)
        d = build_dictionary_with_automatic_analysis(request, skill_rubric)
        print("Context Dictionary:")
        print(d)
        print("Skill rubric")
        print(skill_rubric)
        print(request.session.get('current_project_path'))
        if len(d) > 1:
            csv_filepath = create_csv(request, d)
            summary = create_summary(request, d)   
            print("summary", summary)   
            return render(request, user + '/dashboard-bulk.html', {'summary': summary, 'csv_filepath': csv_filepath})
        else: 
            d = d[0]
            if d['Error'] == 'analyzing':
                return render(request, 'error/analyzing.html')
            elif d['Error'] == 'MultiValueDict':
                return render(request, user + '/main.html', {'error': True})
            elif d['Error'] == 'id_error':
                return render(request, user + '/main.html', {'id_error': True})
            elif d['Error'] == 'no_exists':
                return render(request, user + '/main.html', {'no_exists': True})
            else:
                if d["dashboard_mode"] == 'Default':
                    return render(request, user + '/dashboard-default.html', d)
                elif d["dashboard_mode"] == 'Personalized':
                    return render(request, user + '/dashboard-personal.html', d)               
    else:
        return HttpResponseRedirect('/')    


def process_contact_form(request):
    if request.method == 'POST':
        required_fields = {
            'contact_name': 'Please, fill your name.',
            'contact_email': 'Please, fill your email.',
            'contact_text': 'Please, fill the text area.'
        }
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        for field, error_message in required_fields.items():
            if not request.POST.get(field, ''):
                messages.error(request, error_message)
                request.session['form_data'] = request.POST
                return HttpResponseRedirect('/contact')
        
        if recaptcha_response:
            secret_key = settings.RECAPTCHA_PRIVATE_KEY
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', {
                'secret': secret_key,
                'response': recaptcha_response
            })
            data = response.json()
            if data['success']:
                contact_name = request.POST.get('contact_name')
                contact_email = request.POST.get('contact_email')
                contact_text = request.POST.get('contact_text')
                contact_media = request.FILES.get('contact_media')

                message = f'''
                Name: {contact_name},
                Email: {contact_email},
                Text: {contact_text},
                Media: {contact_media}
                '''

                # Asunto del correo electrónico
                subject = '[CONTACT FORM]'

                email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, ['drscratch@gsyc.urjc.es'])
                if contact_media:
                    email.attach(contact_media.name, contact_media.read(), contact_media.content_type)

                email.send()
                # Renderizar la plantilla de respuesta
                return HttpResponseRedirect('/')    
        else:
            messages.error(request, 'Please, fill the captcha first.')
            return HttpResponseRedirect('/contact')
    else:
        return HttpResponse('METHOD NOT ALLOW', status=405)


    


def generate_rubric(skill_points: str) -> dict:
    mastery = ['Abstraction', 'Parallelization', 'Logic', 'Synchronization', 
               'FlowControl', 'UserInteractivity', 'DataRepresentation',
               'MathOperators', 'MotionOperators']
       
    skill_rubric = {}
    if skill_points != '':
        for skill_name, points in zip(mastery, skill_points):
            skill_rubric[skill_name] = int(points)   
    else:
        for skill_name in mastery:
            skill_rubric[skill_name] = 5           
    return skill_rubric  
    
     

def create_summary(request, d: dict) -> dict:
    summary = {}
    # NUM PROJECTS
    total_maxi_points = d[0]['mastery']['points'][1]
    num_projects = len(d)

    summary['num_projects'] = num_projects
    summary['Points'] = 0
    

    mastery_fields = skills_translation(request) 
    mastery_fields = {skill_en: skill_trans for skill_trans, skill_en in mastery_fields.items()}
    skills = list(mastery_fields.values())
    print("---------------------------- Traza de skills ----------------------------")
    print(skills)


    for project in d:
        summary['Points'] += round(d[project]["mastery"]["points"][0], 2)
        for skill in skills:
            if skill not in summary:
                summary[skill] = 0
            if type(d[project]["mastery"][skill][0]) == list:
                if d[project]["mastery"][skill][0][1] != 0:
                    summary[skill] += d[project]["mastery"][skill][0][0]
                else:
                    summary[skill] = 0
    
    for skill in skills:
        summary[skill] = round(summary[skill] / num_projects, 2)
    
    # AVERAGE MASTERY POINTS
    average_mastery_points = round(summary['Points'] / num_projects, 2)
    
    
    # SET A LIST WITH MAX AND MID POINTS
    mid_points = total_maxi_points / 2
    summary['Points'] = [average_mastery_points, total_maxi_points, mid_points]
    for skill in skills:
        mid_points = d[0]["mastery"][skill][0][1] / 2
        summary[skill] = [summary[skill], d[0]["mastery"][skill][0][1], mid_points]
        


    # MASTERY LEVEL
    master_limit = (total_maxi_points * 15)/21
    developing_limit = (total_maxi_points * 7)/21
    
    if summary['Points'][0] >= master_limit:
        summary['Mastery'] = 'Master'
    elif summary['Points'][0] > developing_limit:
        summary['Mastery'] = 'Developing'
    else:
        summary['Mastery'] = 'Basic'
    return summary


def build_dictionary_with_automatic_analysis(request, skill_points: dict) -> dict:
    """
    Build dictionary with automatic analysis by distinguishing between URL or project
    """
    dict_metrics = {}
    url = None
    filename = None
    project_counter = 0
    
    if request.method == 'POST':
        dashboard_mode = request.POST['dashboard_mode']
    else:
        dashboard_mode = "Personalized"

    if request.POST.get('dashboard_mode') == 'Comparison':
        dict_metrics = _make_comparison(request, skill_points)

    else:
        if "_upload" in request.POST:
            dict_metrics[project_counter] = _make_analysis_by_upload(request, skill_points)
            if dict_metrics[project_counter]['Error'] != 'None':
                return dict_metrics
            filename = request.FILES['zipFile'].name.encode('utf-8')
            dict_metrics[project_counter].update({
                'url': url, 
                'filename': filename,
                'dashboard_mode': dashboard_mode,
                'multiproject': False
            })
        elif '_url' in request.POST:
            dict_metrics[project_counter] = _make_analysis_by_url(request, skill_points)
            filename = url
            dict_metrics[project_counter].update({
                'url': url, 
                'filename': filename,
                'dashboard_mode': dashboard_mode,
                'multiproject': False
            })
        elif '_urls' in request.POST:
            
            urls_file = request.FILES['urlsFile']

            # Iterate over the first 10 URLs in the file
            for i, url in enumerate(urls_file):
                if i >= 10:
                    break
                    
                url = url.decode('utf-8')  # Decode bytes to string
                url = url.strip()  # Remove whitespace from the beginning and end of the string
                filename = url
                # Call _make_analysis_by_url function to process the URL and store the result
                dict_metrics[project_counter] = _make_analysis_by_txt(request, url, skill_points)

                # Update 'dict_metrics' with additional information
                dict_metrics[project_counter].update({
                    'url': url,
                    'filename': filename,
                    'dashboard_mode': dashboard_mode,
                })
                project_counter += 1
    return dict_metrics


def identify_user_type(request) -> str:
    """
    Return authenticated user type (organization, coder, main, None)
    """

    user = None

    if request.user.is_authenticated:
        username = request.user.username
        if Organization.objects.filter(username=username).exists():
            user = 'organization'
        elif Coder.objects.filter(username=username).exists():
            user = 'coder'
        elif request.user.is_staff:
            user = 'staff'
        elif request.user.is_superuser:
            user = 'superuser'
    else:
        user = 'main'

    return user

def identify_admin(user_type):
    is_admin = 0
    if (user_type == 'superuser' or user_type == 'staff'):
        is_admin = 1
    return is_admin


def save_analysis_in_file_db(request, zip_filename):
    now = datetime.now()
    method = "project"

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None

    if Organization.objects.filter(username=username):
        filename_obj = File(filename=zip_filename,
                        organization=username,
                        method=method, time=now,
                        score=0, abstraction=0, parallelization=0,
                        logic=0, synchronization=0, flowControl=0,
                        userInteractivity=0, dataRepresentation=0,
                        spriteNaming=0, initialization=0,
                        deadCode=0, duplicateScript=0)
    elif Coder.objects.filter(username=username):
        filename_obj = File(filename=zip_filename,
                        coder=username,
                        method=method, time=now,
                        score=0, abstraction=0, parallelization=0,
                        logic=0, synchronization=0, flowControl=0,
                        userInteractivity=0, dataRepresentation=0,
                        spriteNaming=0, initialization=0,
                        deadCode=0, duplicateScript=0)
    else:
        filename_obj = File(filename=zip_filename,
                        method=method, time=now,
                        score=0, abstraction=0, parallelization=0,
                        logic=0, synchronization=0, flowControl=0,
                        userInteractivity=0, dataRepresentation=0,
                        spriteNaming=0, initialization=0,
                        deadCode=0, duplicateScript=0)

    filename_obj.save()
    return filename_obj

def check_project(counter):
    if counter == 0:
        project = "Base"
    else:
        project = "Project"
    return project

def _make_comparison(request, skill_points: dict):
    """
    Make comparison of two projects
    """
    counter = 0
    d = {}
    path = {}
    json = {}
    if "_urls" in request.POST:
        for url in request.POST.getlist('urlProject'):
            project = check_project(counter)
            id_project = return_scratch_project_identifier(url)
            if id_project == "error":
                return {'Error': 'id_error'}
            else:
                d[project] = generator_dic(request, id_project, skill_points)
                d[project].update({
                    'url': url, 
                    'filename': url,
                    'dashboard_mode': "Comparison",
                    'multiproject': False
                })
                path[project] = request.session.get('current_project_path')
                counter += 1
    elif "_uploads" in request.POST:
        for upload in request.FILES.getlist('zipFile'):
            project = check_project(counter)
            print("Upload:", upload)
            d[project] = analysis_by_upload(request, skill_points, upload)
            d[project].update({
                'url': None,
                'filename': upload,
                'dashboard_mode': "Comparison",
                'multiproject': False
            })
            path[project] = request.session.get('current_project_path')
            counter += 1
    elif "_mix" in request.POST:
        project = check_project(counter)
        base_type = request.POST.get('baseProjectType')
        if base_type == "urlProject":
            url = request.POST.getlist('urlProject')[0]
            print("Url:", url)
            id_project = return_scratch_project_identifier(url)
            if id_project == "error":
                return {'Error': 'id_error'}
            else:
                d[project] = generator_dic(request, id_project, skill_points)
                d[project].update({
                    'url': url, 
                    'filename': url,
                    'dashboard_mode': "Comparison",
                    'multiproject': False
                })
            path[project] = request.session.get('current_project_path')
            counter += 1
            upload = request.FILES.get('zipFile')
            project = check_project(counter)
            d[project] = analysis_by_upload(request, skill_points, upload)
            d[project].update({
                'url': None,
                'filename': upload,
                'dashboard_mode': "Comparison",
                'multiproject': False
            })
            path[project] = request.session.get('current_project_path')
        else:
            upload = request.FILES.get('zipFile')
            project = check_project(counter)
            d[project] = analysis_by_upload(request, skill_points, upload)
            d[project].update({
                'url': None,
                'filename': upload,
                'dashboard_mode': "Comparison",
                'multiproject': False
            })
            path[project] = request.session.get('current_project_path')
            counter += 1
            url = request.POST.getlist('urlProject')[1]
            id_project = return_scratch_project_identifier(url)
            if id_project == "error":
                return {'Error': 'id_error'}
            else:
                d[project] = generator_dic(request, id_project, skill_points)
                d[project].update({
                    'url': url, 
                    'filename': url,
                    'dashboard_mode': "Comparison",
                    'multiproject': False
                })
                path[project] = request.session.get('current_project_path')
    else:
        return HttpResponseRedirect('/')
    
    print("Path:", path)
    for key,value in path.items():
        print(key, value)
        json[key] = load_json_project(value)    
    print("Json:", json.keys())
    dict_scratch_golfing = ScratchGolfing(json.get('Base'), json.get('Project')).finalize()
    dict_scratch_golfing = dict_scratch_golfing['result']['scratch_golfing']
    print("Estando en views")
    print(dict_scratch_golfing)
    d['Comparison'] = dict_scratch_golfing
    if "same_functionality" in request.POST:
        d['Comparison'].update({
            'same_functionality': True
        })
    else: 
        d['Comparison'].update({
            'same_functionality': False
        })
    
    return d
    
def analysis_by_upload(request, skill_points: dict, upload):
    """
    Upload file from form POST for unregistered users
    """

    zip_filename = upload.name.encode('utf-8')
    filename_obj = save_analysis_in_file_db(request, zip_filename)

    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    project_name = str(uuid.uuid4())
    unique_id = '{}_{}{}'.format(project_name, datetime.now().strftime("%Y_%m_%d_%H_%M_%S_"), datetime.now().microsecond)
    zip_filename = zip_filename.decode('utf-8')
    version = check_version(zip_filename)

    if version == "1.4":
        file_saved = dir_zips + unique_id + ".sb"
    elif version == "2.0":
        file_saved = dir_zips + unique_id + ".sb2"
    else:
        file_saved = dir_zips + unique_id + ".sb3"

    # Create log
    path_log = os.path.dirname(os.path.dirname(__file__)) + "/log/"
    log_file = open(path_log + "logFile.txt", "a")
    log_file.write("FileName: " + str(zip_filename) + "\t\t\t" + "ID: " + str(filename_obj.id) + "\t\t\t" + \
                "Method: " + str(filename_obj.method) + "\t\t\tTime: " + str(filename_obj.time) + "\n")

    # Save file in server
    file_name = os.path.join("uploads", file_saved)
    request.session['current_project_path'] = file_name
    with open(file_name, 'wb+') as destination:
        for chunk in upload.chunks():
            destination.write(chunk)

    try:
        ext_type_project=None
        dict_drscratch_analysis = analyze_project(request, file_name, filename_obj, ext_type_project, skill_points)
        print(dict_drscratch_analysis)
    except Exception:
        traceback.print_exc()
        filename_obj.method = 'project/error'
        filename_obj.save()
        old_path_project = file_saved
        new_path_project = file_saved.split("/uploads/")[0] + "/error_analyzing/" + file_saved.split("/uploads/")[1]
        shutil.copy(old_path_project, new_path_project)
        dict_drscratch_analysis = {'Error': 'analyzing'}
        return dict_drscratch_analysis

    # Redirect to dashboard for unregistered user
    dict_drscratch_analysis['Error'] = 'None'
    return dict_drscratch_analysis


def _make_analysis_by_upload(request, skill_points: dict):
    """
    Upload file from form POST for unregistered users
    """

    if request.method == 'POST':
        try:
            zip_file = request.FILES['zipFile']
        except MultiValueDictKeyError:
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            return {'Error': 'MultiValueDict'}

        zip_filename = zip_file.name.encode('utf-8')
        filename_obj = save_analysis_in_file_db(request, zip_filename)

        dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
        project_name = str(uuid.uuid4())
        unique_id = '{}_{}{}'.format(project_name, datetime.now().strftime("%Y_%m_%d_%H_%M_%S_"), datetime.now().microsecond)
        zip_filename = zip_filename.decode('utf-8')
        version = check_version(zip_filename)

        if version == "1.4":
            file_saved = dir_zips + unique_id + ".sb"
        elif version == "2.0":
            file_saved = dir_zips + unique_id + ".sb2"
        else:
            file_saved = dir_zips + unique_id + ".sb3"

        # Create log
        path_log = os.path.dirname(os.path.dirname(__file__)) + "/log/"
        log_file = open(path_log + "logFile.txt", "a")
        log_file.write("FileName: " + str(zip_filename) + "\t\t\t" + "ID: " + str(filename_obj.id) + "\t\t\t" + \
                       "Method: " + str(filename_obj.method) + "\t\t\tTime: " + str(filename_obj.time) + "\n")

        # Save file in server
        file_name = os.path.join("uploads", file_saved)
        request.session['current_project_path'] = file_name
        with open(file_name, 'wb+') as destination:
            for chunk in zip_file.chunks():
                destination.write(chunk)

        try:
            ext_type_project=None
            dict_drscratch_analysis = analyze_project(request, file_name, filename_obj, ext_type_project, skill_points)
            print(dict_drscratch_analysis)
        except Exception:
            traceback.print_exc()
            filename_obj.method = 'project/error'
            filename_obj.save()
            old_path_project = file_saved
            new_path_project = file_saved.split("/uploads/")[0] + "/error_analyzing/" + file_saved.split("/uploads/")[1]
            shutil.copy(old_path_project, new_path_project)
            dict_drscratch_analysis = {'Error': 'analyzing'}
            return dict_drscratch_analysis

        # Redirect to dashboard for unregistered user
        dict_drscratch_analysis['Error'] = 'None'
        return dict_drscratch_analysis
    else:
        return HttpResponseRedirect('/')


def _make_analysis_by_url(request, skill_points: dict):
    """
    Make the automatic analysis by URL
    """
    
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['urlProject']
            id_project = return_scratch_project_identifier(url)
            if id_project == "error":
                return {'Error': 'id_error'}
            else:
                return generator_dic(request, id_project, skill_points)
        else:
            return {'Error': 'MultiValueDict'}
    else:
        return HttpResponseRedirect('/')

def _make_analysis_by_txt(request, url, skill_points: dict):
    """
    Make the automatic analysis by URLS txt
    """
    
    id_project = return_scratch_project_identifier(url)
    if id_project == "error":
        return {'Error': 'id_error'}
    else:
        return generator_dic(request, id_project, skill_points)
        
    


def return_scratch_project_identifier(url) -> str:
    """
    Process String from URL Form
    """
    id_project = ''
    aux_string = url.split("/")[-1]
    if aux_string == '':
        possible_id = url.split("/")[-2]
        if possible_id == "editor":
            id_project = url.split("/")[-3]
        else:
            id_project = possible_id
    else:
        if aux_string == "editor":
            id_project = url.split("/")[-2]
        else:
            id_project = aux_string

    try:
        check_int = int(id_project)
    except ValueError:
        logger.error('Project id is not an integer')
        id_project = "error"

    return id_project


def generator_dic(request, id_project, skill_points: dict):
    """
    Return a dictionary with static analysis and errors
    """

    try:
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = None
        path_project, file_obj, ext_type_project = send_request_getsb3(id_project, username, method="url")
        request.session['current_project_path'] = path_project
    except DrScratchException:
        logger.error('DrScratchException')
        d = {'Error': 'no_exists'}
        return d
    except FileNotFoundError:
        logger.error('File not found into Scratch server')
        traceback.print_exc()
        d = {'Error': 'no_exists'}
        return d

    try:
        
        d = analyze_project(request, path_project, file_obj, ext_type_project, skill_points)
    except Exception:
        logger.error('Impossible analyze project')
        traceback.print_exc()
        file_obj.method = 'url/error'
        file_obj.save()
        old_path_project = path_project
        new_path_project = path_project.split("/uploads/")[0] + "/error_analyzing/" + path_project.split("/uploads/")[1]
        shutil.copy(old_path_project, new_path_project)
        return {'Error': 'analyzing'}

    # Redirect to dashboard for unregistered user
    d['Error'] = 'None'

    return d


def generate_uniqueid_for_saving(id_project):
    date_now = datetime.now()
    date_now_string = date_now.strftime("%Y_%m_%d_%H_%M_%S_%f")
    return id_project + "_" + date_now_string


def save_projectsb3(path_file_temporary, id_project):

    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"

    unique_id = generate_uniqueid_for_saving(id_project)
    unique_file_name_for_saving = dir_zips + unique_id + ".sb3"

    dir_utemp = path_file_temporary.split(id_project)[0].encode('utf-8')
    path_project = os.path.dirname(os.path.dirname(__file__))

    if '_new_project.json' in path_file_temporary:
        ext_project = '_new_project.json'
    else:
        ext_project = '_old_project.json'

    temporary_file_name = id_project + ext_project

    os.chdir(dir_utemp)

    with ZipFile(unique_file_name_for_saving, 'w') as myzip:
        os.rename(temporary_file_name, 'project.json')
        myzip.write('project.json')

    try:
        os.remove('project.json')
        os.chdir(path_project)
    except OSError:
        logger.error('Error removing temporary project.json')

    return unique_file_name_for_saving, ext_project


def write_activity_in_logfile(file_name):

    log_filename = '{}/log/{}'.format(os.path.dirname(os.path.dirname(__file__)), 'logFile.txt')

    try:
        log_file = open(log_filename, "a+")
        log_file.write("FileName: " + str(file_name.filename) + "\t\t\t" + "ID: " + str(file_name.id) + "\t\t\t" +
                       "Method: " + str(file_name.method) + "\t\t\t" + "Time: " + str(file_name.time) + "\n")
    except OSError:
        logger.error('FileNotFoundError')
    except Exception:
        traceback.print_exc()
    finally:
        log_file.close()


def download_scratch_project_from_servers(path_project, id_project):
    scratch_project_inf = ScratchSession().get_project(id_project)
    url_json_scratch = "{}/{}?token={}".format(consts.URL_SCRATCH_SERVER, id_project, scratch_project_inf.project_token)
    path_utemp = '{}/utemp/{}'.format(path_project, id_project)
    path_json_file = path_utemp + '_new_project.json'

    try:
        logger.info(url_json_scratch)
        response_from_scratch = urlopen(url_json_scratch)
    except HTTPError:
        # Two ways, id does not exist in servers or id is in other server
        logger.error('HTTPError')
        url_json_scratch = "{}/{}".format(consts.URL_GETSB3, id_project)
        response_from_scratch = urlopen(url_json_scratch)
        path_json_file = path_utemp + '_old_project.json'
    except URLError:
        logger.error('URLError')
        traceback.print_exc()
    except:
        traceback.print_exc()

    try:
        json_string_format = response_from_scratch.read()
        json_data = json.loads(json_string_format)
        resulting_file = open(path_json_file, 'wb')
        resulting_file.write(json_string_format)
        resulting_file.close()
    except ValueError as e:
        logger.error('ValueError: %s', e.message)
        raise DrScratchException
    except IOError as e:
        logger.error('IOError %s' % e.message)
        raise IOError

    return path_json_file


def send_request_getsb3(id_project, username, method):
    """
    Send request to getsb3 app
    """

    file_url = '{}{}'.format(id_project, '.sb3')

    path_project = os.path.dirname(os.path.dirname(__file__))
    path_json_file_temporary = download_scratch_project_from_servers(path_project, id_project)
    

    now = datetime.now()

    if Organization.objects.filter(username=username):
        file_obj = File(filename=file_url,
                        organization=username,
                        method=method, time=now,
                        score=0, abstraction=0, parallelization=0,
                        logic=0, synchronization=0, flowControl=0,
                        userInteractivity=0, dataRepresentation=0,
                        spriteNaming=0, initialization=0,
                        deadCode=0, duplicateScript=0)
    elif Coder.objects.filter(username=username):
        file_obj = File(filename=file_url,
                        coder=username,
                        method=method, time=now,
                        score=0, abstraction=0, parallelization=0,
                        logic=0, synchronization=0, flowControl=0,
                        userInteractivity=0, dataRepresentation=0,
                        spriteNaming=0, initialization=0,
                        deadCode=0, duplicateScript=0)
    else:
        file_obj = File(filename=file_url,
                        method=method, time=now,
                        score=0, abstraction=0, parallelization=0,
                        logic=0, synchronization=0, flowControl=0,
                        userInteractivity=0, dataRepresentation=0,
                        spriteNaming=0, initialization=0,
                        deadCode=0, duplicateScript=0)
    
    file_obj.save()

    write_activity_in_logfile(file_obj)
    path_scratch_project_sb3, ext_type_project = save_projectsb3(path_json_file_temporary, id_project)

    return path_scratch_project_sb3, file_obj, ext_type_project


def check_version(filename):
    """
    Check the version of the project and return it
    """

    extension = filename.split('.')[-1]
    if extension == 'sb2':
        version = '2.0'
    elif extension == 'sb3':
        version = '3.0'
    else:
        version = '1.4'

    return version


def load_json_project(path_projectsb3):
    try:
        zip_file = ZipFile(path_projectsb3, "r")
        json_project = json.loads(zip_file.open("project.json").read())
        return json_project
    except BadZipfile:
        print('Bad zipfile')


def analyze_project(request, path_projectsb3, file_obj, ext_type_project, skill_points: dict):

    dict_analysis = {}
    
    if os.path.exists(path_projectsb3):
        json_scratch_project = load_json_project(path_projectsb3)
        dict_mastery = Mastery(path_projectsb3, json_scratch_project, skill_points, request.POST.get('dashboard_mode')).finalize()
        dict_duplicate_script = DuplicateScripts(path_projectsb3, json_scratch_project).finalize()
        dict_dead_code = DeadCode(path_projectsb3, json_scratch_project,).finalize()
        result_sprite_naming = SpriteNaming(path_projectsb3, json_scratch_project).finalize()
        result_backdrop_naming = BackdropNaming(path_projectsb3, json_scratch_project).finalize()
        
        print("Duplicate Script: ", dict_duplicate_script['result']['list_duplicate_scripts'])
        #Refactorings
        refactored_code = RefactorDuplicate(json_scratch_project, dict_duplicate_script).refactor_duplicates()

        dict_analysis.update(proc_mastery(request, dict_mastery, file_obj))
        dict_analysis.update(proc_duplicate_script(dict_duplicate_script, file_obj))
        dict_analysis.update(proc_dead_code(dict_dead_code, file_obj))
        dict_analysis.update(proc_sprite_naming(result_sprite_naming, file_obj))
        dict_analysis.update(proc_backdrop_naming(result_backdrop_naming, file_obj))
        dict_analysis.update(proc_refactored_code(refactored_code))
        # dict_analysis.update(proc_urls(request, dict_mastery, file_obj))
        
        # dictionary.update(proc_initialization(resultInitialization, filename))
        print("Dict Analysis: ", dict_analysis)
        return dict_analysis
    else:
        return dict_analysis
    
def proc_refactored_code(refactor):
    dict_refactor = {}
    dict_refactor["refactor"] = dict_refactor
    dict_refactor["refactor"]["refactor_list"] = refactor

    return dict_refactor


def proc_dead_code(dict_dead_code, filename):

    dict_dc = {}
    dict_dc["deadCode"] = dict_dc
    dict_dc["deadCode"]["number"] = dict_dead_code['result']['total_dead_code_scripts']

    for dict_sprite_dead_code_blocks in dict_dead_code['result']['list_dead_code_scripts']:
        for sprite_name, list_blocks in dict_sprite_dead_code_blocks.items():
            dict_dc["deadCode"][sprite_name] = list_blocks

    filename.deadCode = dict_dead_code['result']['total_dead_code_scripts']
    filename.save()

    return dict_dc

def proc_urls(request, dict_mastery, file_obj):
    dict_urls = {}
    if request.POST.get('dashboard_mode') == 'Default':
        dict_extended = dict_mastery['extended'].copy()
        dict_vanilla = dict_mastery['vanilla'].copy()
        dict_urls["url_extended"] = get_urls(dict_extended)
        dict_urls["url_vanilla"] = get_urls(dict_vanilla)
    elif request.POST.get('dashboard_mode') == 'Personalized':
        dict_personal = dict_mastery['personalized'].copy()
        print(dict_personal)
        dict_urls["url_personal"] = get_urls(dict_personal)
    return dict_urls

def get_urls(dict_mastery):
    list_urls = []
    for key in dict_mastery.keys():
        if key != 'total_points' and key!= 'competence' and key!= 'max_points' and key!= 'average_points':
            list_urls.append(key)
    return list_urls

def proc_mastery(request, dict_mastery, file_obj):

    if request.POST.get('dashboard_mode') == 'Default' or request.POST.get('dashboard_mode') == 'Comparison':
        dict_extended = dict_mastery['extended'].copy()
        dict_vanilla = dict_mastery['vanilla'].copy()
        set_file_obj(request, file_obj, dict_extended)
        set_file_obj(request, file_obj, dict_vanilla, 'Vanilla')
        d_extended_translated = translate(request, dict_extended, file_obj)
        d_vanilla_translated = translate(request, dict_vanilla, file_obj, vanilla=True)
        dic = {"mastery": d_extended_translated, "mastery_vanilla": d_vanilla_translated}
        dic["mastery"]["competence"] = dict_extended["competence"]
        dic["mastery"]["points"] = dict_extended["total_points"]
        dic["mastery_vanilla"]["competence"] = dict_vanilla["competence"]
        dic["mastery_vanilla"]["points"] = dict_vanilla["total_points"]
        
    elif request.POST.get('dashboard_mode') == 'Personalized':
        dict_personal = dict_mastery['personalized'].copy()
        set_file_obj(request, file_obj, dict_personal)
        d_personal_translated = translate(request, dict_personal, file_obj)
        dic = {"mastery": d_personal_translated}
        dic["mastery"]["competence"] = dict_personal["competence"]
        dic["mastery"]["points"] = dict_personal["total_points"]
        print("Lista_Mastery:", dict_personal.keys())
    
    return dic

def set_file_obj(request, file_obj, dict, mode=None):

    file_obj.score = dict["total_points"][0]
    file_obj.competence = dict["competence"]
    file_obj.abstraction = dict["Abstraction"][0]
    file_obj.parallelization = dict["Parallelization"][0]
    file_obj.logic = dict["Logic"][0]
    file_obj.synchronization = dict["Synchronization"][0]
    file_obj.flow_control = dict["FlowControl"][0]
    file_obj.userInteractivity = dict["UserInteractivity"][0]
    file_obj.dataRepresentation = dict["DataRepresentation"][0]
    if mode != 'Vanilla':
        file_obj.mathOperators = dict["MathOperators"][0]
        file_obj.mathOperators = dict["MotionOperators"][0]
    file_obj.save()


def proc_duplicate_script(dict_result, file_obj) -> dict:

    dict_ds = {}
    dict_ds["duplicateScript"] = dict_ds
    dict_ds["duplicateScript"]["number"] = dict_result['result']['total_duplicate_scripts']
    dict_ds["duplicateScript"]["scripts"] = dict_result['result']['list_duplicate_scripts']
    dict_ds["duplicateScript"]["csv_format"] = dict_result['result']['list_csv']

    file_obj.duplicateScript = dict_result['result']['total_duplicate_scripts']
    file_obj.save()

    return dict_ds


def proc_sprite_naming(lines, file_obj):

    dic = {}
    lLines = lines.split('\n')
    number = lLines[0].split(' ')[0]
    lObjects = lLines[1:]
    lfinal = lObjects[:-1]

    dic['spriteNaming'] = dic
    dic['spriteNaming']['number'] = int(number)
    dic['spriteNaming']['sprite'] = lfinal

    file_obj.spriteNaming = number
    file_obj.save()

    return dic


def proc_backdrop_naming(lines, file_obj):

    dic = {}
    lLines = lines.split('\n')
    number = lLines[0].split(' ')[0]
    lObjects = lLines[1:]
    lfinal = lObjects[:-1]
    dic['backdropNaming'] = dic
    dic['backdropNaming']['number'] = int(number)
    dic['backdropNaming']['backdrop'] = lfinal

    file_obj.backdropNaming = number
    file_obj.save()

    return dic


def translate(request, d, filename, vanilla=False):
    """
    Translate the output of Hairball
    """

    if request.LANGUAGE_CODE == "es":
        d_translate_es = {'Abstracción': [d['Abstraction'], 'Abstraction'], 'Paralelismo': [d['Parallelization'], 'Parallelism'],
                          'Pensamiento lógico': [d['Logic'], 'Logic'], 'Sincronización': [d['Synchronization'], 'Synchronization'],
                          'Control de flujo': [d['FlowControl'], 'FlowControl'], 'Interactividad con el usuario': [d['UserInteractivity'], 'UserInteractivity'],
                          'Representación de la información': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: # Check that not is Vanilla Mode
            d_translate_es.update({'Operadores matemáticos': [d['MathOperators'], 'MathOperators'], 'Operadores de movimiento': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "es"
        filename.save()
        return d_translate_es
    elif request.LANGUAGE_CODE == "en":
        d_translate_en = {'Abstraction': [d['Abstraction'], 'Abstraction'], 'Parallelism': [d['Parallelization'], 'Parallelism'], 'Logic': [d['Logic'], 'Logic'],
                          'Synchronization': [d['Synchronization'], 'Synchronization'], 'Flow control': [d['FlowControl'], 'FlowControl'],
                          'User interactivity': [d['UserInteractivity'], 'UserInteractivity'], 'Data representation': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_en.update({'Math operators': [d['MathOperators'], 'MathOperators'], 'Motion operators': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "en"
        filename.save()
        return d_translate_en
    elif request.LANGUAGE_CODE == "ca":
        d_translate_ca = {'Abstracció': [d['Abstraction'], 'Abstraction'], 'Paral·lelisme': [d['Parallelization'], 'Parallelism'], 'Lògica': [d['Logic'], 'Logic'],
                          'Sincronització': [d['Synchronization'], 'Synchronization'], 'Controls de flux': [d['FlowControl'], 'FlowControl'],
                          "Interactivitat de l'usuari": [d['UserInteractivity'], 'UserInteractivity'],
                          'Representació de dades': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_ca.update({'Operadors matemàtics': [d['MathOperators'], 'MathOperators'], 'Operadors de moviment':  [d['MotionOperators'], 'MotionOperators']})
        filename.language = "ca"
        filename.save()
        return d_translate_ca
    elif request.LANGUAGE_CODE == "gl":
        d_translate_gl = {'Abstracción': [d['Abstraction'], 'Abstraction'], 'Paralelismo': [d['Parallelization'], 'Parallelism'], 'Lóxica': [d['Logic'], 'Logic'],
                          'Sincronización': [d['Synchronization'], 'Synchronization'], 'Control de fluxo': [d['FlowControl'], 'FlowControl'],
                          "Interactividade do susario": [d['UserInteractivity'], 'UserInteractivity'],
                          'Representación dos datos': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_gl.update({'Operadores matemáticos': [d['MathOperators'], 'MathOperators'], 'Operadores de movemento': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "gl"
        filename.save()
        return d_translate_gl

    elif request.LANGUAGE_CODE == "pt":
        d_translate_pt = {'Abstração': [d['Abstraction'], 'Abstraction'], 'Paralelismo': [d['Parallelization'], 'Parallelism'], 'Lógica': [d['Logic'], 'Logic'],
                          'Sincronização': [d['Synchronization'], 'Synchronization'], 'Controle de fluxo': [d['FlowControl'], 'FlowControl'],
                          "Interatividade com o usuário": [d['UserInteractivity'], 'UserInteractivity'],
                          'Representação de dados': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_pt.update({'Operadores matemáticos': [d['MathOperators'], 'MathOperators'], 'Operadores de movimento': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "pt"
        filename.save()
        return d_translate_pt
    
    elif request.LANGUAGE_CODE == "el":
        d_translate_el = {'Αφαίρεση': [d['Abstraction'], 'Abstraction'], 'Παραλληλισμός': [d['Parallelization'], 'Parallelism'], 'Λογική': [d['Logic'], 'Logic'],
                          'Συγχρονισμός': [d['Synchronization'], 'Synchronization'], 'Έλεγχος ροής': [d['FlowControl'], 'FlowControl'],
                          'Αλληλεπίδραση χρήστη': [d['UserInteractivity'], 'UserInteractivity'],
                          'Αναπαράσταση δεδομένων': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_el.update({'Μαθηματικοί χειριστές': [d['MathOperators'], 'MathOperators'], 'Χειριστές κίνησης': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "el"
        filename.save()
        return d_translate_el

    elif request.LANGUAGE_CODE == "eu":           
        d_translate_eu = {'Abstrakzioa': [d['Abstraction'], 'Abstraction'], 'Paralelismoa': [d['Parallelization'], 'Parallelism'], 'Logika': [d['Logic'], 'Logic'],
                          'Sinkronizatzea': [d['Synchronization'], 'Synchronization'], 'Kontrol fluxua': [d['FlowControl'], 'FlowControl'],
                          'Erabiltzailearen elkarreragiletasuna': [d['UserInteractivity'], 'UserInteractivity'],
                          'Datu adierazlea': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_eu.update({'Eragile matematikoak': [d['MathOperators'], 'MathOperators'], 'Mugimendu-eragileak': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "eu"
        filename.save()
        return d_translate_eu

    elif request.LANGUAGE_CODE == "it":           
        d_translate_it = {'Astrazione': [d['Abstraction'], 'Abstraction'], 'Parallelismo': [d['Parallelization'], 'Parallelism'], 'Logica': [d['Logic'], 'Logic'],
                          'Sincronizzazione': [d['Synchronization'], 'Synchronization'], 'Controllo di flusso': [d['FlowControl'], 'FlowControl'],
                          'Interattività utente': [d['UserInteractivity'], 'UserInteractivity'],
                          'Rappresentazione dei dati': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_it.update({'Operatori matematici':  [d['MathOperators'], 'MathOperators'], 'Operatori del movimento': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "it"
        filename.save()
        return d_translate_it

    elif request.LANGUAGE_CODE == "ru":
        d_translate_ru = {'Абстракция': [d['Abstraction'], 'Abstraction'], 'Параллельность действий': [d['Parallelization'], 'Parallelism'],
                          'Логика': [d['Logic'], 'Logic'], 'cинхронизация': [d['Synchronization'], 'Synchronization'],
                          'Управление потоком': [d['FlowControl'], 'FlowControl'], 'Интерактивность': [d['UserInteractivity'], 'UserInteractivity'],
                          'Представление данных': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_ru.update({'Математические операторы': [d['MathOperators'], 'MathOperators'], 'Операторы движения': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "ru"
        filename.save()
        return d_translate_ru
    else:
        d_translate_en = {'Abstraction': [d['Abstraction'], 'Abstraction'], 'Parallelism': [d['Parallelization'], 'Parallelism'], 'Logic': [d['Logic'], 'Logic'],
                          'Synchronization': [d['Synchronization'], 'Synchronization'], 'Flow control': [d['FlowControl'], 'FlowControl'],
                          'User interactivity': [d['UserInteractivity'], 'UserInteractivity'], 'Data representation': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_en.update({'Math Operators': [d['MathOperators'], 'MathOperators'], 'Motion Operators': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "any"
        filename.save()
        return d_translate_en

def skills_translation(request) -> dict:
    """
    Create a dict with the skills name translated
    """
    if request.LANGUAGE_CODE == "en":
        dic = {u'Logic': 'Logic',
               u'Parallelism':'Parallelism',
               u'Data representation':'Data representation',
               u'Synchronization':'Synchronization',
               u'User interactivity':'User interactivity',
               u'Flow control':'Flow control',
               u'Abstraction':'Abstraction',
               u'Math operators':'Math operators',
               u'Motion operators': 'Motion operators'}
    elif request.LANGUAGE_CODE == "es":
        #page = unicodedata.normalize('NFKD',page).encode('ascii', 'ignore')
        dic = {'Pensamiento lógico':'Logic',
               'Paralelismo':'Parallelism',
               'Representación de la información':'Data representation',
               'Sincronización':'Synchronization',
               'Interactividad con el usuario':'User',
               'Control de flujo':'Flow control',
               'Abstracción':'Abstraction',
               'Operadores matemáticos':'Math operators',
               'Operadores de movimiento': 'Motion operators'}
    elif request.LANGUAGE_CODE == "ca":
        #page = unicodedata.normalize('NFKD', page).encode('ascii', 'ignore')
        dic = {u'Lògica':'Logic',
               u'Paral·lelisme':'Parallelism',
               u'Representació de dades':'Data representation',
               u'Sincronització':'Synchronization',
               u"Interactivitat de l'usuari":'User interactivity',
               u'Controls de flux':'Flow control',
               u'Abstracció':'Abstraction',
               u'Operadors matemàtics':'Math operators',
               u'Operadors de moviment': 'Motion operators'}
    elif request.LANGUAGE_CODE == "gl":
        #page = unicodedata.normalize('NFKD',page).encode('ascii', 'ignore')
        dic = {'Lóxica':'Logic',
               'Paralelismo':'Parallelism',
               'Representación dos datos':'Data representation',
               'Sincronización':'Synchronization',
               'Interactividade do susario':'User interactivity',
               'Control de fluxo':'Flow control',
               'Abstracción':'Abstraction',
               'Operadores matemáticos':'Math operators',
               'Operadores de movemento': 'Motion operators'}
    elif request.LANGUAGE_CODE == "pt":
        #page = unicodedata.normalize('NFKD',page).encode('ascii', 'ignore')
        dic = {'Lógica':'Logic',
               'Paralelismo':'Parallelism',
               'Representação de dados':'Data representation',
               'Sincronização':'Synchronization',
               'Interatividade com o usuário':'User interactivity',
               'Controle de fluxo':'Flow control',
               'Abstração':'Abstraction',
               'Operadores matemáticos':'Math operators',
               'Operadores de movimento': 'Motion operators'}
    elif request.LANGUAGE_CODE == "el":
        dic = {u'Λογική':'Logic',
           u'Παραλληλισμός':'Parallelism',
           u'Αναπαράσταση δεδομένων':'Data representation',
           u'Συγχρονισμός':'Synchronization',
           u'Αλληλεπίδραση χρήστη':'User interactivity',
           u'Έλεγχος ροής':'Flow control',
           u'Αφαίρεση':'Abstraction',
           u'Μαθηματικοί χειριστές':'Math operators',
           u'Χειριστές κίνησης': 'Motion operators'}
    elif request.LANGUAGE_CODE == "eu":
        #page = unicodedata.normalize('NFKD',page).encode('ascii', 'ignore')
        dic = {u'Logika':'Logic',
           u'Paralelismoa':'Parallelism',
           u'Datu adierazlea':'Data representation',
           u'Sinkronizatzea':'Synchronization',
           u'Erabiltzailearen elkarreragiletasuna':'User interactivity',
           u'Kontrol fluxua':'Flow control',
           u'Abstrakzioa':'Abstraction',
           u'Eragile matematikoak':'Math operators',
           u'Mugimendu-eragileak': 'Motion operators'}
    elif request.LANGUAGE_CODE == "it":
        #page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')
        dic = {u'Logica':'Logic',
           u'Parallelismo':'Parallelism',
           u'Rappresentazione dei dati':'Data representation',
           u'Sincronizzazione':'Synchronization',
           u'Interattività utente':'User interactivity',
           u'Controllo di flusso':'Flow control',
           u'Astrazione':'Abstraction',
           u'Operatori matematici':'Math operators',
           u'Operatori del movimento': 'Motion operators'}
    elif request.LANGUAGE_CODE == "ru":
        dic = {u'Логика': 'Logic',
               u'Параллельность действий': 'Parallelism',
               u'Представление данных': 'Data representation',
               u'cинхронизация': 'Synchronization',
               u'Интерактивность': 'User interactivity',
               u'Управление потоком': 'Flow control',
               u'Абстракция': 'Abstraction',
               u'Математические операторы':'Math operators',
               u'Операторы движения': 'Motion operators'}
    else:
        dic = {u'Logica':'Logic',
               u'Paralelismo':'Parallelism',
               u'Representacao':'Data representation',
               u'Sincronizacao':'Synchronization',
               u'Interatividade':'User interactivity',
               u'Controle':'Flow control',
               u'Abstracao':'Abstraction',
               u'Operadores matemáticos':'Math operators',
               u'Operadores de movimento': 'Motion operators'}
    
    return dic

def learn(request, page):
    """
    Shows pages to learn more about CT
    """

    flag_user = 0

    if request.user.is_authenticated:
        user = request.user.username
        flag_user = 1

    dic = skills_translation(request)

    if page in dic:
        page = dic[page]
    
    page = '{}{}{}'.format('learn/', page, '.html')

    if request.user.is_authenticated:
        user = identify_user_type(request)
        username = request.user.username
        return render(request, page, {'flagUser': flag_user, 'user': user, 'username': username})
    else:
        return render(request, page)

def contact(request):
    """
    Shows contact form
    """
    user = "main"
    captcha_pubkey = settings.RECAPTCHA_PUBLIC_KEY
    context = {
        'captcha_pubkey' : captcha_pubkey
    }
    return render(request, user + '/contact-form.html', context) 


def download_certificate(request):
    """
    Download project's certificate
    """

    if request.method == "POST":
        data = request.POST["certificate"]
        # Encode to make sure that cotains utf-8 chars
        data = unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')
        # Decode again for manipulate the str
        data = data.decode('utf-8') 
        filename = data.split(",")[0]
        filename = clean_filename(filename)
        level = data.split(",")[1]

        if is_supported_language(request.LANGUAGE_CODE):
            language = request.LANGUAGE_CODE
        else:
            language = 'en'

        
        generate_certificate(filename, level, language)
        path_to_file = os.path.dirname(os.path.dirname(__file__)) + "/app/certificate/output.pdf"
        
        with open(path_to_file, 'rb') as pdf_file:
           pdf_data = pdf_file.read()

        response = HttpResponse(pdf_data, content_type='application/pdf')
        try:
            file_pdf = filename.split("/")[-2] + ".pdf"
        except:
            file_pdf = filename.split(".")[0] + ".pdf"

        response['Content-Disposition'] = 'attachment; filename=%s' % file_pdf
        return response
    else:
        return HttpResponseRedirect('/')
    
def clean_filename(filename):
    """
    Clean filename, necessary for .sb3 upload
    """
    pattern = r';.*.sb3'
    matches = re.findall(pattern, filename)
    if matches:
        filename = matches[0]
        filename = re.sub(';', '', filename)
    return filename

def is_supported_language(lenguage_code):
    suported = 0
    for i in supported_languages:
        if i == lenguage_code:
            suported = 1
    return suported

def search_email(request):
    if request.is_ajax():
        user = Organization.objects.filter(email=request.GET['email'])
        if user:
            return HttpResponse(json.dumps({"exist": "yes"}), content_type ='application/json')


def search_username(request):
    if request.is_ajax():
        user = Organization.objects.filter(username=request.GET['username'])
        if user:
            return HttpResponse(json.dumps({"exist": "yes"}), content_type='application/json')


def search_hashkey(request):
    if request.is_ajax():
        user = OrganizationHash.objects.filter(hashkey=request.GET['hashkey'])
        if not user:
            return HttpResponse(json.dumps({"exist": "yes"}), content_type='application/json')


def plugin(request, urlProject):
    user = None
    id_project = return_scratch_project_identifier(urlProject)
    
    d = generator_dic(request, id_project)
    #Find if any error has occurred
    if d['Error'] == 'analyzing':
        return render(request, user + '/error_analyzing.html')

    elif d['Error'] == 'MultiValueDict':
        error = True
        return render(request, user + '/main.html', {'error':error})

    elif d['Error'] == 'id_error':
        id_error = True
        return render(request, user + '/main.html', {'id_error':id_error})

    elif d['Error'] == 'no_exists':
        no_exists = True
        return render(request, user + '/main.html', {'no_exists':no_exists})

    #Show the dashboard according the CT level
    else:
        user = "main"
        base_dir = os.getcwd()
        if d["mastery"]["points"] >= 15:
            return render(request, user + '/dashboard-master.html', d)

        elif d["mastery"]["points"] > 7:
            return render(request, user + '/dashboard-developing.html', d)

        else:
            return render(request, user + '/dashboard-basic.html', d) 


def blocks(request):
    """
    Translate blocks of Scratch shown in learn pages
    """

    callback = request.GET.get('callback')
    headers = {}
    headers['Accept-Language'] = str(request.LANGUAGE_CODE)

    headers = json.dumps(headers)
    if callback:
        headers = '%s(%s)' % (callback, headers)
        return HttpResponse(headers, content_type="application/json")


def blocks_v3(request):
    return render(request, 'learn/blocks_v3.html')


def organization_hash(request):
    if request.method == "POST":
        form = OrganizationHashForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/organization_hash')
    elif request.method == 'GET':
        return render(request, 'organization/organization-hash.html') 

    else:
        return HttpResponseRedirect('/')


def sign_up_organization(request):
    """Method which allow to sign up organizations"""

    flag_organization = 1
    flag_hash = 0
    flag_name = 0
    flag_email = 0
    flag_form = 0

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashkey = form.cleaned_data['hashkey']

            #Checking the validity into the dbdata contents.
            #They will be refused if they already exist.
            #If they exist an error message will be shown.
            if User.objects.filter(username = username):
                #This name already exists
                flag_name = 1
                return render(request, 'error/sign-up.html',
                                          {'flagName':flag_name,
                                           'flagEmail':flag_email,
                                           'flagHash':flag_hash,
                                           'flagForm':flag_form,
                                           'flagOrganization':flag_organization})

            elif User.objects.filter(email = email):
                #This email already exists
                flag_email = 1
                return render(request, 'error/sign-up.html',
                                        {'flagName':flag_name,
                                        'flagEmail':flag_email,
                                        'flagHash':flag_hash,
                                        'flagForm':flag_form,
                                        'flagOrganization':flag_organization})

            if (OrganizationHash.objects.filter(hashkey = hashkey)):
                organizationHashkey = OrganizationHash.objects.get(hashkey=hashkey)
                organization = Organization.objects.create_user(username = username, 
                                                            email=email, 
                                                            password=password, 
                                                            hashkey=hashkey)
                organizationHashkey.delete()
                organization = authenticate(username=username, password=password)
                user=Organization.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token=default_token_generator.make_token(user)
                c = {
                        'email':email,
                        'uid':uid,
                        'token':token}

                body = render_to_string("organization/email-sign-up.html",c)
                subject = "Welcome to Dr. Scratch for organizations"
                sender ="no-reply@drscratch.org"
                to = [email]
                email = EmailMessage(subject,body,sender,to)
                #email.attach_file("static/app/images/logo_main.png")
                email.send()
                login(request, organization)
                return HttpResponseRedirect('/organization/' + organization.username)

            else:
                #Doesn't exist this hash
                flag_hash = 1

                return render(request, 'error/sign-up.html',
                                  {'flagName':flag_name,
                                   'flagEmail':flag_email,
                                   'flagHash':flag_hash,
                                   'flagForm':flag_form,
                                   'flagOrganization':flag_organization})


        else:
            flag_form = 1
            return render(request, 'error/sign-up.html',
                  {'flagName':flag_name,
                   'flagEmail':flag_email,
                   'flagHash':flag_hash,
                   'flagForm':flag_form,
                   'flagOrganization':flag_organization})

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/organization/' + request.user.username)
        else:
            return render(request, 'organization/organization.html')


def login_organization(request):
    """Log in app to user"""

    if request.method == 'POST':
        flag = False
        flagOrganization = 0
        form = LoginOrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            organization = authenticate(username=username, password=password)
            if organization is not None:
                if organization.is_active:
                    login(request, organization)
                    return HttpResponseRedirect('/organization/' + organization.username)

            else:
                flag = True
                flagOrganization = 1
                return render(request, 'sign-password/user-doesnt-exist.html',
                              {'flag': flag, 'flagOrganization': flagOrganization})

    else:
        return HttpResponseRedirect("/")


def logout_organization(request):
    logout(request)
    return HttpResponseRedirect('/')


def organization(request, name):
    """
    Show page of Organizations to sign up
    """

    if request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
            if username == name:
                if Organization.objects.filter(username = username):
                    user = Organization.objects.get(username=username)
                    img = user.img
                    dic={'username':username,
                    "img":str(img)}

                    return render(request, 'organization/main.html', dic)

                else:
                    logout(request)
                    return HttpResponseRedirect("/organization")

            else:
                #logout(request)
                return render(request, 'organization/organization.html')

        return render(request, 'organization/organization.html')

    else:
        return HttpResponseRedirect("/")


def stats(request, username):
    """Generator of the stats from Coders and Organizations"""

    flag_organization = 0
    flag_coder = 0
    if Organization.objects.filter(username=username):
        flag_organization = 1
        page = 'organization'
        user = Organization.objects.get(username=username)
    elif Coder.objects.filter(username=username):
        flag_coder = 1
        page = 'coder'
        user = Coder.objects.get(username=username)

    date_joined = user.date_joined
    end = datetime.today()
    end = date(end.year, end.month, end.day)
    start = date(date_joined.year, date_joined.month,date_joined.day)
    date_list = date_range(start, end)
    daily_score = []
    mydates = []
    for n in date_list:
        mydates.append(n.strftime("%d/%m"))
        if flag_organization:
            points = File.objects.filter(organization=username).filter(time=n)
        elif flag_coder:
            points = File.objects.filter(coder=username).filter(time=n)
        points = points.aggregate(Avg("score"))["score__avg"]
        daily_score.append(points)

    for n in daily_score:
        if n is None:
            daily_score[daily_score.index(n)]=0

    if flag_organization:
        f = File.objects.filter(organization=username)
    elif flag_coder:
        f = File.objects.filter(coder=username)
    if f:

        #If the org has analyzed projects
        Parallelism = f.aggregate(Avg("Parallelism"))
        Parallelism = int(Parallelism["Parallelism__avg"])
        abstraction = f.aggregate(Avg("abstraction"))
        abstraction = int(abstraction["abstraction__avg"])
        logic = f.aggregate(Avg("logic"))
        logic = int(logic["logic__avg"])
        synchronization = f.aggregate(Avg("synchronization"))
        synchronization = int(synchronization["synchronization__avg"])
        flowControl = f.aggregate(Avg("flowControl"))
        flowControl = int(flowControl["flowControl__avg"])
        userInteractivity = f.aggregate(Avg("userInteractivity"))
        userInteractivity = int(userInteractivity["userInteractivity__avg"])
        dataRepresentation = f.aggregate(Avg("dataRepresentation"))
        dataRepresentation = int(dataRepresentation["dataRepresentation__avg"])

        deadCode = File.objects.all().aggregate(Avg("deadCode"))
        deadCode = int(deadCode["deadCode__avg"])
        duplicateScript = File.objects.all().aggregate(Avg("duplicateScript"))
        duplicateScript = int(duplicateScript["duplicateScript__avg"])
        spriteNaming = File.objects.all().aggregate(Avg("spriteNaming"))
        spriteNaming = int(spriteNaming["spriteNaming__avg"])
        initialization = File.objects.all().aggregate(Avg("initialization"))
        initialization = int(initialization["initialization__avg"])
    else:

        #If the org hasn't analyzed projects yet
        Parallelism,abstraction,logic=[0],[0],[0]
        synchronization,flowControl,userInteractivity=[0],[0],[0]
        dataRepresentation,deadCode,duplicateScript=[0],[0],[0]
        spriteNaming,initialization =[0],[0]

    #Saving data in the dictionary
    dic = {
        "date":mydates,
        "username": username,
        "img": user.img,
        "daily_score":daily_score,
        "skillRate":{"Parallelism":Parallelism,
                 "abstraction":abstraction,
                 "logic": logic,
                 "synchronization":synchronization,
                 "flowControl":flowControl,
                 "userInteractivity":userInteractivity,
                 "dataRepresentation":dataRepresentation},
                 "codeSmellRate":{"deadCode":deadCode,
        "duplicateScript":duplicateScript,
        "spriteNaming":spriteNaming,
        "initialization":initialization }}

    return render(request, page + '/stats.html', dic)


def account_settings(request,username):
    """Allow to Coders and Organizations change the image and password"""


    base_dir = os.getcwd()
    if base_dir == "/":
        base_dir = "/var/www/drscratchv3"
    flagOrganization = 0
    flagCoder = 0
    if Organization.objects.filter(username=username):
        page = 'organization'
        user = Organization.objects.get(username=username)
    elif Coder.objects.filter(username=username):
        page = 'coder'
        user = Coder.objects.get(username=username)

    if request.method == "POST":

        #Saving image in DB
        user.img = request.FILES["img"]
        os.chdir(base_dir+"/static/img")
        user.img.name = str(user.img)

        if os.path.exists(user.img.name):
            os.remove(user.img.name)

        os.chdir(base_dir)
        user.save()

    dic = {
    "username": username,
    "img": user.img
    }

    return render(request, page + '/settings.html', dic)


def downloads(request, username, filename=""):
    """
    Allow to Coders and Organizations download the files.CSV already analyzed
    """

    flagOrganization = 0
    flagCoder = 0
    #segmentation
    if Organization.objects.filter(username=username):
        flagOrganization = 1
        user = Organization.objects.get(username=username)
    elif Coder.objects.filter(username=username):
        flagCoder = 1
        user = Coder.objects.get(username=username)

    if flagOrganization:
        csv = CSVs.objects.all().filter(organization=username)
        page = 'organization'
    elif flagCoder:
        csv = CSVs.objects.all().filter(coder=username)
        page = 'coder'
    #LIFO to show the files.CSV

    csv_len = len(csv)
    lower = 0
    upper = 10
    list_csv = {}

    if csv_len > 10:
        for n in range((csv_len/10)+1):
            list_csv[str(n)]= csv[lower:upper-1]
            lower = upper
            upper = upper + 10


        dic = {
        "username": username,
        "img": user.img,
        "csv": list_csv,
        "flag": 1
        }
    else:
        dic = {
        "username": username,
        "img": user.img,
        "csv": csv,
        "flag": 0
        }

    if request.method == "POST":
        #Downloading CSV
        filename = request.POST.get("csv", "")
        safe_filename = os.path.basename(filename)
        csv_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csvs/Dr.Scratch")
        path_to_file = os.path.join(csv_directory, safe_filename)
        # Ensure that the path exists, to avoid injection-attacks
        if not os.path.exists(path_to_file) or not validate_csv(path_to_file):
            return HttpResponse("Invalid CSV file", status=400)
        with open(path_to_file, 'rb') as csv_data:
            response = HttpResponse(csv_data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(safe_filename)
            return response
    return render(request, page + '/downloads.html', dic)

def validate_csv(csv_file_path: str)-> bool:
    is_valid_file = os.path.isfile(csv_file_path)
    is_csv_file = csv_file_path.endswith('.csv')
    return is_valid_file and is_csv_file


def analyze_csv(request):
    """
    Analyze files.CSV with a list of projects to analyze them at a time
    """

    if request.method =='POST':
        if "_upload" in request.POST:
            #Analize CSV file
            csv_data = 0
            flag_csv = False
            file = request.FILES['csvFile']
            file_name = request.user.username + "_" + str(datetime.now()) + \
                        ".csv"# file.name.encode('utf-8')
            dir_csvs = os.path.dirname(os.path.dirname(__file__)) + \
                        "/csvs/" + file_name
            #Save file .csv
            with open(dir_csvs, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            dictionary = {}
            for line in open(dir_csvs, 'r'):
                row = len(line.split(","))
                type_csv = ""
                username = request.user.username

                #Check doesn't exist any old project.json
                try:
                    os.remove(dir_zips + "project.json")
                except:
                    print("No existe")
                
                if row == 2:
                    type_csv = "2_row"
                    code = line.split(",")[0]
                    url = line.split(",")[1]
                    url = url.split("\n")[0]
                    method = "csv"
                    if url.isdigit():
                        id_project = url
                    else:
                        slashNum = url.count('/')
                        if slashNum == 4:
                            id_project = url.split("/")[-1]
                        elif slashNum == 5:
                            id_project = url.split('/')[-2]
                    try:
                        path_project, file = send_request_getsb3(id_project, username, method)
                        d = analyze_project(request, path_project, file)
                    except:
                        d = ["Error analyzing project", url]

                    try:
                        os.remove(dir_zips + "project.json")
                    except:
                        print("No existe")

                    dic = {}
                    dic[line] = d
                    dictionary.update(dic)
                elif row == 1:
                    type_csv = "1_row"
                    url = line.split("\n")[0]
                    method = "csv"
                    if url.isdigit():
                        id_project = url
                    else:
                        slashNum = url.count('/')
                        if slashNum == 4:
                            id_project = url.split("/")[-1]
                        elif slashNum == 5:
                            id_project = url.split('/')[-2]
                    try:
                        path_project, file = send_request_getsb3(id_project, username, method)
                        d = analyze_project(request, path_project, file)
                    except:
                        d = ["Error analyzing project", url]

                    try:
                        os.remove(dir_zips + "project.json")
                    except:
                        print("No existe")


                    dic = {}
                    dic[url] = d
                    dictionary.update(dic)

            csv_data = generate_csv(request, dictionary, file_name, type_csv)

            #segmentation
            if Organization.objects.filter(username = username):
                csv_save = CSVs(filename = file_name, 
                                    directory = csv_data, 
                                    organization = username)
                
                page = 'organization'
            elif Coder.objects.filter(username = username):
                csv_save = CSVs(filename = file_name, 
                                    directory = csv_data, 
                                    coder = username)
                page = 'coder'
            csv_save.save()

            return HttpResponseRedirect('/' + page + "/downloads/" + username)

        elif "_download" in request.POST:
            #Export a CSV File

            if request.user.is_authenticated:
                username = request.user.username
            csv = CSVs.objects.latest('date')

            path_to_file = os.path.dirname(os.path.dirname(__file__)) + \
                            "/csvs/Dr.Scratch/" + csv.filename
            csv_data = open(path_to_file, 'r')
            response = HttpResponse(csv_data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(csv.filename)
            return response

    else:
        return HttpResponseRedirect("/organization")


#_________________________GENERATOR CSV FOR ORGANIZATION____________________________#

def generate_csv(request, dictionary, filename, type_csv):
    """
    Generate a csv file
    """

    csv_directory = os.path.dirname(os.path.dirname(__file__)) + "/csvs/Dr.Scratch/"
    csv_data = csv_directory + filename
    writer = csv.writer(open(csv_data, "wb"))
    dic = org.translate_ct_skills(request.LANGUAGE_CODE)

    if type_csv == "2_row":
        writer.writerow([dic["code"], dic["url"], dic["mastery"],
                        dic["abstraction"], dic["Parallelization"],
                        dic["logic"], dic["sync"],
                        dic["flow_control"], dic["user_inter"], dic["data_rep"],
                        dic["dup_scripts"],dic["sprite_naming"],
                        dic["dead_code"], dic["attr_init"]])

    elif type_csv == "1_row":
        writer.writerow([dic["url"], dic["mastery"],
                        dic["abstraction"], dic["Parallelism"],
                        dic["logic"], dic["sync"],
                        dic["flow_control"], dic["user_inter"], dic["data_rep"],
                        dic["dup_scripts"],dic["sprite_naming"],
                        dic["dead_code"], dic["attr_init"]])

    for key, value in dictionary.items():
        total = 0
        flag = False
        try:
            if value[0] == "Error analyzing project":
                if type_csv == "2_row":
                    row1 = key.split(",")[0]
                    row2 = key.split(",")[1]
                    row2 = row2.split("\n")[0]
                    writer.writerow([row1, row2, dic["error"]])
                elif type_csv == "1_row":
                    row1 = key.split(",")[0]
                    writer.writerow([row1,dic["error"]])
        except:
            total = 0
            row1 = key.split(",")[0]
            if type_csv == "2_row":
                row2 = key.split(",")[1]
                row2 = row2.split("\n")[0]

            for key, subvalue in value.items():
                if key == "duplicateScript":
                    for key, sub2value in subvalue.items():
                        if key == "number":
                            row11 = sub2value
                if key == "spriteNaming":
                    for key, sub2value in subvalue.items():
                        if key == "number":
                            row12 = sub2value
                if key == "deadCode":
                    for key, sub2value in subvalue.items():
                        if key == "number":
                            row13 = sub2value
                if key == "initialization":
                    for key, sub2value in subvalue.items():
                        if key == "number":
                            row14 = sub2value

            for key, value in value.items():
                if key == "mastery":
                    for key, subvalue in value.items():
                        if key!="maxi" and key!="points":
                            if key == dic["Parallelism"]:
                                row5 = subvalue
                            elif key == dic["abstraction"]:
                                row4 = subvalue
                            elif key == dic["logic"]:
                                row6 = subvalue
                            elif key == dic["sync"]:
                                row7 = subvalue
                            elif key == dic["flow_control"]:
                                row8 = subvalue
                            elif key == dic["user_inter"]:
                                row9 = subvalue
                            elif key == dic["data_rep"]:
                                row10 = subvalue
                            total = total + subvalue
                    row3 = total
            if type_csv == "2_row":
                writer.writerow([row1,row2,row3,row4,row5,row6,row7,row8,
                            row9,row10,row11,row12,row13,row14])
            elif type_csv == "1_row":
                writer.writerow([row1,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
    return csv_data


def coder_hash(request):
    """Method for to sign up users in the platform"""
    if request.method == "POST":
        form = CoderHashForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/coder_hash')
    elif request.method == 'GET':
        return render(request, 'coder/coder-hash.html')


def sign_up_coder(request):
    """Method which allow to sign up coders"""


    flagCoder = 1
    flagHash = 0
    flagName = 0
    flagEmail = 0
    flagForm = 0
    flagWrongEmail = 0
    flagWrongPassword = 0
    if request.method == 'POST':
        form = CoderForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            email = form.cleaned_data['email']
            email_confirm = form.cleaned_data['email_confirm']
            birthmonth = form.cleaned_data['birthmonth']
            birthyear = form.cleaned_data['birthyear']
            gender = form.cleaned_data['gender']
            #gender_other = form.cleaned_data['gender_other']
            country = form.cleaned_data['country']
            
            #Checking the validity into the dbdata contents.
            #They will be refused if they already exist.
            #If they exist an error message will be shown.
            if User.objects.filter(username = username):
                #This name already exists
                flagName = 1
                #return render_to_response("error/sign-up.html",
                #                          {'flagName':flagName,
                #                           'flagEmail':flagEmail,
                #                           'flagHash':flagHash,
                #                           'flagForm':flagForm,
                #                           'flagCoder':flagCoder},
                #                          context_instance = RC(request))
                return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                              'flagEmail':flagEmail,
                                                              'flagHash':flagHash,
                                                              'flagForm':flagForm,
                                                              'flagCoder':flagCoder})

            elif User.objects.filter(email = email):
                #This email already exists
                flagEmail = 1
                #return render_to_response("error/sign-up.html",
                #                        {'flagName':flagName,
                #                        'flagEmail':flagEmail,
                #                        'flagHash':flagHash,
                #                        'flagForm':flagForm,
                #                        'flagCoder':flagCoder},
                #                        context_instance = RC(request))
                return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                              'flagEmail':flagEmail,
                                                              'flagHash':flagHash,
                                                              'flagForm':flagForm,
                                                              'flagCoder':flagCoder})
            elif (email != email_confirm):
                flagWrongEmail = 1
                #return render_to_response("error/sign-up.html",
                #        {'flagName':flagName,
                #        'flagEmail':flagEmail,
                #        'flagHash':flagHash,
                #        'flagForm':flagForm,
                #        'flagCoder':flagCoder,
                #        'flagWrongEmail': flagWrongEmail},
                #        context_instance = RC(request))
                return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                              'flagEmail':flagEmail,
                                                              'flagHash':flagHash,
                                                              'flagForm':flagForm,
                                                              'flagCoder':flagCoder,
                                                              'flagWrongEmail': flagWrongEmail})

            elif (password != password_confirm):
                flagWrongPassword = 1
                #return render_to_response("error/sign-up.html",
                #        {'flagName':flagName,
                #        'flagEmail':flagEmail,
                #        'flagHash':flagHash,
                #        'flagForm':flagForm,
                #        'flagCoder':flagCoder,
                #        'flagWrongPassword':flagWrongPassword},
                #        context_instance = RC(request))
                return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                              'flagEmail':flagEmail,
                                                              'flagHash':flagHash,
                                                              'flagForm':flagForm,
                                                              'flagCoder':flagCoder,
                                                              'flagWrongPassword': flagWrongPassword})

            else:
                coder = Coder.objects.create_user(username = username,
                                    email=email, password=password,
                                    birthmonth = birthmonth, 
                                    birthyear = birthyear,
                                    gender = gender,
                                    #gender_other = gender_other,
                                    country = country)

                coder = authenticate(username=username, password=password)
                user = Coder.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token=default_token_generator.make_token(user)
                """
                c = {
                        'email':email,
                        'uid':uid,
                        'token':token}

                body = render_to_string("coder/email-sign-up.html",c)
                subject = "Welcome to Dr. Scratch!"
                sender ="no-reply@drscratch.org"
                to = [email]
                email = EmailMessage(subject,body,sender,to)
                email.send()
                """
                login(request, coder)
                return HttpResponseRedirect('/coder/' + coder.username)

        else:
            flagForm = 1
            #return render_to_response("error/sign-up.html",
            #      {'flagName':flagName,
            #       'flagEmail':flagEmail,
            #       'flagHash':flagHash,
            #       'flagForm':flagForm},
            #      context_instance = RC(request))
            return render(request, 'error/sign-up.html', {'flagName':flagName,
                                                          'flagEmail':flagEmail,
                                                          'flagHash':flagHash,
                                                          'flagForm':flagForm})

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/coder/' + request.user.username)
        else:
            #return render_to_response("main/main.html", 
            #        context_instance = RC(request))
            return render(request, 'main/main.html')



#_________________________ TO SHOW USER'S DASHBOARD ___________#

def coder(request, name):
    """Shows the main page of coders"""


    if (request.method == 'GET') or (request.method == 'POST'):
        if request.user.is_authenticated:
            username = request.user.username
            
            if username == name:
                
                if Coder.objects.filter(username = username):
                    user = Coder.objects.get(username=username)
                    img = user.img
                    dic={'username':username,
                    "img":str(img)}

                    #return render_to_response("coder/main.html",
                    #                            dic,
                    #                            context_instance = RC(request))
                    return render(request, 'coder/main.html', dic)
                else:
                    logout(request)
                    return HttpResponseRedirect("/")

    else:
        return HttpResponseRedirect("/")


def login_coder(request):
    """Log in app to user"""


    if request.method == 'POST':
        flagCoder = 0
        flag = False
        form = LoginOrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            coder = authenticate(username=username, password=password)
            if coder is not None:
                if coder.is_active:
                    login(request, coder)
                    return HttpResponseRedirect('/coder/' + coder.username)

            else:
                flag = True
                flagCoder = 1
                #return render_to_response("sign-password/user-doesnt-exist.html",
                #                            {'flag': flag,
                #                             'flagCoder': flagCoder},
                #                            context_instance=RC(request))
                return render(request, 'sign-password/user-doesnt-exist.html', {'flag': flag, 'flagCoder': flagCoder})
    else:
        return HttpResponseRedirect("/")


def logout_coder(request):
    logout(request)
    return HttpResponseRedirect('/')


def change_pwd(request):
    """Change user's password"""

    if request.method == 'POST':
        recipient = request.POST['email']
        page = identify_user_type(request)
        try:
            if Organization.objects.filter(email=recipient):
                user = Organization.objects.get(email=recipient)
            elif Coder.objects.filter(email=recipient):
                user = Coder.objects.get(email=recipient)
        except:
            #return render_to_response("sign-password/user-doesnt-exist.html",
            #                               context_instance=RC(request))
            return render(request, 'sign-password/user-doesnt-exist.html')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token=default_token_generator.make_token(user)

        
        c = {
                'email':recipient,
                'uid':uid,
                'token':token,
                'id':user.username}


        body = render_to_string("sign-password/email-reset-pwd.html",c)
        subject = "Dr. Scratch: Did you forget your password?"
        sender ="no-reply@drscratch.org"
        to = [recipient]
        email = EmailMessage(subject,body,sender,to)
        email.send()
        #return render_to_response("sign-password/email-sended.html",
        #                        context_instance=RC(request))
        return render(request, 'sign-password/email-sended.html')

    else:

        page = identify_user_type(request)
        #return render_to_response("sign-password/password.html", 
        #                        context_instance=RC(request))
        return render(request, 'sign-password/password.html')



def reset_password_confirm(request,uidb64=None,token=None,*arg,**kwargs):
    """Confirm change password"""


    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64)
        if Organization.objects.filter(pk=uid):
            user = Organization._default_manager.get(pk=uid)
            page = 'organization'
        elif Coder.objects.filter(pk=uid):
            user = Coder._default_manager.get(pk=uid)
            page = 'coder'
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if request.method == "POST":
        flag_error = False
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.POST['password']
            new_confirm = request.POST['confirm']
            if new_password == "":
                return render(request, 'sign-password/new-password.html')

            elif new_password == new_confirm:
                user.set_password(new_password)
                user.save()
                logout(request)
                user = authenticate(username=user.username, 
                                    password=new_password)
                login(request, user)
                return HttpResponseRedirect('/' + page + '/' + user.username)
                return render(request, page + '/main.html')

            else:
                flag_error = True
                return render(request, 'sign-password/new-password.html',
                                    {'flag_error':flag_error})

    else:
         if user is not None and default_token_generator.check_token(user, token):
             return render(request, 'sign-password/new-password.html')
         else:
             return render(request, page + '/main.html')



#_________________________________ DISCUSS ___________________________________#
def discuss(request):
    """Forum to get feedback"""


    comments = dict()
    form = DiscussForm()
    if request.user.is_authenticated:
        user = request.user.username
    else:
        user = ""
    if request.method == "POST":

        form = DiscussForm(request.POST)
        if form.is_valid():
            nick = user
            date = timezone.now()
            comment = form.cleaned_data["comment"]
            new_comment = Discuss(nick = nick,
                                date = date,
                                comment=comment)
            new_comment.save()
        else:
            comments["form"] = form

    data = Discuss.objects.all().order_by("-date")
    lower = 0
    upper = 10
    list_comments = {}
   
    if len(data) > 10:
        for n in range((len(data)/10)+1):
            list_comments[str(n)]= data[lower:upper-1]
            lower = upper
            upper = upper + 10
    else:
        list_comments[0] = data


    comments["comments"] = list_comments

    return render(request, 'discuss.html', comments)


def error404(request):
    """Return own 404 page"""
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def date_range(start, end):
    r = (end+timedelta(days=1)-start).days
    return [start+timedelta(days=i) for i in range(r)]


def error500(request):
    """Return own 500 page"""
    response = render(request, '500.html', {})
    return response


def statistics(request):
    start = date(2015, 8, 1)
    end = datetime.today()
    year = end.year
    month = end.month
    day = end.day
    end = date(year, month, day)
    date_list = date_range(start, end)

    my_dates = []

    for n in date_list:
        my_dates.append(n.strftime("%d/%m")) #used for x axis in

    obj = Stats.objects.order_by("-id")[0]
    data = {
        "date": my_dates,
        "dailyRate": obj.daily_score,
        "levels": {
            "basic": obj.basic,
            "development": obj.development,
            "master": obj.master
        },
        "totalProjects": obj.daily_projects,
        "skillRate": {
            "Parallelism": obj.parallelization,
            "abstraction": obj.abstraction,
            "logic": obj.logic,
            "synchronization": obj.synchronization,
            "flowControl": obj.flow_control,
            "userInteractivity": obj.userInteractivity,
            "dataRepresentation": obj.dataRepresentation
        },
        "codeSmellRate": {
            "deadCode": obj.deadCode,
            "duplicateScript": obj.duplicateScript,
            "spriteNaming": obj.spriteNaming,
            "initialization": obj.initialization
        }
    }

    #Show general statistics page of Dr. Scratch: www.drscratch.org/statistics
    #return render_to_response("main/statistics.html",
    #                                data, context_instance=RC(request))
    return render(request, 'main/statistics.html', data)




"""
def proc_initialization(lines, filename):


    dic = {}
    lLines = lines.split('.sb2')
    d = ast.literal_eval(lLines[1])
    keys = d.keys()
    values = d.values()
    items = d.items()
    number = 0

    for keys, values in items:
        list = []
        attribute = ""
        internalkeys = values.keys()
        internalvalues = values.values()
        internalitems = values.items()
        flag = False
        counterFlag = False
        i = 0
        for internalkeys, internalvalues in internalitems:
            if internalvalues == 1:
                counterFlag = True
                for value in list:
                    if internalvalues == value:
                        flag = True
                if not flag:
                    list.append(internalkeys)
                    if len(list) < 2:
                        attribute = str(internalkeys)
                    else:
                        attribute = attribute + ", " + str(internalkeys)
        if counterFlag:
            number = number + 1
        d[keys] = attribute
    dic["initialization"] = d
    dic["initialization"]["number"] = number

    #Save in DB
    filename.initialization = number
    filename.save()

    return dic

"""


###################################
#
#       API PETITIONS
#
#
###################################


def get_analysis_d(request, skill_points=None):
    if request.method == 'POST':
        url = request.path.split('/')[-1]
        if url != '':
            numbers = base32_to_str(url)
        else:
            numbers = ''
        skill_rubric = generate_rubric(numbers)
        
        
        path_original_project = request.session.get('current_project_path', None)
        
        if path_original_project != None:
            json_scratch_original = load_json_project(path_original_project)
        

        d = build_dictionary_with_automatic_analysis(request, skill_rubric) 
        
        path_compare_project = request.session.get('current_project_path', None)
        
        if path_compare_project != None:
            json_scratch_compare = load_json_project(path_compare_project)
            

        dict_scratch_golfing = ScratchGolfing(json_scratch_original, json_scratch_compare).finalize()
        dict_scratch_golfing = dict_scratch_golfing['result']['scratch_golfing']
        print("Estando en views")
        print(dict_scratch_golfing)
        #dict_comparsion_mode = ComparsionMode(json_scratch_original, json_scratch_compare).finalize()

        
        user = str(identify_user_type(request))
        
        dict_mastery = d[0]['mastery_vanilla']
        dict_dups = d[0]['duplicateScript']
        dict_dead_code = d[0]['deadCode']
        dict_sprite = d[0]['spriteNaming']
        dict_backdrop = d[0]['backdropNaming']
        
        #keys_to_remove = [key for value, key in dict_dups.items() if value == {...}]
        
        #for key in keys_to_remove:
        del dict_dups['duplicateScript']
        del dict_dead_code['deadCode']
        del dict_sprite['spriteNaming']
        del dict_backdrop['backdropNaming']
            
        
        context = {
            'mastery': dict_mastery,
            'duplicateScript': dict_dups,
            'deadCode': dict_dead_code,
            'spriteNaming': dict_sprite,
            'backdropNaming': dict_backdrop,
            'scratchGolfing': dict_scratch_golfing,
        }
        
    return JsonResponse(context)




