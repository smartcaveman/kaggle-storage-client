import os
import json
import kaggle
from os import path, listdir, walk, mkdir, environ
from kaggle import KaggleApi
from kaggle_storage_client import LocalStorage, leafname, DEFAULT_DATA_DIR, DEFAULT_CONFIG_FILE, DATASET_METADATA_FILE, \
    print_fstree
from json import load, loads, dump, dumps


class KaggleStorageClient:

    def __init__(self, datadir=DEFAULT_DATA_DIR, configfile=DEFAULT_CONFIG_FILE):
        self.__local_storage = self.__get_local_storage(datadir)
        self.__api = self.__get_authenticated_kaggle_api(configfile)

    @property
    def api(self):
        return self.__api

    @property
    def local_storage(self):
        return self.__local_storage

    @property
    def username(self):
        return os.environ['KAGGLE_USERNAME']

    def __get_local_storage(self, root):
        # ensure root folder
        if not path.exists(root):
            mkdir(root)
        storage = LocalStorage(root=root)
        return storage

    def __get_authenticated_kaggle_api(self, configfile):
        self.login_with_configfile(configfile)
        api = KaggleApi()
        api.authenticate()
        return api

    def __patch_metadata_file(self, dataset_folder):
        metadata_filepath = path.join(dataset_folder, DATASET_METADATA_FILE)
        with open(metadata_filepath) as mdfile:
            md = json.load(mdfile)
        slug = '-'.join(leafname(dataset_folder).split(' ')).lower()
        title = ' '.join(map(lambda token: f'{token[0].upper()}{token[1:]}', slug.split('-')))
        md['id'] = md['id'].replace('INSERT_SLUG_HERE', slug)
        md['title'] = md['title'].replace('INSERT_TITLE_HERE', title)
        with open(metadata_filepath, 'w') as mdfile:
            mdfile.write(json.dumps(md))
        print(json.dumps(md))


    def login_with_configfile(self, configfile):
        # require configfile
        if not path.exists(configfile):
            print(configfile)
            raise FileNotFoundError(filename=configfile)

        # load credentials into current environment from configfile yaml
        with open(configfile) as file:
            # load configfile
            # credentials = yaml.load(file.read().replace(':', ': '), Loader=yaml.FullLoader)
            credentials = json.loads_literal(file.read())
        self.login(credentials['username'], credentials['key'])

    """Configure the kaggle API to login using the specified username and key"""

    def login(self, username, key):
        if not username or not key:
            raise IOError('Username and Key are required for login')
        # load credentials into current environment from configfile yaml
        environ['KAGGLE_USERNAME'] = username
        environ['KAGGLE_KEY'] = key

    """Remove kaggle login configuration"""

    def logout(self):
        del environ['KAGGLE_USERNAME']
        del environ['KAGGLE_KEY']


    """Create dataset"""

    def create(self, dataset):
        raise NotImplementedError()

    """Download the file from the kaggle dataset"""

    def download(self, username, dataset, filename):
        dataset_file_content = self.api.datasets_download_file(username, dataset, filename)
        filepath = self.local_storage.save(username, dataset, filename, dataset_file_content)
        folder = path.dirname(filepath)
        metadata_filepath = path.join(folder, DATASET_METADATA_FILE)
        if not path.exists(metadata_filepath):
            self.api.dataset_initialize(folder)
            self.__patch_metadata_file(folder)
            self.api.dataset_create_version(folder, version_notes="Patch metadata.")
        return filepath

    def upload(self, dataset, filepath):

        if not path.exists(filepath):
            raise FileNotFoundError(filepath)

        folder = path.dirname(filepath)
        print(f'upload -dataset {dataset} -filepath {filepath} -folder {folder}')
        remote_status = self.api.datasets_status(self.username, dataset)
        print(f'remote-status of {self.username}/{dataset} is {remote_status}')

        self.api.dataset_initialize(folder)
        self.__patch_metadata_file(folder)

        if remote_status != 'ready':
            print(f'create {folder}')
            print_fstree(folder)
            return self.api.dataset_create_new_cli(folder)
        else:
            print(f'sync {folder}')
            print_fstree(folder)
            return self.api.dataset_create_version_cli(folder, version_notes=f"Upload {leafname(filepath)} to {dataset}.")
