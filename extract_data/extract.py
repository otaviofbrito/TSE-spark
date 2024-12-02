import requests
import json
import os
import zipfile

json_path = '/app/extract_data/source.json'
# volume_path = "../Volumes/raw/tse"
volume_path = "/app/data/raw/tse"


def load_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data


def get_file(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.content
        else:
            print(f"Erro ao acessar a URL {url}. Status code: {res.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao fazer requisição: {e}")
        return None


def download_file(file_content, path):
    with open(path, "wb") as open_file:
        open_file.write(file_content)


def extract_zip(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Arquivo {zip_path} extraído com sucesso.")
    except zipfile.BadZipFile:
        print(f"Erro: {zip_path} não é um arquivo ZIP válido.")
    except Exception as e:
        print(f"Erro ao extrair {zip_path}: {e}")


def main():
    os.makedirs(volume_path, exist_ok=True)
    json_data = load_json(json_path)

    for key, value in json_data.items():
        folder_path = os.path.join(volume_path, value['dir'])
        os.makedirs(folder_path, exist_ok=True)

        url = value['link']
        file_name = url.split("/")[-1]
        file_path = os.path.join(folder_path, file_name)

        res_content = get_file(url)
        if res_content:
            download_file(res_content, file_path)
            print(f"Arquivo {file_name} baixado com sucesso.")

            extract_zip(file_path, folder_path)
        else:
            print(f"Falha ao baixar o arquivo {file_name}.")


if __name__ == '__main__':
    main()
