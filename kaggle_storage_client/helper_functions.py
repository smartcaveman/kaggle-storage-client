from kaggle.api.kaggle_api_extended import KaggleApi, DatasetNewVersionRequest
from itertools import chain
# from yaml import load, FullLoader
from os import environ, mkdir, path
from pandas import read_csv
from os import path, listdir, walk, mkdir
from inspect import getmembers, signature
import json
import ntpath
import os

# global constants
DATASET_METADATA_FILE = 'dataset-metadata.json'
DEFAULT_DATA_DIR = 'data'
DEFAULT_CONFIG_FILE = '/root/.kaggle/kaggle.json'

def leafname(path):
    """ gets the local filename if a file or foldername if a folder
    :param path: the filepath from which to extract the leaf name segment
    :return: the last name segment in the filepath
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def load_literal_as_json(literal_text):
    json_text = literal_text.replace('{', '{"').replace('}', '"}').replace(':', '":"').replace(',', '","')
    return json.loads(json_text)


json.loads_literal = load_literal_as_json

def type_descriptor(instance):
    """gets human-readable signature for the instance's type"""
    return (type(instance).__name__,
            [(m, signature(o) if callable(o) else type(o).__name__) for m, o in getmembers(instance) if
             m[0] != '_'])


def print_fstree(path = ".", indent=0):
    tabs = indent * 2 * " "
    if indent == 0:
        print(f'{path}')
    else:
        print(f'{tabs}d> {leafname(path)}/')
    tabs += 2 * " "
    subfolders = []
    files = []
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            files.append(entry)
        else:
            subfolders.append(entry)

    for subfolder in subfolders:
        print_fstree(os.path.join(path, subfolder), indent + 1)
    for file in files:
        print(f'{tabs}f> {file}')
        i = 0
        with open(os.path.join(path, file)) as content:
            for line in content.readlines():
                i += 1
                print(f'{tabs}>> [L{i:03}] {line}'.rstrip())

