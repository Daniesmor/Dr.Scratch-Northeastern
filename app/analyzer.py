from datetime import datetime
import json
import os
import shutil
import traceback
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import uuid
from venv import logger
from zipfile import BadZipfile, ZipFile
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponseRedirect, HttpResponse
from app.exception import DrScratchException
from app.forms import UrlForm
from app.hairball3.backdropNaming import BackdropNaming
from app.hairball3.deadCode import DeadCode
from app.hairball3.duplicateScripts import DuplicateScripts
from app.hairball3.mastery import Mastery
from app.hairball3.refactor import RefactorDuplicate
from app.hairball3.spriteNaming import SpriteNaming
from app.hairball3.scratchGolfing import ScratchGolfing
from app.hairball3.block_sprite_usage import Block_Sprite_Usage
from app.models import Coder, File, Organization
from app.scratchclient import ScratchSession
from app.recomender import RecomenderSystem
import app.consts_drscratch as consts
from .translation import translate
from memory_profiler import profile
from app.hairball3.babiaInfo import Babia

def save_analysis_in_file_db(request, zip_filename):
    filename = zip_filename.decode('utf-8')
    now = datetime.now()
    method = "project"
    if request.POST['batch_id']:
        batch_id = request.POST['batch_id']
    else:
        batch_id = None
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None

    if Organization.objects.filter(username=username):
        filename_obj = File(filename=filename,
                            organization=username,
                            method=method, batch_id=batch_id, time=now,
                            score=0, vanilla_metrics={}, extended_metrics={},
                            spriteNaming=0, backdropNaming=0, initialization=0,
                            deadCode=0, duplicateScript=0)
    elif Coder.objects.filter(username=username):
        filename_obj = File(filename=filename,
                            coder=username,
                            method=method, batch_id=batch_id, time=now,
                            score=0, vanilla_metrics={}, extended_metrics={},
                            spriteNaming=0, backdropNaming=0, initialization=0,
                            deadCode=0, duplicateScript=0)
    else:
        filename_obj = File(filename=filename,
                            method=method, batch_id=batch_id, time=now,
                            score=0, vanilla_metrics={}, extended_metrics={},
                            spriteNaming=0, backdropNaming=0, initialization=0,
                            deadCode=0, duplicateScript=0)

    filename_obj.save()
    return filename_obj


def _make_compare(request, skill_points: dict):
    """
    Make comparison of two projects
    """
    counter = 0
    d = {}
    path = {}
    json = {}
    if request.method == "POST":
        if "_urls" in request.POST:
            for url in request.POST.getlist('urlProject'):
                print("Url:", url)
                project = check_project(counter)
                d[project] = analysis_by_url(request, url, skill_points)
                path[project] = request.session.get('current_project_path')
                counter += 1
        elif "_uploads" in request.POST:
            for upload in request.FILES.getlist('zipFile'):
                project = check_project(counter)
                print("Upload:", upload)
                d[project] = analysis_by_upload(request, skill_points, upload)
                path[project] = request.session.get('current_project_path')
                counter += 1
        elif "_mix" in request.POST:
            project = check_project(counter)
            base_type = request.POST.get('baseProjectType')
            if base_type == "urlProject":
                url = request.POST.getlist('urlProject')[0]
                d[project] = analysis_by_url(request, url, skill_points)
                path[project] = request.session.get('current_project_path')
                counter += 1
                upload = request.FILES.get('zipFile')
                project = check_project(counter)
                d[project] = analysis_by_upload(request, skill_points, upload)
                path[project] = request.session.get('current_project_path')
            else:
                upload = request.FILES.get('zipFile')
                d[project] = analysis_by_upload(request, skill_points, upload)
                path[project] = request.session.get('current_project_path')
                counter += 1
                project = check_project(counter)
                url = request.POST.getlist('urlProject')[1]
                d[project] = analysis_by_url(request, url, skill_points)
                path[project] = request.session.get('current_project_path')

        for key, value in path.items():
            print(key, value)
            json[key] = load_json_project(value)
        dict_scratch_golfing = ScratchGolfing(json.get('Original'), json.get('New')).finalize()
        dict_scratch_golfing = dict_scratch_golfing['result']['scratch_golfing']
        d['Compare'] = dict_scratch_golfing
        check_same_functionality(request, d)

        return d
    else:
        return HttpResponseRedirect('/')


