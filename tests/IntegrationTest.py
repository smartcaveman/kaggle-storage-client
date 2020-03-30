import os
import shutil
import time
import unittest
from os import path
from os.path import exists

import kaggle_storage_client
from tests.support import save_test_config_file, EXAMPLE_DATASET


class IntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if exists(kaggle_storage_client.DEFAULT_DATA_DIR):
            shutil.rmtree(kaggle_storage_client.DEFAULT_DATA_DIR, ignore_errors=False, onerror=None)
        cls.configfile = save_test_config_file()
        cls.client = kaggle_storage_client.KaggleStorageClient(configfile=cls.configfile)

    @property
    def local_data_file_1(self):
        return path.join(f'{self.client.local_storage.root}', EXAMPLE_DATASET['OWNER'], EXAMPLE_DATASET['NAME'],
                         EXAMPLE_DATASET['FILE_1'])

    def test_that_the_configfile_exists(self):
        it = self.configfile
        self.assertTrue(exists(it))

    def test_that_data_folder_exists_as_empty(self):
        it = kaggle_storage_client.DEFAULT_DATA_DIR
        self.assertTrue(exists(it) and len(os.listdir(it)) == 0)

    def test_that_save_puts_file_in_local_storage(self):
        if exists(self.local_data_file_1):
            os.remove(self.local_data_file_1)
        self.assertTrue(not exists(self.local_data_file_1))
        self.client.download(self.client.username, EXAMPLE_DATASET['NAME'], EXAMPLE_DATASET['FILE_1'])
        time.sleep(1)
        self.assertTrue(exists(self.local_data_file_1))

    def test_that_upload_puts_local_file_into_kaggle_dataset(self):
        self.client.upload(EXAMPLE_DATASET['NAME'], self.local_data_file_1)
        time.sleep(1)
        kaggle_files = list(
            map(lambda file: f'{file}', self.client.api.dataset_list_files(EXAMPLE_DATASET['ID']).files))
        print(type(kaggle_files[0]))
        print(kaggle_files[0])

        self.assertIn(EXAMPLE_DATASET['FILE_1'], kaggle_files)

    def test_that_download_puts_kaggle_file_into_local_storage(self):
        if exists(self.local_data_file_1):
            os.remove(self.local_data_file_1)

        self.assertTrue(not exists(self.local_data_file_1))
        self.client.download(self.client.username, EXAMPLE_DATASET['NAME'], EXAMPLE_DATASET['FILE_1'])
        time.sleep(1)
        kaggle_files = list(map(lambda file: f'{file}', self.client.api.dataset_list_files(EXAMPLE_DATASET['ID']).files))

        print(kaggle_files[0])

        self.assertTrue(exists(self.local_data_file_1))


if __name__ == '__main__':
    unittest.main()
