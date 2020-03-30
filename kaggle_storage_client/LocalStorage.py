from os import path, listdir, walk, mkdir
import os

class LocalStorage:


    def __init__(self, root):
        if not path.exists(root):
            raise FileNotFoundError(root)
        self.__root = root

    @property
    def root(self):
        return self.__root

    @property
    def datasets(self):
        return [d for d in os.listdir(self.root)]

    @property
    def files(self):
        folder_files = [(d, f) for d, _, f in os.walk(self.root)]
        return [path.join(folder, file) for folder, files in folder_files for file in files]

    def save(self, username, dataset, filename, content):
        dataset_owner_dir = path.join(self.root, username)
        dataset_dir = path.join(dataset_owner_dir, dataset)
        file = path.join(dataset_dir, filename)
        if not path.exists(dataset_owner_dir):
            mkdir(dataset_owner_dir)
        if not path.exists(dataset_dir):
            mkdir(dataset_dir)
        with open(file, "w") as file_writer:
            file_writer.write(content)
        return file