def check_project(counter):
    if counter == 0:
        project = "Original"
    else:
        project = "New"
    return project


def check_same_functionality(request, d):
    """
    Check if the projects have the same functionality
    """
    same_functionality = request.POST.get('same_functionality') == "True"
    print("Same functionality:", same_functionality)
    if same_functionality:
        d['Compare'].update({
            'same_functionality': True
        })
    else:
        d['Compare'].update({
            'same_functionality': False
        })


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


def generate_uniqueid_for_saving(id_project):
    date_now = datetime.now()
    date_now_string = date_now.strftime("%Y_%m_%d_%H_%M_%S_%f")
    return id_project + "_" + date_now_string


def save_projectsb3(path_file_temporary, id_project):
    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"

    unique_id = generate_uniqueid_for_saving(id_project)
    unique_file_name_for_saving = dir_zips + unique_id + ".sb2"

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


def download_scratch_project_from_servers(path_project, id_project):
    scratch_project_inf = ScratchSession().get_project(id_project)
    url_json_scratch = "{}/{}?token={}".format(consts.URL_SCRATCH_SERVER, id_project, scratch_project_inf.project_token)
    print("URLLLLL -------------------")
    print(url_json_scratch)
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
        print("PATH JSON TEMPORARY FILE in dspfs---------------------------------------------------------")
        print(json_data)
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


def send_request_getsb3(id_project, username, method, batch=None):
    """
    Send request to getsb3 app
    """

    file_url = '{}{}'.format(id_project, '.sb3')

    path_project = os.path.dirname(os.path.dirname(__file__))
    path_json_file_temporary = download_scratch_project_from_servers(path_project, id_project)

    print("PATH JSON TEMPORARY FILE ---------------------------------------------------------")
    print(path_json_file_temporary)

    now = datetime.now()

    if Organization.objects.filter(username=username):
        file_obj = File(filename=file_url,
                        organization=username,
                        method=method, batch_id=None, time=now,
                        score=0, vanilla_metrics={}, extended_metrics={},
                        spriteNaming=0, backdropNaming=0, initialization=0,
                        deadCode=0, duplicateScript=0)
    elif Coder.objects.filter(username=username):
        file_obj = File(filename=file_url,
                        coder=username,
                        method=method, batch_id=None, time=now,
                        score=0, vanilla_metrics={}, extended_metrics={},
                        spriteNaming=0, backdropNaming=0, initialization=0,
                        deadCode=0, duplicateScript=0)
    else:
        file_obj = File(filename=file_url,
                        method=method, batch_id=None, time=now,
                        score=0, vanilla_metrics={}, extended_metrics={},
                        spriteNaming=0, backdropNaming=0, initialization=0,
                        deadCode=0, duplicateScript=0)

    file_obj.save()

    write_activity_in_logfile(file_obj)
    path_scratch_project_sb3, ext_type_project = save_projectsb3(path_json_file_temporary, id_project)

    return path_scratch_project_sb3, file_obj, ext_type_project



def generator_dic(request, id_project, skill_points: dict) -> dict:
    """
    Return a dictionary with static analysis and errors
    """

    try:
        username = None
        path_project, file_obj, ext_type_project = send_request_getsb3(id_project, username, method="url")
        try:
            request.session['current_project_path'] = path_project
        except AttributeError:
            pass
        except TypeError:
            pass
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


# @profile
def load_json_project(path_projectsb3):
    try:
        return json.loads(ZipFile(path_projectsb3, "r").open("project.json").read())
    except BadZipfile:
        print('Bad zipfile')


def proc_refactored_code(refactor):
    dict_refactor = {}
    dict_refactor["refactor"] = dict_refactor
    dict_refactor["refactor"]["refactor_list"] = refactor

    return dict_refactor


def proc_block_sprite_usage(result_block_sprite_usage, filename):
    dict_block_sprite_usage = {}
    dict_block_sprite_usage["block_sprite_usage"] = dict_block_sprite_usage
    dict_block_sprite_usage["block_sprite_usage"] = result_block_sprite_usage

    return dict_block_sprite_usage


