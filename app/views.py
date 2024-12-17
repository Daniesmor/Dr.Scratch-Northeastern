#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import os
import ast
import json
import uuid
import requests
import tempfile
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
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from .models import BatchCSV
from app import org
from django.http import JsonResponse
from app.forms import UrlForm, OrganizationForm, OrganizationHashForm, LoginOrganizationForm, CoderForm, DiscussForm
from app.models import File, CSVs, Organization, OrganizationHash, Coder, Discuss, Stats, BatchCSV
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from zipfile import ZipFile, BadZipfile
import pickle
import shutil
import unicodedata
import csv
from datetime import datetime, timedelta, date
from requests import Request
import traceback
import re
import app.consts_drscratch as consts
from django.utils.translation import get_language
from types import SimpleNamespace
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
from app.hairball3.block_sprite_usage import Block_Sprite_Usage

import logging
import coloredlogs


# Celery imports
from .tasks import init_batch

# Analyzer imports
from .analyzer import analyze_project, generator_dic, return_scratch_project_identifier, send_request_getsb3, _make_compare, analysis_by_upload, analysis_by_url, analyze_babia_project
from .batch import skills_translation

# Recomender System imports
from .recomender import RecomenderSystem

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

def calc_eta(num_projects: int) -> str:
    """
    Calc mean of each url timestamp analysis, and multyply
    to the current number of projects.
    """
    last_ten = BatchCSV.objects.all().order_by('-date')[:10]

    anal_time = sum(batch.task_time/batch.num_projects for batch in last_ten)/10
    mean_tm = anal_time * num_projects
    eta_h = mean_tm // 3600
    eta_m = (mean_tm % 3600) // 60
    eta_s = (mean_tm % 60)

    eta_format = f'{int(eta_h)}h: {int(eta_m)}min: {round(eta_s,2)}s'
    return eta_format
 
def show_dashboard(request, skill_points=None):
    
    if request.method == 'POST':
        url = request.path.split('/')[-1]
        if url != '':
            numbers = base32_to_str(url)
        else:
            numbers = ''
        print(f"Mi url {url}")
        skill_rubric = generate_rubric(numbers)
        user = str(identify_user_type(request)) 
        print("Mode:", request.POST)
        d = build_dictionary_with_automatic_analysis(request, skill_rubric)
        print("Context Dictionary:")
        print(d)
        print("Skill rubric")
        print(skill_rubric)
        d = d[0]
        if d.get('multiproject'):
            context = {
                'ETA': calc_eta(d['num_projects'])
            }
            return render(request, user + '/dashboard-bulk-landing.html', context)
        
        elif d.get('Error') != "None":
            return render(request, 'error/error.html', {'error': d.get('Error')})
        else: 
            if d.get('dashboard_mode') == 'Default':
                return render(request, user + '/dashboard-default.html', d)
            elif d.get('dashboard_mode') == 'Personalized':
                return render(request, user + '/dashboard-personal.html', d)               
            elif d.get('dashboard_mode') == 'Recommender':
                return render(request, user + '/dashboard-recommender.html', d)
            elif d.get('dashboard_mode') == 'Comparison':
                return render(request, user + '/dashboard-compare.html', d)     
    else:
        return HttpResponseRedirect('/')    

@csrf_exempt
def get_recommender(request, skill_points=None):
    if request.method == 'POST':
        url = request.POST.get('urlProject_recom')
        if url == "":
            url = request.POST.get('urlProject_recom')
        currType = request.POST.get('currType')
        print(f"Mi url: {url}")
        numbers = ''
        skill_rubric = generate_rubric(numbers)
        user = str(identify_user_type(request))
        print("Mode:", request.POST)
        d = build_dictionary_with_automatic_analysis(request, skill_rubric)
        print("-------------------- RECOMENDER -------------------------")
        print("Context Dictionary:")
        print(d)
        print("Skill rubric")
        print(skill_rubric)
        d = d.get(0)
        
        return JsonResponse(d['recomenderSystem'])        
    else:
        return HttpResponseRedirect('/')

def batch(request, csv_identifier):
    user = str(identify_user_type(request))
    csv = get_object_or_404(BatchCSV, id=csv_identifier)

    csv_filepath = csv.filepath

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
    
    context = {
        'summary': summary,
        'csv_filepath': csv_filepath
    }

    return render(request, user + '/dashboard-bulk.html', context)
    

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
            skill_rubric[skill_name] = 4 # Falta añadir Finesse           
    return skill_rubric  

def calc_num_projects(batch_path: str) -> int:
    num_projects = 0
    for root, dirs, files in os.walk(batch_path):
        for file in files:
            num_projects += 1
    return num_projects
    
def extract_batch_projects(projects_file: object) -> int:
    project_name = str(uuid.uuid4())
    unique_id = '{}_{}{}'.format(project_name, datetime.now().strftime("%Y_%m_%d_%H_%M_%S_"), datetime.now().microsecond)
    base_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_file_path = os.path.join(temp_dir, projects_file.name)

        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in projects_file.chunks():
                temp_file.write(chunk)

            temp_extraction =  os.path.join(base_dir, 'uploads', 'batch_mode', unique_id)
            with ZipFile(temp_file, 'r') as zip_ref:
                zip_ref.extractall(temp_extraction)
    return temp_extraction

