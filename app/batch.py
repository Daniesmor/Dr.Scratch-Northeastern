

import csv
from datetime import datetime
import os
import shutil
import uuid
from zipfile import ZipFile
from .models import BatchCSV, File
import re
import json
import ast
from django.conf import settings



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
    elif request.LANGUAGE_CODE == "tr":
        dic = {
            u'Logic': 'Mantık',
            u'Parallelism': 'Paralellik',
            u'Data representation': 'Veri temsili',
            u'Synchronization': 'Senkranizasyon',
            u'User interactivity': 'Kullanıcı etkileşimi',
            u'Flow control': 'Akış kontrolü',
            u'Abstraction': 'Soyutlama',
            u'Math operators': 'Matematiksel operatörler',
            u'Motion operators': 'Hareket operatörleri'}
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

def safe_get(data, keys, default=None):
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data


def safe_get_index(data, index, default=None):
    if isinstance(data, list) and len(data) > index:
        return data[index]
    return default


def create_csv_main(request, d: dict, folder_path: str) -> str:
    csv_name = "main.csv"
    csv_filepath = os.path.join(folder_path, csv_name)
    
    mastery_fields = skills_translation(request) 
    mastery_fields = {skill_en: skill_trans for skill_trans, skill_en in mastery_fields.items()}
    mastery_fields['points'] = 'points'    

    headers = [
        'url', 'filename', 'points', 
        'Abstraction', 'Parallelism', 'Logic', 'Synchronization',
        'Flow control', 'User interactivity', 'Data representation',
        'Math operators', 'Motion operators', 'DuplicateScripts',
        'DeadCode', 'SpriteNaming', 'BackdropNaming', 
        'Error', 'dashboard_mode'
    ]

    vanilla_headers = [
        'Van points','Van Abstraction','Van Parallelism', 'Van Logic', 
        'Van Synchronization', 'Van Flow control', 'Van User interactivity',
        'Van Data representation'
    ]

    aditional = [
        'tot_blocks'
    ]

    global_headers = headers + vanilla_headers + aditional

    with open(csv_filepath, 'w', newline='') as csv_file:
        writer_csv = csv.DictWriter(csv_file, fieldnames=global_headers)
        writer_csv.writeheader()

        for project in d:
            row_to_write = {}
            try:
                tot_blocks = safe_get(d[project], ['block_sprite_usage', 'result', 'total_blocks'], default=None)
                row_to_write['tot_blocks'] = tot_blocks if tot_blocks is not None else 'None'
            except TypeError:
                row_to_write['tot_blocks'] = 'None'

            for clave in headers:
                if clave in d[project]:
                    val = d[project].get(clave, '')
                    if clave == "filename":
                        val = re.sub(r"[\;\"\,\n\r]", "", val)
                    row_to_write[clave] = val
                    if clave == 'points':
                        row_to_write[f"Van {clave}"] = safe_get_index(val, 1, default='')
                elif clave in mastery_fields.keys():
                    clave_trans = mastery_fields[clave]
                    try:
                        mastery_list = safe_get(d[project], ['mastery', clave_trans], default=[])
                        if isinstance(mastery_list, list) and mastery_list:
                            if isinstance(mastery_list[0], list):
                                row_to_write[clave] = f'{mastery_list[0][0]}/{mastery_list[0][1]}'
                            else:
                                row_to_write[clave] = mastery_list[0]
                        mastery_list_van = safe_get(d[project], ['mastery_vanilla', clave_trans], default=[])
                        if isinstance(mastery_list_van, list) and mastery_list_van:
                            if isinstance(mastery_list_van[0], list):
                                row_to_write[f"Van {clave}"] = f'{mastery_list_van[0][0]}/{mastery_list_van[0][1]}'
                            else:
                                row_to_write[f"Van {clave}"] = mastery_list_van[0]
                    except KeyError:
                        row_to_write[clave] = 'Error'
                else:
                    row_to_write[clave] = ''
            writer_csv.writerow(row_to_write)

    return csv_filepath