def proc_dead_code(dict_dead_code, filename):
    dict_dc = {}
    dict_dc["deadCode"] = {}
    dict_dc["deadCode"]["number"] = dict_dead_code['result']['total_dead_code_scripts']
    # dict_dc["deadCode"]['plugins']["babia"] = dict_dead_code['babia']

    dict_dc["deadCode"]["scripts"] = {}
    for dict_sprite_dead_code_blocks in dict_dead_code['result']['list_dead_code_scripts']:
        for sprite_name, list_blocks in dict_sprite_dead_code_blocks.items():
            dict_dc["deadCode"]["scripts"][sprite_name] = list_blocks

    filename.deadCode = dict_dead_code['result']['total_dead_code_scripts']
    filename.save()

    return dict_dc


def proc_recomender(dict_recom):
    recomender = {
        'recomenderSystem': {
            'message': "Congrat's you don't have any bad smell at the moment.",
        }
    }
    if (dict_recom["duplicatedScripts"] != None):
        recomender = {
            'recomenderSystem': dict_recom["duplicatedScripts"],
        }
        RecomenderSystem.curr_type = dict_recom["duplicatedScripts"]['type']
        return recomender
    if (dict_recom["deadCode"] != None):
        recomender = {
            'recomenderSystem': dict_recom["deadCode"],
        }
        RecomenderSystem.curr_type = dict_recom["deadCode"]['type']
        return recomender
    if (dict_recom["spriteNaming"] != None):
        recomender = {
            'recomenderSystem': dict_recom["spriteNaming"],
        }
        RecomenderSystem.curr_type = dict_recom["spriteNaming"]['type']
        return recomender
    if (dict_recom["backdropNaming"] != None):
        recomender = {
            'recomenderSystem': dict_recom["backdropNaming"],
        }
        RecomenderSystem.curr_type = dict_recom["backdropNaming"]['type']
        return recomender
    return recomender


def proc_urls(request, dict_mastery, file_obj):
    dict_urls = {}
    mode = request.POST.get('dashboard_mode', 'Default')
    non_personalized = ['Default', 'Comparison', 'Recommender']

    if mode not in non_personalized:
        dict_extended = dict_mastery['extended'].copy()
        dict_vanilla = dict_mastery['vanilla'].copy()
        dict_urls["url_extended"] = get_urls(dict_extended)
        dict_urls["url_vanilla"] = get_urls(dict_vanilla)
    elif mode == 'Personalized':
        dict_personal = dict_mastery['personalized'].copy()
        print(dict_personal)
        dict_urls["url_personal"] = get_urls(dict_personal)
    return dict_urls


def get_urls(dict_mastery):
    list_urls = []
    for key in dict_mastery.keys():
        if key != 'total_points' and key != 'competence' and key != 'max_points' and key != 'average_points':
            list_urls.append(key)
    return list_urls


def proc_mastery(request, dict_mastery, file_obj):
    dic = {}
    mode = request.POST.get('dashboard_mode', 'Default')
    non_personalized = ['Default', 'Comparison', 'Recommender']
    if mode in non_personalized:
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
    elif mode == 'Personalized':
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
    file_obj.vanilla_metrics = dict
    if mode != 'Vanilla':
        file_obj.extended_metrics = dict
    file_obj.save()


def proc_duplicate_script(dict_result, file_obj) -> dict:
    dict_ds = {}
    dict_ds["duplicateScript"] = {}
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

    dic['spriteNaming'] = {}
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
    dic['backdropNaming'] = {}
    dic['backdropNaming']['number'] = int(number)
    dic['backdropNaming']['backdrop'] = lfinal

    file_obj.backdropNaming = number
    file_obj.save()

    return dic


import sys


