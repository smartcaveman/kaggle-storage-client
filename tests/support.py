
EXAMPLE_DATASET_OWNER = 'coronawhybeta'
EXAMPLE_DATASET_NAME = 'example-dataset'
EXAMPLE_DATASET_ID = f'{EXAMPLE_DATASET_OWNER}/{EXAMPLE_DATASET_NAME}'
EXAMPLE_DATASET_FILE_1 = f'records.csv'
EXAMPLE_DATASET_FILE_1_CONTENT = 'id,desc\n1,The first example record\n2,The second example record'
EXAMPLE_DATASET_FILE_2 = 'vowels.csv'
EXAMPLE_DATASET_FILE_2_CONTENT = 'index,upper,lower\n0,A,a\n4,E,e\n8,I,i\n14,O,o\n20,U,u\n'

EXAMPLE_DATASET = {
    'OWNER': EXAMPLE_DATASET_OWNER,
    'NAME': EXAMPLE_DATASET_NAME,
    'ID': EXAMPLE_DATASET_ID,
    'FILE_1': EXAMPLE_DATASET_FILE_1,
    'FILE_1_CONTENT': EXAMPLE_DATASET_FILE_1_CONTENT,
    'FILE_2': EXAMPLE_DATASET_FILE_2,
    'FILE_2_CONTENT': EXAMPLE_DATASET_FILE_2_CONTENT,
}

def save_test_config_file(configfile_path="kaggle.json", configfile_content="{username:coronawhybeta,key:6d67ed08ee2a272b499665d746184fd0}"):
    with open(configfile_path, "w") as config:
        config.write(configfile_content)
    return configfile_path