def create_csv_dups(d: dict, folder_path: str):
    csv_name = "duplicateScript.csv"
    csv_filepath = os.path.join(folder_path, csv_name)
    
    # headers list
    headers = ['url', 'filename', 'number']

    try:
        max_dup_scripts = 0
        # create headers
        for project in d.values():
            duplicate_scripts = project.get('duplicateScript', {}).get('csv_format', [])

            scripts_num = sum(len(script_list) for script_list in duplicate_scripts)
            max_dup_scripts = scripts_num if max_dup_scripts < scripts_num else max_dup_scripts
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
                    'number': project_data.get('duplicateScript', {}).get('number', ''),
                }
                duplicate_scripts = project_data.get('duplicateScript', {}).get('csv_format', [])
                if duplicate_scripts:
                    script_number = 0
                    for script_list in duplicate_scripts:
                        for script in script_list:
                            script_number += 1
                            row_to_write[f'duplicateScript_{script_number}'] = script
                else:
                    row_to_write.update({f'duplicateScript_{i}': 'N/A' for i in range(1, max_dup_scripts + 1)})        
                writer_csv.writerow(row_to_write)
    except KeyError:
        print("Error in creation of csv duplicates.")


def create_csv_sprites(d: dict, folder_path: str):
    csv_name = "spriteNaming.csv"
    csv_filepath = os.path.join(folder_path, csv_name)
    # headers list
    headers = ['url', 'filename','number']

    total_sprite_names = max(len(proj.get('spriteNaming', {}).get('sprite', [])) for proj in d.values())
    headers.extend(f'spriteNaming{i}' for i in range(1, total_sprite_names+1))
    
    with open(csv_filepath, 'w') as csv_file:
        writer_csv = csv.DictWriter(csv_file, fieldnames=headers)
        writer_csv.writeheader()

        row_to_write = {}
        for project in d.values():
            row_to_write = {key: project.get(key, 'N/A') for key in headers}
            
            # Fill sprites
            sprites = project.get('spriteNaming', {}).get('sprite', [])
            for i, sprite in enumerate(sprites, 1):
                row_to_write[f'spriteNaming{i}'] = sprite if sprite else 'N/A'
            writer_csv.writerow(row_to_write)
  
def create_csv_backdrops(d: dict, folder_path: str):
    csv_name = "backdropNaming.csv"
    csv_filepath = os.path.join(folder_path, csv_name)
    # headers list
    headers = ['url', 'filename','number']

    total_backdrop_names = max(len(proj.get('backdropNaming', {}).get('backdrop', [])) for proj in d.values())
    headers.extend(f'backdropNaming{i}' for i in range(1, total_backdrop_names+1))
    
    with open(csv_filepath, 'w') as csv_file:
        writer_csv = csv.DictWriter(csv_file, fieldnames=headers)
        writer_csv.writeheader()

        row_to_write = {}
        for project in d.values():
            row_to_write = {key: project.get(key, 'N/A') for key in headers}
            
            # Fill backdrops
            backdrops = project.get('backdropNaming', {}).get('backdrop', [])
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
            for sprite_list_name, sprite_list in project_data.get('deadCode', {}).items():
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
    print(summary['num_projects'])
    print(skills)


    for project in d:
        try:
            summary['Points'] += round(d[project].get("mastery", {}).get("points", [0])[0], 2)
            for skill in skills:
                try:
                    if skill not in summary:
                        summary[skill] = 0
                    if type(d[project]["mastery"][skill][0]) == list:
                        if d[project]["mastery"][skill][0][1] != 0:
                            summary[skill] += d[project]["mastery"][skill][0][0]
                        else:
                            summary[skill] = 0
                except KeyError:
                    pass
        except TypeError:
            summary['Points'] += 0
    
    for skill in skills:
        summary[skill] = round(summary[skill] / num_projects, 2)
    
    # AVERAGE MASTERY POINTS
    average_mastery_points = round(summary['Points'] / num_projects, 2)
    
    
    # SET A LIST WITH MAX AND MID POINTS
    mid_points = total_maxi_points / 2
    summary['Points'] = [average_mastery_points, total_maxi_points, mid_points]
    for skill in skills:
        mid_points = d[0]["mastery"][skill][0][1] / 2
        summary[skill] = [summary[skill], d[0]["mastery"][skill][0][1]]
        


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

def create_obj(data: dict, csv_filepath: str) -> uuid.UUID:
    cs_data = BatchCSV.objects.create(
        filepath= csv_filepath,
        num_projects=data['num_projects'],
        points=data['Points'][0],
        max_points=data['Points'][1],
        logic=data['Logic'][0],
        max_logic=data['Logic'][1],
        parallelization=data['Parallelism'][0],
        max_parallelization=data['Parallelism'][1],
        data=data['Data representation'][0],
        max_data=data['Data representation'][1],
        synchronization=data['Synchronization'][0],
        max_synchronization=data['Synchronization'][1],
        userInteractivity=data['User interactivity'][0],
        max_userInteractivity=data['User interactivity'][1],
        flowControl=data['Flow control'][0],
        max_flowControl=data['Flow control'][1],
        abstraction=data['Abstraction'][0],
        max_abstraction=data['Abstraction'][1],
        math_operators=data['Math operators'][0],
        max_math_operators=data['Math operators'][1],
        motion_operators=data['Motion operators'][0],
        max_motion_operators=data['Motion operators'][1],
        mastery=data['Mastery']
    )

    return cs_data.id