# @profile
def analyze_project(request, path_projectsb3, file_obj, ext_type_project, skill_points: dict):
    dict_analysis = {}

    dashboard = request.POST.get('dashboard_mode', 'Default')
    curr_type = request.POST.get('curr_type', '')
    batch_id = request.POST.get('batch_id', '')

    if not os.path.exists(path_projectsb3):
        logger.error(f'Project file not found: {path_projectsb3}')
        return {'Error': 'file_not_found'} # Explicit return on file not found

    try:
        json_scratch_project = load_json_project(path_projectsb3)
        if json_scratch_project is None:
             logger.error(f'Failed to load JSON from project file: {path_projectsb3}')
             return {'Error': 'invalid_project_file'} # Explicit return on invalid JSON

        dict_mastery = Mastery(path_projectsb3, json_scratch_project, skill_points, dashboard).finalize()
        dict_duplicate_script = DuplicateScripts(path_projectsb3, json_scratch_project).finalize()
        dict_dead_code = DeadCode(path_projectsb3, json_scratch_project).finalize()
        dict_babia = Babia(path_projectsb3, json_scratch_project).finalize()
        result_sprite_naming = SpriteNaming(path_projectsb3, json_scratch_project).finalize()
        result_backdrop_naming = BackdropNaming(path_projectsb3, json_scratch_project).finalize()

        refactored_code = None
        if not batch_id:
            try:
                refactored_code = RefactorDuplicate(json_scratch_project, dict_duplicate_script).refactor_duplicates()
            except Exception as e:
                 logger.warning(f"Error during RefactorDuplicate: {e}")


        del json_scratch_project

        # RECOMENDER SECTION
        if (dashboard == 'Recommender'):
            dict_recom = {}
            recomender = RecomenderSystem(curr_type)
            dict_recom["deadCode"] = recomender.recomender_deadcode(dict_dead_code)
            dict_recom["spriteNaming"] = recomender.recomender_sprite(result_sprite_naming)
            dict_recom["backdropNaming"] = recomender.recomender_backdrop(result_backdrop_naming)
            dict_recom["duplicatedScripts"] = recomender.recomender_duplicatedScripts(dict_duplicate_script,
                                                                                      refactored_code)
            print("PROBANMD")
            print(proc_recomender(dict_recom))
            dict_analysis.update(proc_recomender(dict_recom))

        dict_analysis.update(proc_mastery(request, dict_mastery, file_obj))
        dict_analysis.update(proc_duplicate_script(dict_duplicate_script, file_obj))
        dict_analysis.update(proc_dead_code(dict_dead_code, file_obj))
        dict_analysis['babia'] = dict_babia
        dict_analysis.update(proc_sprite_naming(result_sprite_naming, file_obj))
        dict_analysis.update(proc_backdrop_naming(result_backdrop_naming, file_obj))

        if not batch_id:
             if isinstance(refactored_code, dict):
                dict_analysis.update(proc_refactored_code(refactored_code))
             else:
                logger.warning("refactored_code is not a dictionary, skipping update.")

        # Clean up temporary analysis results if they are large and not needed later
        # dict_duplicate_script = None
        # dict_dead_code = None
        # result_sprite_naming = None
        # result_backdrop_naming = None


    except Exception as e:
        logger.error(f'Error during project analysis: {e}')
        traceback.print_exc()
        return {'Error': 'analysis_failed', 'details': str(e)} # Explicit return on analysis failure

    # Explicit return for the successful analysis path
    return dict_analysis


# @profile
def analysis_by_upload(request, skill_points: dict, upload):
    """
    Upload file from form POST for unregistered users
    """
    zip_filename = upload.name.encode('utf-8')
    filename_obj = save_analysis_in_file_db(request, zip_filename)
    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    project_name = str(uuid.uuid4())
    unique_id = '{}_{}{}'.format(project_name, datetime.now().strftime("%Y_%m_%d_%H_%M_%S_"),
                                 datetime.now().microsecond)
    zip_filename = zip_filename.decode('utf-8')
    version = check_version(zip_filename)
    file_saved = dir_zips + unique_id + ".sb2"
    if version == "1.4":
        file_saved = dir_zips + unique_id + ".sb"
    elif version == "2.0":
        file_saved = dir_zips + unique_id + ".sb2"
    else:
        file_saved = dir_zips + unique_id + ".sb3"

    # Create log

    # Save file in server
    file_name = os.path.join("uploads", file_saved)
    request.session['current_project_path'] = file_name
    with open(file_name, 'wb+') as destination:
        for chunk in upload.chunks():
            destination.write(chunk)
    try:
        ext_type_project = None
        analyze_project(request, file_name, filename_obj, ext_type_project, skill_points)
    except Exception:
        traceback.print_exc()

    del request.session['current_project_path']
    del filename_obj

    # Delete the uploaded file after processing if necessary
    if os.path.exists(file_name):
        os.remove(file_name)


def analysis_by_url(request, url, skill_points: dict):
    """
    Make the automatic analysis by URL
    """

    id_project = return_scratch_project_identifier(url)
    if id_project == "error":
        return {'Error': 'id_error'}
    else:
        dic = generator_dic(request, id_project, skill_points)
        dic.update({
            'url': url,
            'filename': url,
            'dashboard_mode': request.POST.get('dashboard_mode', 'Default'),
            'multiproject': False
        })
        return dic