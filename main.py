import json
import requests
import configparser
from tqdm import tqdm
from time import sleep

#файл для хранения токена
config = configparser.ConfigParser()
config.read('settings.ini')
tokens = config['tokens']['ya_disk']


class YD:
    base_url = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.headers = {'Authorization' : f'OAuth {token}'}

    def create_folder(self, folder):
        """Создание папки.
            folder: Название папки."""
        params = {'path' : folder}
        response = requests.put(f'{self.base_url}/v1/disk/resources',
                                params=params,
                                headers=self.headers)
        return response.status_code

    def upload_photo(self, folder, text):
        """Получение фото котика и скачивание в папку.
            folder: Название папки.
            text: текст на фото"""
        print(f'Введен текст для картинки:{text}')
        url_photo = f'https://cataas.com/cat/cat/says/{text}'
        name = url_photo.split('/')[-1]
        params = {
            'path': f'{folder}/{name}',
            'url' : f'{url_photo}'
        }
        response = requests.post(f'{self.base_url}/v1/disk/resources/upload',
                                params=params,
                                headers=self.headers)
        return response.status_code

    def delete_folder(self, folder):
        """Удаление папки.
            folder: Название папки."""
        params = {'path': folder,
                  'permanently' : 'true'}
        response = requests.delete(f'{self.base_url}/v1/disk/resources',
                                params=params,
                                headers=self.headers)
        return response.status_code

    def info_file(self, path_to_file):
        """Сохранение информации о размере файла в json-файл.
            path_to_file: Путь к папке."""
        params = {
            'path': path_to_file
        }
        response = requests.get(f'{self.base_url}/v1/disk/resources',
                                params=params,
                                headers=self.headers)
        file_name = path_to_file.split('/')[-1]
        file_info = {'имя файла' : file_name,
                     'размер файла' : response.json()['size']}

        with open('files_info.json', 'a', encoding='utf-8') as f:
            json.dump(file_info, f, ensure_ascii=False, indent='\t')

        print(f"Информация о файле '{file_name}' успешно сохранена в файл")


test_yd = YD(tokens)

#прогресс бар
lst = [1, 2, 3, 4]
for i in tqdm(lst):
    sleep(0.5)

test_yd.create_folder('PD-FPY-136')
test_yd.upload_photo('PD-FPY-136', 'hello')
test_yd.info_file('PD-FPY-136/hello')
#test_yd.delete_folder('PD-FPY-136')