def safe_json_load(value):
    try:
        return ast.literal_eval(value)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {value}")
        return None
    
extended_metrics_fields = [
        'url', 'filename', 'total_blocks','total_points', 
        'Abstraction', 'Parallelization', 'Logic', 'Synchronization',
        'FlowControl', 'UserInteractivity', 'DataRepresentation',
        'MathOperators', 'MotionOperators'
    ]

vanilla_metrics_fields = [
    'Van total_points','Van Abstraction','Van Parallelization', 'Van Logic', 
    'Van Synchronization', 'Van FlowControl', 'Van UserInteractivity',
    'Van DataRepresentation'
]

bad_smells_fields = ['duplicateScript', 'spriteNaming', 'initialization']
other_extended_fields = ['Error']
common_metrics = ['total_points','Abstraction', 'Parallelization', 'Logic', 'Synchronization',
        'FlowControl', 'UserInteractivity', 'DataRepresentation']

def format_field_value(value):
    return "/".join([str(item) for item in value]) if isinstance(value, list) else str(value)

def process_batches(batches):
    for batch in batches:
        project_row = {}
        ext_metrics = batch.get("extended_metrics", {})
        van_metrics = batch.get("vanilla_metrics", {})

        project_row.update({
            dim: format_field_value(ext_metrics.get(dim, "")) 
            for dim in extended_metrics_fields
        })

        project_row.update({
            f"Van {dim}": format_field_value(van_metrics.get(dim, "")) 
            for dim in common_metrics
        })

        project_row.update({
            dim: batch.get(dim, "") 
            for dim in bad_smells_fields
        })

        project_row.update({
            dim: format_field_value(ext_metrics.get(dim, "")) 
            for dim in other_extended_fields
        })
        project_row["filename"] = batch.get("filename", "").replace(",", "")
        yield project_row  
    
def make_csv_path(batch_id: str):
    csv_name = f"{batch_id}_main.csv"
    root_path = settings.BASE_DIR
    csv_path = os.path.join(root_path, "csvs", "Dr.Scratch", f"{csv_name}.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    return csv_path

def write_to_csv(batch_id: str, row_generator: dict):
    fieldnames = extended_metrics_fields + vanilla_metrics_fields + bad_smells_fields + other_extended_fields
    csv_path = make_csv_path(batch_id)

    try:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in row_generator:
                writer.writerow(row)
    except IOError as e:
        raise IOError(f"Error writing CSV file at {csv_path}: {e}")

def create_csv(request, temp_dict_metrics) -> uuid.UUID:
    batch_id = request.POST["batch_id"]
    batches = File.objects.filter(batch_id=batch_id).values("filename", "extended_metrics", "vanilla_metrics", "duplicateScript", "spriteNaming", "initialization")

    row_generator = process_batches(batches)

    write_to_csv(batch_id, row_generator)    



    """
    for batch in batches_querysets:
        print("METRICS VANILLA")
        print(batch.vanilla_metrics)
        print("METRICS EXTENDED")
        print(batch.extended_metrics)
        print("BAD SMELLS")
        print("Duplicate:",batch.duplicateScript)
        print("SpriteName:",batch.spriteNaming)
        print("BackdropName:",batch.initialization)
    """
    """
    with open(temp_dict_metrics, 'r') as dict_metrics:
        d = json.loads(dict_metrics.read())
    
    d = {int(key): value for key, value in d.items()}
    for key in d:
        d[key] = safe_json_load(d[key])

    print("DICCIOANRIO---------------------")
    print(d)
    
    summary = {}
    now = datetime.now()
    folder_name = str(uuid.uuid4()) + '_' + now.strftime("%Y%m%d%H%M%S")
    base_dir = os.getcwd()
    folder_path = os.path.join(base_dir, 'csvs', 'Dr.Scratch', folder_name)
    os.mkdir(folder_path)
    
    create_csv_main(request, d, folder_path)
    create_csv_dups(d, folder_path)
    create_csv_sprites(d, folder_path)
    create_csv_backdrops(d, folder_path)
    create_csv_deadcode(d, folder_path)
    summary = create_summary(request, d) 
    csv_filepath = zip_folder(folder_path)
    id = create_obj(summary, csv_filepath)
    os.remove(temp_dict_metrics)
    
    return id
    """