def build_dictionary_with_automatic_analysis(request, skill_points: dict) -> dict:
    dict_metrics = {}
    url = None
    filename = None
    project_counter = 0

    if request.method == 'POST':
        dashboard_mode = request.POST.get('dashboard_mode', 'Default')

    if dashboard_mode == 'Comparison':
        dict_metrics = _make_compare(request, skill_points)
    else:
        if "_upload" in request.POST:
            try:
                zip_file = request.FILES['zipFile']
            except MultiValueDictKeyError:
                print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                dict_metrics[project_counter] = {'Error': 'MultiValueDict'}
                return dict_metrics
            dict_metrics[project_counter] = analysis_by_upload(request, skill_points, zip_file)
        elif '_url_recom' in request.POST:
            url = request.POST.get('urlProject_recom',)
            if url != None:
                dict_metrics[project_counter] = analysis_by_url(request, url, skill_points)
            else:
                dict_metrics[project_counter] =  {'Error': 'MultiValueDict'}
        elif '_url' in request.POST:
            form = UrlForm(request.POST)
            if form.is_valid():
                url = form.cleaned_data['urlProject']
                dict_metrics[project_counter] = analysis_by_url(request, url, skill_points)
            else:
                dict_metrics[project_counter] =  {'Error': 'MultiValueDict'}
        elif '_urls' in request.POST:
            projects_file = request.FILES['urlsFile']
            
            if projects_file.content_type.endswith('zip') == False: 
                # List of urls
                projects = projects_file.readlines()
                num_projects = len(projects)
            else:
                # Str with temp path of projects
                projects_path = extract_batch_projects(projects_file)
                num_projects = calc_num_projects(projects_path)
                projects = projects_path
    
            request_data = {
                'LANGUAGE_CODE': request.LANGUAGE_CODE,
                'POST': {
                    'urlsFile': projects,
                    'dashboard_mode': 'Default', 
                    'email': request.POST['batch-email']       
                }
            }
            init_batch.delay(request_data, skill_points) # Call to analyzer task

            dict_metrics[project_counter] = {
                'multiproject': True,
                'num_projects': num_projects
            }

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

def learn(request, category, page):
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

    page_path = f'learn/{category}/{page}.html'

    if request.user.is_authenticated:
        user = identify_user_type(request)
        username = request.user.username
        return render(request, page_path, {'flagUser': flag_user, 'user': user, 'username': username})
    else:
        return render(request, page_path)

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
        filename = request.POST["filename"]
        # Encode to make sure that cotains utf-8 chars
        filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore')
        # Decode again for manipulate the str
        filename = filename.decode('utf-8') 
        filename = clean_filename(filename)
        print("Filename: ", filename)
        level = request.POST["level"]
        print("Level: ", level)

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
##
##      API PETITIONS
##
###################################

def load_json_project(path_projectsb3):
    try:
        zip_file = ZipFile(path_projectsb3, "r")
        json_project = json.loads(zip_file.open("project.json").read())
        return json_project
    except BadZipfile:
        print('Bad zipfile')

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


###################################
##
##      BABIA PROJECTS
##
###################################


def get_babia(request):
    # TEMP DATA
    numbers = ''
    skill_rubric = generate_rubric(numbers)

    # Create a fake request instead of fill the form ______________________________________
    """
    This is a fake provisional request for testing purposes.
    """
    fake_request = SimpleNamespace()
    fake_request.method = 'POST'
    fake_request.POST = {'_url': '',
                         'urlProject': 'https://scratch.mit.edu/projects/282489021/'}
    fake_request.GET = SimpleNamespace()
    fake_request.session = SimpleNamespace()
    fake_request.LANGUAGE_CODE = get_language()
    # _____________________________________________________________________________________
    


    d = build_dictionary_with_automatic_analysis(fake_request, skill_rubric)
    babia_dict = format_babia_dict(d[0])

    context = {
        'babia_dict': json.dumps(babia_dict)
    }

    return render(request, 'babia/project_babia.html', context)


import random

def format_babia_dict(d: dict):
    global_babia = d['babia']
    deadCode_babia = d['deadCode']['scripts']

    print("Mi deadCode")
    print(deadCode_babia)
    colors = {}

    #print("deadCode babia")
    #print(deadCode_babia)


    #colors =  ["#eb4034", "#4554ff", "#03ff96"]

    data = {
        "id": "Root",
        "children": [],
    }

    for sprite_name, script_dicc in deadCode_babia.items():
        colors[sprite_name] = {}
        for script_key, script_value in script_dicc.items():
            colors[sprite_name][script_key] = '#3a85fc'
    


    for sprite_key, sprite_item in global_babia['sprites'].items():
        sprite_data = {
            "id": sprite_key,
            "children": [],
        }
        for script_key, script_value in sprite_item.items():
            """ 
            script_data = {
                "id": script_key,
                "area": 2,
                "Blocks": len(script_value.split('\n')),
                "building_color": colors[script_key],
                "script_blocks": script_value
            }
            """
            #print("-------------------------------------")
            #print(" ".join(script_value.split('\n')))
            #print("--------------------------------------")
            if script_key not in colors[sprite_key]:
                colors[sprite_key][script_key] = "#ffffff"
            
            script_data = {
                "id": script_key,
                "area": 2,
                "Blocks": len(script_value.split('\n')),
                "building_color": colors[sprite_key][script_key],
                "script_blocks": script_value
            }
            
            
            sprite_data["children"].append(script_data)
        data["children"].append(sprite_data)
    #print(data)

    

    return data


