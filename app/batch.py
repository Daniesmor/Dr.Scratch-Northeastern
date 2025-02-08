

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
from django.db.models import QuerySet
from pathlib import Path
from .consts_drscratch import EXTENDED_RUBRIC, get_mastery
import logging

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


bad_smells_fields = ['deadcode', 'duplicateScript', 'spriteNaming', 'initialization']
other_extended_fields = ['Error']
common_metrics = ['total_points','Abstraction', 'Parallelization', 'Logic', 'Synchronization',
        'FlowControl', 'UserInteractivity', 'DataRepresentation']


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


def zip_folder(folder_path: str):
    with ZipFile(folder_path + '.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, os.path.basename(filePath))
                
    # Remove the original folder
    shutil.rmtree(folder_path)
    return folder_path + '.zip'


def get_avg_points(batches: QuerySet) -> int:
    scores = [project['score'] for project in batches]
    return sum(scores) // len(batches) if scores else 0


def get_avg_dim_points(batches: QuerySet, dim_name: str) -> int:
    tot_dim_points = sum(
        safe_get(project['extended_metrics'], [dim_name])[0]
        for project in batches
        if safe_get(project['extended_metrics'], [dim_name]) is not None
    )
    return tot_dim_points // len(batches) if len(batches) != 0 else 0


def create_batch_obj(batch_id: uuid.UUID, batches: QuerySet):
    avg_points = get_avg_points(batches)

    BatchCSV.objects.create(
        id=batch_id,
        filepath=make_csv_path(batch_id),
        num_projects=len(batches),
        points=avg_points,
        max_points=EXTENDED_RUBRIC['EXTENDED_POINTS'],
        logic=get_avg_dim_points(batches, 'Logic'),
        max_logic=EXTENDED_RUBRIC['LOGIC'],
        parallelism=get_avg_dim_points(batches, 'Parallelism'),
        max_parallelism=EXTENDED_RUBRIC['LOGIC'],
        data=get_avg_dim_points(batches, 'Data representation'),
        max_data=EXTENDED_RUBRIC['DATA_REPRESENTATION'],
        synchronization=get_avg_dim_points(batches, 'Synchronization'),
        max_synchronization=EXTENDED_RUBRIC['SYNCHRONIZATION'],
        userInteractivity=get_avg_dim_points(batches, 'User interactivity'),
        max_userInteractivity=EXTENDED_RUBRIC['USER_INTERACTIVITY'],
        flowControl=get_avg_dim_points(batches, 'Flow control'),
        max_flowControl=EXTENDED_RUBRIC['FLOW_CONTROL'],
        abstraction=get_avg_dim_points(batches, 'Abstraction'),
        max_abstraction=EXTENDED_RUBRIC['ABSTRACTION'],
        math_operators=get_avg_dim_points(batches, 'Math operators'),
        max_math_operators=EXTENDED_RUBRIC['MATH_OPERATORS'],
        motion_operators=get_avg_dim_points(batches, 'Motion operators'),
        max_motion_operators=EXTENDED_RUBRIC['MOTION_OPERATORS'],
        mastery=get_mastery(avg_points)
    )


def safe_json_load(value):
    try:
        return json.loads(value)
    except (json.JSONDecodeError, ValueError, SyntaxError) as e:
        logging.warning(f"Error decoding JSON: {value} - {e}")
        return None
    

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
    csv_path = os.path.join(root_path, "csvs", "Dr.Scratch", f"{csv_name}")
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
    batches = File.objects.filter(batch_id=batch_id).values(
        "score",
        "filename", 
        "extended_metrics", 
        "vanilla_metrics", 
        "duplicateScript", 
        "spriteNaming", 
        "initialization"
    )
    create_batch_obj(batch_id, batches)
    row_generator = process_batches(batches)

    write_to_csv(batch_id, row_generator)    

    return batch_id